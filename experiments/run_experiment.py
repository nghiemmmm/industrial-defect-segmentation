#!/usr/bin/env python3
"""
Master Experiment Runner (EXP-00 to EXP-08).
Orchestrates:
1. Strict Defect-Free Data Engine Preprocessing & Synthetic Generation.
2. Ultralytics YOLOv11-seg Training with auto GPU/CPU detection.
3. Dual-Domain Evaluation on isolated real test split (Mask mAP + Pixel AUROC + Image AUROC + FAR).
4. MVTec-AD-C Robustness Degradation Curves & Table V Tier Summaries (when enabled).
"""

import argparse
import gc
import json
import logging
import os
import random
import shutil
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
import yaml

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_engine.base import MaterialAdaptiveRouter, Pipeline
from data_engine.exporters.yolo_seg_exporter import YOLOSegExporter
from data_engine.frequency.dwt_filter import DWTSubbandFilter
from data_engine.frequency.fft_filter import FFTPeriodicSuppressionFilter
from data_engine.loaders.mvtec_loader import MVTecLoader
from data_engine.sample import Sample
from data_engine.synthesizers.cutpaste_synthesizer import CutPasteSynthesizer
from data_engine.synthesizers.draem_synthesizer import DRAEMSynthesizer
from data_engine.synthesizers.nsa_synthesizer import NSASynthesizer
from evaluation.dual_domain_metrics import (
    DualDomainEvaluator,
    compute_false_alarm_rate,
    masks_to_anomaly_map,
)
from evaluation.robustness_evaluator import RobustnessEvaluator

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("ExperimentRunner")


