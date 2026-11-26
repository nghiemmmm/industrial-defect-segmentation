# MISSION STATEMENT & RESEARCH SCOPE CONTRACT (LA BÀN CHIẾN LƯỢC)

> **Cảnh báo chống lạc đề (Anti-Drift Guardrail):** Đây là tài liệu định hướng bất biến của bài báo. Mọi bổ sung thuật toán, viết lại đoạn văn hay tinh chỉnh thí nghiệm BẮT BUỘC phải đối chiếu với các nguyên tắc dưới đây. Bất kỳ nội dung nào làm loãng 4 đóng góp cốt lõi hoặc đi ra ngoài phạm vi sẽ bị loại bỏ ngay lập tức.

---

## 1. Thông Tin Định Danh Bài Báo (Paper Metadata)

* **Tiêu đề chính thức (Official Title):**
  > **Frequency-Spatial Anomaly Synthesis for False-Alarm-Suppressed Industrial Surface Defect Segmentation**
* **Tạp chí / Hội nghị mục tiêu (Target Venues):**
  - *Hội nghị mục tiêu trực tiếp:* **FJCAI** (Hội thảo Khoa học Quốc gia về Trí tuệ Nhân tạo, \url{https://fjcai.org.vn}) — Chuẩn định dạng IEEE Conference (`\documentclass[conference]{IEEEtran}`), quy cách bài toàn văn từ **6 đến 8 trang** (phản biện Double-Blind Review).
  - *Phương án nâng cấp mở rộng (Tạp chí Q1):* IEEE Transactions on Industrial Informatics (TII) hoặc IEEE Access (8 đến 10 trang).
* **Định dạng & Quy chuẩn:** Chuẩn `IEEEtran` 2 cột (Conference mode, Font 10pt Times Roman, Letter paper).
* **Dung lượng trang mục tiêu:** 6 đến 8 trang (Hiện tại: 7 trang hoàn chỉnh).
* **Tác giả:** Trung-Tru Huynh, Duc-Hao Do, Duc-Nghiem Nguyen, and Thanh-Hung Nguyen (Khoa CNTT 2, Học viện Công nghệ Bưu chính Viễn thông - PTIT Cơ sở tại TP.HCM).

---

## 2. Phát Biểu Bài Toán & Nút Thắt Cần Giải Quyết (Central Problem)

Trong môi trường sản xuất công nghiệp thông minh (Smart Manufacturing), sản phẩm lỗi thực tế vô cùng hiếm ($< 1\%$), khiến việc thu thập dữ liệu có nhãn để huấn luyện các mạng phân vùng thực thể sâu (như YOLO-seg) gặp trở ngại lớn.

Các phương pháp sinh khuyết tật tự giám sát hiện nay (CutPaste, DRAEM, NSA) vấp phải **3 nút thắt tử huyệt**:
1. **Sự lấn át của hoa văn nền (Texture Interference):** Thao tác thuần túy trong miền không gian khiến lỗi nhân tạo dễ bị các cấu trúc nền tuần hoàn (như lưới thép `grid`, thảm dệt `carpet`) làm mờ nhạt hoặc biến dạng bất tự nhiên.
2. **Nạn báo động giả (The False Alarm Dilemma):** Mô hình được huấn luyện hoàn toàn trên ảnh sinh lỗi nhân tạo có xu hướng nhìn đâu cũng thấy lỗi trên ảnh lành, dẫn đến việc liên tục dừng nhầm dây chuyền sản xuất, gây tổn thất kinh tế khổng lồ.
3. **Độ trễ suy luận biên thời gian thực (Edge Inference Latency):** Các mô hình Anomaly Detection hiện nay (Autoencoder, PaDiM, PatchCore) quá nặng, không thể đáp ứng tốc độ trên 100 FPS của băng chuyền thực tế.

---

## 3. Ba Đóng Góp Khoa Học Cốt Lõi (3 Core Image-Processing Contributions)

Mọi phần trong bài báo phải xoay quanh và chứng minh 3 trụ cột xử lý ảnh cốt lõi sau (đánh giá tốc độ FP16 TensorRT đóng vai trò kiểm chứng phụ trợ về hiệu năng suy luận trong Section IV-I):

1. **Đóng góp 1 — Điều biến Liên miền Tần số - Không gian (Inter-Domain Frequency-Spatial Synthesis):**
   - Miền tần số: Bộ lọc 2D-FFT Notch thích nghi triệt tiêu hoa văn tuần hoàn + 2D-DWT Haar Wavelet khuếch đại dải chi tiết cao ($LH, HL, HH$).
   - Kiểm chứng định lượng bảo toàn số học & tọa độ trên 2,857 ảnh MVTec AD: $\text{MAE} \le 0.4807$, $\text{PSNR} = 51.31\text{ dB}$, $\text{SSIM} = 0.9983$ (2D-FFT) và đẳng cấu tuyệt đối (2D-DWT).

2. **Đóng góp 2 — Kỹ nghệ Sinh Khuyết tật Không gian Kích thước Tùy ý (Arbitrary-Resolution Spatial Anomaly Engineering):**
   - Giải quyết triệt để lỗi chia lưới mảng NumPy của mã nguồn DRAEM gốc trên các ảnh không phải lũy thừa của 2 (`bottle` $900\times 900$, `tile` $840\times 840$) bằng cơ chế sinh Perlin noise trên lưới chuẩn $512\times 512$ kết hợp nội suy song tuyến thích nghi.
   - Kết hợp CutPaste (Normal/Scar), NSA Poisson liền mạch ($\Delta f = \operatorname{div}\mathbf{v}$) kẹp tiền cảnh Otsu và vector hóa đa giác Suzuki-Abe/RDP.

3. **Đóng góp 3 — Triệt tiêu Báo động giả Zero-Leakage & Khung Đánh giá Bền vững Quang học:**
   - Cam kết Zero Data Leakage tuyệt đối kết hợp tỷ lệ bảo toàn mẫu âm bắt buộc ($\rho_{\text{neg}} = 0.15$).
   - Khung đánh giá kép (COCO Mask mAP, Mask IoU, Pixel/Image AUROC, $\text{FAR}@\tau$) và kiểm thử suy thoái quang học MVTec-AD-C (Gaussian Noise/Blur, Motion Blur, Defocus Blur).
   - *Kiểm chứng phụ trợ về hiệu năng (IV-I):* Đo tốc độ suy luận FP16 TensorRT ($6.7\text{ ms}$ trên $1024\times 1024$, $\approx 149.2\text{ FPS}$) xác nhận tính khả thi triển khai dây chuyền.

---

## 4. Ranh Giới Phạm Vi & Điều Khoản Cấm (Boundary & Anti-Drift Guardrails)

* **TRONG PHẠM VI (IN-SCOPE):**
  - Tập dữ liệu: 6 danh mục đại diện của MVTec AD (2,857 ảnh: `grid`, `carpet`, `tile`, `screw`, `pill`, `bottle`).
  - Mô hình nền tảng: Ultralytics YOLOv11-seg.
  - Phân hệ tiền xử lý: Python thuần kết hợp NumPy 2.x, OpenCV, PyWavelets 1.8.0, SciPy.
  - Kiểm thử độ bền: Benchmark suy thoái quang học MVTec-AD-C (Noise, Blur, Motion, Defocus).
  - Tối ưu biên: TensorRT 10.x C++ engine.

* **NGOÀI PHẠM VI (OUT-OF-SCOPE / CẤM ĐƯA VÀO LÀM XÁO TRỘN):**
  - Tuyệt đối không thay đổi mô hình trung tâm sang Transformer nặng nề (như SAM, SegFormer) làm mất đi ưu thế tốc độ 150 FPS.
  - Không biến bài báo thành bài khảo sát chung chung (Survey). Mọi so sánh chỉ nhằm tôn bật giải pháp liên miền đề xuất.
  - Không tự ý thêm bớt các lớp sản phẩm ngoài 6 danh mục đã kiểm chứng nếu chưa có số liệu thực nghiệm đầy đủ.

---

## 5. Quy Tắc Gắn Kết Tuyệt Đối với Mã Nguồn (Strict Grounding Contract)

* Tất cả tên hàm, tham số và hằng số trong văn bản tiếng Anh phải đồng bộ 100% với mã nguồn:
  - `tau_peak = 3.5`, `r0 = 5.0` $\to$ khớp với `configs/experiments/` và `data_engine/frequency/`.
  - `good_ratio = 0.15` $\to$ khớp với `data_engine/loaders/mvtec_loader.py`.
  - `epsilon = 0.002 * arc_length` $\to$ khớp với `data_engine/exporters/yolo_seg_exporter.py`.
  - `6.7 ms latency` $\to$ khớp với log kiểm chứng `cpp/trt_seg_inference/`.
