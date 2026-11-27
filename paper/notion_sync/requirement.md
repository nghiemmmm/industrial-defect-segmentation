# REQUIREMENTS — Quy Chuẩn Đồng Bộ Notion ↔ Paper

1. **Khớp 100% Schema Metric:** 9 cột metric trong `paper` (`Mask_mAP50`, `Mask_mAP50_95`, `Pixel_AUROC`, `Image_AUROC`, `FAR_025`, `Texture_mAP50`, `Object_mAP50`, `Texture_PxAUROC`, `Object_PxAUROC`) phải ánh xạ trực tiếp từ `results/experiments/<exp_id>/summary.json` và `results/ablation_summary.csv`.
2. **Chống Nhầm Lẫn `DRY_RUN`:** Mọi bản chạy thử bắt buộc gắn `Run_Type = DRY_RUN`. Lệnh `export-latex --official-only` mặc định loại bỏ toàn bộ dòng `DRY_RUN` hoặc `Status != DONE`.
3. **Bảo Mật Tuyệt Đối:**
   - `NOTION_TOKEN` chỉ tồn tại trong `.env` (được ignore bởi `.gitignore`).
   - Không ghi, in, hay log token trong stdout/stderr hoặc mã nguồn.
4. **Tính Dễ In & Trích Xuất:** Trang Hub giữ bảng tóm tắt gọn gàng, rõ ràng để xuất PDF/in trực tiếp hoặc copy sang LaTeX.
