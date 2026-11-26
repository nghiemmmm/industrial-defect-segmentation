# SECTION IV: EXPERIMENTAL EVALUATION — YÊU CẦU THIẾT KẾ & ĐỐI CHIẾU DỮ LIỆU (REQUIREMENTS)

> **Mục đích:** Định nghĩa cấu trúc thực nghiệm minh bạch 100% (Zero Hallucination) cho Section IV (`paper/sections/experiments.tex`), tách bạch rõ ràng số liệu thật đã kiểm chứng với khung bảng chờ nạp kết quả Colab A100 (`EXP-00..11`).

## 1. Cấu Trúc 5 Tiểu Mục (IV-A đến IV-E)
* **IV-A. Dataset, Benchmark Setup, and Implementation Details:**
  - Thống kê 6 danh mục trọng tâm MVTec AD (2,857 ảnh: `grid`, `carpet`, `tile`, `screw`, `pill`, `bottle`) kèm độ phân giải thực tế ($800\times 800$ đến $1024\times 1024$).
  - Môi trường phần mềm/phần cứng (Python 3.11, PyTorch 2.4, OpenCV 4.10, PyWavelets 1.8.0, Ultralytics YOLOv11-seg, NVIDIA A100-SXM4 40 GB, AdamW, batch 16, 50 epochs, seed 42).
  - Bảng siêu tham số đầy đủ chuyển từ Section III ($\tau_{\text{peak}}=3.5, r_{\text{inner}}=15, r_0=5.0, \alpha=0.6, \gamma=1.4, S_0=512, L=5, \tau_{\text{perlin}}=0.5, \rho_{\text{neg}}=0.15, \eta=0.002$).
* **IV-B. Dual-Domain Evaluation Metrics:**
  - Mask mAP@50, mAP@50-95; Pixel-AUROC, Image-AUROC; công thức $\text{FAR}@\tau$.
* **IV-C. Frequency Roundtrip Numerical Integrity Verification:**
  - Table I (`tab:reconstruction_metrics`) đo thật trên 2,857 ảnh (2D-FFT: PSNR $51.31\text{ dB}$, SSIM $0.9983$, MAE $0.4807$; 2D-DWT: exact identity).
* **IV-D. Per-Category Segmentation Benchmark and Ablation Matrix:**
  - **Table II (`tab:per_category_real`):** Số liệu thật từ `results/metrics/extra_eval/per_category_ap.csv` & `false_alarms_summary.csv` (`yolo11l-seg@640` vs `yolo11x-seg@1024`, 6-Cat mean, All-15 mean, FAR trên 467 ảnh lành).
  - **Table III (`tab:ablation_results`):** Ma trận 12 kịch bản (`EXP-00`–`EXP-11`) ghi chú minh bạch `dry_run=true` cho `EXP-00` và chờ nạp số liệu thật cho `EXP-01..11`.
* **IV-E. Qualitative Visual Analysis:**
  - Phân tích trực quan `Fig. 2` (`bottle_cutpaste_normal_comparison.png`) và `Fig. 3` (`grid_fft_montage.png`).
