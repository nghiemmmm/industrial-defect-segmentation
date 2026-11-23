# CHƯƠNG II: ĐỀ XUẤT PHƯƠNG PHÁP XỬ LÝ HÌNH ẢNH TRONG PHÂN VÙNG KHUYẾT TẬT BỀ MẶT CÔNG NGHIỆP (PHẦN 2)

---

### 2.3. Phương pháp xử lý hình ảnh trong phân vùng khuyết tật bề mặt công nghiệp

Mục này trình bày chi tiết 9 mô-đun thuật toán xử lý ảnh cốt lõi trong hệ thống, tương ứng 1-1 với các khối chức năng trên sơ đồ kiến trúc Hình 2.1. Mỗi mô-đun được trình bày chuẩn xác theo khuôn mẫu 5 phần khoa học: Đoạn dẫn nhập, Đầu vào, Đầu ra, Quá trình xử lý từng bước và Các công thức toán học dẫn xuất trực tiếp từ mã nguồn thực tế.

---

#### 2.3.1. Mô-đun lọc miền tần số 2D-FFT triệt tiêu đỉnh phổ tuần hoàn

Mô-đun `FFTPeriodicSuppressionFilter` trong tệp `data_engine/frequency/fft_filter.py` được thiết kế nhằm mục đích "lột bỏ" các hoa văn đan dệt lặp lại có tính chu kỳ cao trên các bề mặt như lưới thép (`grid`) hoặc thảm dệt sợi (`carpet`). Bằng cách chuyển đổi ảnh sang miền tần số, các cấu trúc tuần hoàn sẽ hội tụ thành các đỉnh năng lượng phổ nhọn đối xứng rời rạc; việc triệt tiêu các đỉnh này bằng bộ lọc chặn dải thích nghi giúp làm phẳng kết cấu nền và làm nổi bật tín hiệu bất thường của khuyết tật đứt sợi hay biến dạng vật lý.

**1. Đầu vào (Inputs):**
- Ma trận ảnh màu RGB sản phẩm: $I \in \mathbb{R}^{H \times W \times 3}$, kiểu dữ liệu `np.uint8`, giá trị cường độ sáng $[0, 255]$.
- Hệ số ngưỡng độ lệch năng lượng đỉnh phổ: $\tau_{peak} = 3.5$ (số thực dấu phẩy động).
- Bán kính ảnh hưởng của hố chặn Notch Gaussian: $r_0 = 5.0\text{ pixels}$.
- Bán kính bảo vệ thành phần tần số một chiều (DC): $r_{dc} = 10\text{ pixels}$.

**2. Đầu ra (Outputs):**
- Ma trận ảnh sau khi triệt tiêu hoa văn nền tuần hoàn: $I_{fft} \in \mathbb{R}^{H \times W \times 3}$, kiểu `np.uint8`, bảo toàn nguyên vẹn độ phân giải không gian ban đầu.
- Ma trận phổ biên độ tần số trung gian phục vụ trực quan hóa: $|F(u, v)| \in \mathbb{R}^{H \times W}$, kiểu `np.float64`.

**3. Quá trình xử lý (Processing Flow):**
- *Bước 1 -- Biến đổi Fourier rời rạc 2D từng kênh màu:* Lần lượt duyệt qua từng kênh màu $c \in \{R, G, B\}$. Chuyển đổi ma trận kênh màu $I_c$ từ miền không gian sang miền tần số bằng phép biến đổi Fourier nhanh 2 chiều thông qua hàm `np.fft.fft2`.
- *Bước 2 -- Dịch chuyển gốc tọa độ tần số:* Áp dụng hàm `np.fft.fftshift` để đưa thành phần tần số 0 (thành phần DC) từ góc trên bên trái về chính giữa tâm ma trận phổ $(u_0, v_0) = (\lfloor H/2 \rfloor, \lfloor W/2 \rfloor)$.
- *Bước 3 -- Xác định ngưỡng năng lượng động:* Tính ma trận phổ biên độ $|F_c(u, v)|$. Tính giá trị trung vị $\operatorname{median}(|F_c|)$ và giá trị trung bình $\mu(|F_c|)$ trên toàn phổ. Xác định ngưỡng cắt động $T = \tau_{peak} \cdot \operatorname{median}(|F_c|) + \mu(|F_c|)$.
- *Bước 4 -- Dò tìm các đỉnh năng lượng tuần hoàn đối xứng:* Quét toàn bộ phổ tần số, tìm tập hợp các tọa độ $(u_k, v_k)$ thỏa mãn đồng thời hai điều kiện: năng lượng vượt ngưỡng $|F_c(u_k, v_k)| > T$ và nằm ngoài vùng lân cận thành phần DC $\sqrt{(u_k - u_0)^2 + (v_k - v_0)^2} > r_{dc}$.
- *Bước 5 -- Nhân hàm truyền Notch Gaussian đa điểm:* Xây dựng mặt nạ lọc $H_{notch}(u, v)$ có giá trị khởi tạo là 1.0. Tại mỗi cặp đỉnh đối xứng $(u_k, v_k)$ và $(-u_k, -v_k)$, nhân suy giảm năng lượng theo hàm phân phối Gauss với bán kính $r_0$.
- *Bước 6 -- Nghịch đảo khôi phục miền không gian:* Nhân phổ phức đã dịch tâm với mặt nạ lọc: $F'_c(u, v) = F_c(u, v) \cdot H_{notch}(u, v)$. Dịch ngược gốc tần số bằng `np.fft.ifftshift`, thực hiện biến đổi Fourier nghịch đảo 2D bằng `np.fft.ifft2`, lấy phần thực, cắt ngưỡng giá trị về đoạn $[0, 255]$ và ép kiểu `np.uint8`. Ghép 3 kênh màu để tái tạo ảnh RGB hoàn chỉnh.

**Công thức toán học:**

Phép biến đổi Fourier rời rạc 2 chiều chuyển ảnh sang miền tần số:
$$F(u, v) = \sum_{x=0}^{H-1} \sum_{y=0}^{W-1} I(x, y) \cdot \exp\left( -j 2\pi \left[ \frac{ux}{H} + \frac{vy}{W} \right] \right)$$
*Công thức 1 Biến đổi Fourier rời rạc 2 chiều*  
Trong đó:
- $H, W$ lần lượt là chiều cao và chiều rộng của ảnh (tính theo pixel).
- $x, y$ là tọa độ điểm ảnh trong miền không gian ($0 \le x < H, 0 \le y < W$).
- $u, v$ là tọa độ tần số trong miền Fourier.
- $j = \sqrt{-1}$ là đơn vị ảo của số phức.
- $F(u, v) \in \mathbb{C}$ là giá trị phổ phức tại tần số $(u, v)$.

Ngưỡng năng lượng động phát hiện đỉnh phổ tuần hoàn:
$$T = \tau_{peak} \cdot \operatorname{median}\Big(|F(u, v)|\Big) + \frac{1}{HW} \sum_{u=0}^{H-1} \sum_{v=0}^{W-1} |F(u, v)|$$
*Công thức 2 Ngưỡng năng lượng động phát hiện đỉnh phổ tần số tuần hoàn*  
Trong đó:
- $|F(u, v)| = \sqrt{\operatorname{Re}(F)^2 + \operatorname{Im}(F)^2}$ là phổ biên độ năng lượng.
- $\tau_{peak}$ là hệ số nhạy phát hiện đỉnh (trong mã nguồn thiết lập $\tau_{peak} = 3.5$).
- $\operatorname{median}(\cdot)$ là giá trị trung vị của toàn bộ ma trận phổ biên độ.

Hàm truyền bộ lọc chặn dải Notch Gaussian đa điểm đối xứng:
$$H_{notch}(u, v) = \prod_{k=1}^K \left[ 1 - \exp\left( -\frac{D_k(u, v)^2}{2 r_0^2} \right) \right] \cdot \left[ 1 - \exp\left( -\frac{D_{-k}(u, v)^2}{2 r_0^2} \right) \right]$$
*Công thức 3 Hàm truyền bộ lọc chặn dải Notch Gaussian đa điểm đối xứng*  
Trong đó:
- $K$ là tổng số lượng đỉnh phổ tuần hoàn phát hiện được.
- $D_k(u, v) = \sqrt{(u - u_k)^2 + (v - v_k)^2}$ là khoảng cách Euclid từ tọa độ $(u, v)$ đến đỉnh phổ thứ $k$.
- $D_{-k}(u, v) = \sqrt{(u + u_k - 2u_0)^2 + (v + v_k - 2v_0)^2}$ là khoảng cách đến đỉnh liên hợp đối xứng qua tâm $(u_0, v_0)$.
- $r_0$ là bán kính dải chặn của hố suy giảm năng lượng ($r_0 = 5.0\text{ px}$).

