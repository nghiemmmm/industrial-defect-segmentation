# ROADMAP — GitHub ↔ Google Drive ↔ Notion Sync & Experiment Tracking

| Giai đoạn | Hạng mục | Trạng thái | Ghi chú |
| :---: | :--- | :---: | :--- |
| **Pha 1** | Chuẩn hóa 9 thí nghiệm (`EXP-00`–`EXP-08`), `MaterialAdaptiveRouter`, vá 2 lỗi metric (Pixel-AUROC & Table V `mAP@50`/`FAR@0.25`), nâng cấp `colab_runner.ipynb` (`RUN_ONLY` + 9 cell riêng + auto-sync Drive) | **DONE** | `39/39` pytest pass; `CHANGELOG.md` created |
| **Pha 2** | Rà soát bảo mật `.gitignore`, commit & push sạch lên `origin/main` | **DONE** | Commits `4bf9570` + `80630dc` verified via GitHub MCP |
| **Pha 3** | Khởi tạo cây thư mục lưu trữ trên Google Drive (`nguyenducnghiem.thptllqt@gmail.com`, 5 TB) + upload backup `colab_runner.ipynb` | **DONE** | Root ID: `1wbDT8vogSHK-1uqVabM0asTFqhPr8--K` |
| **Pha 4** | Đồng bộ Notion DB `paper` (`424e9079-9593-8045-b0b6-d6c4482add47`) về đúng 9 dòng `EXP-00`–`EXP-08` (`PLANNED`) + 2 Oracle (`OFFICIAL DONE`), lưu trữ 3 dòng cũ thừa | **DONE** | Verified via `notion_experiment_sync.py paper-status` |
| **Pha 5A** | Chạy `EXP-00`–`EXP-08` + MVTec-AD-C (`EXP-01`, `EXP-05`) + GPU `cuFFT`/DWT latency qua Colab Extension trên IDE | **READY** | Mở trực tiếp `experiments/colab_runner.ipynb` |
| **Pha 5B** | Tải kết quả từ Drive → `notion_experiment_sync.py sync-csv` → điền Table III–VI → ép gọn đúng 8 trang Double-Blind FJCAI | **PLANNED** | Sau khi có kết quả GPU từ Pha 5A |

## Google Drive Folder IDs (`nguyenducnghiem.thptllqt@gmail.com`)
* `industrial-defect-segmentation/`: `1wbDT8vogSHK-1uqVabM0asTFqhPr8--K`
* `mvtec_ad/`: `1nj9SDjchrIspmd9JM2AC-JFc4l4xia_b`
* `notebooks/`: `1TZDMmKhQ-3Q-r_nFfEHYnGEwPdF0NbIf` (`colab_runner.ipynb`: `15ewNz0dMYWSzGWzpT0Qs7-MCflnjAbnS`)
* `results/`: `1tO2_QTJAnVjaskZZZhwaNM4wOXdO8poL`
* `checkpoints/`: `1pg3i-SQ25xoEPk1JX90ewq6wswEvtylk`
