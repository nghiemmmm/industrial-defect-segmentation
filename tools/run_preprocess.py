#!/usr/bin/env python3
"""
CLI Tool: Run Industrial Defect Preprocessing & Export Pipeline.

Usage:
    python tools/run_preprocess.py --config configs/mvtec_preprocessing.yaml
    python tools/run_preprocess.py --dataset mvtec --root ./mvtec_ad --out ./datasets/processed/mvtec_v1
"""

import os
import sys
import argparse
import logging
import yaml
from typing import Dict, Any

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_engine.loaders.mvtec_loader import MVTecLoader
from data_engine.loaders.visa_loader import VisALoader
from data_engine.exporters.yolo_seg_exporter import YOLOSegExporter
from data_engine.base import Pipeline

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("DataEngineCLI")


def load_yaml_config(config_path: str) -> Dict[str, Any]:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Industrial Defect Segmentation Preprocessing Pipeline")
    parser.add_argument("--config", type=str, default="", help="Path to YAML configuration file")
    parser.add_argument("--dataset", type=str, choices=["mvtec", "visa"], default="mvtec", help="Dataset type")
    parser.add_argument("--root", type=str, default="", help="Root directory of the raw dataset")
    parser.add_argument("--out", type=str, default="", help="Output directory for processed dataset")
    parser.add_argument("--good-ratio", type=float, default=None, help="Ratio of normal images to defects (e.g. 0.15)")
    parser.add_argument("--split-ratio", type=float, default=0.8, help="Train/val split ratio for defect images")
    parser.add_argument("--save-masks", action="store_true", help="Save debug mask PNGs")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for deterministic splitting")
    args = parser.parse_args()

    # Load configuration
    cfg = {}
    if args.config:
        cfg = load_yaml_config(args.config)

    # CLI arguments override config
    ds_cfg = cfg.get("dataset", {})
    exp_cfg = cfg.get("export", {})

    dataset_name = args.dataset or ds_cfg.get("name", "mvtec")
    root_dir = args.root or ds_cfg.get("root_dir", "./mvtec_ad")
    output_dir = args.out or exp_cfg.get("output_dir", "./datasets/processed/output")
    split_ratio = args.split_ratio if args.split_ratio != 0.8 else ds_cfg.get("split_ratio", 0.8)
    good_ratio = args.good_ratio if args.good_ratio is not None else ds_cfg.get("good_ratio", 0.15)
    save_masks = args.save_masks or exp_cfg.get("save_debug_masks", False)
    seed = args.seed if args.seed != 42 else ds_cfg.get("seed", 42)

    logger.info("=" * 60)
    logger.info("  INDUSTRIAL DEFECT DATASET PREPROCESSING ENGINE  ")
    logger.info("=" * 60)
    logger.info(f"Dataset      : {dataset_name.upper()}")
    logger.info(f"Source Root  : {root_dir}")
    logger.info(f"Output Target: {output_dir}")
    logger.info(f"Split Ratio  : {split_ratio:.2f}")
    logger.info(f"Good Ratio   : {good_ratio}")
    logger.info(f"Seed         : {seed}")
    logger.info("=" * 60)

    if not os.path.exists(root_dir):
        logger.error(f"Source directory does not exist: {root_dir}")
        logger.info("Please provide a valid dataset path via --root or check your config file.")
        sys.exit(1)

    # 1. Instantiate Dataset Loader
    if dataset_name.lower() in ("mvtec", "mvtec_ad"):
        loader = MVTecLoader(
            root_dir=root_dir,
            split_ratio=split_ratio,
            include_good_train=True,
            good_ratio=good_ratio,
            seed=seed,
        )
    elif dataset_name.lower() == "visa":
        loader = VisALoader(
            root_dir=root_dir,
            split_ratio=split_ratio,
            good_ratio=good_ratio,
            seed=seed,
        )
    else:
        raise ValueError(f"Unsupported dataset: {dataset_name}")

    categories = loader.get_categories()
    logger.info(f"Found {len(categories)} categories: {', '.join(categories)}")

    # 2. Load Train and Val Splits
    logger.info("Loading training samples...")
    train_samples = loader.load(split="train")
    logger.info("Loading validation samples...")
    val_samples = loader.load(split="val")

    # 3. Setup Pipeline (empty or populated with processors)
    pipeline = Pipeline()
    logger.info(f"Executing pipeline: {pipeline}")
    processed_train = pipeline.run(train_samples)
    processed_val = pipeline.run(val_samples)

    # 4. Export to YOLO format
    exporter = YOLOSegExporter(
        output_dir=output_dir,
        save_debug_masks=save_masks,
    )
    logger.info("Exporting train split...")
    train_stats = exporter.export(processed_train, split="train", dataset_name=dataset_name)
    logger.info("Exporting val split...")
    val_stats = exporter.export(processed_val, split="val", dataset_name=dataset_name)

    logger.info("=" * 60)
    logger.info("PROCESSING SUMMARY:")
    logger.info(f"Train samples exported : {train_stats['total_exported']} (Anomalies: {train_stats['anomalies']}, Normal: {train_stats['defect_free']})")
    logger.info(f"Val samples exported   : {val_stats['total_exported']} (Anomalies: {val_stats['anomalies']}, Normal: {val_stats['defect_free']})")
    logger.info(f"YOLO dataset config     : {os.path.join(output_dir, 'dataset.yaml')}")
    logger.info(f"Pipeline metadata log  : {os.path.join(output_dir, 'pipeline_meta.json')}")
    logger.info("=" * 60)
    logger.info("Done! Dataset is ready for YOLO training.")


if __name__ == "__main__":
    main()
