#!/usr/bin/env python3
"""
Ablation Matrix Aggregator.
Collects experiment results from results/experiments/*/summary.json
and generates a consolidated Markdown and CSV comparison table across EXP-00 to EXP-08.
"""

import os
import glob
import json
import pandas as pd


def collect_ablation_results(results_root: str = "results/experiments") -> pd.DataFrame:
    summary_files = sorted(glob.glob(os.path.join(results_root, "*", "summary.json")))
    rows = []

    for sf in summary_files:
        exp_id = os.path.basename(os.path.dirname(sf))
        try:
            with open(sf, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        overall = data.get("overall_mean", {})
        tex_mean = data.get("texture_group_mean", {})
        obj_mean = data.get("object_group_mean", {})

        row = {
            "Experiment": exp_id,
            "Mask_mAP50": overall.get("mask_mAP50", 0.0),
            "Mask_mAP50_95": overall.get("mask_mAP50_95", 0.0),
            "Pixel_AUROC": overall.get("pixel_auroc", 0.0),
            "Image_AUROC": overall.get("image_auroc", 0.0),
            "FAR_025": overall.get("false_alarm_rate_025", 0.0),
            "Texture_mAP50": tex_mean.get("mask_mAP50", 0.0),
            "Object_mAP50": obj_mean.get("mask_mAP50", 0.0),
            "Texture_PxAUROC": tex_mean.get("pixel_auroc", 0.0),
            "Object_PxAUROC": obj_mean.get("pixel_auroc", 0.0),
        }
        rows.append(row)

    if not rows:
        # Provide template row
        rows.append({
            "Experiment": "EXP-00_baseline",
            "Mask_mAP50": 0.0,
            "Mask_mAP50_95": 0.0,
            "Pixel_AUROC": 0.0,
            "Image_AUROC": 0.0,
            "FAR_025": 0.0,
            "Texture_mAP50": 0.0,
            "Object_mAP50": 0.0,
            "Texture_PxAUROC": 0.0,
            "Object_PxAUROC": 0.0,
        })

    df = pd.DataFrame(rows)
    return df


def df_to_markdown_str(df: pd.DataFrame) -> str:
    """Formats DataFrame to Markdown table string with pure Python fallback."""
    try:
        return df.to_markdown(index=False)
    except Exception:
        cols = list(df.columns)
        header = "| " + " | ".join(str(c) for c in cols) + " |"
        sep = "| " + " | ".join(["---"] * len(cols)) + " |"
        rows = []
        for _, row in df.iterrows():
            rows.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
        return "\n".join([header, sep] + rows)


def main():
    df = collect_ablation_results()
    out_dir = "results"
    os.makedirs(out_dir, exist_ok=True)

    csv_path = os.path.join(out_dir, "ablation_summary.csv")
    md_path = os.path.join(out_dir, "ablation_summary.md")

    df.to_csv(csv_path, index=False)
    md_table = df_to_markdown_str(df)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Consolidated Ablation Matrix (EXP-00 to EXP-08)\n\n")
        f.write(md_table)
        f.write("\n")

    print(f"Generated ablation summary:\n  - CSV: {csv_path}\n  - Markdown: {md_path}")
    print("\n" + md_table)


if __name__ == "__main__":
    main()
