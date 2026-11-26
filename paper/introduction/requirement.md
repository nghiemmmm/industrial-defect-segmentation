# SECTION I: INTRODUCTION — YÊU CẦU & ĐẶC TẢ NỘI DUNG (REQUIREMENTS)

> **Mục tiêu Section:** Thuyết phục Reviewer ngay từ trang đầu tiên về tính cấp thiết của bài toán, tính sâu sắc của khoảng trống nghiên cứu (Research Gap), và 4 đóng góp mới đột phá của giải pháp đề xuất.

---

## 1. Ngân Sách Trang & Định Dạng
* **Độ dài mục tiêu:** Khoảng 1.2 đến 1.4 cột (~800–900 từ tiếng Anh học thuật chuẩn IEEE Transactions).
* **Kiến trúc file:** Tách riêng tại `paper/sections/introduction.tex` và nạp vào `paper/paper.tex` bằng `\input{sections/introduction}`.
* **Văn phong:** Tiếng Anh học thuật trang trọng (Formal Academic English), dùng từ vựng chuyên ngành thị giác máy tính chính xác (*spatial-frequency inter-domain modulation, high-throughput assembly lines, self-supervised representation, zero data leakage*).

---

## 2. Bản Thiết Kế 6 Đoạn Văn Chi Tiết (Paragraph-by-Paragraph Blueprint)

* **Paragraph 1: Bối cảnh sản xuất & Nhu cầu cấp thiết của phân vùng thực thể**
  - Mở đầu bằng lệnh `\IEEEPARstart{I}{n}`.
  - Phân tích sự chuyển dịch từ bài toán phân loại nhị phân (Pass/Fail) sang bài toán phân vùng thực thể đa giác (Pixel-level polygonal instance segmentation).
  - Nêu rõ sự đánh đổi kinh tế sống còn giữa **Tỷ lệ bỏ lọt khuyết tật (Defect Escape Rate)** và **Tỷ lệ báo động giả dừng chuyền (False Alarm Rate)**.

* **Paragraph 2: Nghịch lý Dữ liệu trong Sản xuất Thực tế & Sự trỗi dậy của Self-Supervision**
  - Nêu thực trạng tỷ lệ sản phẩm đạt chuẩn thường $> 99\%$, phế phẩm cực hiếm và đa dạng hình thái.
  - Rào cản chi phí gán nhãn thủ công và sự xuất hiện của các hướng tiếp cận sinh lỗi nhân tạo tự giám sát (CutPaste \cite{li2021cutpaste}, DRAEM \cite{zavrtanik2021draem}, NSA \cite{schluter2022natural}).

* **Paragraph 3: Phân tích Sâu 3 Điểm Nghẽn Tử Huyệt (Core Bottlenecks)**
  - *1. Background Lattice Domination:* Lồng ghép ví dụ đối lập thực tế từ MVTec AD: trên nhóm kết cấu tuần hoàn lặp lại (`grid`, `carpet`), năng lượng phổ nền lấn át tín hiệu lỗi; đối lập với nhóm vật thể khối đồng nhất (`bottle`, `screw`) nơi biên cạnh vật lý dễ bị biến dạng nếu cấy ghép lỗi tùy tiện.
  - *2. The Fatal False Alarm Dilemma:* Khi mô hình học vẹt trên ảnh lỗi nhân tạo, nó nhìn đâu trên ảnh lành cũng tưởng lỗi $\to$ dừng nhầm dây chuyền sản xuất.
  - *3. The Real-Time Edge Latency Barrier:* Các phương pháp Anomaly Detection hiện hành (Autoencoder, PaDiM, PatchCore) quá nặng ($> 50\text{ ms}$), không vượt qua mốc 100 FPS.

* **Paragraph 4: Đề xuất Giải pháp Liên miền Tần số - Không gian**
  - Luận giải cơ chế kết hợp biến đổi Fourier 2D (2D-FFT Notch), sóng con 2D (2D-DWT Haar) và giải tích Poisson để giải quyết triệt để 3 điểm nghẽn trên.

* **Paragraph 5: Bốn Đóng Góp Khoa Học Chính (4 Key Contributions)**
  - Liệt kê rành mạch 4 bullet points với số liệu neo chuẩn hóa:
    1. Inter-domain frequency-spatial synthesis with numerical integrity proof ($\text{PSNR} = 51.31\text{ dB}$, $\text{SSIM} = 0.9983$).
    2. Arbitrary dimension Perlin noise generation ($512\times 512$ bilinear mapping) khắc phục lỗi chia lưới trên `bottle` $900\times 900$, `tile` $840\times 840$.
    3. False-alarm suppression with zero data leakage, đưa $\text{FAR@0.25} = 0.000$ ($0\%$) qua $\text{good\_ratio} = 0.15$.
    4. Dual-domain evaluation ($\text{mAP@50} = 0.800$, $\text{Pixel-AUROC} = 1.000$) và C++ TensorRT FP16 engine ($6.7\text{ ms}$, ~149.2 FPS).

* **Paragraph 6: Cấu trúc Tổ chức của Bài Báo (Paper Organization Outline)**
  - Giới thiệu lộ trình từ Section II đến Section VII.

---

## 3. Danh Mục Trích Dẫn & Bảng Tra Cứu Số Liệu Bắt Buộc

* **Trích dẫn BibTeX:** `\cite{bergmann2019mvtec}`, `\cite{li2021cutpaste}`, `\cite{zavrtanik2021draem}`, `\cite{schluter2022natural}`, `\cite{defard2021padim}`, `\cite{roth2022towards}`.
* **Số liệu thực tế bắt buộc:** $\text{good\_ratio} = 0.15$, $\text{FAR@0.25} = 0.000$, Mask mAP@50 $0.800$, Latency $6.7\text{ ms}$ trên ảnh $1024 \times 1024$.
