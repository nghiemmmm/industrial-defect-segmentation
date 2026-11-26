# SECTION II: RELATED WORK — YÊU CẦU NỘI DUNG & ĐỊNH VỊ HỌC THUẬT (REQUIREMENTS)

> **Mục đích:** Định nghĩa cấu trúc, chiều sâu phê phán và danh sách trích dẫn bắt buộc cho Section II (*Related Work*) nhằm định vị rõ khoảng trống nghiên cứu dẫn trực tiếp sang Section III (*Proposed Methodology*), tuyệt đối không sa đà thành bài khảo sát chung chung (Survey).

---

## 1. Cấu Trúc 3 Tiểu Mục & Đoạn Định Vị
* **II-A. Industrial Anomaly Detection and Localization:**
  - Tổng hợp 2 nhánh kinh điển: Reconstruction-based (Autoencoder/GAN) và Feature-Embedding (PaDiM, PatchCore).
  - Phê phán 3 hạn chế trực tiếp cho sản xuất thực tế: độ trễ/băng thông tra cứu bộ nhớ ($<100\text{ FPS}$), đầu ra chỉ là heatmap liên tục thay vì mặt nạ đa giác thực thể, và thiếu cơ chế kiểm soát FAR tường minh.
* **II-B. Self-Supervised Anomaly Synthesis:**
  - Phân tích CutPaste, DRAEM (Perlin noise), NSA (Poisson image editing).
  - Chỉ thẳng 3 khoảng trống nghiên cứu: (1) thuần miền không gian bị hoa văn nền lấn át, (2) giả định lưới lũy thừa của 2 ($2^m$) gây lỗi trên kích thước ảnh công nghiệp tùy ý, (3) khuếch đại báo động giả (FAR) nếu thiếu mẫu âm bảo toàn.
* **II-C. Frequency-Domain Inspection and Optical Robustness:**
  - Trình bày nền tảng 2D-DFT Notch và 2D-DWT Haar (Gonzalez & Woods, Mallat).
  - Gắn kết với bài toán bền vững quang học (Hendrycks & Dietterich, MVTec-AD-C) dưới nhiễu cảm biến, mờ chuyển động và mất nét quang học.
  - Kết bằng đoạn **Positioning** sắc nét đối chiếu trực tiếp bài báo với các công trình trước.

## 2. Quy Chuẩn Kỹ Thuật
- Tách mô-đun tại `paper/sections/related_work.tex`, nạp qua `\input{sections/related_work}`.
- Toàn bộ trích dẫn phải tồn tại và đã xác thực trong `paper/references.bib` (0 trích dẫn ảo).
- Không có `Overfull \hbox`, không có BibTeX warning.
