# SECTION III: PROPOSED METHODOLOGY — TIÊU CHÍ NGHIỆM THU & KIỂM TOÁN CHÉO (VALIDATION)

> **Mục đích:** Bộ câu hỏi kiểm toán chất lượng độc lập dành cho Section III. Chỉ khi toàn bộ 100% các tiêu chí dưới đây đạt yêu cầu (tất cả các ô được đánh dấu `[x]`), Section III mới được chuyển sang trạng thái `VERIFIED` trong `paper/RoadMap.md`.

---

## 1. Kiểm Toán Gắn Kết Toán Học & Mã Nguồn (Mathematical & Code Grounding Audit)

- [x] **Không có số liệu bịa đặt (Zero Hallucination):** Toàn bộ tham số giải thuật ($\tau_{\text{peak}} = 3.5$, $r_0 = 5.0$, $r_{\text{inner}} = 15$, $\alpha = 0.6$, $\gamma = 1.4$, $\rho_{\text{neg}} = 0.15$, $\epsilon = 0.002$, $\tau_{\text{perlin}} = 0.5$) khớp $100\%$ với mã nguồn `data_engine/` và báo cáo `report/03`, `04`.
- [x] **Tính chính xác của công thức 2D-FFT Notch:** Phương trình biến đổi Fourier 2D độc lập trên từng kênh màu $c \in \{1, \dots, C\}$, ngưỡng tìm đỉnh phổ $\mathcal{S}_{\text{peaks}}$, và hàm truyền lọc chắn dải Gaussian đa điểm $H_{\text{notch}}(u, v)$ có tọa độ đối xứng qua tâm DC $D_{-k}(u, v)$ được biểu diễn chính xác về mặt giải tích.
- [x] **Tính chính xác của công thức 2D-DWT Haar:** Phân rã 4 dải tần và công thức điều biến năng lượng dải xấp xỉ $\tilde{I}_{LL} = \alpha \cdot I_{LL}$ và các dải con chi tiết độc lập $\tilde{I}_\theta = \gamma \cdot I_\theta$ ($\forall \theta \in \{LH, HL, HH\}$) khớp 100% với hàm gọi `pywt.idwt2`.
- [x] **Bảo chứng thực nghiệm bảo toàn hình học (Table I):** Bảng số liệu phản ánh trung thực kết quả nghiệm thu $\text{PSNR} = 51.31\text{ dB}$, $\text{SSIM} = 0.9983$, chứng minh không gây xê dịch tọa độ mask.
- [x] **Giải pháp lưới chuẩn Perlin 512:** Diễn giải rõ cơ chế tránh lỗi broadcast crash của NumPy trên ảnh kích thước tùy ý bằng phép nội suy song tuyến tính từ lưới chuẩn $512 \times 512$ với tọa độ không gian $(s, t)$.
- [x] **Phương trình đạo hàm riêng Poisson:** Định nghĩa đúng toán tử Laplacian $\Delta$ và điều kiện biên Dirichlet trong thuật toán NSA kết hợp kẹp tiền cảnh tự động (foreground Otsu clamping).
- [x] **Cân bằng mẫu âm invariant:** Trình bày rõ cấu trúc batch $\mathcal{D}_{\text{batch}}$ đảm bảo tỷ lệ $\rho_{\text{neg}} = 0.15$ và cam kết Zero Data Leakage.
- [x] **Đa giác hóa Suzuki-Abe & RDP:** Định nghĩa chính xác thuật toán dò biên và công thức rút gọn đỉnh theo chu vi $\epsilon = 0.002 \cdot \oint_{\mathcal{C}} ds$.

---

## 2. Kiểm Toán Tính Nhất Quán & Triệt Tiêu Trùng Lặp Ký Hiệu (Zero Symbol Collisions)

- [x] **Phân biệt kênh màu và đường viền:** $C=3$ là số kênh màu RGB; $\mathcal{C}$ là tập đỉnh đường viền đa giác.
- [x] **Phân biệt tọa độ tần số và không gian:** $(u, v)$ là tọa độ tần số Fourier; $(s, t)$ là tọa độ lưới chuẩn Perlin.
- [x] **Phân biệt số đỉnh phổ và số đỉnh đa giác:** $K$ là số cặp đỉnh phổ Fourier; $N_v$ là số đỉnh đa giác $\mathcal{C}$.
- [x] **Phân biệt bán kính và tỷ lệ khung hình:** $r_0, r_{\text{inner}}$ là bán kính bộ lọc; $r_{\text{aspect}}$ là tỷ lệ khung hình mảng cắt.
- [x] **Thống nhất không gian mặt nạ:** $M \in \{0, 1\}^{H \times W}$ thống nhất toàn bài.

---

## 3. Kiểm Toán Định Dạng IEEEtran & Trích Dẫn (Formatting & Compilation Audit)

- [x] **Kiến trúc Modular:** Tách độc lập tại `paper/sections/methodology.tex` và nạp vào `paper/paper.tex` bằng `\input{sections/methodology}`.
- [x] **Bố cục 2 cột vừa vặn:** Hoàn toàn triệt tiêu cảnh báo tràn lề (`Overfull \hbox`) trong các công thức toán học và bảng Table I.
- [x] **Trích dẫn BibTeX đầy đủ:** Đã bổ sung đầy đủ trích dẫn nền tảng (`gonzalez2018digital`, `mallat2008wavelet`, `perlin1985image`, `li2021cutpaste`, `zavrtanik2021draem`, `perez2003poisson`, `suzuki1985topological`, `douglas1973algorithms`), 0 cảnh báo `undefined citation`.
- [x] **Biên dịch sạch:** Mã thoát biên dịch `pdflatex` + `bibtex` đạt 0 (Success).

---

## 4. Kết Luận Nghiệm Thu (Audit Verdict)
* **Trạng thái phê duyệt:** `APPROVED (VERIFIED)`
* **Thời điểm nghiệm thu:** 25/11/2026 (Chuẩn hóa ký hiệu & công thức toán học)
* **Kết quả biên dịch:** `pdflatex` + `bibtex` thành công 100%, 0 lỗi, toàn bộ bài báo đạt 7 trang chuẩn FJCAI.