def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_pipelines_from_config(
    de_cfg: Dict[str, Any],
    seed: Optional[int] = None,
) -> Tuple[Pipeline, Pipeline]:
    """
    Builds separate (train_pipeline, eval_pipeline) from YAML config.
    - train_pipeline: Spatial Synthesizer (1 - rho_neg anomaly_prob) + Frequency Filter T_freq.
    - eval_pipeline: Frequency Filter T_freq ONLY (never synthesizes defects on real test images).
    """
    train_pipeline = Pipeline()
    eval_pipeline = Pipeline()
    if not de_cfg:
        return train_pipeline, eval_pipeline

    # 1. Synthesizer (Group A) -> train only
    synth_cfg = de_cfg.get("synthesizer")
    if synth_cfg:
        stype = synth_cfg.get("type", "").lower()
        anomaly_prob = float(synth_cfg.get("anomaly_prob", 0.85))
        if stype == "cutpaste":
            train_pipeline.add(CutPasteSynthesizer(
                mode=synth_cfg.get("mode", "union"),
                anomaly_prob=anomaly_prob,
                seed=seed,
            ))
        elif stype == "draem":
            train_pipeline.add(DRAEMSynthesizer(
                perlin_threshold=synth_cfg.get("perlin_threshold", 0.45),
                beta_range=tuple(synth_cfg.get("beta_range", [0.2, 0.8])),
                anomaly_prob=anomaly_prob,
                seed=seed,
            ))
        elif stype == "nsa":
            train_pipeline.add(NSASynthesizer(
                width_ratio_range=tuple(synth_cfg.get("width_ratio_range", [0.05, 0.22])),
                height_ratio_range=tuple(synth_cfg.get("height_ratio_range", [0.05, 0.22])),
                anomaly_prob=anomaly_prob,
                seed=seed,
            ))
        elif stype == "material_adaptive":
            tex_cfg = synth_cfg.get("texture", {})
            obj_cfg = synth_cfg.get("object", {})
            tex_proc = DRAEMSynthesizer(
                perlin_threshold=tex_cfg.get("perlin_threshold", 0.45),
                beta_range=tuple(tex_cfg.get("beta_range", [0.2, 0.8])),
                anomaly_prob=float(tex_cfg.get("anomaly_prob", anomaly_prob)),
                seed=seed,
            )
            obj_proc = NSASynthesizer(
                width_ratio_range=tuple(obj_cfg.get("width_ratio_range", [0.05, 0.22])),
                height_ratio_range=tuple(obj_cfg.get("height_ratio_range", [0.05, 0.22])),
                anomaly_prob=float(obj_cfg.get("anomaly_prob", anomaly_prob)),
                seed=seed,
            )
            train_pipeline.add(MaterialAdaptiveRouter(
                texture_processor=tex_proc,
                object_processor=obj_proc,
                texture_categories=synth_cfg.get("texture_categories"),
                name="MaterialAdaptiveSynthesizer",
            ))

    # 2. Frequency Filter (Group B) -> applied identically to train AND eval/test
    freq_cfg = de_cfg.get("frequency_filter")
    if freq_cfg:
        ftype = freq_cfg.get("type", "").lower()
        if ftype == "fft":
            fft_params = dict(
                tau=freq_cfg.get("tau", 3.5),
                notch_sigma=freq_cfg.get("notch_sigma", 3.5),
            )
            train_pipeline.add(FFTPeriodicSuppressionFilter(**fft_params))
            eval_pipeline.add(FFTPeriodicSuppressionFilter(**fft_params))
        elif ftype == "dwt":
            dwt_params = dict(
                alpha=freq_cfg.get("alpha", 0.6),
                gamma=freq_cfg.get("gamma", 1.4),
                wavelet=freq_cfg.get("wavelet", "haar"),
            )
            train_pipeline.add(DWTSubbandFilter(**dwt_params))
            eval_pipeline.add(DWTSubbandFilter(**dwt_params))
        elif ftype == "material_adaptive":
            tex_fcfg = freq_cfg.get("texture", {})
            obj_fcfg = freq_cfg.get("object", {})
            fft_params = dict(
                tau=tex_fcfg.get("tau", 3.5),
                notch_sigma=tex_fcfg.get("notch_sigma", 3.5),
            )
            dwt_params = dict(
                alpha=obj_fcfg.get("alpha", 0.5),
                gamma=obj_fcfg.get("gamma", 1.6),
                wavelet=obj_fcfg.get("wavelet", "haar"),
            )
            tex_cats = freq_cfg.get("texture_categories")
            train_pipeline.add(MaterialAdaptiveRouter(
                texture_processor=FFTPeriodicSuppressionFilter(**fft_params),
                object_processor=DWTSubbandFilter(**dwt_params),
                texture_categories=tex_cats,
                name="MaterialAdaptiveFrequencyFilter",
            ))
            eval_pipeline.add(MaterialAdaptiveRouter(
                texture_processor=FFTPeriodicSuppressionFilter(**fft_params),
                object_processor=DWTSubbandFilter(**dwt_params),
                texture_categories=tex_cats,
                name="MaterialAdaptiveFrequencyFilter",
            ))

    return train_pipeline, eval_pipeline


def build_pipeline_from_config(de_cfg: Dict[str, Any]) -> Pipeline:
    """Backward-compatible helper returning the training pipeline."""
    train_pipeline, _ = build_pipelines_from_config(de_cfg)
    return train_pipeline


def _predict_anomaly_map(yolo_model, img_rgb: np.ndarray, imgsz: int = 640, conf: float = 0.01) -> Tuple[np.ndarray, float]:
    """Runs YOLOv11-seg on a single RGB image and returns (continuous anomaly_map, max_conf)."""
    h, w = img_rgb.shape[:2]
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    results = yolo_model.predict(img_bgr, imgsz=imgsz, conf=conf, verbose=False)
    if not results:
        return np.zeros((h, w), dtype=np.float32), 0.0

    r = results[0]
    if r.masks is None or r.boxes is None or len(r.boxes) == 0:
        return np.zeros((h, w), dtype=np.float32), 0.0

    confs = r.boxes.conf.cpu().numpy().tolist()
    raw_masks = r.masks.data.cpu().numpy()
    resized_masks = []
    for m in raw_masks:
        if m.shape[:2] != (h, w):
            m_res = cv2.resize(m, (w, h), interpolation=cv2.INTER_LINEAR)
        else:
            m_res = m
        resized_masks.append((m_res >= 0.5).astype(np.uint8))

    anomaly_map = masks_to_anomaly_map(resized_masks, confs, (h, w))
    max_conf = float(max(confs)) if confs else 0.0
    return anomaly_map, max_conf


