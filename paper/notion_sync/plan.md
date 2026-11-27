# PLAN — Quy Trình Vận Hành Đồng Bộ Thí Nghiệm & Bài Báo

## 1. Khi bắt đầu chạy thí nghiệm
```bash
python tools/notion_experiment_sync.py start --exp exp01_cutpaste --seed 42 --run-type OFFICIAL
```
→ Chuyển dòng `exp01_cutpaste` trên Notion sang `Status = RUNNING`.

## 2. Khi kết thúc thí nghiệm
```bash
python tools/notion_experiment_sync.py finish --exp exp01_cutpaste --summary results/experiments/exp01_cutpaste/summary.json --run-type OFFICIAL
```
→ Tự động đọc `summary.json`, điền 9 cột metric và chuyển `Status = DONE`.

## 3. Đồng bộ hàng loạt từ `results/ablation_summary.csv`
```bash
python tools/notion_experiment_sync.py sync-csv --csv results/ablation_summary.csv --run-type OFFICIAL
```

## 4. Xuất bảng LaTeX chuẩn `booktabs` để dán vào `paper/sections/experiments.tex`
```bash
python tools/notion_experiment_sync.py export-latex --official-only
```

## 4.5. Kiểm tra nhanh tiến độ hoàn thiện 5 bảng của Paper từ terminal
```bash
python tools/notion_experiment_sync.py paper-status
```

## 5. Đồng bộ hai chiều qua Notion MCP trong Antigravity
- Agent gọi `API-query-data-source` (`424e9079-9593-809f-91a2-000b5235736f`) để kiểm tra tiến độ.
- Agent cập nhật bảng Print/LaTeX-Ready Summary trên **Paper Control Hub** (`424e9079-9593-812d-99ce-fb52a3c872da`) bằng `API-update-page-markdown`.
