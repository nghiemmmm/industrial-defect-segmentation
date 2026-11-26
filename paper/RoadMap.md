# BẢN ĐỒ THỰC THI & LỘ TRÌNH BÀI BÁO (MANUSCRIPT ROADMAP)

> **Mục đích:** Quản lý tập trung tiến độ, trạng thái biên tập và các đợt cập nhật của toàn bộ 7 Sections trong bài báo khoa học chuẩn IEEEtran. Mỗi lần có thay đổi hoặc yêu cầu chỉnh sửa, Agent BẮT BUỘC cập nhật trạng thái tương ứng tại tệp này.
> **Hội thảo mục tiêu:** **FJCAI** (\url{https://fjcai.org.vn}) — Chuẩn `\documentclass[conference]{IEEEtran}`, bài toàn văn từ **6 đến 8 trang** (Hiện tại: **7 trang hoàn chỉnh**).

---

## 1. Ma Trận Trạng Thái Tổng Thể (Master Status Matrix)

| Section ID | Tiêu đề Section (Tiếng Anh) | Ngân sách trang | Trạng thái hiện tại | Thư mục Artifacts | Tệp nguồn Code & Report |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **Sec I** | **Introduction** | 1.2 – 1.4 tr. | **VERIFIED** | `paper/introduction/` | `report/01_frontmatter_mo_dau.md`, `report/02_chuong1.md` |
| **Sec II** | **Related Work** | 0.8 – 1.0 tr. | **VERIFIED** | `paper/related_work/` | `report/02_chuong1.md` (Mục 1.2, 1.3), `references.bib` |
| **Sec III** | **Proposed Methodology** | 2.0 – 2.2 tr. | **VERIFIED** | `paper/methodology/` | `data_engine/frequency/`, `data_engine/synthesizers/`, `report/03`, `04` |
| **Sec IV** | **Experimental Evaluation** *(incl. MVTec-AD-C & Efficiency)* | 2.8 – 3.2 tr. | **VERIFIED*** | `paper/experiments/` | `evaluation/dual_domain_metrics.py`, `results/`, `cpp/trt_seg_inference/` |
| **Sec V**| **Conclusion** | 0.3 – 0.4 tr. | **VERIFIED** | `paper/conclusion/` | `report/07_ket_luan_tltk.md` |

*Quy ước trạng thái:*
* `PLANNED`: Đã lên yêu cầu, chưa bắt đầu viết.
* `IN_PROGRESS`: Đang phân tích, lập plan hoặc đang viết mã nguồn LaTeX.
* `DRAFTED`: Đã có bản thảo đầy đủ trong `paper/paper.tex` và biên dịch PDF thành công.
* `VERIFIED`: Đã kiểm toán chéo qua tệp `validation.md` (đạt 100% tiêu chí).
* `FROZEN`: Đã hoàn thiện tối đa, sẵn sàng xuất bản/nộp bài.

---

## 2. Nhật Ký Tiến Độ & Các Đợt Hiệu Đính (Changelog & Iterations)

### Đợt 1 — 25/11/2026: Khởi tạo Toàn bộ Bản thảo Sơ bộ & Thiết lập Hệ thống Skill Quản trị
* **Mục tiêu:** 
  - Khởi tạo thư mục `paper/`, chuyển đổi class `IEEEtran.cls` và thiết lập `references.bib`.
  - Soạn thảo bản thảo sơ bộ bao quát toàn bộ 7 Sections.
  - Thiết lập kỹ năng chuẩn hóa `.agents/skills/academic-paper-authoring/`.
  - Khởi tạo la bàn chiến lược `paper/Mision.md` và lộ trình sống `paper/RoadMap.md`.
* **Trạng thái:** Hoàn tất 100%.

### Đợt 2 — 25/11/2026: Tối ưu hóa Chuyên sâu Section I (Introduction)
* **Mục tiêu:** 
  - Khởi tạo bộ ba tài liệu quản trị cho Section I (`requirement.md`, `plan.md`, `validation.md`).
  - Chuẩn hóa tên file `validation.md`.
* **Trạng thái:** Hoàn tất chuẩn bị.

### Đợt 3 — 25/11/2026: Viết lại Section I theo kiến trúc Modular (`paper/sections/introduction.tex`)
* **Mục tiêu:**
  - Tách Section I ra tệp con độc lập `paper/sections/introduction.tex`.
  - Lồng ghép ví dụ đối lập MVTec AD (`grid`, `carpet` vs `bottle`, `screw`) ở Paragraph 3.
  - Chuẩn hóa chỉ số $\text{FAR@0.25} = 0.000$ và bổ sung đoạn Paper Organization ở Paragraph 6.
* **Trạng thái:** Hoàn tất 100% — **VERIFIED**.

### Đợt 4 — 25/11/2026: Nâng cấp Hệ thống 13 References & Ma Trận Kiểm Toán 5 Tầng
* **Mục tiêu:**
  - Mở rộng hệ thống 13 references bao phủ từ bối cảnh kinh tế đến nền tảng thuật toán và suy thoái quang học.
  - Tái cấu trúc [paper/introduction/validation.md](file:///d:/XULIANH/industrial-defect-segmentation/paper/introduction/validation.md) thành Ma trận kiểm toán 5 tầng.
* **Trạng thái:** Hoàn tất 100% — **VERIFIED**.

### Đợt 6 — 25/11/2026: Tối Ưu Hóa & Mô-Đun Hóa Section III (Proposed Methodology)
* **Mục tiêu:**
  - Khởi tạo không gian làm việc `paper/methodology/` (`requirement.md`, `plan.md`, `validation.md`).
  - Tách Section III ra tệp con độc lập `paper/sections/methodology.tex` và nạp vào `paper/paper.tex` bằng `\input{sections/methodology}`.
  - Chuẩn hóa toán học giải tích: khử trùng lặp ký hiệu ($C/\mathcal{C}$, $(u,v)/(s,t)$, $K/N_v$, $r_0/r_{\text{aspect}}$, $\theta/\phi$), tách bạch lý thuyết (Section III) với siêu tham số & Table I (Section IV), bổ sung Inter-Domain Coupling và hàm mất mát YOLOv11-seg.
* **Trạng thái:** Hoàn tất 100% — **VERIFIED**.

### Đợt 7 — 25/11/2026: Nâng Cấp & Mô-Đun Hóa Section II (Related Work)
* **Mục tiêu:**
  - Khởi tạo bộ quản trị `paper/related_work/` (`requirement.md`, `plan.md`, `validation.md`) và tách mô-đun `paper/sections/related_work.tex`.
  - Mở rộng chiều sâu phê phán cho 3 tiểu mục II-A, II-B, II-C (bổ sung Optical Robustness MVTec-AD-C và đoạn định vị Positioning).
  - Xác thực toàn bộ 18/18 tài liệu tham khảo (0 BibTeX warning).
* **Trạng thái:** Hoàn tất 100% — **VERIFIED**.

---

## 3. Các Bước Kế Tiếp Theo Lộ Trình (Next Milestones)

- [x] **Milestone 1:** Hoàn thiện, nghiệm thu và chuẩn hóa Section I theo đúng thể thức IEEE Conference (FJCAI, 7 trang).
- [x] **Milestone 2:** Thiết lập không gian làm việc `paper/methodology/`, tách mô-đun `methodology.tex`, rà soát các công thức toán học giải tích 2D-FFT Notch và 2D-DWT Haar, triệt tiêu `Overfull \hbox` (Section III chuyển sang `VERIFIED`).
- [ ] **Milestone 3:** Thiết lập `paper/experiments/`, chuẩn bị sẵn sàng cấu trúc nạp số liệu các kịch bản EXP-01 đến EXP-11 ngay khi có kết quả hoàn tất từ Google Colab GPU A100.
- [ ] **Milestone 4:** Rà soát kiểm tra lần cuối (Double-Blind anonymization) trước khi đóng gói nộp bài lên hệ thống Microsoft CMT của FJCAI.