def run_post_train_evaluation(
    yolo_model,
    test_samples: List[Sample],
    eval_pipeline: Pipeline,
    categories: List[str],
    processed_dir: str,
    out_dir: str,
    exp_id: str,
    imgsz: int = 640,
    run_robustness: bool = False,
) -> Dict[str, Any]:
    """
    Evaluates a trained YOLOv11-seg model on the isolated real test split:
    1. COCO Mask mAP@50 & mAP@50-95 via Ultralytics val() on exported test split.
    2. Pixel-AUROC, Image-AUROC, Mean Mask IoU, FAR@0.25, FAR@0.50 via DualDomainEvaluator.
    3. Optional MVTec-AD-C robustness curves & Table V severity tier summaries.
    """
    # Apply eval_pipeline (T_freq only) to real test samples
    processed_test = eval_pipeline.run(test_samples) if len(eval_pipeline) > 0 else test_samples

    # Export real test split as 'val' in a dedicated eval_dataset folder for exact Ultralytics mAP
    eval_ds_dir = os.path.join(processed_dir, "test_eval")
    if os.path.exists(eval_ds_dir):
        shutil.rmtree(eval_ds_dir)
    category_map = {cat: idx for idx, cat in enumerate(sorted(categories))}
    eval_exporter = YOLOSegExporter(output_dir=eval_ds_dir, category_map=category_map, save_debug_masks=False)
    eval_exporter.export(processed_test, split="val")
    eval_yaml = os.path.join(eval_ds_dir, "dataset.yaml")

    val_metrics = yolo_model.val(data=eval_yaml, imgsz=imgsz, split="val", verbose=False)
    per_cat_mask_map50: Dict[str, float] = {}
    per_cat_mask_map50_95: Dict[str, float] = {}
    per_cat_box_map50: Dict[str, float] = {}

    overall_mask_map50 = float(getattr(val_metrics.seg, "map50", 0.0)) if hasattr(val_metrics, "seg") else 0.0
    overall_mask_map50_95 = float(getattr(val_metrics.seg, "map", 0.0)) if hasattr(val_metrics, "seg") else 0.0
    overall_box_map50 = float(getattr(val_metrics.box, "map50", 0.0)) if hasattr(val_metrics, "box") else 0.0

    # Map per-class APs if available
    if hasattr(val_metrics, "seg") and hasattr(val_metrics.seg, "ap50") and len(val_metrics.seg.ap50) == len(categories):
        for idx, cat in enumerate(sorted(categories)):
            per_cat_mask_map50[cat] = float(val_metrics.seg.ap50[idx])
            per_cat_mask_map50_95[cat] = float(val_metrics.seg.ap[idx]) if hasattr(val_metrics.seg, "ap") else overall_mask_map50_95
            per_cat_box_map50[cat] = float(val_metrics.box.ap50[idx]) if hasattr(val_metrics.box, "ap50") else overall_box_map50

    # Dual-domain pixel/image AUROC & FAR evaluation
    evaluator = DualDomainEvaluator(target_categories=categories)
    cat_results = []
    for cat in categories:
        cat_samples = [s for s in processed_test if s.category == cat]
        defect_gt_masks, defect_pred_maps, defect_max_confs = [], [], []
        good_pred_maps, good_max_confs = [], []
        for s in cat_samples:
            a_map, max_conf = _predict_anomaly_map(yolo_model, s.image, imgsz=imgsz)
            if s.is_anomaly:
                defect_gt_masks.append(s.mask)
                defect_pred_maps.append(a_map)
                defect_max_confs.append(max_conf)
            else:
                good_pred_maps.append(a_map)
                good_max_confs.append(max_conf)

        cat_res = evaluator.evaluate_category(
            category=cat,
            defect_gt_masks=defect_gt_masks,
            defect_pred_maps=defect_pred_maps,
            defect_max_confs=defect_max_confs,
            good_max_confs=good_max_confs,
            good_pred_maps=good_pred_maps,
            box_map50=per_cat_box_map50.get(cat, overall_box_map50),
            mask_map50=per_cat_mask_map50.get(cat, overall_mask_map50),
            mask_map50_95=per_cat_mask_map50_95.get(cat, overall_mask_map50_95),
        )
        cat_results.append(cat_res)

    summary = evaluator.aggregate_results(cat_results)
    summary["ultralytics_overall"] = {
        "mask_mAP50": round(overall_mask_map50, 4),
        "mask_mAP50_95": round(overall_mask_map50_95, 4),
        "box_mAP50": round(overall_box_map50, 4),
    }
    summary["experiment_id"] = exp_id
    summary["timestamp"] = datetime.now().isoformat()

    summary_path = os.path.join(out_dir, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    logger.info(f"Saved Dual-Domain Test Evaluation Summary to {summary_path}")

    # Optional MVTec-AD-C Optical Robustness Benchmark (Table V)
    if run_robustness:
        logger.info("Running MVTec-AD-C Optical Robustness Benchmark (4 corruptions x 5 severities)...")
        rob_eval = RobustnessEvaluator(output_dir=os.path.join(out_dir, "robustness"))
        raw_images = [s.image for s in test_samples]
        raw_masks = [s.mask for s in test_samples]

        def _predict_with_freq(corrupted_rgb: np.ndarray) -> Tuple[np.ndarray, float]:
            if len(eval_pipeline) > 0:
                tmp_s = Sample(image=corrupted_rgb, category="eval", defect_type="eval", is_anomaly=False)
                corrupted_rgb = eval_pipeline.run([tmp_s])[0].image
            return _predict_anomaly_map(yolo_model, corrupted_rgb, imgsz=imgsz)

        rob_df = rob_eval.run_robustness_benchmark(
            images=raw_images,
            gt_masks=raw_masks,
            predict_fn=_predict_with_freq,
            experiment_id=exp_id,
        )
        # Aggregate Sev 1-3 vs Sev 4-5 tiers for Table V (Mask mAP@50 & FAR@0.25)
        tier_summary: Dict[str, Any] = {}
        for corr in rob_eval.corruptions:
            sub_13 = rob_df[(rob_df["corruption"] == corr) & (rob_df["severity"].isin([1, 2, 3]))]
            sub_45 = rob_df[(rob_df["corruption"] == corr) & (rob_df["severity"].isin([4, 5]))]
            tier_summary[corr] = {
                "sev_1_3_mask_mAP50": round(float(sub_13["mask_mAP50"].mean()), 4) if len(sub_13) else 0.0,
                "sev_4_5_mask_mAP50": round(float(sub_45["mask_mAP50"].mean()), 4) if len(sub_45) else 0.0,
                "sev_1_3_far_025": round(float(sub_13["far_025"].mean()), 4) if len(sub_13) else 0.0,
                "sev_4_5_far_025": round(float(sub_45["far_025"].mean()), 4) if len(sub_45) else 0.0,
                "sev_1_3_mean_iou": round(float(sub_13["mean_iou"].mean()), 4) if len(sub_13) else 0.0,
                "sev_4_5_mean_iou": round(float(sub_45["mean_iou"].mean()), 4) if len(sub_45) else 0.0,
                "sev_1_3_pixel_auroc": round(float(sub_13["pixel_auroc"].mean()), 4) if len(sub_13) else 0.0,
                "sev_4_5_pixel_auroc": round(float(sub_45["pixel_auroc"].mean()), 4) if len(sub_45) else 0.0,
            }
        corr_only_13 = rob_df[(rob_df["corruption"] != "clean") & (rob_df["severity"].isin([1, 2, 3]))]
        corr_only_45 = rob_df[(rob_df["corruption"] != "clean") & (rob_df["severity"].isin([4, 5]))]
        tier_summary["overall_mean"] = {
            "sev_1_3_mask_mAP50": round(float(corr_only_13["mask_mAP50"].mean()), 4) if len(corr_only_13) else 0.0,
            "sev_4_5_mask_mAP50": round(float(corr_only_45["mask_mAP50"].mean()), 4) if len(corr_only_45) else 0.0,
            "sev_1_3_far_025": round(float(corr_only_13["far_025"].mean()), 4) if len(corr_only_13) else 0.0,
            "sev_4_5_far_025": round(float(corr_only_45["far_025"].mean()), 4) if len(corr_only_45) else 0.0,
        }
        tier_path = os.path.join(out_dir, "robustness", f"{exp_id}_tier_summary.json")
        with open(tier_path, "w", encoding="utf-8") as f:
            json.dump(tier_summary, f, indent=2)
        summary["robustness_tiers"] = tier_summary
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Saved MVTec-AD-C Tier Summary to {tier_path}")

    return summary


def main():
    parser = argparse.ArgumentParser(description="MVTec YOLOv11-seg Master Experiment Runner")
    parser.add_argument("--config", type=str, required=True, help="Path to experiment YAML config")
    parser.add_argument("--dry-run", action="store_true", help="Dry-run without training heavy model")
    parser.add_argument("--device", type=str, default="", help="Device override (e.g. '0', 'cpu')")
    parser.add_argument("--seed", type=int, default=None, help="Random seed override for multi-seed variance analysis")
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    exp_id = cfg.get("experiment_id", "exp_default")
    ds_cfg = cfg.get("dataset", {})
    active_seed = args.seed if args.seed is not None else ds_cfg.get("seed", 42)
    random.seed(active_seed)
    np.random.seed(active_seed)

    if args.seed is not None and args.seed != ds_cfg.get("seed", 42):
        exp_id = f"{exp_id}_seed{args.seed}"

    out_dir = os.path.join("results", "experiments", exp_id)
    processed_dir = os.path.join("datasets", "processed", exp_id)
    os.makedirs(out_dir, exist_ok=True)

    logger.info("=" * 65)
    logger.info(f"  EXECUTING EXPERIMENT: {exp_id.upper()} (Seed: {active_seed})")
    logger.info(f"  Description: {cfg.get('description', '')}")
    logger.info(f"  Target Dir : {out_dir}")
    logger.info("=" * 65)

    categories = ds_cfg.get("target_categories", ["grid", "carpet", "tile", "screw", "pill", "bottle"])

    # 1. Pipeline Building (separate train vs eval pipelines, seeded deterministically)
    train_pipeline, eval_pipeline = build_pipelines_from_config(cfg.get("data_engine", {}), seed=active_seed)
    logger.info(f"Constructed Train Pipeline: {train_pipeline}")
    logger.info(f"Constructed Eval  Pipeline: {eval_pipeline}")

    # Check for raw dataset directory
    raw_root = ds_cfg.get("root_dir", "./mvtec_ad")
    if not os.path.exists(raw_root) and not args.dry_run:
        logger.error(f"Raw dataset path not found: {raw_root}. Use --dry-run for local unit verification.")
        sys.exit(1)

    # 2. Hardware Device Resolution
    device = args.device or cfg.get("model", {}).get("device", "auto")
    if device == "auto":
        try:
            import torch
            device = "0" if torch.cuda.is_available() else "cpu"
        except ImportError:
            device = "cpu"
    logger.info(f"Resolved Computing Device: {device}")

    # 3. Execution (Dry-Run vs Full Train + Eval)
    if args.dry_run:
        logger.info("Running in DRY-RUN mode: Verifying evaluation & metrics pipeline on mock inputs...")
        evaluator = DualDomainEvaluator(target_categories=categories)
        mock_results = []
        for cat in categories:
            mock_res = evaluator.evaluate_category(
                category=cat,
                defect_gt_masks=[np.zeros((64, 64), dtype=np.uint8)],
                defect_pred_maps=[np.zeros((64, 64), dtype=np.float32)],
                defect_max_confs=[0.8],
                good_max_confs=[0.05],
                box_map50=0.82,
                mask_map50=0.80,
                mask_map50_95=0.48,
            )
            mock_results.append(mock_res)

        summary = evaluator.aggregate_results(mock_results)
        summary["dry_run"] = True
        summary["timestamp"] = datetime.now().isoformat()
        summary_path = os.path.join(out_dir, "summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Dry-run complete! Saved verified metrics template to {summary_path}")
        return

    # Real Run on GPU (Strict Defect-Free Training Regime by default)
    defect_free_mode = bool(ds_cfg.get("defect_free", True))
    logger.info(f"Preparing dataset in {processed_dir} (defect_free={defect_free_mode})...")
    loader = MVTecLoader(
        root_dir=raw_root,
        split_ratio=ds_cfg.get("split_ratio", 0.85),
        include_good_train=True,
        good_ratio=ds_cfg.get("good_ratio", 0.15),
        seed=active_seed,
        defect_free=defect_free_mode,
    )

    # Clean stale processed_dir to prevent duplicate image accumulation across retries
    if os.path.exists(processed_dir):
        logger.info(f"Cleaning existing processed dataset directory: {processed_dir}")
        shutil.rmtree(processed_dir)

    # Stream per category to keep peak RAM low (<1.5 GB) and guarantee fixed class IDs
    category_map = {cat: idx for idx, cat in enumerate(sorted(categories))}
    exporter = YOLOSegExporter(output_dir=processed_dir, category_map=category_map, save_debug_masks=False)
    for cat in categories:
        train_samples = loader.load(categories=[cat], split="train")
        processed_train = train_pipeline.run(train_samples)
        exporter.export(processed_train, split="train")
        del train_samples, processed_train

        val_samples = loader.load(categories=[cat], split="val")
        processed_val = train_pipeline.run(val_samples)
        exporter.export(processed_val, split="val")
        del val_samples, processed_val
        gc.collect()

    # Launch Ultralytics YOLOv11-seg training with standardized optimizer & absolute save_dir
    from ultralytics import YOLO
    model_cfg = cfg.get("model", {})
    weights = model_cfg.get("weights", "yolo11l-seg.pt")
    epochs = model_cfg.get("epochs", 100)
    imgsz = model_cfg.get("imgsz", 640)
    batch = model_cfg.get("batch", 16)
    abs_out_dir = os.path.abspath(out_dir)

    logger.info(f"Launching YOLOv11-seg training: {weights} on {device} -> {abs_out_dir}/train_run")
    yolo_model = YOLO(weights)
    yolo_model.train(
        data=os.path.join(processed_dir, "dataset.yaml"),
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        workers=2,
        device=device,
        seed=active_seed,
        optimizer=model_cfg.get("optimizer", "AdamW"),
        cos_lr=bool(model_cfg.get("cos_lr", True)),
        deterministic=True,
        cache=model_cfg.get("cache", False),
        project=abs_out_dir,
        name="train_run",
        exist_ok=True,
    )

    save_dir = (
        str(yolo_model.trainer.save_dir)
        if getattr(yolo_model, "trainer", None) is not None
        else os.path.join(abs_out_dir, "train_run")
    )
    best_weights = os.path.join(save_dir, "weights", "best.pt")
    logger.info(f"Resolved training save_dir={save_dir} | best_weights_exists={os.path.exists(best_weights)}")
    del yolo_model
    gc.collect()

    # Load best checkpoint and isolated real test split ONLY after training finishes
    eval_model = YOLO(best_weights) if os.path.exists(best_weights) else YOLO(weights)
    test_samples = loader.load(categories=categories, split="test")
    run_robustness = bool(
        cfg.get("evaluation", {}).get("robustness_benchmark", False)
        or cfg.get("robustness", {}).get("enabled", False)
    )
    run_post_train_evaluation(
        yolo_model=eval_model,
        test_samples=test_samples,
        eval_pipeline=eval_pipeline,
        categories=categories,
        processed_dir=processed_dir,
        out_dir=out_dir,
        exp_id=exp_id,
        imgsz=imgsz,
        run_robustness=run_robustness,
    )
    del test_samples, eval_model
    gc.collect()
    logger.info(f"Experiment {exp_id} successfully completed!")


if __name__ == "__main__":
    main()
