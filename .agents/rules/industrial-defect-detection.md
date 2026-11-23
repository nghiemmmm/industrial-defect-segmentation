# Industrial Defect Detection & Segmentation Rules

Các nguyên tắc bắt buộc khi thiết kế, triển khai và đánh giá mô hình phân vùng khuyết tật công nghiệp (như MVTec AD, VisA):

## 1. Nguyên Tắc Bảo Toàn Dữ Liệu (Zero Data Leakage Invariant)
- **Tập Train chỉ dùng ảnh bình thường**: Tuyệt đối KHÔNG đưa ảnh lỗi thật trong tập `test` hoặc ground-truth masks của tập `test` vào dữ liệu huấn luyện. Mọi khuyết tật trong tập train bắt buộc phải là khuyết tật nhân tạo (Synthetic Anomalies) sinh ra từ `train/good`.
- **Tập Test đóng băng**: Tập `test` gốc (bao gồm cả `test/good` và `test/<defect_type>`) được bảo lưu nguyên vẹn để đánh giá năng lực tổng quát hóa ngoài phân phối (Out-of-Distribution Generalization).

## 2. Tỷ Lệ Mẫu Âm Tính (Negative Sample Ratio / good_ratio)
- Khi chuẩn bị dữ liệu train cho mô hình phát hiện/phân vùng (như YOLO-seg), KHÔNG ĐƯỢC huấn luyện trên 100% ảnh khuyết tật nhân tạo.
- Bắt buộc phải duy trì tỷ lệ mẫu âm tính `good_ratio` tối thiểu từ $15\%$ đến $30\%$ (ảnh sạch ban đầu với nhãn text rỗng - không có polygon) để kiểm soát và triệt tiêu tỷ lệ báo động giả (False Alarm Rate - FAR).

## 3. Tương Thích Kích Thước Ảnh Bất Kỳ (Arbitrary Image Dimensions)
- Không bao giờ giả định ảnh đầu vào luôn có kích thước lũy thừa của 2 ($256 \times 256$, $512 \times 512$).
- Khi triển khai các thuật toán Perlin noise (DRAEM), dải tần Fourier (FFT), hoặc sóng con (DWT), phải xử lý phần dư chia lưới bằng cách:
  - Sinh biến đổi trên lưới chuẩn lũy thừa 2 và nội suy song tuyến tính (`cv2.resize` với `INTER_LINEAR`) về kích thước $(W, H)$ của ảnh gốc.
  - Xử lý chẵn/lẻ kích thước trục khi thực hiện DWT / IDWT để bảo đảm ảnh tái tạo khớp pixel tuyệt đối với Ground-Truth Mask.

## 4. Chiến Lược Kiểm Định (Validation Strategy)
- Đối với mô hình Deep Learning nặng chạy trên GPU đám mây (Google Colab):
  - Áp dụng phương pháp phân chia Train/Val 80/20 cố định trên tập Normal Data thay vì k-Fold toàn diện để tối ưu chi phí tính toán.
  - Sử dụng chiến lược Multi-Seed Variance Analysis (chạy 3 seeds cố định như 42, 1337, 2026 trên các mô hình nòng cốt) để báo cáo trung bình và độ lệch chuẩn ($\mu \pm \sigma$).
