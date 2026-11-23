# BẢN KIỂM TOÁN VÀ ĐỐI CHIẾU HỆ THỐNG BÁO CÁO CUỐI KỲ (AUDIT CHECKLIST)
**Học phần:** INT14123_CLC -- Xử lý ảnh (Image Processing)  
**Tập tài liệu kiểm toán:** Toàn bộ các file từ `report/01_frontmatter_mo_dau.md` đến `report/07_ket_luan_tltk.md` đối chiếu với `report/STYLE_RULES.md`.

---

## PHẦN 1: BẢN TỔNG HỢP KIỂM TRA 4 DANH MỤC TỰ ĐỘNG

### 1.1. Cây Mục lục Toàn văn (Kiểm toán Đánh số và Dấu chấm Quy chuẩn)

Hệ thống phân cấp tiêu đề tuân thủ 100% quy tắc: cấp chương viết IN HOA, cấp mục số Ả Rập bắt buộc có dấu chấm đi kèm sau cùng (`X.Y.`, `X.Y.Z.`). Không phát hiện bất kỳ mục nào bị nhảy cóc số thứ tự.

```text
PHẦN THỦ TỤC ĐẦU BÁO CÁO (Đánh số La Mã thường: i, ii, iii...)
├── Trang bìa chính
├── Trang phụ bìa
├── LỜI CAM ĐOAN
├── LỜI CẢM ƠN
├── MỤC LỤC
├── DANH MỤC HÌNH VẼ
├── DANH MỤC BẢNG BIỂU
├── DANH MỤC CÔNG THỨC
└── DANH MỤC TỪ VIẾT TẮT

MỞ ĐẦU (Đánh số Ả Rập bắt đầu từ trang 1)
├── 1. Lý do chọn đề tài
├── 2. Tổng quan về vấn đề nghiên cứu
├── 3. Mục tiêu và nhiệm vụ nghiên cứu
├── 4. Đối tượng và phạm vi nghiên cứu
└── 5. Cấu trúc của báo cáo

CHƯƠNG I: TỔNG QUAN VỀ HỆ THỐNG PHÂN VÙNG KHUYẾT TẬT BỀ MẶT CÔNG NGHIỆP
├── [Đoạn dẫn nhập đầu chương I]
├── 1.1. Phát biểu bài toán
│   ├── 1.1.1. Định nghĩa và câu hỏi bài toán
│   └── 1.1.2. Phân rã bài toán (Đầu vào, Mục tiêu, Đầu ra, Ví dụ minh họa)
├── 1.2. Kiến trúc hệ thống tổng quát
│   ├── 1.2.1. Thành phần của hệ thống
│   └── 1.2.2. Quy trình hoạt động cơ bản
├── 1.3. Các hướng tiếp cận và phương pháp liên quan
│   ├── 1.3.1. Phân loại các trường phái tiếp cận
│   ├── 1.3.2. Phương pháp xử lý ảnh số cổ điển
│   ├── 1.3.3. Phương pháp học sâu tái tạo không giám sát (Reconstruction-based)
│   ├── 1.3.4. Phương pháp học sâu dựa trên dữ liệu tổng hợp kết hợp xử lý miền tần số
│   └── 1.3.5. Định hướng tiếp cận của nghiên cứu
├── 1.4. Các công nghệ và kỹ thuật phổ biến
│   ├── 1.4.1. Kỹ thuật biến đổi miền tần số và sóng con (2D-FFT và 2D-DWT)
│   ├── 1.4.2. Kỹ thuật sinh khuyết tật tổng hợp (CutPaste, DRAEM, NSA)
│   ├── 1.4.3. Mô hình phân vùng thực thể học sâu (YOLOv11-seg) và định dạng nhãn đa giác
│   └── 1.4.4. Ứng dụng thực tế và triển khai biên thời gian thực
├── 1.5. Những thách thức và vấn đề còn tồn tại
│   ├── 1.5.1. Nhiễu môi trường, biến động ánh sáng và độ tương phản thấp
│   ├── 1.5.2. Giới hạn tài nguyên phần cứng và yêu cầu thời gian thực
│   ├── 1.5.3. Đặc thù đối tượng và sự mất cân bằng dữ liệu cực đoan
│   ├── 1.5.4. Thách thức về tốc độ xử lý và đồng bộ trên dây chuyền băng chuyền
│   └── 1.5.5. Bài toán triển khai và tương thích kích thước ảnh tùy ý
└── 1.6. Kết luận chương I

CHƯƠNG II: ĐỀ XUẤT PHƯƠNG PHÁP XỬ LÝ HÌNH ẢNH TRONG PHÂN VÙNG KHUYẾT TẬT BỀ MẶT CÔNG NGHIỆP
├── [Đoạn dẫn nhập đầu chương II]
├── 2.1. Kiến trúc mô hình hệ thống đề xuất
│   ├── 2.1.1. Tổng quan kiến trúc hệ thống
│   ├── 2.1.2. Thành phần chi tiết của hệ thống
│   ├── 2.1.3. Quy trình hoạt động của hệ thống
│   └── 2.1.4. Ưu điểm và tính khả thi của hệ thống
├── 2.2. Biểu diễn dữ liệu hình ảnh
│   ├── 2.2.1. Các định dạng dữ liệu được sử dụng
│   ├── 2.2.2. Tiền xử lý dữ liệu
│   └── 2.2.3. Kỹ thuật lựa chọn, gắn nhãn và tăng cường dữ liệu
├── 2.3. Phương pháp xử lý hình ảnh trong phân vùng khuyết tật bề mặt công nghiệp
│   ├── 2.3.1. Mô-đun lọc miền tần số 2D-FFT triệt tiêu đỉnh phổ tuần hoàn
│   ├── 2.3.2. Mô-đun phân rã biến đổi sóng con 2D-DWT và tăng cường dải chi tiết biên
│   ├── 2.3.3. Mô-đun sinh khuyết tật tổng hợp dạng mảng bám và vết xước CutPaste
│   ├── 2.3.4. Mô-đun sinh khuyết tật hữu cơ đa tỉ lệ DRAEM
│   ├── 2.3.5. Mô-đun ghép khuyết tật liền mạch Poisson NSA
│   ├── 2.3.6. Mô-đun trích xuất đường viền và chuẩn hóa đa giác YOLOv11-seg
│   ├── 2.3.7. Mô-đun phân vùng thực thể học sâu YOLOv11-seg
│   ├── 2.3.8. Mô-đun suy luận thời gian thực C++ TensorRT và giải mã tensor đầu ra
│   └── 2.3.9. Mô-đun đánh giá phân vùng đa miền và benchmark suy thoái quang học
└── 2.4. Kết luận chương II

CHƯƠNG III: KIỂM NGHIỆM VÀ ĐÁNH GIÁ HỆ THỐNG
├── [Đoạn dẫn nhập đầu chương III]
├── 3.1. Dữ liệu thực nghiệm
│   ├── 3.1.1. Nguồn dữ liệu
│   ├── 3.1.2. Cách thu thập và chuẩn bị dữ liệu
│   ├── 3.1.3. Đặc điểm dữ liệu
│   └── 3.1.4. Quy trình xử lý dữ liệu thực nghiệm
├── 3.2. Cài đặt thực nghiệm
│   ├── 3.2.1. Công cụ và nền tảng sử dụng
│   ├── 3.2.2. Quy trình cài đặt và triển khai
│   └── 3.2.3. Các tệp hình ảnh kết quả thực nghiệm có sẵn trong workspace
├── 3.3. Đánh giá thực nghiệm
│   ├── 3.3.1. Tiêu chí đánh giá
│   ├── 3.3.2. So sánh với các phương pháp/hệ thống hiện tại
│   └── 3.3.3. Kết quả và phân tích chi tiết
├── 3.4. Xây dựng thử nghiệm trong kịch bản thực tế / kiểm thử mở rộng
│   ├── 3.4.1. Quy mô và kịch bản thử nghiệm
│   └── 3.4.2. Đánh giá tính khả thi và đối chiếu vận hành
└── 3.5. Kết luận chương III

KẾT LUẬN (IN HOA, không đánh số)
├── Về mặt khoa học
├── Về mặt công nghệ
├── Về mặt thực tiễn
└── Hướng phát triển tiếp theo

TÀI LIỆU THAM KHẢO (IN HOA, không đánh số)
```

