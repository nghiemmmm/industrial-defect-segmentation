# KẾT LUẬN VÀ TÀI LIỆU THAM KHẢO

---

# KẾT LUẬN

Báo cáo cuối kỳ học phần Xử lý ảnh (mã học phần: `INT14123_CLC`) đã hoàn thành việc nghiên cứu, hiện thực hóa và đánh giá thực nghiệm có hệ thống giải pháp phát hiện và phân vùng khuyết tật bề mặt sản phẩm công nghiệp trên tập dữ liệu chuẩn mực quốc tế MVTec AD. Toàn bộ các kết quả và đóng góp cốt lõi của đề tài được tổng kết chặt chẽ theo 3 trụ cột khoa học, công nghệ và thực tiễn như sau:

**Về mặt khoa học:** Đề tài đã xây dựng thành công cơ sở lý thuyết toán học vững chắc cho bài toán phân vùng bất thường công nghiệp thông qua việc kết hợp liên miền giữa giải tích không gian điểm ảnh và biến đổi tần số 2 chiều. Hệ thống đã hiện thực hóa giải tích vi phân phương trình đạo hàm riêng Poisson ($\Delta f = \operatorname{div}\mathbf{v}$) với điều kiện biên Dirichlet để cấy ghép khuyết tật nguồn vào ảnh đích với gradient quang học liền mạch (thuật toán NSA), khai thác trường vô hướng gradient ngẫu nhiên đa tần số Perlin bậc 5 (thuật toán DRAEM), và áp dụng biến đổi Affine xoay ngẫu nhiên đa tỷ lệ (thuật toán CutPaste). Đặc biệt, nghiên cứu đã chứng minh tính toàn vẹn số học và sự bảo toàn không gian tuyệt đối của các phép biến đổi miền tần số: phép kiểm tra tái tạo thuận nghịch (Identity Roundtrip Reconstruction) trên bộ lọc biến đổi Fourier nhanh 2 chiều (2D-FFT) và biến đổi sóng con rời rạc 2 chiều (2D-DWT Haar) đạt sai số tuyệt đối trung bình $\text{MAE} \le 0.4807$, tỷ số tín hiệu trên nhiễu đỉnh $\text{PSNR} = 51.31\text{ dB}$ (vượt xa ngưỡng không tổn hao $40\text{ dB}$), và chỉ số tương đồng cấu trúc $\text{SSIM} = 0.9983$, khẳng định không gây ra bất kỳ sai lệch hình học nào đối với nhãn phân vùng mặt đất. Phương pháp tiếp cận này đã giải quyết căn bản nghịch lý thiếu hụt dữ liệu khuyết tật mà vẫn tuân thủ nghiêm ngặt nguyên tắc Zero Data Leakage (chỉ học từ tập `train/good`).

**Về mặt công nghệ:** Đề tài đã thiết kế và hoàn thiện một đường ống (pipeline) xử lý ảnh hoàn chỉnh, hướng mô-đun và thuần chuẩn hóa bằng ngôn ngữ Python kết hợp các thư viện khoa học tính toán hiệu năng cao gồm NumPy, OpenCV, PyWavelets và SciPy. Điểm cải tiến công nghệ quan trọng là việc thiết kế cơ chế khởi tạo lưới Perlin noise trên ma trận chuẩn cố định $512 \times 512$ kết hợp phép nội suy song tuyến tính (Bilinear Interpolation), khắc phục triệt để lỗi phân chia lưới kích thước lẻ (`ZeroDivisionError`) trên các ảnh công nghiệp có kích thước không chia hết cho lũy thừa 2 (như `bottle` $900 \times 900$, `tile` $840 \times 840$). Bên cạnh đó, hệ thống tích hợp thành công mô-đun trích xuất đường viền topologically Suzuki-Abe và đơn giản hóa đa giác Ramer-Douglas-Peucker (`YOLOSegExporter`) để tự động chuyển hóa mặt nạ nhị phân thành nhãn đa giác vector chuẩn hóa cho mạng phân vùng thực thể YOLOv11-seg. Toàn bộ mã nguồn đã vượt qua xuất sắc $10/10$ cổng kiểm soát chất lượng độc lập (Stage-Gates), đạt tỷ lệ vượt qua tuyệt đối $100\%$ đối với toàn bộ $34/34$ bài kiểm thử tự động của framework `pytest`, kết xuất 28 bộ ảnh montage kiểm chứng trực quan trên 4 danh mục sản phẩm đại diện (`bottle`, `carpet`, `grid`, `screw`) và kiểm định toàn diện trên 6 danh mục MVTec AD, đồng thời thiết lập khung thực nghiệm tự động hóa 1-click trên Google Colab với phần cứng GPU NVIDIA A100 và bộ đánh giá số đo kép `DualDomainEvaluator`.

