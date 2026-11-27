# MISSION — Notion Paper Control & Experiment Sync

## 1. Mục Tiêu Chiến Lược
Xây dựng hệ thống đồng bộ hai chiều giữa mã nguồn thực nghiệm (`experiments/`, `results/`), **Notion Paper Control Hub**, và bản thảo bài báo (`paper/sections/experiments.tex`) nhằm:
- Theo dõi tập trung toàn bộ ma trận thực nghiệm `EXP-00` đến `EXP-11` theo thời gian thực (`PLANNED` → `RUNNING` → `DONE`/`FAILED`).
- Bảo vệ tuyệt đối nguyên tắc **Zero Hallucination** của skill `academic-paper-authoring` (tách bạch `OFFICIAL` vs `DRY_RUN`, giữ `--` cho các ô chưa chạy xong).
- Cung cấp giao diện rõ ràng, dễ in/xuất PDF và dễ trích xuất bảng LaTeX `booktabs` cho bài báo FJCAI / Q1.

## 2. Tài Nguyên Notion Liên Kết
- **Paper Control Hub:** `424e9079-9593-812d-99ce-fb52a3c872da`
- **Experiment Metrics Tracker DB (`paper`):**
  - `database_id`: `424e9079-9593-8045-b0b6-d6c4482add47`
  - `data_source_id`: `424e9079-9593-809f-91a2-000b5235736f`
- **5 trang quản trị con:**
  - `01_Mission`: `424e9079-9593-8147-9c51-f97cf6e40292`
  - `02_RoadMap`: `424e9079-9593-816c-9eca-cb22a5dfe384`
  - `03_Requirements`: `424e9079-9593-8120-a776-eb52179c580b`
  - `04_Plan`: `424e9079-9593-81af-a476-c22ba57132ea`
  - `05_Validation`: `424e9079-9593-81d3-b05a-c465c6cf7ca7`
  - `06_Verified_Benchmarks`: `424e9079-9593-81f7-91bc-c30bf7c28f72`