---

### 1.2. Danh mục Hình vẽ và Kiểm toán Dẫn chiếu Văn bản (Cross-References)

Tất cả các hình vẽ được đánh số theo cấu trúc `Hình <Chương>.<Thứ tự>`, caption không có dấu hai chấm. **100% hình vẽ đều đã được viện dẫn trực tiếp trong các đoạn văn liền kề**.

| Mã hình | Tên mô tả hình vẽ | File chứa định nghĩa | Trạng thái dẫn chiếu trong văn bản (Cross-Ref) | Nguồn tệp đồ họa thực tế trong workspace |
| :--- | :--- | :--- | :--- | :--- |
| **Hình 1.1** | Sơ đồ khối kiến trúc hệ thống tổng quát | `report/02_chuong1.md` (Dòng 40) | **Đã dẫn chiếu** tại Dòng 34, 42 ("như minh họa tại Hình 1.1...") | Mã nguồn Mermaid đồ họa kiến trúc |
| **Hình 1.2** | Minh họa bài toán phân vùng điểm ảnh khuyết tật trên mẫu sản phẩm `bottle` và `grid` | `report/02_chuong1.md` (Dòng 30) | **Đã dẫn chiếu** tại Dòng 29 | Ảnh mẫu `bottle` & `grid` từ MVTec AD |
| **Hình 1.3** | Minh họa sự phân rã dải tần 2 chiều của biến đổi Wavelet Haar | `report/02_chuong1.md` (Dòng 186) | **Đã dẫn chiếu** tại Dòng 185 | Sơ đồ 4 dải tần con $LL, LH, HL, HH$ |
| **Hình 1.4** | Các thách thức khuyết tật bề mặt thực tế | `report/02_chuong1.md` (Dòng 224) | **Đã dẫn chiếu** tại Dòng 223 | Ảnh mẫu 3 dạng thách thức thực tế |
| **Hình 2.1** | Sơ đồ kiến trúc hệ thống đề xuất | `report/03_chuong2_part1.md` (Dòng 85) | **Đã dẫn chiếu** tại Dòng 28, 87, 91 (`03`) & Dòng 7 (`04`) | Mã nguồn Mermaid luồng xử lý toàn diện |
| **Hình 3.1** | Mẫu ảnh đại diện từ 6 danh mục sản phẩm công nghiệp trong tập dữ liệu MVTec AD | `report/05_chuong3_part1.md` (Dòng 21) | **Đã dẫn chiếu** tại Dòng 20 | 6 ảnh đại diện sản phẩm trong workspace |
| **Hình 3.2** | Minh họa quy trình chuẩn bị dữ liệu từ ảnh gốc lành, sinh khuyết tật tổng hợp đến nhãn đa giác YOLOv11-seg | `report/05_chuong3_part1.md` (Dòng 41) | **Đã dẫn chiếu** tại Dòng 40 | `report/figures/bottle_cutpaste_normal_comparison.png` |
| **Hình 3.3** | Kết quả kiểm chứng trực quan các phương pháp sinh khuyết tật tổng hợp Nhóm A | `report/05_chuong3_part1.md` (Dòng 141) | **Đã dẫn chiếu** tại Dòng 141 | `bottle_cutpaste_normal_comparison.png` & `screw_nsa_comparison.png` |
| **Hình 3.4** | Kết quả phân tích phổ tần số 2D-FFT và phân rã sóng con 2D-DWT Nhóm B | `report/05_chuong3_part1.md` (Dòng 142) | **Đã dẫn chiếu** tại Dòng 142 | `grid_fft_montage.png` & `bottle_dwt_montage.png` |
| **Hình 3.5** | Diễn tiến suy thoái quang học MVTec-AD-C từ Mức 1 đến Mức 5 Nhóm C | `report/05_chuong3_part1.md` (Dòng 143) | **Đã dẫn chiếu** tại Dòng 143 | `bottle_gaussian_noise_progression.png` & `bottle_motion_blur_progression.png` |
| **Hình 3.6** | Biểu đồ tiến trình hội tụ hàm mất mát phân vùng và đường cong tăng trưởng Mask mAP@50 qua 50 epochs | `report/06_chuong3_part2.md` (Dòng 10) | **Đã dẫn chiếu** tại Dòng 9 | `[CẦN CẬP NHẬT: Đồ thị loss/metric xuất từ Colab]` |
| **Hình 3.7** | Trực quan hóa kết quả phân vùng thực tế (True Positives vs False Positives / False Negatives) | `report/06_chuong3_part2.md` (Dòng 113) | **Đã dẫn chiếu** tại Dòng 112 | `[CẦN CẬP NHẬT: Ảnh kết quả suy luận từ Colab]` |
| **Hình 3.8** | Đồ thị đường cong suy thoái độ chính xác Mask mAP@50 theo 5 cấp độ nghiêm trọng của 4 loại suy thoái MVTec-AD-C | `report/06_chuong3_part2.md` (Dòng 136) | **Đã dẫn chiếu** tại Dòng 135 | `[CẦN CẬP NHẬT: Đồ thị mCE xuất từ Colab]` |

