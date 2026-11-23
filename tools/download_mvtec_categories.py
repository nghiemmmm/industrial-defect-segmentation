#!/usr/bin/env python3
"""
MVTec AD 6-Category Downloader.
Downloads only the 6 representative target categories:
- Textures: grid, carpet, tile
- Objects: screw, pill, bottle

Utilizes high-speed HuggingFace CDN mirror (bhanu6969/mvtec-ad) to download
directly into ./mvtec_ad/ without downloading the remaining 9 unused categories.
"""

import os
import sys
import argparse
from typing import List

try:
    from huggingface_hub import snapshot_download
except ImportError:
    print("[ERROR] huggingface_hub is not installed. Please install with: pip install huggingface_hub")
    sys.exit(1)

DEFAULT_CATEGORIES = ["grid", "carpet", "tile", "screw", "pill", "bottle"]
HF_REPO_ID = "bhanu6969/mvtec-ad"


def download_categories(categories: List[str], target_dir: str = "./mvtec_ad"):
    os.makedirs(target_dir, exist_ok=True)
    patterns = [f"{cat}/**" for cat in categories]

    print("=================================================================")
    print("           MVTEC AD TARGET DATASET PREPARATION TOOL              ")
    print("=================================================================")
    print(f"HuggingFace Mirror   : {HF_REPO_ID}")
    print(f"Target Directory     : {os.path.abspath(target_dir)}")
    print(f"Selected Categories  : {categories} ({len(categories)} categories)")
    print(f"Filter Patterns      : {patterns}")
    print("=================================================================")
    print("[INFO] Fetching files from CDN. Only the 6 selected categories will be downloaded...")

    downloaded_path = snapshot_download(
        repo_id=HF_REPO_ID,
        repo_type="dataset",
        local_dir=target_dir,
        allow_patterns=patterns,
        max_workers=8,
    )

    print(f"\n[SUCCESS] Categories downloaded successfully into: {downloaded_path}")
    print("Verifying downloaded category directories:")
    for cat in categories:
        cat_p = os.path.join(target_dir, cat)
        if os.path.exists(cat_p):
            subdirs = os.listdir(cat_p)
            print(f"  [V] {cat:8s}: {subdirs}")
        else:
            print(f"  [X] {cat:8s}: Missing!")


def main():
    parser = argparse.ArgumentParser(description="Download target 6 MVTec AD categories.")
    parser.add_argument(
        "--categories",
        type=str,
        default=",".join(DEFAULT_CATEGORIES),
        help="Comma-separated category list",
    )
    parser.add_argument(
        "--target-dir",
        type=str,
        default="./mvtec_ad",
        help="Target root directory",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only display download plan without downloading.",
    )

    args = parser.parse_args()
    cats = [c.strip() for c in args.categories.split(",") if c.strip()]

    if args.dry_run:
        print("[DRY RUN] Target categories to download:", cats)
        print("HuggingFace patterns:", [f"{c}/**" for c in cats])
        return

    download_categories(cats, target_dir=args.target_dir)


if __name__ == "__main__":
    main()
