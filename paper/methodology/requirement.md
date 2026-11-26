# SECTION III: PROPOSED METHODOLOGY — YÊU CẦU THIẾT KẾ & ĐẶC TẢ TOÁN HỌC (REQUIREMENTS)

> **Mục đích:** Tài liệu kỹ thuật định nghĩa toàn bộ cấu trúc toán học, tham số giải thuật và ánh xạ mã nguồn cho Mục III (Proposed Methodology) của bài báo. Đảm bảo tính nhất quán 100% với `paper/Mision.md`, `report/03_chuong2_part1.md`, `report/04_chuong2_part2.md` và mã nguồn trong `data_engine/`.

---

## 1. Mục Tiêu & Cấu Trúc Đề Cương (Section Architecture)

Section III chiếm ngân sách khoảng **2.0 – 2.5 trang** trong bản thảo IEEE Conference, đóng vai trò là "trái tim kỹ thuật" của bài báo. Cấu trúc chia thành 5 tiểu mục logic:

### Subsection A: Problem Formulation & Zero-Data-Leakage Constraint
* **Ký hiệu toán học:**
  - Ảnh bề mặt công nghiệp: $I \in \mathbb{R}^{H \times W \times C}$ với $H, W$ là chiều cao, chiều rộng và $C=3$ kênh màu RGB.
  - Tập huấn luyện hoàn toàn lành: $\mathcal{D}_{\text{train}} = \{I_k \in \mathbb{R}^{H \times W \times C} \mid I_k \text{ is nominal}\}_{k=1}^{N_{\text{train}}}$.
  - Tập kiểm thử có lỗi thật: $\mathcal{D}_{\text{test}} = \{(I_i, M_i^*)\}_{i=1}^{N_{\text{test}}}$, với $M_i^* \in \{0, 1\}^{H \times W}$ là nhãn ground-truth pixel-level.
* **Cam kết Zero-Data-Leakage:**
  - Không bao giờ quan sát, trích xuất đặc trưng hoặc lấy mẫu từ $\mathcal{D}_{\text{test}}$ trong toàn bộ quá trình sinh mẫu tổng hợp $\mathcal{G}(I)$ hay huấn luyện mô hình $\mathcal{F}_\theta$.

### Subsection B: Frequency-Domain Preprocessing (Group B)
* **1. Adaptive 2D-FFT Periodic Notch Filter (Triệt tiêu hoa văn tuần hoàn):**
  - Biến đổi Fourier 2D độc lập trên từng kênh màu $c \in \{1, \dots, C\}$:
    $$F_c(u, v) = \sum_{x=0}^{H-1} \sum_{y=0}^{W-1} I_c(x, y) e^{-j 2\pi \left(\frac{ux}{H} + \frac{vy}{W}\right)}$$
  - Tọa độ tâm DC: $(u_0, v_0) = (H/2, W/2)$. Phổ biên độ tập trung: $|F_c(u, v)|$.
  - Phát hiện đỉnh phổ thích nghi: 
    $$\mathcal{S}_{\text{peaks}} = \{ (u, v) \mid |F_c(u, v)| > \mu_{|F|} + \tau_{\text{peak}} \cdot \sigma_{|F|}, \, d(u, v) > r_{\text{inner}} \}$$
  - Tham số chuẩn mã nguồn: $\tau_{\text{peak}} = 3.5$, $r_{\text{inner}} = 15\text{ px}$.
  - Hàm truyền Gaussian reject đối xứng qua tâm DC cho $K = |\mathcal{S}_{\text{peaks}}| / 2$ cặp đỉnh:
    $$H_{\text{notch}}(u, v) = \prod_{k=1}^K \left[ 1 - \exp\left( -\frac{D_k(u, v) D_{-k}(u, v)}{2 r_0^2} \right) \right]$$
    với $D_k(u, v) = \sqrt{(u - u_k)^2 + (v - v_k)^2}$, $D_{-k}(u, v) = \sqrt{(u - (2u_0 - u_k))^2 + (v - (2v_0 - v_k))^2}$, $r_0 = 5.0\text{ px}$.
  - Biến đổi ngược 2D-IFFT: Cho ảnh đã lọc hoa văn nền, làm nổi bật vi nứt.
