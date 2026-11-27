#!/usr/bin/env python3
"""
Full-Dataset Table I Verification Benchmark (Multi-Core):
Evaluates Unfiltered Identity Roundtrip (T^{-1}(T(I))) numerical preservation
for 2D-FFT and 2D-DWT across ALL unique RGB images in the 6 focus MVTec AD categories
(train/good + test/good + test/<defect_type>).

Outputs reproducible JSON and Markdown reports to results/verification/.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor
import json
import math
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Tuple

import cv2
import numpy as np

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_engine.frequency.dwt_filter import DWTSubbandFilter
from data_engine.frequency.fft_filter import FFTPeriodicSuppressionFilter
from data_engine.sample import Sample

DEFAULT_CATEGORIES = ["grid", "carpet", "tile", "screw", "pill", "bottle"]
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".bmp")

_WORKER_FFT = None
_WORKER_DWT = None


def _init_worker():
    global _WORKER_FFT, _WORKER_DWT
    cv2.setNumThreads(1)
    _WORKER_FFT = FFTPeriodicSuppressionFilter(tau=1e9, butterworth_cutoff=None, use_luminance=True)
    _WORKER_DWT = DWTSubbandFilter(alpha=1.0, gamma=1.0, wavelet="haar", use_luminance=True)


def compute_image_metrics(img1: np.ndarray, img2: np.ndarray) -> Tuple[float, float, float, float]:
    """Computes (MAE, MSE, PSNR, SSIM) between two uint8 RGB images (Wang et al. 2004)."""
    f1 = img1.astype(np.float32)
    f2 = img2.astype(np.float32)
    diff = np.abs(f1 - f2)
    mae = float(np.mean(diff))
    mse = float(np.mean(diff * diff))
    psnr = float("inf") if mse == 0.0 else float(10.0 * math.log10((255.0 ** 2) / mse))

    if mse == 0.0:
        return mae, mse, psnr, 1.0

    c1 = (0.01 * 255.0) ** 2
    c2 = (0.03 * 255.0) ** 2
    mu1 = cv2.GaussianBlur(f1, (11, 11), 1.5, borderType=cv2.BORDER_REFLECT)[5:-5, 5:-5]
    mu2 = cv2.GaussianBlur(f2, (11, 11), 1.5, borderType=cv2.BORDER_REFLECT)[5:-5, 5:-5]
    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.GaussianBlur(f1 * f1, (11, 11), 1.5, borderType=cv2.BORDER_REFLECT)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.GaussianBlur(f2 * f2, (11, 11), 1.5, borderType=cv2.BORDER_REFLECT)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.GaussianBlur(f1 * f2, (11, 11), 1.5, borderType=cv2.BORDER_REFLECT)[5:-5, 5:-5] - mu1_mu2
    ssim_map = ((2.0 * mu1_mu2 + c1) * (2.0 * sigma12 + c2)) / (
        (mu1_sq + mu2_sq + c1) * (sigma1_sq + sigma2_sq + c2)
    )
    ssim = float(np.mean(ssim_map))
    return mae, mse, psnr, ssim


def _process_single_image(args: Tuple[str, str]):
    cat, path = args
    bgr = cv2.imread(path, cv2.IMREAD_COLOR)
    if bgr is None:
        raise IOError(f"Failed to read image: {path}")
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    sample = Sample(image=rgb, category=cat, defect_type="good", is_anomaly=False, image_path=path)

    t0 = time.perf_counter()
    fft_out = _WORKER_FFT.process(sample)
    fft_ms = (time.perf_counter() - t0) * 1000.0
    fft_m = compute_image_metrics(rgb, fft_out.image)

    t0 = time.perf_counter()
    dwt_out = _WORKER_DWT.process(sample)
    dwt_ms = (time.perf_counter() - t0) * 1000.0
    dwt_m = compute_image_metrics(rgb, dwt_out.image)

    return fft_m, dwt_m, fft_ms, dwt_ms


def collect_unique_rgb_images(root_dir: str, categories: List[str]) -> Dict[str, Dict[str, List[str]]]:
    """Collects all unique RGB images (train/good and test/**) without double-counting."""
    collected: Dict[str, Dict[str, List[str]]] = {}
    for cat in categories:
        cat_dir = os.path.join(root_dir, cat)
        train_good_dir = os.path.join(cat_dir, "train", "good")
        test_dir = os.path.join(cat_dir, "test")
        gt_dir = os.path.join(cat_dir, "ground_truth")

        train_good = []
        if os.path.isdir(train_good_dir):
            train_good = sorted(
                os.path.join(train_good_dir, f)
                for f in os.listdir(train_good_dir)
                if f.lower().endswith(IMAGE_EXTS)
            )

        test_good = []
        test_defect = []
        if os.path.isdir(test_dir):
            for sub in sorted(os.listdir(test_dir)):
                sub_path = os.path.join(test_dir, sub)
                if not os.path.isdir(sub_path):
                    continue
                files = sorted(
                    os.path.join(sub_path, f)
                    for f in os.listdir(sub_path)
                    if f.lower().endswith(IMAGE_EXTS)
                )
                if sub == "good":
                    test_good.extend(files)
                else:
                    test_defect.extend(files)

        gt_masks = []
        if os.path.isdir(gt_dir):
            for sub in sorted(os.listdir(gt_dir)):
                sub_path = os.path.join(gt_dir, sub)
                if not os.path.isdir(sub_path):
                    continue
                gt_masks.extend(
                    sorted(
                        os.path.join(sub_path, f)
                        for f in os.listdir(sub_path)
                        if f.lower().endswith(IMAGE_EXTS)
                    )
                )

        collected[cat] = {
            "train_good": train_good,
            "test_good": test_good,
            "test_defect": test_defect,
            "gt_masks": gt_masks,
        }
    return collected


def summarize_metrics(maes: List[float], mses: List[float], psnrs: List[float], ssims: List[float]) -> Dict[str, object]:
    mean_mae = float(np.mean(maes))
    mean_mse = float(np.mean(mses))
    all_exact = all(m == 0.0 for m in mses)
    if all_exact:
        mean_psnr_val = "inf"
        min_psnr_val = "inf"
    else:
        finite_psnrs = [p for p in psnrs if math.isfinite(p)]
        mean_psnr_val = round(float(np.mean(finite_psnrs)), 2) if finite_psnrs else "inf"
        min_psnr_val = round(float(np.min(finite_psnrs)), 2) if finite_psnrs else "inf"
    return {
        "mae_mean": round(mean_mae, 4),
        "mae_max": round(float(np.max(maes)), 4),
        "mse_mean": round(mean_mse, 4),
        "psnr_mean_db": mean_psnr_val,
        "psnr_min_db": min_psnr_val,
        "psnr_from_mean_mse_db": "inf" if mean_mse == 0.0 else round(float(10.0 * math.log10((255.0 ** 2) / mean_mse)), 2),
        "ssim_mean": round(float(np.mean(ssims)), 4),
        "ssim_min": round(float(np.min(ssims)), 4),
        "exact_identity_count": int(sum(1 for m in mses if m == 0.0)),
        "total_images": len(maes),
    }


def run_full_roundtrip_benchmark(
    root_dir: str = "mvtec_ad",
    categories: List[str] = DEFAULT_CATEGORIES,
    output_dir: str = "results/verification",
    workers: int = 0,
) -> Dict[str, object]:
    collected = collect_unique_rgb_images(root_dir, categories)
    num_workers = workers if workers > 0 else max(1, min(8, (os.cpu_count() or 4)))
    print(f"Starting Table I benchmark with {num_workers} worker processes...", flush=True)

    all_fft_mae, all_fft_mse, all_fft_psnr, all_fft_ssim = [], [], [], []
    all_dwt_mae, all_dwt_mse, all_dwt_psnr, all_dwt_ssim = [], [], [], []
    fft_times_ms, dwt_times_ms = [], []

    per_category: Dict[str, object] = {}
    dataset_counts: Dict[str, object] = {}

    total_train_good = 0
    total_test_good = 0
    total_test_defect = 0
    total_gt_masks = 0

    with ProcessPoolExecutor(max_workers=num_workers, initializer=_init_worker) as ex:
        for cat in categories:
            info = collected[cat]
            rgb_paths = info["train_good"] + info["test_good"] + info["test_defect"]
            total_train_good += len(info["train_good"])
            total_test_good += len(info["test_good"])
            total_test_defect += len(info["test_defect"])
            total_gt_masks += len(info["gt_masks"])

            dataset_counts[cat] = {
                "train_good": len(info["train_good"]),
                "test_good": len(info["test_good"]),
                "test_defect": len(info["test_defect"]),
                "test_total": len(info["test_good"]) + len(info["test_defect"]),
                "gt_masks": len(info["gt_masks"]),
                "unique_rgb_total": len(rgb_paths),
            }

            cat_fft_mae, cat_fft_mse, cat_fft_psnr, cat_fft_ssim = [], [], [], []
            cat_dwt_mae, cat_dwt_mse, cat_dwt_psnr, cat_dwt_ssim = [], [], [], []

            t_cat_start = time.perf_counter()
            tasks = [(cat, p) for p in rgb_paths]
            for fft_m, dwt_m, fft_ms, dwt_ms in ex.map(_process_single_image, tasks, chunksize=8):
                cat_fft_mae.append(fft_m[0])
                cat_fft_mse.append(fft_m[1])
                cat_fft_psnr.append(fft_m[2])
                cat_fft_ssim.append(fft_m[3])
                cat_dwt_mae.append(dwt_m[0])
                cat_dwt_mse.append(dwt_m[1])
                cat_dwt_psnr.append(dwt_m[2])
                cat_dwt_ssim.append(dwt_m[3])
                fft_times_ms.append(fft_ms)
                dwt_times_ms.append(dwt_ms)

            elapsed = time.perf_counter() - t_cat_start
            per_category[cat] = {
                "unique_rgb_images": len(rgb_paths),
                "fft_2d": summarize_metrics(cat_fft_mae, cat_fft_mse, cat_fft_psnr, cat_fft_ssim),
                "dwt_2d": summarize_metrics(cat_dwt_mae, cat_dwt_mse, cat_dwt_psnr, cat_dwt_ssim),
                "elapsed_sec": round(elapsed, 2),
            }

            all_fft_mae.extend(cat_fft_mae)
            all_fft_mse.extend(cat_fft_mse)
            all_fft_psnr.extend(cat_fft_psnr)
            all_fft_ssim.extend(cat_fft_ssim)
            all_dwt_mae.extend(cat_dwt_mae)
            all_dwt_mse.extend(cat_dwt_mse)
            all_dwt_psnr.extend(cat_dwt_psnr)
            all_dwt_ssim.extend(cat_dwt_ssim)

            print(
                f"[{cat:6s}] n={len(rgb_paths):3d} | "
                f"FFT PSNR={per_category[cat]['fft_2d']['psnr_mean_db']} dB, SSIM={per_category[cat]['fft_2d']['ssim_mean']}, MAE={per_category[cat]['fft_2d']['mae_mean']} | "
                f"DWT PSNR={per_category[cat]['dwt_2d']['psnr_mean_db']} dB, SSIM={per_category[cat]['dwt_2d']['ssim_mean']}, MAE={per_category[cat]['dwt_2d']['mae_mean']} "
                f"({elapsed:.1f}s)",
                flush=True,
            )

    total_rgb = total_train_good + total_test_good + total_test_defect
    report = {
        "timestamp": datetime.now().isoformat(),
        "root_dir": os.path.abspath(root_dir),
        "categories": categories,
        "dataset_totals": {
            "train_good": total_train_good,
            "test_good": total_test_good,
            "test_defect": total_test_defect,
            "test_total": total_test_good + total_test_defect,
            "unique_rgb_total": total_rgb,
            "gt_masks": total_gt_masks,
            "total_png_files": total_rgb + total_gt_masks,
        },
        "dataset_per_category": dataset_counts,
        "overall": {
            "fft_2d": {
                **summarize_metrics(all_fft_mae, all_fft_mse, all_fft_psnr, all_fft_ssim),
                "mean_cpu_latency_ms": round(float(np.mean(fft_times_ms)), 2),
            },
            "dwt_2d": {
                **summarize_metrics(all_dwt_mae, all_dwt_mse, all_dwt_psnr, all_dwt_ssim),
                "mean_cpu_latency_ms": round(float(np.mean(dwt_times_ms)), 2),
            },
        },
        "per_category": per_category,
    }

    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, "table1_roundtrip_full.json")
    md_path = os.path.join(output_dir, "table1_roundtrip_full.md")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    fft_ov = report["overall"]["fft_2d"]
    dwt_ov = report["overall"]["dwt_2d"]
    md_lines = [
        "# Table I Full-Dataset Unfiltered Identity Roundtrip Verification",
        "",
        f"- **Timestamp:** {report['timestamp']}",
        f"- **Total Unique RGB Images:** {total_rgb:,} (`{total_train_good:,}` train/good + `{total_test_good + total_test_defect:,}` test = `{total_test_defect:,}` defect + `{total_test_good:,}` test/good)",
        f"- **Ground-Truth Masks:** {total_gt_masks:,} (Total PNG files: `{total_rgb + total_gt_masks:,}`)",
        "",
        "## Overall Summary (Table I)",
        "",
        "| Transform | MAE (0-255) | Mean PSNR (dB) | Global PSNR (dB) | SSIM | Mean CPU Latency (ms) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: |",
        f"| **2D-FFT** | `{fft_ov['mae_mean']:.4f}` | `{fft_ov['psnr_mean_db']}` | `{fft_ov['psnr_from_mean_mse_db']}` | `{fft_ov['ssim_mean']:.4f}` | `{fft_ov['mean_cpu_latency_ms']:.2f}` |",
        f"| **2D-DWT (Haar)** | `{dwt_ov['mae_mean']:.4f}` | `{dwt_ov['psnr_mean_db']}` | `{dwt_ov['psnr_from_mean_mse_db']}` | `{dwt_ov['ssim_mean']:.4f}` | `{dwt_ov['mean_cpu_latency_ms']:.2f}` |",
        "",
        "## Per-Category Breakdown",
        "",
        "| Category | Train Good | Test Good | Test Defect | Unique RGB | FFT MAE | FFT PSNR (dB) | FFT SSIM | DWT MAE | DWT PSNR (dB) | DWT SSIM |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    for cat in categories:
        dc = dataset_counts[cat]
        fc = per_category[cat]["fft_2d"]
        wc = per_category[cat]["dwt_2d"]
        md_lines.append(
            f"| `{cat}` | {dc['train_good']} | {dc['test_good']} | {dc['test_defect']} | {dc['unique_rgb_total']} | "
            f"{fc['mae_mean']:.4f} | {fc['psnr_mean_db']} | {fc['ssim_mean']:.4f} | "
            f"{wc['mae_mean']:.4f} | {wc['psnr_mean_db']} | {wc['ssim_mean']:.4f} |"
        )

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")

    print(f"\nSaved full Table I verification reports to:\n  - {json_path}\n  - {md_path}", flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description="Full-dataset Table I frequency identity roundtrip benchmark.")
    parser.add_argument("--root", type=str, default="mvtec_ad", help="Path to MVTec AD root directory")
    parser.add_argument("--output-dir", type=str, default="results/verification", help="Output directory")
    parser.add_argument("--categories", nargs="+", default=DEFAULT_CATEGORIES, help="Target categories")
    parser.add_argument("--workers", type=int, default=0, help="Number of worker processes (0=auto)")
    args = parser.parse_args()
    run_full_roundtrip_benchmark(
        root_dir=args.root,
        categories=args.categories,
        output_dir=args.output_dir,
        workers=args.workers,
    )


if __name__ == "__main__":
    main()