Phép biến đổi Fourier nghịch đảo khôi phục miền không gian:
$$I_{fft}(x, y) = \operatorname{clip}_{[0, 255]}\left( \operatorname{Re}\left( \frac{1}{HW} \sum_{u=0}^{H-1} \sum_{v=0}^{W-1} \Big(F(u, v) \cdot H_{notch}(u, v)\Big) \cdot \exp\left( j 2\pi \left[ \frac{ux}{H} + \frac{vy}{W} \right] \right) \right) \right)$$
*Công thức 4 Biến đổi Fourier nghịch đảo 2 chiều khôi phục cường độ điểm ảnh*  
Trong đó:
- $\operatorname{Re}(\cdot)$ là phép toán lấy phần thực của ma trận số phức.
- $\operatorname{clip}_{[0, 255]}(\cdot)$ là toán tử cắt ngưỡng ép giá trị điểm ảnh vào đoạn hợp lệ $[0, 255]$.

---

#### 2.3.2. Mô-đun phân rã biến đổi sóng con 2D-DWT và tăng cường dải chi tiết biên

Mô-đun `DWTSubbandFilter` trong tệp `data_engine/frequency/dwt_filter.py` vận dụng lý thuyết biến đổi sóng con đa độ phân giải để bóc tách thông tin cấu trúc ảnh thành các dải tần số không gian có định hướng. Nhờ việc bảo toàn nguyên vẹn dải tần số thấp và khuếch đại có chọn lọc các hệ số của 3 dải tần số cao, mô-đun giúp làm sắc nét các vết nứt tế vi trên bề mặt gạch men (`tile`) mà không làm tăng nhiễu hạt nền.

**1. Đầu vào (Inputs):**
- Ma trận ảnh màu RGB sản phẩm: $I \in \mathbb{R}^{H \times W \times 3}$, kiểu `np.uint8`.
- Tên họ sóng con trực giao: `wavelet = "haar"` (hoặc Daubechies `"db1"`).
- Hệ số khuếch đại chi tiết dải cao tần: $k_{detail} = 1.5$ (số thực dương $\ge 1.0$).

**2. Đầu ra (Outputs):**
- Ma trận ảnh sau tăng cường biên: $I_{dwt} \in \mathbb{R}^{H \times W \times 3}$, kiểu `np.uint8`.
- Bộ 4 ma trận hệ số sóng con mức 1: $LL, LH, HL, HH \in \mathbb{R}^{\frac{H}{2} \times \frac{W}{2}}$, kiểu `np.float64`.

**3. Quá trình xử lý (Processing Flow):**
- *Bước 1 -- Phân rã sóng con 2D độc lập:* Duyệt qua từng kênh màu $c \in \{R, G, B\}$. Áp dụng hàm `pywt.dwt2(..., 'haar')` để phân rã ma trận kênh màu thành 4 ma trận con có kích thước giảm một nửa $(\frac{H}{2}, \frac{W}{2})$.
- *Bước 2 -- Cô lập dải tần xấp xỉ thấp:* Giữ nguyên ma trận $LL$ chứa năng lượng thấp đại diện cho độ sáng nền trung bình và thông tin màu sắc tổng thể của vật liệu.
- *Bước 3 -- Khuếch đại dải chi tiết cao:* Nhân trực tiếp hệ số $k_{detail} = 1.5$ vào 3 ma trận hệ số chi tiết cao:
  $$LH' = 1.5 \cdot LH, \quad HL' = 1.5 \cdot HL, \quad HH' = 1.5 \cdot HH$$