---

### 1.3. Danh mục Công thức Toán học (Kiểm toán Đánh số Liên tục Toàn bài)

Công thức được đánh số **liên tục từ 1 đến 29 không đứt quãng, không trùng lặp số hiệu**. Tên gọi mô tả khớp hoàn toàn với biểu thức toán học và giải thích biến số ngay bên dưới:

| Số hiệu | Tên gọi công thức | Biểu thức toán học cốt lõi | Vị trí định nghĩa |
| :---: | :--- | :--- | :--- |
| **Công thức 1** | Biến đổi Fourier rời rạc 2 chiều | $F(u, v) = \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} f(x, y) e^{-j 2\pi (\frac{ux}{M} + \frac{vy}{N})}$ | `04_chuong2_part2.md` (Dòng 37) |
| **Công thức 2** | Ngưỡng năng lượng động phát hiện đỉnh phổ tần số tuần hoàn | $T_{peak} = \mu_S + k \cdot \sigma_S$ | `04_chuong2_part2.md` (Dòng 47) |
| **Công thức 3** | Hàm truyền bộ lọc chặn dải Notch Gaussian đa điểm đối xứng | $H_{notch}(u, v) = \prod_{k=1}^K \left[ 1 - e^{-\frac{D_k(u,v)^2}{2 r_0^2}} \right] \left[ 1 - e^{-\frac{D_{-k}(u,v)^2}{2 r_0^2}} \right]$ | `04_chuong2_part2.md` (Dòng 55) |
| **Công thức 4** | Biến đổi Fourier nghịch đảo 2 chiều khôi phục cường độ điểm ảnh | $f_{filtered}(x, y) = \frac{1}{MN} \sum_{u=0}^{M-1} \sum_{v=0}^{N-1} G(u, v) e^{j 2\pi (\frac{ux}{M} + \frac{vy}{N})}$ | `04_chuong2_part2.md` (Dòng 64) |
| **Công thức 5** | Phân rã 4 dải tần số con của biến đổi sóng con 2D Haar | $LL, LH, HL, HH = \text{DWT2D}(I, \text{'haar'})$ | `04_chuong2_part2.md` (Dòng 101) |
| **Công thức 6** | Tăng cường dải chi tiết cao và tái tạo sóng con ngược 2 chiều | $I_{boosted} = \text{IDWT2D}(LL \leftarrow 0, \alpha LH, \alpha HL, \alpha HH)$ | `04_chuong2_part2.md` (Dòng 111) |
| **Công thức 7** | Ma trận biến đổi Affine xoay và tịnh tiến mảnh vá khuyết tật | $\mathbf{x}' = \mathbf{A} (\mathbf{x} - \mathbf{x}_c) + \mathbf{x}_c + \mathbf{t}$ | `04_chuong2_part2.md` (Dòng 147) |
| **Công thức 8** | Toán tử dán đè điểm ảnh theo mặt nạ nhị phân CutPaste | $I_{synth}(x, y) = (1 - M_p(x, y)) \cdot I_{src}(x, y) + M_p(x, y) \cdot P_{trans}(x, y)$ | `04_chuong2_part2.md` (Dòng 157) |
| **Công thức 9** | Hàm đa thức nội suy làm mượt bậc 5 Perlin | $s(t) = 6t^5 - 15t^4 + 10t^3$ | `04_chuong2_part2.md` (Dòng 194) |
| **Công thức 10** | Nội suy song tuyến tính co giãn trường vô hướng Perlin | $P(x, y) = \text{lerp}(\text{lerp}(n_0, n_1, s(\Delta x)), \text{lerp}(n_2, n_3, s(\Delta x)), s(\Delta y))$ | `04_chuong2_part2.md` (Dòng 201) |
| **Công thức 11** | Hòa trộn mờ điểm ảnh phi tuyến mô phỏng khuyết tật DRAEM | $I_{synth} = (1 - \bar{M}) \odot I_{clean} + \bar{M} \odot ((1 - \beta) I_{clean} + \beta P_{texture})$ | `04_chuong2_part2.md` (Dòng 209) |
| **Công thức 12** | Tiêu chí phân ngưỡng tối ưu phương sai giữa các lớp Otsu | $t^* = \arg\max_{t} \left[ \omega_0(t) \omega_1(t) (\mu_0(t) - \mu_1(t))^2 \right]$ | `04_chuong2_part2.md` (Dòng 245) |
| **Công thức 13** | Phương trình đạo hàm riêng vi phân Poisson trong ghép ảnh | $\Delta f = \operatorname{div}\mathbf{v} \quad \text{trên } \Omega, \quad f|_{\partial\Omega} = I_d|_{\partial\Omega}$ | `04_chuong2_part2.md` (Dòng 253) |
| **Công thức 14** | Xấp xỉ sai phân hữu hạn bậc hai của toán tử Poisson trên lưới ảnh | $4 f_p - \sum_{q \in N_p \cap \Omega} f_q = \sum_{q \in N_p \cap \partial\Omega} I_d(q) + \sum_{q \in N_p} v_{pq}$ | `04_chuong2_part2.md` (Dòng 263) |
| **Công thức 15** | Tiêu chí rút gọn đỉnh đa giác Ramer-Douglas-Peucker | $\max_{P} \operatorname{dist}(P, AB) \le \epsilon = 0.002 \cdot \oint_C ds$ | `04_chuong2_part2.md` (Dòng 294) |
| **Công thức 16** | Chuẩn hóa tọa độ đỉnh đa giác thực thể YOLO | $x_i^{norm} = \operatorname{clip}\left(\frac{x_i}{W}, 0.0, 1.0\right), \quad y_i^{norm} = \operatorname{clip}\left(\frac{y_i}{H}, 0.0, 1.0\right)$ | `04_chuong2_part2.md` (Dòng 302) |
| **Công thức 17** | Hàm mất mát tổng hợp mạng phân vùng thực thể YOLOv11-seg | $\mathcal{L}_{total} = \lambda_{box} \mathcal{L}_{box} + \lambda_{cls} \mathcal{L}_{cls} + \lambda_{dfl} \mathcal{L}_{dfl} + \lambda_{mask} \mathcal{L}_{mask}$ | `04_chuong2_part2.md` (Dòng 336) |
| **Công thức 18** | Hàm mất mát phân vùng nhị phân mức điểm ảnh | $\mathcal{L}_{mask} = \mathcal{L}_{BCE}(M_{pred}, M_{gt}) + \mathcal{L}_{Dice}(M_{pred}, M_{gt})$ | `04_chuong2_part2.md` (Dòng 345) |
| **Công thức 19** | Giải mã ma trận mặt nạ nhị phân thực thể trong C++ TensorRT | $M_i = \sigma\left( \mathbf{c}_i \times \mathbf{P}_{proto} \right)$ | `04_chuong2_part2.md` (Dòng 381) |
| **Công thức 20** | Chuyển đổi tọa độ không gian ngược loại bỏ phần đệm Letterbox | $x_{orig} = \frac{x_{net} - pad_w}{scale}, \quad y_{orig} = \frac{y_{net} - pad_h}{scale}$ | `04_chuong2_part2.md` (Dòng 390) |
| **Công thức 21** | Bản đồ xác suất bất thường liên tục mức điểm ảnh | $P(y, x) = \max_{i=1 \dots N} \left( c_i \cdot \mathbb{I}\{(y, x) \in \mathcal{P}_i\} \right)$ | `04_chuong2_part2.md` (Dòng 427) |
| **Công thức 22** | Tỷ số diện tích giao trên diện tích hợp (IoU) của mặt nạ | $\text{IoU}(M_A, M_B) = \frac{|M_A \cap M_B|}{|M_A \cup M_B|}$ | `04_chuong2_part2.md` (Dòng 435) |
| **Công thức 23** | Diện tích dưới đường cong ROC (AUROC) | $\text{AUROC} = \int_{0}^{1} \text{TPR}(\tau) \, d(\text{FPR}(\tau))$ | `04_chuong2_part2.md` (Dòng 442) |
| **Công thức 24** | Tỷ lệ báo động giả trên tập sản phẩm lành (FAR) | $\text{FAR}@\tau = \frac{1}{|\mathcal{D}_{good}|} \sum_{I \in \mathcal{D}_{good}} \mathbb{I}\left( \max_{(x, y)} P_I(x, y) \ge \tau \right)$ | `04_chuong2_part2.md` (Dòng 449) |
| **Công thức 25** | Sai số tuyệt đối trung bình đo lường suy hao mức xám (MAE) | $\text{MAE}(I, \hat{I}) = \frac{1}{H \times W \times C} \sum_{x,y,c} |I(x, y, c) - \hat{I}(x, y, c)|$ | `06_chuong3_part2.md` (Dòng 33) |
| **Công thức 26** | Tỷ số tín hiệu cực đại trên nhiễu (PSNR) | $\text{PSNR} = 10 \log_{10}\left( \frac{\text{MAX}_I^2}{\text{MSE}(I, \hat{I})} \right)$ | `06_chuong3_part2.md` (Dòng 40) |
| **Công thức 27** | Chỉ số tương đồng cấu trúc không gian (SSIM) | $\text{SSIM}(x, y) = \frac{(2\mu_x\mu_y + C_1)(2\sigma_{xy} + C_2)}{(\mu_x^2 + \mu_y^2 + C_1)(\sigma_x^2 + \sigma_y^2 + C_2)}$ | `06_chuong3_part2.md` (Dòng 47) |
| **Công thức 28** | Độ chính xác trung bình AP tính bằng tích phân đường cong Precision-Recall | $\text{AP} = \int_{0}^{1} p(r) \, dr$ | `06_chuong3_part2.md` (Dòng 56) |
| **Công thức 29** | Chỉ số Mask mAP toàn diện trên dải ngưỡng IoU từ 0.50 đến 0.95 | $\text{mAP@[0.50:0.95]} = \frac{1}{10} \sum_{k=0}^{9} \text{mAP@}(0.50 + 0.05k)$ | `06_chuong3_part2.md` (Dòng 63) |

