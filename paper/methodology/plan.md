# SECTION III: PROPOSED METHODOLOGY — KẾ HOẠCH TRIỂN KHAI (RE-PLANNED)

> **Mục tiêu:** Xây dựng Section III (`paper/sections/methodology.tex`) thuần lý thuyết & toán học giải tích chuẩn IEEE Conference, gắn kết chặt chẽ 100% với tiêu đề bài báo (*Frequency-Spatial Anomaly Synthesis for False-Alarm-Suppressed Industrial Surface Defect Segmentation*) và la bàn chiến lược `paper/Mision.md`.

---

## 1. Kiến Trúc 5 Tiểu Mục Chuẩn Hóa

1. **III-A. Problem Formulation and Zero-Data-Leakage Constraint:**
   - Phát biểu toán học $\mathcal{D}_{\text{train}}$, $\mathcal{D}_{\text{test}}$ và cam kết Zero Data Leakage.
   - **Inter-Domain Coupling:** Công thức ghép nối $\tilde{I}_{\text{syn}} = \mathcal{T}_{\text{freq}}(I_{\text{syn}})$ kết hợp tính nhất quán miền phổ tại pha suy luận $\tilde{I}_{\text{test}} = \mathcal{T}_{\text{freq}}(I_{\text{test}})$.
2. **III-B. Frequency-Domain Preprocessing:**
   - Bỏ nhãn nội bộ `(Group B)`.
   - 2D-FFT Periodic Notch Filter tổng quát (độc lập theo kênh màu $c \in \{1, \dots, C\}$, không chèn con số thực nghiệm chưa kiểm chứng).
   - 2D-DWT Haar Sub-Band Modulation tổng quát ($0 < \alpha < 1 < \gamma$).
   - **Coordinate-Preserving Spatial Invariance:** Lý thuyết bảo toàn tọa độ, dẫn chiếu kiểm chứng định lượng (Table I) sang Section IV-C.
3. **III-C. Spatial Anomaly Synthesis:**
   - Bỏ nhãn nội bộ `(Group A)`.
   - Rigid & Scar CutPaste (góc xoay $\phi$, tỷ lệ $r_{\text{aspect}}$).
   - DRAEM Multi-Octave Perlin Noise trên lưới chuẩn $S_0 \times S_0$ ($L$ octaves, tọa độ không gian $(s, t)$).
   - Poisson Seamless Cloning (NSA) + Otsu Foreground Clamping.
4. **III-D. False-Alarm Suppression via Negative Invariant:**
   - Tỷ lệ mẫu âm $\rho_{\text{neg}} \in (0, 1)$ kết hợp nhãn polygon rỗng.
5. **III-E. Polygonal Vectorization and Segmentation Optimization:**
   - Suzuki-Abe + Ramer-Douglas-Peucker ($\epsilon = \eta \cdot \oint_{\mathcal{C}} ds$).
   - Khép kín hàm mục tiêu huấn luyện đa nhiệm YOLOv11-seg ($\mathcal{L} = \mathcal{L}_{\text{box}} + \mathcal{L}_{\text{cls}} + \mathcal{L}_{\text{mask}}$), giải thích cơ chế phạt báo động giả của $\mathcal{L}_{\text{cls}}$ trên $\mathcal{D}_{\text{clean}}$.

---

## 2. Nguyên Tắc Tách Bạch Lý Thuyết – Thực Nghiệm
- **Section III:** Chỉ giữ ký hiệu toán học tổng quát, điều kiện biên và tính chất lý thuyết.
- **Section IV-A:** Quy tụ toàn bộ giá trị siêu tham số cụ thể (*Implementation Details*).
- **Section IV-C:** Tiếp nhận **Table I** và số liệu kiểm chứng roundtrip trên 2,857 ảnh MVTec AD.
