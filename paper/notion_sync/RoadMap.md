# ROADMAP — Notion Sync & Experiment Tracking

| Giai đoạn | Hạng mục | Trạng thái | Ghi chú |
| :---: | :--- | :---: | :--- |
| **Phase 1** | Cấu hình Notion MCP Server (`.agents/plugins/notion-mcp`) & bảo mật `.env` | **DONE** | Đã xác thực 24 tools |
| **Phase 2** | Nâng cấp schema Database `paper` (15 cột) & seed `EXP-00..EXP-11` | **DONE** | `exp00_baseline` gắn `DRY_RUN`; `EXP-01..11` = `PLANNED` |
| **Phase 3** | Tạo Paper Control Hub + 5 trang con (`01_Mission`..`05_Validation`) | **DONE** | Có bảng Print/LaTeX-Ready Summary |
| **Phase 4** | Tạo Python helper `tools/notion_experiment_sync.py` (start/finish/sync-csv/export-latex/paper-status) | **DONE** | Dùng stdlib Python, đọc `NOTION_TOKEN` từ `.env` |
| **Phase 4.5** | Bổ sung `06_Verified_Benchmarks` (Table I, II, SOTA, V & C++ parity) + 2 dòng Oracle vào DB `paper` | **DONE** | Khớp 100% `paper/sections/experiments.tex` & `results/` |
| **Phase 5** | Chạy thực nghiệm `EXP-00..EXP-11` trên Colab GPU A100 & đồng bộ số liệu `OFFICIAL` | **PLANNED** | Gắn `--run-type OFFICIAL`, đủ 3 seeds (`42, 1337, 2026`) |
| **Phase 6** | Xuất bảng LaTeX từ Notion sang `paper/sections/experiments.tex` & kiểm toán PDF | **PLANNED** | Biên dịch `pdflatex` + `bibtex` 2 vòng |