---

### 1.4. Danh mục Bảng biểu và Khuyến nghị Đánh số Thống nhất (Liên tục Toàn bài)

Trong các tệp Markdown độc lập, mỗi tệp được sinh theo prompt riêng nên có số thứ tự cục bộ (ví dụ file `02` có Bảng 1, file `03` có Bảng 1, file `05` có Bảng 1). Khi xuất ra bản báo cáo hoàn chỉnh (Word / LaTeX), **bắt buộc đánh số liên tục từ Bảng 1 đến Bảng 6** như bảng đối chiếu dưới đây:

| Mã bảng gốc trong Markdown | Đề xuất đánh số liên tục toàn văn | Tên mô tả bảng biểu | File nguồn và dòng | Vị trí caption hiện tại | Khuyến nghị chuẩn hóa theo STYLE_RULES.md (Mục 5.2) |
| :---: | :---: | :--- | :--- | :---: | :--- |
| `Bảng 1` | **Bảng 1** | So sánh ưu nhược điểm của các trường phái tiếp cận bài toán kiểm tra khuyết tật công nghiệp | `02_chuong1.md` (Dòng 159) | Dưới bảng | Đưa caption lên **phía trên** bảng |
| `Bảng 1` | **Bảng 2** | So sánh định tính phương pháp đề xuất với các phương pháp đối chứng theo các tiêu chí kỹ thuật | `03_chuong2_part1.md` (Dòng 25) | Dưới bảng | Đưa caption lên **phía trên** bảng |
| `Bảng 1` | **Bảng 3** | Thống kê phân bố số lượng mẫu ảnh và các dạng khuyết tật thực tế trên 6 danh mục MVTec AD | `05_chuong3_part1.md` (Dòng 51) | Dưới bảng | Đưa caption lên **phía trên** bảng |
| `Bảng 2` | **Bảng 4** | Tổng hợp các tiêu chí đánh giá định lượng được sử dụng trong hệ thống xử lý ảnh của dự án | `06_chuong3_part2.md` (Dòng 27) | Dưới bảng | Đưa caption lên **phía trên** bảng |
| `Bảng 3` | **Bảng 5** | Bảng tổng hợp kết quả định lượng ma trận thực nghiệm cắt bỏ trên tập dữ liệu MVTec AD | `06_chuong3_part2.md` (Dòng 88) | Dưới bảng | Đưa caption lên **phía trên** bảng |
| `Bảng 4` | **Bảng 6** | Đối chiếu giữa điều kiện thử nghiệm kiểm soát trong phòng thí nghiệm và điều kiện vận hành thực tế tại nhà máy | `06_chuong3_part2.md` (Dòng 151) | Dưới bảng | Đưa caption lên **phía trên** bảng |