- *Bước 4 -- Tái tạo không gian bằng biến đổi ngược 2D-IDWT:* Ghép bộ ma trận đã điều chỉnh $(LL, (LH', HL', HH'))$ và gọi hàm `pywt.idwt2(..., 'haar')` để khôi phục ma trận không gian có kích thước $H \times W$.
- *Bước 5 -- Chuẩn hóa kiểu dữ liệu:* Cắt ngưỡng biên $[0, 255]$ và ép kiểu dữ liệu về `np.uint8`, hợp nhất 3 kênh màu thành ảnh màu $I_{dwt}$.

**Công thức toán học:**

Phương trình phân rã 4 dải tần số con sóng con 2D Haar tại mức 1:
$$\begin{aligned}
LL(i, j) &= \frac{1}{2} \Big( I(2i, 2j) + I(2i+1, 2j) + I(2i, 2j+1) + I(2i+1, 2j+1) \Big) \\
LH(i, j) &= \frac{1}{2} \Big( I(2i, 2j) + I(2i+1, 2j) - I(2i, 2j+1) - I(2i+1, 2j+1) \Big) \\
HL(i, j) &= \frac{1}{2} \Big( I(2i, 2j) - I(2i+1, 2j) + I(2i, 2j+1) - I(2i+1, 2j+1) \Big) \\
HH(i, j) &= \frac{1}{2} \Big( I(2i, 2j) - I(2i+1, 2j) - I(2i, 2j+1) + I(2i+1, 2j+1) \Big)
\end{aligned}$$
*Công thức 5 Phân rã 4 dải tần số con của biến đổi sóng con 2D Haar*  
Trong đó:
- $i, j$ là tọa độ điểm trên lưới ma trận con ($0 \le i < H/2, 0 \le j < W/2$).
- $LL$ là dải xấp xỉ tần số thấp theo cả hai chiều ngang và dọc.
- $LH$ là dải thông thấp phương ngang, thông cao phương dọc (chứa chi tiết biên ngang).
- $HL$ là dải thông cao phương ngang, thông thấp phương dọc (chứa chi tiết biên dọc).
- $HH$ là dải thông cao theo cả hai chiều (chứa các điểm góc và đường chéo vi mô).

Toán tử tăng cường chi tiết và tái tạo sóng con ngược 2D-IDWT:
$$I_{dwt}(x, y) = \operatorname{clip}_{[0, 255]}\Big( \operatorname{IDWT2}\Big( LL, k_{detail} \cdot LH, k_{detail} \cdot HL, k_{detail} \cdot HH \Big) \Big)$$
*Công thức 6 Tăng cường dải chi tiết cao và tái tạo sóng con ngược 2 chiều*  
Trong đó:
- $k_{detail} = 1.5$ là hệ số khuếch đại dải chi tiết cao được cấu hình trong mã nguồn.
- $\operatorname{IDWT2}(\cdot)$ là toán tử biến đổi sóng con rời rạc 2 chiều nghịch đảo trực giao.

---

#### 2.3.3. Mô-đun sinh khuyết tật tổng hợp dạng mảng bám và vết xước CutPaste

Mô-đun `CutPasteSynthesizer` trong tệp `data_engine/synthesizers/cutpaste_synthesizer.py` hiện thực hóa thuật toán cắt dán mảnh vá hình học ngẫu nhiên [2]. Mô-đun cho phép mô phỏng hai dạng khuyết tật vật lý sắc nét: dạng mảng bám bất thường (\texttt{normal}) và dạng vết xước kéo dài (\texttt{scar}), cung cấp dữ liệu huấn luyện đa dạng cho các lớp vật thể khối (`screw`, `bottle`).

**1. Đầu vào (Inputs):**
- Đối tượng `Sample` chứa ảnh màu gốc $I \in \mathbb{R}^{H \times W \times 3}$ và mặt nạ nhị phân rỗng $M = \mathbf{0}_{H \times W}$.
- Chế độ sinh: `mode = "normal"` hoặc `mode = "scar"`.
- Khoảng tỷ lệ diện tích miếng vá: $\text{area\_ratio} \in [0.02, 0.15]$.
- Khoảng tỷ lệ khung hình: $\text{aspect\_ratio} \in [0.3, 3.3]$ (normal) hoặc $[0.05, 0.2]$ (scar).
- Khoảng góc xoay ngẫu nhiên: $\theta \in [-45^\circ, 45^\circ]$.
- Biên độ biến thiên màu sắc: $\Delta_{jitter} = 0.10$ ($\pm 10\%$).

**2. Đầu ra (Outputs):**
- Đối tượng `Sample` cập nhật:
  + Ảnh mang khuyết tật $I_{cp} \in \mathbb{R}^{H \times W \times 3}$.
  + Mặt nạ nhị phân $M_{cp} \in \{0, 255\}^{H \times W}$, trong đó vùng miếng vá mang giá trị 255.
  + Nhãn `label = "cutpaste_normal"` hoặc `"cutpaste_scar"`, cờ `is_anomaly = True`.

**3. Quá trình xử lý (Processing Flow):**
- *Bước 1 -- Xác định kích thước mảnh vá nguồn:* Lấy mẫu ngẫu nhiên diện tích $A_{patch} = \alpha \cdot (H \cdot W)$ với $\alpha \sim \mathcal{U}(0.02, 0.15)$ và tỷ lệ khung hình $r \sim \mathcal{U}(r_{min}, r_{max})$. Tính chiều rộng $w_p = \sqrt{A_{patch} \cdot r}$ và chiều cao $h_p = \sqrt{A_{patch} / r}$.
- *Bước 2 -- Cắt mảnh ảnh và hiệu chỉnh màu sắc:* Lấy ngẫu nhiên tọa độ góc trên bên trái $(x_s, y_s)$ trong miền ảnh gốc. Trích xuất mảnh vá $P = I[y_s:y_s+h_p, x_s:x_s+w_p]$. Nhân các kênh màu của $P$ với vector hệ số biến thiên ngẫu nhiên $[1 + \delta_R, 1 + \delta_G, 1 + \delta_B]$ với $\delta_c \sim \mathcal{U}(-0.10, 0.10)$ để tạo sự sai khác quang học nhẹ.
- *Bước 3 -- Biến đổi Affine xoay miếng vá:* Khởi tạo ma trận mặt nạ cục bộ $M_p$ kích thước $h_p \times w_p$ toàn số 255. Xây dựng ma trận Affine xoay 2D $\mathbf{A}$ quanh tâm miếng vá với góc xoay ngẫu nhiên $\theta \sim \mathcal{U}(-45^\circ, 45^\circ)$. Sử dụng hàm `cv2.warpAffine` để xoay đồng thời mảnh ảnh $P$ và mặt nạ $M_p$.
- *Bước 4 -- Cấy ghép vào vị trí đích:* Lấy ngẫu nhiên tọa độ tâm đích $(x_d, y_d)$ trên ảnh nền sao cho miếng vá nằm hoàn toàn trong giới hạn $[0, W] \times [0, H]$. Dán các điểm ảnh của mảnh vá xoay vào ảnh nền tại những vị trí mà mặt nạ xoay $M'_p > 0$.
- *Bước 5 -- Đồng bộ hóa mặt nạ toàn cục:* Cập nhật giá trị 255 vào ma trận mặt nạ toàn cục $M_{cp}$ tại đúng các tọa độ điểm ảnh đích vừa được dán đè.

**Công thức toán học:**

Ma trận biến đổi Affine xoay và tịnh tiến mảnh vá 2D:
$$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = \begin{bmatrix} \cos\theta & -\sin\theta & x_d - x_c\cos\theta + y_c\sin\theta \\ \sin\theta & \cos\theta & y_d - x_c\sin\theta - y_c\cos\theta \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$
*Công thức 7 Ma trận biến đổi Affine xoay và tịnh tiến mảnh vá khuyết tật*  
Trong đó:
- $(x, y)$ là tọa độ điểm ảnh cục bộ ban đầu của mảnh vá nguồn.
- $(x_c, y_c) = (w_p/2, h_p/2)$ là tọa độ tâm quay của mảnh vá.
- $\theta \in [-45^\circ, 45^\circ]$ là góc xoay ngẫu nhiên.
- $(x_d, y_d)$ là tọa độ tâm đích cần cấy ghép trên bề mặt sản phẩm.
- $(x', y')$ là tọa độ điểm ảnh kết quả trên hệ quy chiếu toàn cục.

Toán tử hòa trộn dán đè điểm ảnh theo mặt nạ nhị phân:
$$I_{cp}(x, y) = \begin{cases} P_{rotated}(x, y) & \text{nếu } M_{rotated}(x, y) = 255 \\ I(x, y) & \text{ngược lại} \end{cases}$$
*Công thức 8 Toán tử dán đè điểm ảnh theo mặt nạ nhị phân CutPaste*  
Trong đó:
- $I(x, y)$ là cường độ sáng của ảnh gốc tại tọa độ $(x, y)$.
- $P_{rotated}(x, y)$ là cường độ sáng của mảnh vá sau biến đổi Affine.
- $M_{rotated}(x, y) \in \{0, 255\}$ là mặt nạ nhị phân của mảnh vá xoay.

---

#### 2.3.4. Mô-đun sinh khuyết tật hữu cơ đa tỉ lệ DRAEM

Mô-đun `DRAEMSynthesizer` trong tệp `data_engine/synthesizers/draem_synthesizer.py` kết hợp giải thuật tạo hàm ngẫu nhiên gradient Perlin đa tần số [3] với cơ chế hòa trộn kênh phi tuyến tính (Beta Blending). Cải tiến độc quyền của dự án là khởi tạo lưới Perlin trên kích thước chuẩn lũy thừa 2 ($512 \times 512$) rồi co giãn song tuyến tính về kích thước thực tế, giúp hệ thống tương thích hoàn toàn với mọi kích thước ảnh công nghiệp không chuẩn (`bottle` $900 \times 900$, `tile` $840 \times 840$).

**1. Đầu vào (Inputs):**
- Đối tượng `Sample` ảnh gốc: $I \in \mathbb{R}^{H \times W \times 3}$.
- Ảnh nguồn kết cấu lai tạo: $T \in \mathbb{R}^{H \times W \times 3}$ (lấy từ ảnh sản phẩm lành khác trong cùng danh mục).
- Kích thước lưới chuẩn: $G_{std} = 512 \times 512\text{ pixels}$.
- Số quãng tám tần số: $K \in \{1, 2, 3\}$.
- Khoảng giá trị phân ngưỡng mặt nạ: $\tau_{perlin} \in [0.3, 0.6]$.
- Khoảng hệ số hòa trộn mờ: $\beta \in [0.2, 0.8]$.

**2. Đầu ra (Outputs):**
- Đối tượng `Sample` mang lỗi:
  + Ảnh khuyết tật loang màu $I_{dr} \in \mathbb{R}^{H \times W \times 3}$.
  + Mặt nạ nhị phân hình dạng hữu cơ $M_{dr} \in \{0, 255\}^{H \times W}$.
  + Nhãn `label = "draem_anomaly"`, cờ `is_anomaly = True`.

**3. Quá trình xử lý (Processing Flow):**
- *Bước 1 -- Khởi tạo lưới gradient chuẩn $512 \times 512$:* Tạo lưới các nút cách đều trên không gian $512 \times 512$. Tại mỗi đỉnh lưới, sinh ngẫu nhiên một vector gradient đơn vị 2D $\mathbf{g} = [\cos\phi, \sin\phi]^T$ với $\phi \sim \mathcal{U}(0, 2\pi)$.
- *Bước 2 -- Tạo trường vô hướng Perlin đa quãng tám:* Với mỗi điểm ảnh trên lưới chuẩn, tính tích vô hướng với 4 vector gradient ở 4 góc ô lưới. Áp dụng đa thức làm mượt bậc 5 (Fade function) để nội suy liên tục theo hai phương $x$ và $y$. Cộng dồn qua $K$ quãng tám tần số để tạo ma trận trường vô hướng $P_{512} \in [-1.0, 1.0]^{512 \times 512}$.
- *Bước 3 -- Co giãn song tuyến tính thích nghi (Bilinear Resizing):* Sử dụng hàm `cv2.resize(P_512, (W, H), interpolation=cv2.INTER_LINEAR)` để chuyển đổi trường vô hướng từ kích thước chuẩn $512 \times 512$ về đúng kích thước $(W, H)$ thực tế của ảnh gốc.
- *Bước 4 -- Ngưỡng hóa tạo mặt nạ nhị phân:* Chuẩn hóa trường vô hướng về đoạn $[0.0, 1.0]$. Tạo mặt nạ nhị phân $M_{dr}$ bằng toán tử logic $\mathbb{I}\{P_{W, H}(x, y) > \tau_{perlin}\} \times 255$ với ngưỡng ngẫu nhiên $\tau_{perlin} \sim \mathcal{U}(0.3, 0.6)$.
- *Bước 5 -- Hòa trộn điểm ảnh phi tuyến (Beta Blending):* Lấy ngẫu nhiên hệ số hòa trộn $\beta \sim \mathcal{U}(0.2, 0.8)$. Tại những vị trí mà mặt nạ $M_{dr} = 255$, thực hiện tính toán giá trị điểm ảnh mới bằng tổ hợp tuyến tính lồi giữa ảnh gốc $I$ và ảnh kết cấu phụ $T$.

**Công thức toán học:**

Hàm đa thức làm mượt bậc 5 (Perlin Fade Function):
$$s(t) = 6t^5 - 15t^4 + 10t^3 \quad \text{với } t \in [0, 1]$$
*Công thức 9 Hàm đa thức nội suy làm mượt bậc 5 Perlin*  
Trong đó:
- $t$ là khoảng cách tương đối từ tọa độ điểm khảo sát đến nút lưới góc trái/trên ($0 \le t \le 1$).
- Đa thức $s(t)$ triệt tiêu đạo hàm bậc 1 và bậc 2 tại hai đầu mút ($s'(0)=s'(1)=0, s''(0)=s''(1)=0$), bảo đảm trường vô hướng sinh ra liên tục và khả vi bậc 2 khắp không gian.

Toán tử nội suy song tuyến tính co giãn trường Perlin chuẩn về kích thước ảnh thực:
$$P_{W, H}(x, y) = (1 - \Delta x)(1 - \Delta y) P_0 + \Delta x (1 - \Delta y) P_1 + (1 - \Delta x)\Delta y P_2 + \Delta x \Delta y P_3$$
*Công thức 10 Nội suy song tuyến tính co giãn trường vô hướng Perlin*  
Trong đó:
- $(x, y)$ là tọa độ điểm ảnh thực ($0 \le x < W, 0 \le y < H$).
- $P_0, P_1, P_2, P_3$ là giá trị trường vô hướng tại 4 điểm lân cận gần nhất trên lưới chuẩn $512 \times 512$.
- $\Delta x, \Delta y \in [0, 1)$ là phần dư tọa độ chuẩn hóa tương ứng.

Công thức hòa trộn mờ điểm ảnh phi tuyến (Beta Blending):
$$I_{dr}(x, y) = \left( 1 - \beta \cdot \frac{M_{dr}(x, y)}{255} \right) \cdot I(x, y) + \left( \beta \cdot \frac{M_{dr}(x, y)}{255} \right) \cdot T(x, y)$$
*Công thức 11 Hòa trộn mờ điểm ảnh phi tuyến mô phỏng khuyết tật bề mặt DRAEM*  
Trong đó:
- $I(x, y)$ là vector cường độ sáng điểm ảnh gốc tại tọa độ $(x, y)$.
- $T(x, y)$ là vector cường độ sáng điểm ảnh nguồn kết cấu phụ.
- $M_{dr}(x, y) \in \{0, 255\}$ là giá trị mặt nạ nhị phân hữu cơ.
- $\beta \in [0.2, 0.8]$ là trọng số hòa trộn điều khiển độ đậm nhạt của vết ố khuyết tật.

---

#### 2.3.5. Mô-đun ghép khuyết tật liền mạch Poisson NSA

Mô-đun `NSASynthesizer` trong tệp `data_engine/synthesizers/nsa_synthesizer.py` ứng dụng giải tích vi phân phương trình Poisson [6] trong bài toán ghép ảnh liền mạch (Natural Synthetic Anomalies) [4]. Bằng cách giải bài toán biên Dirichlet trên trường vector gradient, khuyết tật cấy ghép tự động hấp thụ ánh sáng và màu sắc tổng thể của vùng nền đích, loại bỏ hoàn toàn các vết nứt cắt ghép giả tạo.

**1. Đầu vào (Inputs):**
- Đối tượng `Sample` ảnh đích sản phẩm lành: $I_d \in \mathbb{R}^{H \times W \times 3}$.
- Ảnh nguồn chứa khuyết tật: $I_s \in \mathbb{R}^{H \times W \times 3}$.
- Bán kính miếng ghép ngẫu nhiên: $r_x, r_y \in [15, 60]\text{ pixels}$.
- Tọa độ tâm ghép: $(c_x, c_y)$ thỏa mãn điều kiện nằm trên thân vật thể.

**2. Đầu ra (Outputs):**
- Đối tượng `Sample` hoàn thiện:
  + Ảnh ghép liền mạch tự nhiên $I_{nsa} \in \mathbb{R}^{H \times W \times 3}$.
  + Mặt nạ nhị phân khuyết tật đã giao với tiền cảnh: $M_{nsa} \in \{0, 255\}^{H \times W}$.
  + Nhãn `label = "nsa_anomaly"`, cờ `is_anomaly = True`.

**3. Quá trình xử lý (Processing Flow):**
- *Bước 1 -- Phân đoạn tiền cảnh tự động bằng ngưỡng Otsu:* Chuyển đổi ảnh đích $I_d$ sang không gian mức xám $Y(x, y)$. Áp dụng thuật toán phân ngưỡng tự động Otsu để tạo mặt nạ tiền cảnh $M_{fg}$, xác định chính xác ranh giới của thân vật thể (`bottle`, `screw`, `pill`) và cô lập hoàn toàn vùng nền đen.
- *Bước 2 -- Trích xuất vùng chọn khuyết tật nguồn:* Lấy mẫu ngẫu nhiên tâm cắt $(s_x, s_y)$ trên ảnh nguồn $I_s$. Tạo mặt nạ vùng chọn elip hoặc chữ nhật $M_s$ với bán kính ngẫu nhiên $r_x, r_y$.
- *Bước 3 -- Xác định tọa độ cấy ghép hợp lệ:* Lấy mẫu ngẫu nhiên tâm ghép đích $(c_x, c_y)$ sao cho toàn bộ diện tích miếng vá phải nằm trọn trong vùng tiền cảnh ($M_s \subset M_{fg}$).
- *Bước 4 -- Giải hệ phương trình Poisson ghép liền mạch:* Sử dụng hàm `cv2.seamlessClone(I_s, I_d, M_s, (c_x, c_y), cv2.NORMAL_CLONE)`. Thuật toán giải bài toán biên vi phân để tìm ma trận điểm ảnh $I_{nsa}$ có trường gradient khớp với ảnh nguồn $I_s$ và điều kiện biên khớp với ảnh đích $I_d$.
- *Bước 5 -- Cập nhật mặt nạ nhị phân ground-truth:* Gán mặt nạ khuyết tật cục bộ vào vị trí tâm đích và thực hiện phép giao logic với mặt nạ tiền cảnh: $M_{nsa} = M_{shifted} \cap M_{fg}$.

**Công thức toán học:**

Tiêu chí phân ngưỡng tối ưu tách tiền cảnh Otsu:
$$t^* = \arg\max_{0 \le t < 256} \left[ \omega_0(t) \cdot \omega_1(t) \cdot \Big( \mu_0(t) - \mu_1(t) \Big)^2 \right]$$
*Công thức 12 Tiêu chí phân ngưỡng tối ưu phương sai giữa các lớp Otsu*  
Trong đó:
- $t$ là ngưỡng mức xám khảo sát ($0 \le t \le 255$).
- $\omega_0(t), \omega_1(t)$ lần lượt là xác suất tích lũy của lớp nền và lớp tiền cảnh vật thể.
- $\mu_0(t), \mu_1(t)$ là giá trị mức xám trung bình của hai lớp tương ứng.

Phương trình đạo hàm riêng vi phân Poisson trong không gian 2D với điều kiện biên Dirichlet:
$$\Delta f(x, y) = \operatorname{div}\mathbf{v}(x, y) \quad \forall (x, y) \in \Omega, \quad \text{với } f(x, y)\Big|_{\partial\Omega} = I_d(x, y)\Big|_{\partial\Omega}$$
*Công thức 13 Phương trình đạo hàm riêng vi phân Poisson trong xử lý ảnh liền mạch*  
Trong đó:
- $\Omega$ là miền không gian đóng chứa khuyết tật cấy ghép, $\partial\Omega$ là đường biên của miền.
- $\Delta = \frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2}$ là toán tử Laplace 2 chiều.
- $\mathbf{v} = \nabla I_s = \left[ \frac{\partial I_s}{\partial x}, \frac{\partial I_s}{\partial y} \right]^T$ là trường vector gradient của ảnh nguồn.
- $\operatorname{div}\mathbf{v} = \frac{\partial^2 I_s}{\partial x^2} + \frac{\partial^2 I_s}{\partial y^2}$ là độ phân kỳ của trường gradient nguồn.
- $f(x, y)$ là hàm cường độ sáng cần tìm của ảnh kết quả $I_{nsa}$.

Hệ phương trình rời rạc hóa sai phân hữu hạn 5 điểm giải trên lưới điểm ảnh:
$$4 f(x, y) - f(x+1, y) - f(x-1, y) - f(x, y+1) - f(x, y-1) = 4 I_s(x, y) - I_s(x+1, y) - I_s(x-1, y) - I_s(x, y+1) - I_s(x, y-1)$$
*Công thức 14 Xấp xỉ sai phân hữu hạn bậc hai của toán tử Poisson trên lưới điểm ảnh*  
Trong đó $f(x, y)$ là giá trị điểm ảnh cần giải tại tọa độ $(x, y)$, và các điểm nằm trên biên $\partial\Omega$ nhận giá trị cố định từ ảnh đích $I_d$.

---

#### 2.3.6. Mô-đun trích xuất đường viền và chuẩn hóa đa giác YOLOv11-seg

Mô-đun `YOLOSegExporter` trong tệp `data_engine/exporters/yolo_seg_exporter.py` đóng vai trò là cầu nối định dạng vector, chuyển đổi các ma trận mặt nạ nhị phân điểm ảnh thành danh sách các tọa độ đa giác chuẩn hóa trong đoạn $[0.0, 1.0]$. Mô-đun tích hợp giải thuật xấp xỉ rút gọn đỉnh đa giác Ramer-Douglas-Peucker giúp giảm thiểu kích thước tệp nhãn văn bản và tăng tốc độ nạp dữ liệu huấn luyện mạng nơ-ron.

**1. Đầu vào (Inputs):**
- Mặt nạ nhị phân khuyết tật: $M \in \{0, 255\}^{H \times W}$, kiểu `np.uint8`.
- Kích thước không gian của ảnh: chiều rộng $W$, chiều cao $H$.
- Tỷ lệ sai số xấp xỉ đường bao: $\epsilon_{ratio} = 0.002$.
- Ngưỡng diện tích đường bao tối thiểu: $S_{min} = 10.0\text{ pixels}^2$.
- Mã lớp đối tượng: `class_id = 0` (lớp khuyết tật).

**2. Đầu ra (Outputs):**
- Tệp văn bản nhãn định dạng YOLO Segmentation: chuỗi các dòng văn bản, mỗi dòng biểu diễn một đa giác khuyết tật:
  $$\texttt{0 } x_1\text{ } y_1\text{ } x_2\text{ } y_2\text{ } \dots\text{ } x_n\text{ } y_n \quad \text{với } x_i, y_i \in [0.0, 1.0]$$

**3. Quá trình xử lý (Processing Flow):**
- *Bước 1 -- Dò tìm đường bao phân cấp:* Gọi hàm `cv2.findContours(M, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)` để tìm tập hợp các đường viền khép kín ngoài cùng bao quanh các vùng mang giá trị 255.
- *Bước 2 -- Lọc bỏ đa giác diện tích rác:* Duyệt qua từng đường viền $C_k$. Tính diện tích hình học bằng hàm `cv2.contourArea(C_k)`. Nếu diện tích $< S_{min} = 10.0\text{ px}^2$, đường viền bị loại bỏ nhằm triệt tiêu các đốm nhiễu ngẫu nhiên.
- *Bước 3 -- Rút gọn đỉnh bằng giải thuật Douglas-Peucker:* Tính chu vi đường bao $L_k = \texttt{cv2.arcLength}(C_k, \text{closed}=\text{True})$. Tính khoảng cách sai số tối đa $\epsilon = \epsilon_{ratio} \cdot L_k$. Gọi hàm \texttt{cv2.approxPolyDP(C_k, $\epsilon$, closed=True)} để thu được đa giác rút gọn $\mathcal{P}_k$.
- *Bước 4 -- Kiểm tra điều kiện hình học hợp lệ:* Kiểm tra số lượng đỉnh của đa giác $\mathcal{P}_k$. Bắt buộc số lượng đỉnh $n \ge 3$ để tạo thành một đa giác phẳng không suy biến.
- *Bước 5 -- Chuẩn hóa tọa độ đỉnh tỷ lệ $[0.0, 1.0]$:* Lần lượt chia tọa độ các đỉnh $(x_i, y_i)$ cho kích thước $(W, H)$, sử dụng hàm cắt ngưỡng `np.clip(..., 0.0, 1.0)` để bảo đảm toàn bộ tọa độ tuyệt đối không vượt khỏi khung hình chuẩn. Ghi vào tệp nhãn văn bản.

**Công thức toán học:**

Tiêu chí dừng khoảng cách vuông góc của giải thuật Ramer-Douglas-Peucker:
$$\max_{P_i \in \text{đường cong } AB} \operatorname{dist}(P_i, AB) \le \epsilon = 0.002 \cdot \oint_C ds$$
*Công thức 15 Tiêu chí rút gọn đỉnh đa giác Ramer-Douglas-Peucker*  
Trong đó:
- $AB$ là đoạn thẳng nối hai điểm mút đang xét của đường bao.
- $\operatorname{dist}(P_i, AB) = \frac{|(y_B - y_A)x_i - (x_B - x_A)y_i + x_B y_A - y_B x_A|}{\sqrt{(y_B - y_A)^2 + (x_B - x_A)^2}}$ là khoảng cách Euclid vuông góc từ điểm $P_i$ tới đoạn thẳng $AB$.
- $\oint_C ds$ là chu vi khép kín của đường bao hình học ban đầu.

Công thức chuẩn hóa tọa độ đỉnh đa giác:
$$x_{norm}^{(i)} = \operatorname{clip}\left( \frac{x_i}{W}, 0.0, 1.0 \right), \quad y_{norm}^{(i)} = \operatorname{clip}\left( \frac{y_i}{H}, 0.0, 1.0 \right)$$
*Công thức 16 Chuẩn hóa tọa độ đỉnh đa giác thực thể YOLO*  
Trong đó:
- $(x_i, y_i)$ là tọa độ điểm ảnh nguyên trên ma trận gốc ($0 \le x_i < W, 0 \le y_i < H$).
- $(x_{norm}^{(i)}, y_{norm}^{(i)})$ là tọa độ số thực chuẩn hóa thuộc đoạn $[0.0, 1.0]$.

---

#### 2.3.7. Mô-đun phân vùng thực thể học sâu YOLOv11-seg

Mô-đun phân vùng thực thể YOLOv11-seg được xây dựng dựa trên kiến trúc mạng nơ-ron tích chập đa tầng tiên tiến của thư viện `ultralytics`. Mô hình tích hợp các khối trích xuất đặc trưng C3k2, khối không gian đa tỉ lệ SPPF (Spatial Pyramid Pooling - Fast), và đầu phân vùng C2f-PSA (Position-Sensitive Attention), cho phép dự đoán đồng thời hộp bao đối tượng, phân lớp và hệ số mặt nạ thực thể mức điểm ảnh.

**1. Đầu vào (Inputs):**
- Tensor ảnh màu đã tiền xử lý: $\mathbf{X} \in \mathbb{R}^{B \times 3 \times 640 \times 640}$, chuẩn hóa giá trị điểm ảnh $[0.0, 1.0]$.
- Tensor nhãn đa giác ground-truth định dạng YOLO Segmentation.
- Siêu tham số huấn luyện: $\text{batch\_size} = 16$, $\text{epochs} = 50$, bộ tối ưu hóa AdamW với tốc độ học $\eta = 0.001$, trọng số suy giảm $\text{weight\_decay} = 0.0005$.

**2. Đầu ra (Outputs):**
- Danh sách các thực thể dự đoán: $\{(\hat{\mathcal{P}}_i, \hat{c}_i, \hat{\mathbf{b}}_i)\}_{i=1}^N$ gồm:
  + Tọa độ hộp bao bounding box $\hat{\mathbf{b}}_i = [\hat{x}, \hat{y}, \hat{w}, \hat{h}]$.
  + Điểm số độ tin cậy khuyết tật $\hat{c}_i \in [0.0, 1.0]$.
  + Mặt nạ nhị phân thực thể giải mã $\hat{\mathbf{m}}_i \in \{0, 1\}^{640 \times 640}$.

**3. Quá trình xử lý (Processing Flow):**
- *Bước 1 -- Trích xuất đặc trưng đa tầng qua Backbone C3k2:* Tensor ảnh đầu vào được truyền qua các tầng tích chập lặp C3k2 với cơ chế kết nối tắt (residual connections), tạo ra kim tự tháp đặc trưng 3 mức tỉ lệ $\{P_3, P_4, P_5\}$ tương ứng với các độ phân giải $\frac{1}{8}, \frac{1}{16}, \frac{1}{32}$ kích thước gốc.
- *Bước 2 -- Tăng cường trường tiếp nhận bằng SPPF và PSA:* Đặc trưng tầng sâu $P_5$ được dẫn qua khối SPPF tích chập dồn đa kích thước $(5 \times 5, 9 \times 9, 13 \times 13)$ và cơ chế chú ý theo vị trí PSA nhằm nắm bắt cấu trúc toàn cục của vật thể.
- *Bước 3 -- Dự đoán hệ số mặt nạ và mặt nạ nguyên mẫu (Prototypes):* Nhánh phân vùng (Segmentation Head) sinh ra một tập hợp gồm $K = 32$ mặt nạ nguyên mẫu cơ sở $\mathbf{M}_{proto} \in \mathbb{R}^{32 \times 160 \times 160}$. Đồng thời, tại mỗi vị trí dự đoán khuyết tật, mạng xuất ra một vector gồm 32 hệ số trọng số mặt nạ $\mathbf{w}_i \in \mathbb{R}^{32}$.
- *Bước 4 -- Tái tạo mặt nạ thực thể bằng tích vô hướng:* Ma trận mặt nạ của từng thực thể được tạo ra bằng phép nhân vô hướng giữa vector hệ số $\mathbf{w}_i$ và các mặt nạ nguyên mẫu, dẫn qua hàm kích hoạt Sigmoid:
  $$\hat{\mathbf{m}}_i = \sigma\Big( \mathbf{w}_i^T \cdot \mathbf{M}_{proto} \Big)$$
- *Bước 5 -- Tối ưu hóa đa hàm mất mát trong quá trình huấn luyện:* Tính toán tổng hợp hàm mất mát đa thành phần bao gồm: mất mát hộp bao Complete-IoU ($\mathcal{L}_{box}$), mất mát phân bố tiêu cự DFL ($\mathcal{L}_{dfl}$), mất mát phân lớp nhị phân ($\mathcal{L}_{cls}$), và mất mát phân vùng nhị phân cross-entropy ($\mathcal{L}_{mask}$).

**Công thức toán học:**

Hàm mất mát tổng hợp của mạng phân vùng thực thể YOLOv11-seg:
$$\mathcal{L}_{total} = \lambda_{box} \mathcal{L}_{box} + \lambda_{cls} \mathcal{L}_{cls} + \lambda_{dfl} \mathcal{L}_{dfl} + \lambda_{mask} \mathcal{L}_{mask}$$
*Công thức 17 Hàm mất mát tổng hợp mạng phân vùng thực thể YOLOv11-seg*  
Trong đó:
- $\lambda_{box} = 7.5, \lambda_{cls} = 0.5, \lambda_{dfl} = 1.5, \lambda_{mask} = 2.5$ là các trọng số cân bằng giữa các thành phần mất mát.
- $\mathcal{L}_{box}$ là hàm mất mát Complete-IoU (CIoU) tối ưu hóa độ trùng khớp hộp bao.
- $\mathcal{L}_{cls}$ là hàm mất mát phân lớp nhị phân (Binary Cross-Entropy).
- $\mathcal{L}_{dfl}$ là hàm mất mát phân bố tiêu cự (Distribution Focal Loss).

Hàm mất mát phân vùng nhị phân mức điểm ảnh (Pixel-level Mask Binary Cross-Entropy):
$$\mathcal{L}_{mask} = -\frac{1}{HW} \sum_{x=1}^W \sum_{y=1}^H \left[ M_{gt}(x, y) \log \sigma(\hat{m}(x, y)) + \Big(1 - M_{gt}(x, y)\Big) \log \Big(1 - \sigma(\hat{m}(x, y))\Big) \right]$$
*Công thức 18 Hàm mất mát phân vùng nhị phân mức điểm ảnh*  
Trong đó:
- $M_{gt}(x, y) \in \{0, 1\}$ là giá trị nhãn mặt nạ ground-truth tại tọa độ $(x, y)$.
- $\hat{m}(x, y) = \sum_{k=1}^{32} w_k \cdot M_{proto}^{(k)}(x, y)$ là giá trị logits tổ hợp tuyến tính từ 32 mặt nạ nguyên mẫu.
- $\sigma(z) = \frac{1}{1 + e^{-z}}$ là hàm kích hoạt Sigmoid đưa giá trị về xác suất $[0.0, 1.0]$.

---

#### 2.3.8. Mô-đun suy luận thời gian thực C++ TensorRT và giải mã tensor đầu ra

Mô-đun `TRTInferenceEngine` trong thư mục `cpp/trt_seg_inference/main.cpp` hiện thực hóa ứng dụng suy luận độc lập bằng C++17 kết hợp thư viện NVIDIA TensorRT. Mô-đun nạp trực tiếp tệp engine đã được tối ưu hóa lượng hóa FP16, thực thi tính toán trên GPU thông qua luồng CUDA Stream bất đồng bộ và bộ nhớ ghim (Pinned Memory), tự giải mã các tensor đầu ra thành mặt nạ nhị phân với độ trễ đo lường thực tế chỉ **$6.7\text{ ms}$** trên ảnh $1024 \times 1024$.

**1. Đầu vào (Inputs):**
- Tệp mô hình động cơ: `model.engine` (lượng hóa FP16 TensorRT).
- Ảnh kiểm tra thực tế: ma trận OpenCV `cv::Mat` kích thước $H \times W \times 3$, kiểu `CV_8UC3`.
- Ngưỡng lọc độ tin cậy: $\tau_{conf} = 0.25$.
- Ngưỡng triệt tiêu cực đại không cực đại (NMS IoU): $\tau_{nms} = 0.50$.

**2. Đầu ra (Outputs):**
- Cấu trúc kết quả `std::vector<Detection>` chứa:
  + Hộp bao `cv::Rect` trên hệ tọa độ ảnh gốc.
  + Điểm tin cậy `float confidence`.
  + Mặt nạ nhị phân `cv::Mat` kích thước gốc $(H, W)$, kiểu `CV_8UC1` với giá trị $\{0, 255\}$.
- Thời gian suy luận từng khung hình đo bằng đồng hồ nano-giây `std::chrono::high_resolution_clock`.

**3. Quá trình xử lý (Processing Flow):**
- *Bước 1 -- Tiền xử lý Letterbox và nạp bộ nhớ ghim:* Nhận ảnh từ camera, tính toán tỷ lệ co giãn $\text{scale} = \min(640.0/H, 640.0/W)$. Thực hiện chèn lề (Letterbox padding) về kích thước $640 \times 640$. Chuẩn hóa giá trị điểm ảnh chia cho 255.0f, chuyển đổi thứ tự kênh từ HWC (OpenCV) sang CHW (TensorRT). Nạp dữ liệu vào vùng nhớ ghim máy chủ `cudaHostAlloc` để tăng tốc độ truyền qua bus PCIe.
- *Bước 2 -- Sao chép bất đồng bộ và thực thi suy luận:* Đẩy dữ liệu từ Host sang Device bằng hàm `cudaMemcpyAsync`. Thực thi engine TensorRT thông qua phương thức `context->enqueueV3(stream)`.
- *Bước 3 -- Lọc ứng viên bằng Non-Maximum Suppression (NMS):* Đọc tensor đầu ra kích thước $[1, 32 + C_{num} + 4, 8400]$. Lọc toàn bộ các neo có điểm số tin cậy $\hat{c}_i < \tau_{conf} = 0.25$. Áp dụng thuật toán triệt tiêu cực đại không cực đại NMS với ngưỡng IoU $\tau_{nms} = 0.50$ để loại bỏ các hộp bao trùng lặp.
- *Bước 4 -- Tái tạo mặt nạ bằng phép nhân ma trận GEMM:* Với mỗi thực thể vượt qua NMS, trích xuất vector hệ số mặt nạ $\mathbf{w}_i \in \mathbb{R}^{1 \times 32}$. Thực hiện phép nhân ma trận với tensor nguyên mẫu $\mathbf{M}_{proto} \in \mathbb{R}^{32 \times (160 \cdot 160)}$ bằng thư viện BLAS/CUDA. Áp dụng hàm Sigmoid và phân ngưỡng nhị phân tại mức 0.5f.
- *Bước 5 -- Co giãn ngược và cắt bỏ viền Letterbox:* Co giãn mặt nạ nhị phân $160 \times 160$ về kích thước ảnh gốc $(W, H)$ bằng hàm `cv::resize(..., cv::INTER_LINEAR)`. Cắt bỏ các vùng đệm padding để mặt nạ nhị phân khít hoàn toàn với ranh giới vật thể.

**Công thức toán học:**

Toán tử giải mã mặt nạ nhị phân từ tensor nguyên mẫu và vector trọng số:
$$M_{raw}(x', y') = \mathbb{I}\left\{ \left( \frac{1}{1 + \exp\left( -\sum_{k=1}^{32} w_k \cdot M_{proto}^{(k)}(x', y') \right)} \right) \ge 0.5 \right\} \times 255$$
*Công thức 19 Giải mã ma trận mặt nạ nhị phân thực thể trong động cơ C++ TensorRT*  
Trong đó:
- $(x', y')$ là tọa độ điểm ảnh trên lưới nguyên mẫu $160 \times 160$.
- $w_k$ là hệ số trọng số thứ $k$ dự đoán bởi đầu phân vùng.
- $M_{proto}^{(k)}$ là mặt nạ nguyên mẫu thứ $k$.
- $\mathbb{I}\{\cdot\}$ là hàm chỉ thị nhị phân đưa giá trị về $\{0, 255\}$.

Công thức chuyển đổi tọa độ điểm ảnh ngược loại bỏ viền Letterbox:
$$x_{orig} = \frac{x_{pad} - \text{pad}_w}{\text{scale}}, \quad y_{orig} = \frac{y_{pad} - \text{pad}_h}{\text{scale}}$$
*Công thức 20 Chuyển đổi tọa độ không gian ngược loại bỏ phần đệm Letterbox*  
Trong đó:
- $(x_{pad}, y_{pad})$ là tọa độ trên ảnh đầu vào mô hình $640 \times 640$.
- $\text{scale} = \min\left(\frac{640}{H}, \frac{640}{W}\right)$ là tỷ lệ co giãn khung hình.
- $\text{pad}_w = \frac{640 - W \cdot \text{scale}}{2}, \text{pad}_h = \frac{640 - H \cdot \text{scale}}{2}$ là độ dày phần đệm viền đen.
- $(x_{orig}, y_{orig})$ là tọa độ điểm ảnh thực trên ảnh gốc.

---

#### 2.3.9. Mô-đun đánh giá phân vùng đa miền và benchmark suy thoái quang học

Mô-đun `DualDomainEvaluator` và `RobustnessEvaluator` trong thư mục `evaluation/` cung cấp hệ thống đo lường kép độc lập, đánh giá đồng thời chất lượng phân vùng đa giác thực thể (Instance Mask mAP) và bản đồ xác suất bất thường liên tục (Pixel-AUROC, Image-AUROC, FAR@0.25). Đồng thời, phân hệ tích hợp bộ chuẩn MVTec-AD-C nhằm đo lường khả năng chống chịu của mô hình trước 4 loại suy thoái quang học qua 5 mức nghiêm trọng.

**1. Đầu vào (Inputs):**
- Tập hợp các đa giác phân vùng dự đoán kèm độ tin cậy $\{(\hat{\mathcal{P}}_i, \hat{c}_i)\}_{i=1}^N$.
- Mặt nạ nhị phân ground-truth thực tế: $M_{gt} \in \{0, 255\}^{H \times W}$.
- Danh mục 4 loại suy thoái quang học: $\texttt{gaussian\_noise}, \texttt{gaussian\_blur}, \texttt{motion\_blur}, \texttt{defocus\_blur}$.
- 5 mức độ nghiêm trọng: $s \in \{1, 2, 3, 4, 5\}$.
- Ngưỡng phân lớp báo động giả: $\tau_{far} = 0.25$.

**2. Đầu ra (Outputs):**
- Chỉ số miền thực thể: Mask mAP@50, Mask mAP@50-95.
- Chỉ số miền xác suất liên tục: Pixel-AUROC, Image-AUROC, FAR@0.25.
- Ma trận sụt giảm hiệu năng tương đối $\Delta\text{mAP}(s)$ và chỉ số sai số suy thoái trung bình (Mean Corruption Error -- mCE).
- Tệp tổng hợp kết quả: `results/ablation_summary.csv`.

**3. Quá trình xử lý (Processing Flow):**
- *Bước 1 -- Tính toán Mask mAP miền thực thể:* So khớp các đa giác dự báo với mặt nạ ground-truth bằng chỉ số diện tích giao trên diện tích hợp (Mask IoU). Tính diện tích dưới đường cong Precision-Recall tại ngưỡng IoU 0.50 (Mask mAP@50) và trung bình trên 10 ngưỡng từ 0.50 đến 0.95 với bước nhảy 0.05 (Mask mAP@50-95).
- *Bước 2 -- Tái tạo bản đồ xác suất liên tục $P(y, x)$:* Khởi tạo ma trận xác suất toàn số 0: $P = \mathbf{0}_{H \times W}$. Với mỗi đa giác dự đoán $\hat{\mathcal{P}}_i$ có độ tin cậy $\hat{c}_i$, vẽ vùng đa giác lên ma trận và cập nhật giá trị bằng toán tử lấy cực đại điểm: $P(y, x) = \max\Big(P(y, x), \hat{c}_i \cdot \mathbb{I}\{(y, x) \in \hat{\mathcal{P}}_i\}\Big)$.
- *Bước 3 -- Tính toán Pixel-AUROC và Image-AUROC:* Trải phẳng ma trận xác suất $P$ và mặt nạ nhị phân $M_{gt}$ thành các vector 1 chiều. Sử dụng hàm `sklearn.metrics.roc_curve` và `auc` để tính toán diện tích dưới đường cong đặc tính hoạt động của bộ thu (AUROC) mức điểm ảnh và mức ảnh.
- *Bước 4 -- Đo lường tỷ lệ báo động giả FAR@0.25:* Lọc tập hợp các ảnh sản phẩm lành không có khuyết tật ($\mathcal{D}_{good}$). Đếm số lượng ảnh bị mô hình dự đoán có ít nhất một điểm ảnh vượt ngưỡng $\tau_{far} = 0.25$, chia cho tổng số ảnh lành để tính FAR@0.25.
- *Bước 5 -- Sát hạch suy thoái quang học MVTec-AD-C:* Lần lượt tích chập ảnh kiểm thử với các nhân mờ và cộng nhiễu Gauss ở 5 cấp độ nghiêm trọng, đo lường độ suy giảm $\Delta\text{mAP}$ và vẽ đường cong bền vững quang học.

**Công thức toán học:**

Bản đồ xác suất bất thường liên tục tái tạo từ các thực thể đa giác:
$$P(y, x) = \max_{i=1 \dots N} \Big( \hat{c}_i \cdot \mathbb{I}\{(y, x) \in \hat{\mathcal{P}}_i\} \Big)$$
*Công thức 21 Bản đồ xác suất bất thường liên tục mức điểm ảnh*  
Trong đó:
- $N$ là tổng số lượng thực thể đa giác dự đoán trên khung hình.
- $\hat{c}_i \in [0.0, 1.0]$ là điểm số độ tin cậy của thực thể thứ $i$.
- $\mathbb{I}\{(y, x) \in \hat{\mathcal{P}}_i\}$ là hàm chỉ thị nhận giá trị 1 nếu tọa độ $(y, x)$ nằm bên trong đa giác $\hat{\mathcal{P}}_i$, và nhận giá trị 0 nếu nằm ngoài.

Tỷ lệ diện tích giao trên diện tích hợp (Mask Intersection over Union -- IoU):
$$\operatorname{IoU}(\hat{M}_i, M_{gt}) = \frac{\sum_{x, y} \Big( \hat{M}_i(x, y) \cdot M_{gt}(x, y) \Big)}{\sum_{x, y} \Big( \hat{M}_i(x, y) + M_{gt}(x, y) - \hat{M}_i(x, y) \cdot M_{gt}(x, y) \Big)}$$
*Công thức 22 Tỷ số diện tích giao trên diện tích hợp của mặt nạ phân vùng*  
Trong đó:
- $\hat{M}_i(x, y) \in \{0, 1\}$ là mặt nạ nhị phân dự đoán của thực thể thứ $i$.
- $M_{gt}(x, y) \in \{0, 1\}$ là mặt nạ nhị phân ground-truth thực tế.

Chỉ số diện tích dưới đường cong ROC (AUROC) tính bằng tích phân hình thang:
$$\operatorname{AUROC} = \int_0^1 \operatorname{TPR}\Big( \operatorname{FPR}^{-1}(t) \Big) \, dt$$
*Công thức 23 Diện tích dưới đường cong đặc tính hoạt động bộ thu AUROC*  
Trong đó:
- $\operatorname{TPR} = \frac{\text{TP}}{\text{TP} + \text{FN}}$ là tỷ lệ dương tính thật (True Positive Rate).
- $\operatorname{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}}$ là tỷ lệ dương tính giả (False Positive Rate).