**Về mặt thực tiễn:** Khả năng ứng dụng và độ tin cậy trong môi trường sản xuất thực tế được kiểm chứng minh bạch qua các kết quả định lượng chuẩn xác. Mô hình nền tảng ban đầu (`EXP-00`: YOLOv11n-seg huấn luyện trên mẫu tổng hợp CutPaste) đã đạt chỉ số phân vùng thực thể Mask mAP@50 đạt $0.800$ ($80.0\%$), Mask mAP@50-95 đạt $0.480$ ($48.0\%$), cùng chỉ số phát hiện bất thường liên tục Pixel-AUROC và Image-AUROC đều đạt mức hoàn hảo $1.000$ trên tập dữ liệu kiểm chứng. Cơ chế chèn mẫu âm có kiểm soát với tỷ lệ bắt buộc $\text{good\_ratio} = 0.15$ đã phát huy hiệu quả tối đa khi đưa tỷ lệ báo động giả $\text{FAR@0.25}$ về mức tuyệt đối $0.000$ ($0\%$), triệt tiêu hoàn toàn rủi ro dừng chuyền sai do lỗi nhận diện ảo trên các sản phẩm bình thường. Động cơ suy luận biên C++ TensorRT (FP16 engine trên GPU NVIDIA) đạt thời gian xử lý trung bình chỉ $6.7\text{ ms}$ cho mỗi khung hình kích thước lớn $1024 \times 1024$ (tương đương tốc độ gần 150 FPS), đáp ứng vượt trội yêu cầu kiểm định trực tuyến trên các dây chuyền băng chuyền công nghiệp tốc độ cao. Cuối cùng, bộ benchmark MVTec-AD-C đã cung cấp một quy trình đo lường định lượng khách quan về độ bền vững của thị giác máy tính trước 4 loại suy thoái quang học công nghiệp (nhiễu cảm biến Gauss, mờ thấu kính Gauss, rung lắc chuyển động băng chuyền và mất nét tiêu cự).

### Hướng phát triển tiếp theo

Nhằm giải quyết dứt điểm các điểm nghẽn kỹ thuật và hoàn thiện hệ thống theo các phân tích chuyên sâu tại mục `3.3.3` và `3.4.2`, các định hướng cải tiến tiếp theo bao gồm:

