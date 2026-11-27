#!/usr/bin/env python3
"""
Lightweight Notion Experiment Sync Helper (stdlib-only).

Syncs experiment lifecycle & metrics between local runs (experiments/, results/)
and the Notion Experiment Metrics Tracker database (`paper`).

Reads NOTION_TOKEN from environment or workspace root `.env` without ever
printing or logging the secret.

Usage examples:
  python tools/notion_experiment_sync.py start --exp exp01_cutpaste --seed 42 --run-type OFFICIAL
  python tools/notion_experiment_sync.py finish --exp exp01_cutpaste --summary results/experiments/exp01_cutpaste/summary.json --run-type OFFICIAL
  python tools/notion_experiment_sync.py sync-csv --csv results/ablation_summary.csv --run-type DRY_RUN
  python tools/notion_experiment_sync.py export-latex --official-only
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_DATABASE_ID = "424e9079-9593-8045-b0b6-d6c4482add47"
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

METRIC_COLUMNS = [
    "Mask_mAP50",
    "Mask_mAP50_95",
    "Pixel_AUROC",
    "Image_AUROC",
    "FAR_025",
    "Texture_mAP50",
    "Object_mAP50",
    "Texture_PxAUROC",
    "Object_PxAUROC",
]


def load_notion_token() -> str:
    """Load NOTION_TOKEN from environment or workspace root .env safely."""
    token = os.environ.get("NOTION_TOKEN", "").strip()
    if token:
        return token

    repo_root = Path(__file__).resolve().parent.parent
    env_path = repo_root / ".env"
    if env_path.is_file():
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export "):].strip()
            if not line.startswith("NOTION_TOKEN"):
                continue
            key, sep, value = line.partition("=")
            if key.strip() != "NOTION_TOKEN" or not sep:
                continue
            value = value.strip()
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            if value:
                return value
    raise RuntimeError("NOTION_TOKEN is not set in environment or workspace .env.")


def notion_request(method: str, path: str, token: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = f"{NOTION_API_BASE}{path}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Notion API {method} {path} failed (HTTP {exc.code}): {body[:300]}") from None


def query_all_rows(database_id: str, token: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    cursor: Optional[str] = None
    while True:
        payload: Dict[str, Any] = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor
        res = notion_request("POST", f"/databases/{database_id}/query", token, payload)
        rows.extend(res.get("results", []))
        if not res.get("has_more"):
            break
        cursor = res.get("next_cursor")
    return rows


def find_page_by_exp_name(database_id: str, exp_name: str, token: str) -> Optional[str]:
    payload = {
        "filter": {"property": "Name", "title": {"equals": exp_name}},
        "page_size": 5,
    }
    res = notion_request("POST", f"/databases/{database_id}/query", token, payload)
    results = res.get("results", [])
    return results[0]["id"] if results else None


def upsert_experiment_row(
    database_id: str,
    exp_name: str,
    properties: Dict[str, Any],
    token: str,
) -> str:
    page_id = find_page_by_exp_name(database_id, exp_name, token)
    if page_id:
        notion_request("PATCH", f"/pages/{page_id}", token, {"properties": properties})
        return f"UPDATED:{page_id}"
    full_props = {"Name": {"title": [{"text": {"content": exp_name}}]}, **properties}
    res = notion_request(
        "POST",
        "/pages",
        token,
        {"parent": {"database_id": database_id}, "properties": full_props},
    )
    return f"CREATED:{res['id']}"


def extract_metrics_from_summary(summary_path: Path) -> Dict[str, float]:
    data = json.loads(summary_path.read_text(encoding="utf-8"))
    overall = data.get("overall_mean", {})
    tex = data.get("texture_group_mean", {})
    obj = data.get("object_group_mean", {})
    mapping = {
        "Mask_mAP50": overall.get("mask_mAP50"),
        "Mask_mAP50_95": overall.get("mask_mAP50_95"),
        "Pixel_AUROC": overall.get("pixel_auroc"),
        "Image_AUROC": overall.get("image_auroc"),
        "FAR_025": overall.get("false_alarm_rate_025"),
        "Texture_mAP50": tex.get("mask_mAP50"),
        "Object_mAP50": obj.get("mask_mAP50"),
        "Texture_PxAUROC": tex.get("pixel_auroc"),
        "Object_PxAUROC": obj.get("pixel_auroc"),
    }
    return {k: round(float(v), 4) for k, v in mapping.items() if v is not None}


def build_metric_properties(metrics: Dict[str, float]) -> Dict[str, Any]:
    return {col: {"number": val} for col, val in metrics.items() if col in METRIC_COLUMNS}


def cmd_start(args: argparse.Namespace, token: str) -> None:
    props: Dict[str, Any] = {
        "Status": {"select": {"name": "RUNNING"}},
        "Run_Type": {"select": {"name": args.run_type}},
    }
    if args.seed:
        props["Seed"] = {"rich_text": [{"text": {"content": str(args.seed)}}]}
    if args.notes:
        props["Notes"] = {"rich_text": [{"text": {"content": args.notes}}]}
    outcome = upsert_experiment_row(args.database_id, args.exp, props, token)
    print(f"[start] {args.exp} -> Status=RUNNING ({outcome})")


def cmd_finish(args: argparse.Namespace, token: str) -> None:
    props: Dict[str, Any] = {
        "Status": {"select": {"name": args.status}},
        "Run_Type": {"select": {"name": args.run_type}},
    }
    if args.summary:
        metrics = extract_metrics_from_summary(Path(args.summary))
        props.update(build_metric_properties(metrics))
    if args.latency_ms is not None:
        props["Latency_ms"] = {"number": round(float(args.latency_ms), 2)}
    if args.notes:
        props["Notes"] = {"rich_text": [{"text": {"content": args.notes}}]}
    outcome = upsert_experiment_row(args.database_id, args.exp, props, token)
    print(f"[finish] {args.exp} -> Status={args.status} ({outcome})")


def cmd_sync_csv(args: argparse.Namespace, token: str) -> None:
    csv_path = Path(args.csv)
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            exp_name = (row.get("Experiment") or "").strip()
            if not exp_name:
                continue
            metrics: Dict[str, float] = {}
            for col in METRIC_COLUMNS:
                raw = (row.get(col) or "").strip()
                if raw:
                    metrics[col] = round(float(raw), 4)
            props: Dict[str, Any] = {
                "Status": {"select": {"name": "DONE"}},
                "Run_Type": {"select": {"name": args.run_type}},
                **build_metric_properties(metrics),
            }
            outcome = upsert_experiment_row(args.database_id, exp_name, props, token)
            print(f"[sync-csv] {exp_name} ({outcome})")


def _get_title(props: Dict[str, Any]) -> str:
    arr = props.get("Name", {}).get("title", [])
    return "".join(t.get("plain_text", "") for t in arr).strip()


def _get_select(props: Dict[str, Any], key: str) -> str:
    sel = props.get(key, {}).get("select")
    return sel.get("name", "") if isinstance(sel, dict) else ""


def _fmt_num(props: Dict[str, Any], key: str) -> str:
    val = props.get(key, {}).get("number")
    return f"{val:.3f}" if isinstance(val, (int, float)) else "--"


def cmd_export_latex(args: argparse.Namespace, token: str) -> None:
    rows = query_all_rows(args.database_id, token)
    parsed = []
    for r in rows:
        p = r.get("properties", {})
        name = _get_title(p)
        status = _get_select(p, "Status")
        run_type = _get_select(p, "Run_Type")
        if args.official_only and (run_type != "OFFICIAL" or status != "DONE"):
            continue
        parsed.append((name, status, run_type, p))

    parsed.sort(key=lambda x: x[0])

    print("% Auto-generated from Notion Experiment Metrics Tracker (paper)")
    print(r"\begin{tabular}{lccccc}")
    print(r"\toprule")
    print(r"Experiment & mAP$_{50}$ & mAP$_{50:95}$ & Px-AUROC & Img-AUROC & FAR@0.25 \\")
    print(r"\midrule")
    if not parsed:
        print(r"\multicolumn{6}{c}{\textit{No matching OFFICIAL DONE records yet}} \\")
    for name, _status, run_type, p in parsed:
        esc_name = name.replace("_", r"\_")
        if run_type == "DRY_RUN":
            esc_name += r"$^*$"
        line = " & ".join([
            esc_name,
            _fmt_num(p, "Mask_mAP50"),
            _fmt_num(p, "Mask_mAP50_95"),
            _fmt_num(p, "Pixel_AUROC"),
            _fmt_num(p, "Image_AUROC"),
            _fmt_num(p, "FAR_025"),
        ])
        print(f"{line} \\\\")
    print(r"\bottomrule")
    print(r"\end{tabular}")


def cmd_paper_status(args: argparse.Namespace, token: str) -> None:
    rows = query_all_rows(args.database_id, token)
    buckets: Dict[str, Dict[str, int]] = {}
    for r in rows:
        p = r.get("properties", {})
        table = _get_select(p, "Target_Table") or "Unassigned"
        status = _get_select(p, "Status") or "UNKNOWN"
        run_type = _get_select(p, "Run_Type") or "UNKNOWN"
        b = buckets.setdefault(
            table, {"total": 0, "official_done": 0, "dry_run_done": 0, "running": 0, "planned": 0, "failed": 0}
        )
        b["total"] += 1
        if status == "DONE" and run_type == "OFFICIAL":
            b["official_done"] += 1
        elif status == "DONE" and run_type == "DRY_RUN":
            b["dry_run_done"] += 1
        elif status == "RUNNING":
            b["running"] += 1
        elif status == "PLANNED":
            b["planned"] += 1
        elif status == "FAILED":
            b["failed"] += 1

    print(f"Notion Paper Progress ({len(rows)} records in database `paper`):")
    print("| Target Table | Total | OFFICIAL DONE | DRY_RUN DONE | RUNNING | PLANNED | FAILED |")
    print("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")
    for table in sorted(buckets.keys()):
        b = buckets[table]
        print(
            f"| {table} | {b['total']} | {b['official_done']} | {b['dry_run_done']} "
            f"| {b['running']} | {b['planned']} | {b['failed']} |"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync experiment status and metrics with Notion.")
    parser.add_argument(
        "--database-id",
        default=os.environ.get("NOTION_DATABASE_ID", DEFAULT_DATABASE_ID),
        help="Notion database ID (default: paper)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("start", help="Mark an experiment as RUNNING")
    p_start.add_argument("--exp", required=True)
    p_start.add_argument("--seed", default="")
    p_start.add_argument("--run-type", choices=["OFFICIAL", "DRY_RUN"], default="OFFICIAL")
    p_start.add_argument("--notes", default="")

    p_finish = sub.add_parser("finish", help="Upload summary.json metrics and mark DONE/FAILED")
    p_finish.add_argument("--exp", required=True)
    p_finish.add_argument("--summary", default="")
    p_finish.add_argument("--run-type", choices=["OFFICIAL", "DRY_RUN"], default="OFFICIAL")
    p_finish.add_argument("--status", choices=["DONE", "FAILED"], default="DONE")
    p_finish.add_argument("--latency-ms", type=float, default=None)
    p_finish.add_argument("--notes", default="")

    p_csv = sub.add_parser("sync-csv", help="Batch sync results/ablation_summary.csv to Notion")
    p_csv.add_argument("--csv", default="results/ablation_summary.csv")
    p_csv.add_argument("--run-type", choices=["OFFICIAL", "DRY_RUN"], default="OFFICIAL")

    p_tex = sub.add_parser("export-latex", help="Export Notion rows as an IEEEtran booktabs table")
    p_tex.add_argument("--official-only", action="store_true", help="Include only OFFICIAL + DONE rows")

    sub.add_parser("paper-status", help="Summarize experiment completion per Target_Table from Notion")

    args = parser.parse_args()
    token = load_notion_token()

    if args.command == "start":
        cmd_start(args, token)
    elif args.command == "finish":
        cmd_finish(args, token)
    elif args.command == "sync-csv":
        cmd_sync_csv(args, token)
    elif args.command == "export-latex":
        cmd_export_latex(args, token)
    elif args.command == "paper-status":
        cmd_paper_status(args, token)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