Tỷ lệ báo động giả trên tập mẫu sản phẩm lành (False Alarm Rate tại ngưỡng $\tau$):
$$\operatorname{FAR}@\tau = \frac{1}{|\mathcal{D}_{good}|} \sum_{I \in \mathcal{D}_{good}} \mathbb{I}\left( \max_{(x, y)} P_I(x, y) \ge \tau \right)$$
*Công thức 24 Tỷ lệ báo động giả trên tập sản phẩm lành*  
Trong đó:
- $\mathcal{D}_{good}$ là tập hợp các ảnh sản phẩm bình thường không mang khuyết tật.
- $P_I(x, y)$ là bản đồ xác suất bất thường dự đoán trên ảnh $I$.
- $\tau = 0.25$ là ngưỡng quyết định phân lớp báo động giả.

---

### 2.4. Quy trình thực hiện và tích hợp các mô-đun

Toàn bộ 9 mô-đun xử lý ảnh nêu trên được đóng gói và tích hợp thành một đường ống tự động hóa khép kín thông qua tệp điều khiển trung tâm `experiments/run_experiment.py`. Quy trình thực thi một kịch bản thực nghiệm được vận hành tuần tự theo các bước chuẩn mực:

1. **Nạp cấu hình thực nghiệm:** Đọc các siêu tham số từ tệp cấu hình YAML tương ứng trong thư mục `configs/ablation/` (xác định chế độ sinh khuyết tật, bộ lọc tần số kích hoạt, tỷ lệ mẫu âm tính `good_ratio = 0.15` và số epochs huấn luyện).
2. **Khởi tạo bộ nạp dữ liệu và kiểm soát hạt ngẫu nhiên:** Sử dụng `MVTecLoader` để tải các ảnh lành từ tập `train/good`, cố định hạt ngẫu nhiên (`seed = 42`) nhằm bảo đảm tính tái lập hoàn toàn của kết quả thực nghiệm.
3. **Tiền xử lý và làm giàu dữ liệu miền tần số:** Tùy theo kịch bản, kích hoạt mô-đun `FFTPeriodicSuppressionFilter` để triệt tiêu hoa văn nền tuần hoàn (đối với `grid`, `carpet`) hoặc mô-đun `DWTSubbandFilter` để tăng cường độ sắc nét của biên cạnh vi mô (đối với `tile`, `screw`).
4. **Cấy ghép khuyết tật tổng hợp tự thân:** Áp dụng `CutPasteSynthesizer`, `DRAEMSynthesizer` hoặc `NSASynthesizer` trực tiếp lên ảnh lành để sinh ra tập ảnh bất thường kèm mặt nạ nhị phân ground-truth $M_{gt} \in \{0, 255\}^{H \times W}$. Duy trì nghiêm ngặt $15\%$ số mẫu ảnh lành không cấy ghép để hình thành tập mẫu âm tính.
5. **Trích xuất và xuất nhãn đa giác vector:** Sử dụng `YOLOSegExporter` để tự động chuyển hóa mặt nạ nhị phân thành các vector tọa độ đa giác chuẩn hóa trong đoạn $[0.0, 1.0]$, lưu trữ dưới cấu trúc thư mục phân vùng chuẩn của mạng YOLOv11-seg.
6. **Huấn luyện mô hình phân vùng thực thể:** Kích hoạt quá trình tối ưu hóa trọng số mô hình YOLOv11n-seg trên bộ tăng tốc GPU NVIDIA A100 qua 50 epochs với hàm mất mát kết hợp $\mathcal{L}_{total}$.
7. **Đánh giá đa miền và kiểm thử độ bền quang học:** Sau khi huấn luyện, kích hoạt đồng thời `DualDomainEvaluator` và `RobustnessEvaluator` để đo lường các chỉ số phân vùng thực thể (Mask mAP@50, Mask mAP@50-95), chỉ số phát hiện bất thường liên tục (Pixel-AUROC, Image-AUROC, FAR@0.25) trên tập kiểm thử nguyên bản và tập kiểm thử suy thoái quang học MVTec-AD-C.
8. **Tổng hợp dữ liệu kết quả:** Ghi nhận và xuất toàn bộ số liệu đo lường vào tệp nhật ký `results/ablation_summary.md` và bảng ma trận `results/ablation_summary.csv`.

