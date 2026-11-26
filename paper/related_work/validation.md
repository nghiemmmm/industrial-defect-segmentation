# SECTION II: RELATED WORK — KIỂM TOÁN NGHIỆM THU (VALIDATION)

- [x] **Kiến trúc Modular:** Đã tách độc lập tại `paper/sections/related_work.tex` và gọi bằng `\input{sections/related_work}` trong `paper/paper.tex`.
- [x] **Cập nhật SOTA 2023–2025:** Đã bổ sung đầy đủ `SimpleNet` (CVPR'23), `EfficientAD` (WACV'24), `DeSTSeg` (CVPR'23), `RealNet` (CVPR'24), `FAIR` (*Adv. Eng. Inform.*'25), và `Omni-Frequency Channel-Selection` (*IEEE TIP*'23).
- [x] **Tính phê phán học thuật & Cầu nối YOLO:** Loại bỏ lỗi cài đặt *Power-of-Two* khỏi danh sách hạn chế khoa học (chỉ giữ 2 hạn chế cốt lõi ở II-B: *Purely Spatial Operation* và *False-Alarm Amplification*); bổ sung cầu nối sang họ YOLO một giai đoạn ở cuối II-A.
- [x] **Khử lặp từ với Section I:** Đã đánh bóng câu ImageNet-C/MVTec-AD-C, bỏ lặp `identity-shortcut reconstruction`, `benign`, và cấu trúc câu lặp từ Section I.
- [x] **Độ phù hợp 20/20 trích dẫn trong Section II:** 100% trích dẫn khớp đúng phương pháp, năm, hội nghị/tạp chí; 0 lặp nội bộ; gộp chuẩn `[x, y]` theo `ieee-citation-formatting`; tổng toàn bài **26/26** tài liệu (`warning$ -- 0`).

**Trạng thái phê duyệt:** `APPROVED (VERIFIED)` — 26/11/2026.