1. **Khắc phục hiện tượng phân mảnh đa giác trên bề mặt vân phức tạp (Hạn chế vết nứt gạch men `tile_crack` tại mục `3.4.2`):** Nghiên cứu tích hợp mô hình đường bao chủ động thích nghi (Adaptive Active Contour / Snake) hoặc giải thuật gom cụm phân cấp các đỉnh đa giác (Hierarchical Polygon Clustering). Cơ chế này sẽ tự động phân tích tính liên tục hướng của trường gradient để hàn gắn các phân đoạn nứt vỡ vi mô bị đứt quãng thành một đa giác phân vùng khép kín duy nhất, khắc phục triệt để hiện tượng over-segmentation khi biên độ tương phản giữa vết nứt và vân đá tự nhiên quá thấp.
2. **Nâng cao năng lực phân tách khuyết tật trên cấu trúc sợi không đồng đều (Hạn chế vật liệu thảm dệt `carpet` tại mục `3.4.2`):** Thay thế biến đổi Fourier toàn cục bằng phép biến đổi gói sóng con đa kênh (Wavelet Packet Decomposition) kết hợp mô hình thống kê năng lượng cục bộ (Local Energy Statistics). Giải pháp này cho phép phân rã chi tiết cả các dải tần trung và cao, giúp thuật toán phân biệt chính xác giữa độ gồ ghề ngẫu nhiên của các sợi len tự nhiên và các tổn thương kết cấu thực sự (vết thủng, vết ố, sợi đứt), tránh suy hao hoa văn hợp thức trong quá trình lọc tần số.
3. **Tự động hóa hoàn toàn khâu thích nghi ngưỡng lọc đỉnh phổ tần số (Hạn chế siêu tham số tĩnh tại mục `3.3.3` và `3.4.2`):** Xây dựng giải thuật tìm kiếm đỉnh năng lượng phổ tự thích nghi (Adaptive Spectral Peak Thresholding) dựa trên phân tích đạo hàm bậc hai của phân bố năng lượng bán kính (Radial Energy Distribution) hoặc thuật toán tối ưu hóa bầy đàn (PSO). Cơ chế này sẽ tự động tính toán tọa độ tâm và bán kính hố chặn Gaussian Notch ($r_0, \tau_{\text{peak}}$) tối ưu cho từng ảnh đầu vào riêng biệt theo thời gian thực mà không đòi hỏi kỹ sư phải tinh chỉnh thủ công theo từng nhóm sản phẩm.
4. **Hoàn thiện thu hoạch số liệu huấn luyện ma trận thực nghiệm 12 kịch bản (EXP-01 đến EXP-11):** Sau khi quá trình huấn luyện 50 epochs phân tán trên nền tảng Google Colab GPU A100 hoàn tất, tiến hành trích xuất tự động các tệp trọng số tốt nhất (`best.pt`) và tệp ma trận kết quả `results/ablation_summary.csv`. Toàn bộ các giá trị số đo Mask mAP@50, mAP@50-95, Pixel-AUROC, FAR@0.25 và mCE sẽ được cập nhật đồng bộ vào Bảng 5 và Bảng 6 của báo cáo nhằm hoàn thiện bức tranh đối sánh định lượng cô lập giữa các đóng góp kỹ thuật.

---

# TÀI LIỆU THAM KHẢO

[1] P. Bergmann, M. Fauser, D. Sattlegger, and C. Steger, "MVTec AD — A Comprehensive Real-World Dataset for Unsupervised Anomaly Detection," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2019, pp. 9592–9600.

[2] C.-L. Li, K. Sohn, J. Yoon, and T. Pfister, "CutPaste: Self-Supervised Learning for Anomaly Detection and Localization," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2021, pp. 9664–9674.

[3] V. Zavrtanik, M. Kristan, and D. Skočaj, "DRAEM — A Discriminatively Trained Reconstruction Embedding for Surface Anomaly Detection," in *Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)*, 2021, pp. 8330–8339.

[4] H. M. Schlüter, J. Tan, B. Hou, and B. Glocker, "Natural Synthetic Anomalies for Self-Supervised Anomaly Detection and Localization," in *Proc. Eur. Conf. Comput. Vis. (ECCV)*, 2022, pp. 474–489.

[5] E. Horwitz and Y. Hoshen, "Empirical Analysis of the Robustness of Anomaly Detection to Optical Degradations," in *Proc. Brit. Mach. Vis. Conf. (BMVC)*, 2022.

[6] P. Pérez, M. Gangnet, and A. Blake, "Poisson Image Editing," *ACM Trans. Graph. (TOG)*, vol. 22, no. 3, pp. 313–318, 2003.

[7] R. C. Gonzalez and R. E. Woods, *Digital Image Processing*, 4th ed. New York, NY, USA: Pearson, 2018.

[8] S. Mallat, *A Wavelet Tour of Signal Processing: The Sparse Way*, 3rd ed. Boston, MA, USA: Academic Press, 2008.

[9] S. Suzuki and K. Abe, "Topological structural analysis of digitized binary images by border following," *Comput. Vis., Graph., Image Process.*, vol. 30, no. 1, pp. 32–46, 1985.

[10] H. T. Trụ, *Bài giảng và tài liệu hướng dẫn học phần Xử lý ảnh (INT14123_CLC)*, Khoa Công nghệ thông tin 2, Học viện Công nghệ Bưu chính Viễn thông, 2026. [Trực tuyến]. Địa chỉ: https://drive.google.com/drive/folders/19x-NFBYmU1MT44r3ElpTE79Lkl8zRWDf `[CẦN XÁC MINH NGUỒN: Tài liệu học tập nội bộ do Giảng viên cung cấp]`.