* **2. 2D-DWT Haar Wavelet Sub-Band Modulation (Khuếch đại biên độ chi tiết):**
  - Phân rã 4 dải băng tần: $I(x, y) \xrightarrow{\text{2D-DWT}} \{I_{LL}, I_{LH}, I_{HL}, I_{HH}\}$.
  - Điều biến năng lượng độc lập từng dải con (khớp `pywt.idwt2`):
    $$\tilde{I}_{LL} = \alpha \cdot I_{LL}, \quad \alpha = 0.6$$
    $$\tilde{I}_{\theta} = \gamma \cdot I_{\theta}, \quad \forall \theta \in \{LH, HL, HH\}, \quad \gamma = 1.4$$
  - Tái tạo không gian qua 2D-IDWT: Chống lại hiện tượng mờ quang học/mất nét.
* **3. Identity Roundtrip Numerical Integrity Proof (Chứng minh bảo toàn số học):**
  - Bảng số liệu Table I: $\text{PSNR} = 51.31\text{ dB}$, $\text{SSIM} = 0.9983$, $\text{MAE} \le 0.4807/255$ cho 2D-FFT và đẳng cấu toán học tuyệt đối ($\text{PSNR}=\infty, \text{SSIM}=1.0$) cho 2D-DWT.
  - Khẳng định toán học: Zero coordinate shift (không gây lệch tọa độ mask phân đoạn).

### Subsection C: Spatial Anomaly Synthesis (Group A)
* **1. Rigid & Scar CutPaste:**
  - Vùng cắt hình chữ nhật với diện tích $a \in [0.02, 0.15]$, tỷ lệ co giãn $r_{\text{aspect}} \in [0.3, 3.3]$, góc xoay ngẫu nhiên $\phi \in [-45^\circ, 45^\circ]$.
  - Scar CutPaste: Dải hẹp $r_{\text{aspect}} \in [0.05, 0.2]$ mô phỏng vết cào xước kim loại.
* **2. DRAEM Multi-Octave Perlin Noise for Arbitrary Dimensions:**
  - Sinh trường vô hướng Perlin $\mathcal{N}$ trên lưới chuẩn cố định $\Omega_0 \in \mathbb{R}^{512 \times 512}$ với tọa độ không gian $(s, t) \in [0, 512]^2$ qua 5 octaves:
    $$\mathcal{N}(s, t) = \sum_{i=1}^5 \frac{1}{2^i} f_i(2^i s, 2^i t)$$
  - Ánh xạ song tuyến tính thích nghi sang kích thước ảnh công nghiệp $(H, W)$:
    $$\mathcal{M}_{\text{perlin}}(x, y) = \mathcal{B}_{\text{linear}}\left(\mathcal{N}, \frac{512}{H} x, \frac{512}{W} y\right)$$
  - Phân ngưỡng $\mathcal{M}_{\text{perlin}} > \tau_{\text{perlin}}$ ($\tau_{\text{perlin}} = 0.5$) tạo mặt nạ hình học hữu cơ mượt mà.
* **3. Poisson Seamless Cloning (NSA) with Automated Foreground Clamping:**
  - Giải phương trình đạo hàm riêng Poisson: $\Delta f = \operatorname{div}\mathbf{v}$ với điều kiện biên Dirichlet $f|_{\partial \Omega} = I_{\text{target}}|_{\partial \Omega}$.
  - Kẹp tiền cảnh tự động (Foreground Clamping) qua Otsu thresholding để ngăn dị tật rơi ra ngoài băng tải đối với các sản phẩm khối (`screw`, `bottle`, `pill`).