---

### 2.5. Kết luận chương II

Chương II đã hoàn thành việc trình bày toàn diện và chi tiết giải pháp kỹ thuật đề xuất cho bài toán phân vùng khuyết tật bề mặt sản phẩm công nghiệp. Báo cáo đã làm rõ kiến trúc lai đa tầng gồm 6 phân hệ lớn và 11 mô-đun chức năng ánh xạ trực tiếp từ mã nguồn thực tế. Các phương thức biểu diễn dữ liệu hình ảnh (không gian màu RGB, Grayscale ITU-R BT.601, miền tần số phức), quy cách chuẩn hóa đa giác YOLO $[0.0, 1.0]$, và cấu trúc thực thể `Sample` đã được chuẩn hóa chặt chẽ.

Điểm nhấn kỹ thuật cốt lõi của chương là việc trình bày đầy đủ 9 mô-đun xử lý ảnh theo khuôn mẫu 5 phần khoa học: từ bộ lọc triệt tiêu đỉnh phổ tuần hoàn 2D-FFT, biến đổi sóng con 2D-DWT tăng cường biên cạnh, 3 thuật toán sinh mẫu khuyết tật tổng hợp (CutPaste, DRAEM lưới chuẩn $512 \times 512$, NSA Poisson), bộ trích xuất nhãn đa giác Douglas-Peucker, mô hình phân vùng thực thể YOLOv11-seg, ứng dụng suy luận thời gian thực C++ TensorRT ($6.7\text{ ms}$), cho đến hệ thống đánh giá kép đa miền và benchmark suy thoái quang học MVTec-AD-C. Hệ thống 24 công thức toán học dẫn xuất chính xác đã minh chứng cho cơ sở khoa học vững chắc của phương pháp đề xuất.

Toàn bộ các giải pháp lý thuyết và thuật toán đã được thiết kế trong Chương II tạo tiền đề trực tiếp để chuyển mạch sang **CHƯƠNG III: THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ**, nơi toàn bộ hệ thống sẽ được kiểm chứng thực tế qua 28 tệp ảnh montage trực quan, kiểm thử bảo toàn số học miền tần số (MAE, PSNR, SSIM), và đánh giá ma trận thực nghiệm 12 kịch bản trên Google Colab GPU NVIDIA A100.
