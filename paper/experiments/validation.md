# SECTION IV: EXPERIMENTAL EVALUATION — KIỂM TOÁN NGHIỆM THU (VALIDATION)

- [x] **Kiến trúc Modular:** Tách độc lập tại `paper/sections/experiments.tex` và gọi qua `\input{sections/experiments}`.
- [x] **Zero Hallucination & Trung thực dữ liệu:**
  - Table I khớp 100% số liệu đo 2,857 ảnh MVTec AD.
  - Table II khớp 100% `results/metrics/extra_eval/per_category_ap.csv` và `false_alarms_summary.csv`.
  - Table III minh bạch trạng thái `dry_run=true` cho `EXP-00` và `--` (Pending A100 sweep) cho `EXP-01..11`, không tự bịa số liệu.
- [x] **Tách bạch Lý thuyết – Thực nghiệm:** Quy tụ đầy đủ siêu tham số từ Section III về IV-A và Table I về IV-C.
- [x] **Tham chiếu hình/bảng đầy đủ:** `Table I`, `Table II`, `Table III`, `Fig. 2`, `Fig. 3` đều được gọi và phân tích kỹ thuật trong văn bản.
- [x] **Biên dịch sạch:** 0 lỗi, 0 BibTeX warning, 0 `Overfull \hbox` trong toàn bộ Section IV.

**Trạng thái phê duyệt:** `VERIFIED (Structure & Real Baseline; Pending Colab EXP-01..11 population)` — 25/11/2026.