> [!NOTE]
> Trong tệp [main.tex](file:///d:/XULIANH/industrial-defect-segmentation/report/main.tex), gói lệnh `chngcntr` với khai báo `\counterwithout{table}{chapter}` đã tự động đánh số liên tục toàn bài từ 1 đến 6 và hiển thị caption phía trên chuẩn mực theo cấu hình `\captionsetup[table]{name=Bảng, labelsep=period}`.

---

## PHẦN 2: DANH MỤC CÁC VỊ TRÍ GẮN THẺ CHỜ BỔ SUNG & CẬP NHẬT

Dưới đây là danh sách chi tiết các vị trí gắn thẻ giữ chỗ cần điền thông tin hoặc nạp kết quả huấn luyện từ Google Colab trước khi xuất bản bản cứng:

### 2.1. Nhóm Thông tin Hành chính và Chữ ký
1. **`report/01_frontmatter_mo_dau.md` (Dòng 21):**
   - Thẻ: `[CẦN BỔ SUNG: TÊN CƠ QUAN / ĐƠN VỊ ĐÀO TẠO CẤP TRÊN]`
   - Vị trí: Trang bìa chính và trang phụ bìa.
   - Hướng dẫn điền: Ghi rõ cơ quan chủ quản (ví dụ: `BỘ THÔNG TIN VÀ TRUYỀN THÔNG`).
2. **`report/01_frontmatter_mo_dau.md` (Dòng 31 & Dòng 80):**
   - Thẻ: Chữ ký của Sinh viên tại trang bìa và trang LỜI CAM ĐOAN.
   - Hướng dẫn điền: Ký tên hoặc chèn ảnh chữ ký số `Nguyen Duc Nghiem`.

### 2.2. Nhóm Số liệu Huấn luyện Đang chạy trên Google Colab (GPU NVIDIA A100)
1. **`report/06_chuong3_part2.md` (Dòng 75 đến Dòng 85 - Bảng 3 ma trận thực nghiệm):**
   - Thẻ: `[CẦN CẬP NHẬT]` trên các cột số đo của **`EXP-01` đến `EXP-11`**:
     + Cột Mask mAP@50 (IoU=0.50).
     + Cột Mask mAP@50-95 (IoU=0.50:0.95).
     + Cột Pixel-AUROC.
     + Cột Image-AUROC.
     + Cột Tỷ lệ báo động giả FAR@0.25.
     + Cột Chỉ số suy thoái quang học trung bình mCE.
     + Cột Tốc độ xử lý FPS (Inference Speed).
   - *Ghi chú:* Kịch bản baseline **EXP-00** đã có số liệu nghiệm thu chính xác: Mask mAP@50 đạt `0.800`, mAP@50-95 đạt `0.480`, Pixel-AUROC đạt `1.000`, Image-AUROC đạt `1.000`, FAR@0.25 đạt `0.000`, FPS đạt `149.2`.
2. **`report/06_chuong3_part2.md` (Dòng 10 - Vị trí đề xuất `Hình 3.6`):**
   - Thẻ: `[Hình 3.6]` - Biểu đồ hội tụ hàm mất mát phân vùng ($\mathcal{L}_{total}$) và đường cong tăng trưởng Mask mAP qua 50 epochs.
   - Hướng dẫn điền: Xuất tệp đồ thị `loss_curve.png` / `results.png` sinh ra tự động từ thư mục `runs/segment/` của Colab và sao chép vào `report/figures/`.
3. **`report/06_chuong3_part2.md` (Dòng 113 - Vị trí đề xuất `Hình 3.7`):**
   - Thẻ: `[Hình 3.7]` - Trực quan hóa ảnh kết quả suy luận thực tế (True Positives, False Positives, False Negatives).
   - Hướng dẫn điền: Lấy 4 ảnh kết quả phân vùng minh họa từ tập test của Colab lưu vào `report/figures/`.
4. **`report/06_chuong3_part2.md` (Dòng 136 - Vị trí đề xuất `Hình 3.8`):**
   - Thẻ: `[Hình 3.8]` - Đồ thị đường cong suy thoái độ chính xác Mask mAP theo 5 cấp độ nghiêm trọng của bộ chuẩn MVTec-AD-C.
   - Hướng dẫn điền: Chạy script `evaluation/robustness_evaluator.py` trên Colab để xuất đồ thị đường cong suy thoái.

### 2.3. Nhóm Xác minh Nguồn Tài liệu Tham khảo
1. **`report/07_ket_luan_tltk.md` (Dòng 52 - Mục `[10]`):**
   - Thẻ: `[CẦN XÁC MINH NGUỒN: Tài liệu học tập nội bộ do Giảng viên cung cấp]`
   - Trích dẫn hiện tại: `Huỳnh Trung Trụ, Bài giảng và tài liệu hướng dẫn học phần Xử lý ảnh (INT14123_CLC), Khoa Công nghệ thông tin 2, Học viện Công nghệ Bưu chính Viễn thông, 2026. [Trực tuyến]. Địa chỉ: https://drive.google.com/drive/folders/19x-NFBYmU1MT44r3ElpTE79Lkl8zRWDf`.
   - Hướng dẫn: Giảng viên hoặc người đọc có thể nhấp trực tiếp vào liên kết Drive để tra cứu các slide bài giảng và giáo trình môn học.
