# VALIDATION — Checklist Kiểm Toán Đồng Bộ Notion ↔ Paper

- [x] Database `paper` có đủ 15 cột chuẩn paper và 12 dòng `exp00_baseline`..`exp11_full_system`.
- [x] `exp00_baseline` gắn rõ `Run_Type = DRY_RUN`; các kịch bản `EXP-01..EXP-11` ở trạng thái `PLANNED` với ô metric trống (Zero Hallucination).
- [x] Paper Control Hub và 5 trang con (`01_Mission`..`05_Validation`) đã tạo và đồng bộ nội dung từ `paper/`.
- [x] `tools/notion_experiment_sync.py` chạy được `export-latex` kiểm thử đọc dữ liệu thực tế từ Notion mà không lộ `NOTION_TOKEN`.
- [x] Trang `06_Verified_Benchmarks` và 2 dòng Oracle (`ref_oracle_yolo11l_640`, `ref_oracle_yolo11x_1024`) đã khớp 100% số liệu trong `paper/sections/experiments.tex` và `results/`.
- [x] Lệnh `python tools/notion_experiment_sync.py paper-status` báo cáo đúng tiến độ theo từng `Target_Table`.
- [ ] (Khi có kết quả Colab A100) Mọi dòng `OFFICIAL` khớp 100% với `results/experiments/*/summary.json`.
- [ ] (Trước khi nộp bài) Biên dịch `paper/paper.tex` 2 vòng `pdflatex` + `bibtex` đạt `exit code 0`.