### Subsection D: False-Alarm Suppression via Negative Invariant
* **Cơ chế cân bằng mẫu âm bắt buộc:**
  - Tỷ lệ mẫu âm cố định: $\rho_{\text{neg}} = 0.15$ ($15\%$ ảnh trong mỗi batch là ảnh hoàn toàn lành paired with empty polygon label).
  - Cấu trúc batch: $\mathcal{D}_{\text{batch}} = (1 - \rho_{\text{neg}}) \cdot \mathcal{D}_{\text{synthetic}} \cup \rho_{\text{neg}} \cdot \mathcal{D}_{\text{clean}}$.
  - Cơ chế phạt hàm mất mát: Ngăn chặn triệt để xu hướng over-predict trên vân bề mặt tự nhiên, ép $\text{FAR@0.25} = 0.000$.

### Subsection E: Polygonal Vectorization for Real-Time Segmentation
* **Trích xuất đường viền Suzuki-Abe:**
  - Mặt nạ nhị phân chuẩn hóa $M \in \{0, 1\}^{H \times W}$.
  - Thuật toán border following trích xuất chuỗi đỉnh liên tục $\mathcal{C} = \{p_1, p_2, \dots, p_{N_v}\}$ với $N_v$ đỉnh.
* **Đơn giản hóa Ramer-Douglas-Peucker (RDP):**
  - Bán kính dung sai thích nghi theo chu vi: $\epsilon = 0.002 \cdot \oint_{\mathcal{C}} ds$.
  - Bão hòa số đỉnh (tối đa 30–50 đỉnh/đa giác), chuẩn hóa tọa độ $[0.0, 1.0]$ khớp trực tiếp với format YOLOv11-seg.

---

## 2. Bảng Ánh Xạ Ký Hiệu Đã Chuẩn Hóa (Zero Collision Notation Table)

| Đại lượng toán học | Ký hiệu chuẩn hóa | Tránh nhầm lẫn với |
| :--- | :---: | :--- |
| Số kênh màu RGB | $C = 3$ | Đã phân biệt với đường viền đa giác $\mathcal{C}$ |
| Đường viền đa giác | $\mathcal{C} = \{p_1, \dots, p_{N_v}\}$ | Đã phân biệt với số kênh màu $C$ |
| Tọa độ tần số Fourier | $(u, v)$ | Đã phân biệt với tọa độ lưới Perlin $(s, t)$ |
| Tọa độ lưới chuẩn Perlin | $(s, t) \in [0, 512]^2$ | Đã phân biệt với tọa độ tần số $(u, v)$ |
| Số lượng cặp đỉnh phổ Notch | $K = \|\mathcal{S}_{\text{peaks}}\| / 2$ | Đã phân biệt với số đỉnh đa giác $N_v$ |
| Số đỉnh đa giác đường viền | $N_v$ | Đã phân biệt với số đỉnh phổ Notch $K$ |
| Tỷ lệ khung hình mảng CutPaste | $r_{\text{aspect}} \in [0.3, 3.3]$ | Đã phân biệt với bán kính lọc $r_0, r_{\text{inner}}$ |
| Bán kính lọc notch Gaussian | $r_0 = 5.0\text{ px}$ | Đã phân biệt với tỷ lệ khung hình $r_{\text{aspect}}$ |
| Mặt nạ phân đoạn nhị phân | $M \in \{0, 1\}^{H \times W}$ | Thống nhất chuẩn $\{0, 1\}$ toàn bài báo |
| Dải sóng con chi tiết | $\tilde{I}_\theta = \gamma \cdot I_\theta$ | Điều biến độc lập cho $\theta \in \{LH, HL, HH\}$ |
| Góc xoay mảng CutPaste | $\phi \in [-45^\circ, 45^\circ]$ | Đã phân biệt với chỉ số dải sóng con $\theta$ |
