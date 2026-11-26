# SECTION I: INTRODUCTION — KẾ HOẠCH TRIỂN KHAI & ÁNH XẠ MÃ NGUỒN (SYNCED)

> **Mục tiêu:** Duy trì Section I (`paper/sections/introduction.tex`) tập trung 100% vào 3 trụ cột Xử lý ảnh (Tần số–Không gian, Sinh lỗi kích thước tùy ý, Zero-Leakage FAR & Độ bền quang học), đồng bộ số liệu `2,676 RGB images` (6 lớp MVTec AD) và bố cục **5 Sections** chuẩn IEEE Conference (FJCAI).

## Bảng Ánh Xạ Kỹ Thuật (Code & Report Mapping)

| Luận điểm trong Introduction | Nguồn tham chiếu trong Code | Dẫn chứng kiểm chứng |
| :--- | :--- | :--- |
| **Triệt tiêu vân nền tuần hoàn (`grid`, `carpet`)** | `data_engine/frequency/fft_filter.py` | 2D-FFT Notch trên kênh độ sáng YCrCb; roundtrip $\text{PSNR}=51.31\text{ dB}, \text{SSIM}=0.9983$. |
| **Vật thể khối (`bottle`, `screw`) & kẹp tiền cảnh** | `data_engine/synthesizers/nsa_synthesizer.py` | Poisson seamless cloning + Otsu foreground clamping. |
| **Lỗi kích thước lẻ của Perlin noise** | `data_engine/synthesizers/draem_synthesizer.py` | Lưới chuẩn $512\times 512$ + nội suy song tuyến cho `bottle` $900\times 900$, `tile` $840\times 840$. |
| **Ràng buộc triệt tiêu báo động giả ($\rho_{\text{neg}} = 0.15$)** | `data_engine/loaders/mvtec_loader.py` | Đối chứng thực nghiệm FAR baseline ($4.50\%$–$8.78\%$) trên 467 ảnh lành. |
| **Độ bền suy thoái quang học (MVTec-AD-C)** | `data_engine/corruptions/corruptions_engine.py` | 4 loại nhiễu × 5 mức độ + Haar 2D-DWT detail boosting ($\alpha=0.6, \gamma=1.4$). |
| **Kiểm chứng phụ trợ tốc độ suy luận** | `cpp/trt_seg_inference/` | $6.7\text{ ms}$ ($\approx 149.2\text{ FPS}$) trên $1024\times 1024$ (Section IV-I). |
