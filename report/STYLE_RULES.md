# QUY CHUẨN TRÌNH BÀY BÁO CÁO CUỐI KỲ HỌC PHẦN XỬ LÝ ẢNH
**Học phần:** Xử lý ảnh (Image Processing) - Mã HP: `INT14123_CLC`  
**Cấp độ đào tạo:** Đại học (Chương trình Chất lượng cao)  
**Trình biên dịch mục tiêu:** MiKTeX (Phiên bản 25.12) / pdfLaTeX / XeLaTeX tại `C:\Users\ASUS\AppData\Local\Programs\MiKTeX\miktex\bin\x64\`  
**Tài liệu áp dụng:** Báo cáo học phần cuối kỳ môn Xử lý ảnh  

---

## 1. VĂN PHONG VÀ TÍNH CHẤT HỌC THUẬT

### 1.1. Định vị văn phong
- **Tính chất:** Sử dụng tiếng Việt học thuật, chuẩn mực, khách quan, súc tích và logic. Phù hợp với chuẩn mực của một bài báo cáo cuối kỳ môn học ở bậc đại học.
- **Trọng tâm nội dung:** Tập trung làm rõ bản chất toán học, nguyên lý xử lý tín hiệu/ảnh 2 chiều, luồng xử lý dữ liệu ma trận điểm ảnh, và phân tích thực nghiệm so sánh.
- **Tuyệt đối tránh:**
  - Không sử dụng văn phong quảng cáo, tiếp thị, giật gân ("đột phá", "vượt trội hoàn toàn", "công nghệ tiên tiến nhất thế giới").
  - Không tuyên bố quá mức về mặt đóng góp nghiên cứu (đây là báo cáo học phần, không phải luận án tiến sĩ hay bài báo khoa học đỉnh cao độc lập).
  - Không sử dụng đại từ nhân xưng cảm tính ("tôi", "chúng em", "nhóm mình") trong phần thân bài kỹ thuật. Sử dụng đại từ khách quan ("nghiên cứu này", "báo cáo này", "quy trình đề xuất", "nhóm thực hiện").

### 1.2. Phân định rõ ràng các tầng nội dung
Báo cáo phải phân tách minh bạch giữa 4 thành phần:
1. **Kiến thức lý thuyết nền tảng:** Các định lý toán học, phép biến đổi tích phân Fourier 2 chiều, biến đổi Wavelet, phương trình vi phân Poisson, lý thuyết xác suất thống kê.
2. **Phương pháp đề xuất / triển khai:** Kiến trúc mô hình, pipeline xử lý cụ thể được thiết kế cho bài toán phát hiện khuyết tật bề mặt công nghiệp.
3. **Chi tiết cài đặt thực tế:** Các lớp mã nguồn Python, thư viện OpenCV, NumPy, PyWavelets, cấu hình siêu tham số thực tế trong dự án.
4. **Kết quả thực nghiệm:** Dữ liệu số đo, biểu đồ, ảnh montage thực tế thu được từ quá trình kiểm chứng trên tập dữ liệu MVTec AD.

---

## 2. QUY CHUẨN PHÂN CẤP TIÊU ĐỀ

Tuân thủ nghiêm ngặt hệ thống phân cấp tiêu đề sau:

### 2.1. Phần khung đầu và cuối báo cáo (Không đánh số, viết IN HOA)
- `MỞ ĐẦU`
- `KẾT LUẬN`
- `TÀI LIỆU THAM KHẢO`
- Các trang phụ trợ: `MỤC LỤC`, `DANH MỤC HÌNH VẼ`, `DANH MỤC BẢNG BIỂU`, `DANH MỤC CÔNG THỨC`, `DANH MỤC TỪ VIẾT TẮT`.

### 2.2. Tiêu đề cấp chương (Chữ số La Mã)
- `CHƯƠNG I: TỔNG QUAN VỀ BÀI TOÁN XỬ LÝ ẢNH`
- `CHƯƠNG II: PHƯƠNG PHÁP VÀ QUY TRÌNH TRIỂN KHAI XỬ LÝ ẢNH`
- `CHƯƠNG III: THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ`

### 2.3. Tiêu đề cấp mục và mục con (Chữ số Ả Rập, bắt buộc có dấu chấm sau mỗi số mục)
- Cấp 1 (Section): `1.1.`, `1.2.`, `2.1.`, `2.2.`, `3.1.` ...
- Cấp 2 (Subsection): `1.2.1.`, `2.3.1.`, `3.3.2.` ...
- Cấp 3 (Sub-subsection - nếu cần): `2.3.1.1.`, `3.3.1.1.` ...

*Quy tắc kiểm tra:* Bất kỳ mục số Ả Rập nào thiếu dấu chấm kết thúc (ví dụ viết nhầm thành `1.1` thay vì `1.1.`) đều là vi phạm quy chuẩn.

---

## 3. CẤU TRÚC VÀ TỔ CHỨC NỘI DUNG TỪNG CHƯƠNG

Mỗi chương trong báo cáo bắt buộc phải tuân theo khung tổ chức 3 phần:
1. **Đoạn dẫn nhập đầu chương:**
   - Đặt ngay bên dưới tiêu đề `CHƯƠNG X: ...`.
   - Độ dài: từ 1 đến 2 đoạn văn (khoảng 100 - 200 từ).
   - Tuyệt đối không đánh số mục.
   - Nội dung: Tóm tắt mục đích, vai trò của chương và định hướng logic của các mục nội dung tiếp theo.
2. **Thân chương (Các mục nội dung logic):**
   - Sắp xếp từ tổng quan, cơ sở lý thuyết đến mô tả chi tiết giải pháp, từ thiết lập môi trường đến phân tích kết quả định lượng/định tính.
3. **Mục kết luận chương:**
   - Mục cuối cùng của mỗi chương phải là `X.Y. Kết luận chương X` (ví dụ `1.6. Kết luận chương I`, `2.5. Kết luận chương II`, `3.5. Kết luận chương III`).
   - Tóm tắt những điểm cốt lõi đã đạt được trong chương và chuyển tiếp logic sang chương kế tiếp.

---

## 4. QUY CHUẨN TRÌNH BÀY THUẬT TOÁN VÀ MÔ-ĐUN XỬ LÝ ẢNH (CHƯƠNG II)

### 4.1. Cấm tuyệt đối mã nguồn thô
- **Quy tắc bất di bất dịch:** Tuyệt đối không copy-paste mã nguồn thô (raw Python/C++ code) vào phần nội dung báo cáo.
- **Hình thức thay thế hợp lệ:** Sử dụng giả mã thuật toán (pseudocode theo chuẩn `algorithm2e` hoặc `algorithmicx` trong LaTeX), sơ đồ khối luồng dữ liệu (flowchart) hoặc bảng mô tả tham số.

### 4.2. Cấu trúc 5 phần bắt buộc cho mỗi thuật toán / mô-đun xử lý ảnh
Khi trình bày bất kỳ mô-đun nào tại Mục 2.3, bắt buộc phải trình bày theo đúng 5 mục thành phần sau:

```markdown
#### 2.3.x. Tên mô-đun / Thuật toán

1. **Đầu vào (Inputs):**
   - Định dạng ảnh, kiểu dữ liệu ma trận (ví dụ: RGB uint8 kích thước H x W x 3).
   - Tọa độ, tham số siêu hình học, ảnh mặt nạ gốc hoặc mặt nạ nhị phân hỗ trợ.

2. **Đầu ra (Outputs):**
   - Ảnh sau xử lý / ảnh tổng hợp (ví dụ: RGB uint8 kích thước H x W x 3).
   - Mặt nạ phân vùng nhị phân mặt đất (Ground-truth Binary Mask uint8 kích thước H x W, giá trị thuộc {0, 255}).
   - Vector tọa độ đa giác chuẩn hóa hoặc ma trận phổ tần số.

3. **Luồng xử lý (Processing Flow):**
   - Bước 1: [Mô tả chi tiết bước tiền xử lý, trích xuất hoặc biến đổi]
   - Bước 2: [Mô tả chi tiết toán tử hoặc phép biến đổi chính]
   - Bước 3: [Mô tả khâu ghép biên, nghịch đảo hoặc hậu xử lý]
   - Bước 4: [Mô tả khâu tạo nhãn và kiểm tra tính toàn vẹn hình học]

4. **Công thức toán học:**
   - Trình bày tường minh bằng công thức LaTeX tách dòng.
   - Đánh số công thức theo chuẩn toàn bài (Công thức X).
   - Định nghĩa và giải thích chi tiết ý nghĩa vật lý của từng biến số và siêu tham số ngay bên dưới công thức.

5. **Nhận xét về vai trò của mô-đun:**
   - Phân tích vai trò của thuật toán đối với toàn bộ pipeline kiểm tra khuyết tật công nghiệp (giải quyết bài toán mất cân bằng mẫu, khử nhiễu nền tuần hoàn, hay tăng cường độ bền vững quang học).
```

---

## 5. QUY CHUẨN HÌNH ẢNH, BẢNG BIỂU VÀ CÔNG THỨC TOÁN HỌC

### 5.1. Hình ảnh, đồ thị, sơ đồ khối
- **Quy tắc đánh số:** Đánh số theo chương: `Hình 1.1`, `Hình 1.2`, `Hình 2.1`, `Hình 3.1`, `Hình 3.2`...
- **Vị trí caption:** Đặt **bên dưới** hình ảnh.
- **Định dạng caption:** `Hình X.Y. Tên mô tả hình ảnh` (bắt buộc dùng dấu chấm ngăn cách, **tuyệt đối không dùng dấu hai chấm** như `Hình X.Y: Tên...`).
- **Liên kết văn bản (Cross-reference):** Bắt buộc phải có đoạn văn liền kề (ngay trước hoặc sau hình) viện dẫn trực tiếp đến hình ảnh (ví dụ: "Như được minh họa trên Hình 2.1, quy trình tổng thể...").
- **Nguồn ảnh:** Ưu tiên 100% hình ảnh thực tế được trích xuất từ workspace dự án (`runs/verification/visualizations/group_a/`, `group_b/`, `group_c/`). Tuyệt đối không dùng ảnh minh họa trừu tượng hoặc ảnh placeholder không rõ nguồn gốc.

### 5.2. Bảng biểu số liệu
- **Quy tắc đánh số:** Đánh số **liên tục toàn bài**: `Bảng 1`, `Bảng 2`, `Bảng 3`, `Bảng 4`...
- **Vị trí caption:** Đặt **phía trên** bảng.
- **Định dạng caption:** `Bảng X. Tên mô tả nội dung bảng` (dùng dấu chấm, không dùng dấu hai chấm).
- **Yêu cầu hiển thị:** Cột số liệu phải có tiêu đề rõ ràng, ghi rõ đơn vị tính (ví dụ: `ms`, `%`, `dB`, điểm số $[0, 1]$), các chú thích điều kiện thực nghiệm đặt ngay dưới bảng nếu cần.

### 5.3. Công thức toán học
- **Quy tắc đánh số:** Đánh số **liên tục toàn bài**: `Công thức 1`, `Công thức 2`, `Công thức 3`... (hoặc hiển thị dạng `(1)`, `(2)` ở mép phải công thức theo chuẩn LaTeX).
- **Định dạng:** Trình bày bằng môi trường toán LaTeX tách dòng (`equation` hoặc `align`), định dạng chuẩn xác các ký hiệu giải tích, ma trận, tổng sigma, tích phân, biến ngẫu nhiên.
- **Giải thích ký hiệu:** Ngay bên dưới công thức, sử dụng cấu trúc:  
  `Trong đó:`  
  `- $x, y$: tọa độ không gian điểm ảnh.`  
  `- $I(x, y)$: cường độ sáng tại tọa độ $(x, y)$.`  
  `- $\sigma$: độ lệch chuẩn của hàm Gaussian.`

---

## 6. QUY CHUẨN TRÍCH DẪN TÀI LIỆU THAM KHẢO

- **Chuẩn định dạng:** Tuân thủ quy chuẩn quốc tế IEEE.
- **Hình thức trích dẫn trong bài:** Dùng số thứ tự đặt trong ngoặc vuông: `[1]`, `[2]`, `[3, 4]`.
- **Nguyên tắc trung thực:**
  - Tuyệt đối không tự bịa tên tác giả, tên hội nghị/tạp chí, năm xuất bản, chỉ số DOI hoặc liên kết URL.
  - Các bài báo nền tảng chính thức đã sử dụng trong dự án:
    - MVTec AD Dataset: Bergmann et al. (CVPR 2019 / IJCV 2021) `[1]`.
    - CutPaste: Li et al. (CVPR 2021) `[2]`.
    - DRAEM: Zavrtanik et al. (ICCV 2021) `[3]`.
    - NSA: Schlüter et al. (ECCV 2022) `[4]`.
    - MVTec-AD-C: Horwitz & Hoshen (BMVC 2022) `[5]`.
    - Poisson Image Editing: Pérez et al. (ACM TOG / SIGGRAPH 2003) `[6]`.
  - Mọi tài liệu chưa đủ dữ kiện xác minh hoặc cần người dùng cung cấp thêm bắt buộc phải ghi rõ: `[CẦN BỔ SUNG: Tài liệu tham khảo cho ...]`.

---

## 7. NGUYÊN TẮC TRUNG THỰC DỮ LIỆU VÀ XÁC THỰC THỰC NGHIỆM

- **Tên thuật toán & mã nguồn:** Chỉ trình bày những thuật toán thực sự có file cài đặt trong workspace (`CutPasteSynthesizer`, `DRAEMSynthesizer`, `NSASynthesizer`, `FFTPeriodicSuppressionFilter`, `DWTSubbandFilter`, `apply_corruption`, `DualDomainEvaluator`, `YOLOSegExporter`).
- **Thư viện thực tế:** Chỉ nhắc đến các thư viện đã được cài đặt và kiểm chứng (`numpy 2.4.6`, `opencv-python 5.1.0`, `PyWavelets 1.9.0`, `scipy 1.17.1`, `scikit-learn 1.9.1`, `pandas 3.1.1`, `ultralytics 8.4`).
- **Số liệu định lượng:** Số liệu thực nghiệm phải trích xuất chính xác từ các file kết quả thực tế (`runs/verification/verification_report.md`, `results/ablation_summary.md`, `results/ablation_summary.csv`).
- **Xử lý thiếu hụt thông tin:** Nếu có bất kỳ hạng mục nào chưa chạy xong hoặc chưa có số liệu đo lường cụ thể (ví dụ kết quả huấn luyện mô hình sâu trên GPU Colab đối với các thực nghiệm EXP-01 đến EXP-11 chưa hoàn tất thu hoạch), bắt buộc phải sử dụng nhãn cảnh báo:
  `[CẦN BỔ SUNG: Mô tả chi tiết dữ liệu cần bổ sung]`
- **Cấm đoán:** Tuyệt đối không tự suy đoán số liệu phần trăm mAP, không bịa đặt biểu đồ huấn luyện giả tạo.

---

## 8. HƯỚNG DẪN CẤU TRÚC LATEX VÀ BIÊN DỊCH VỚI MIKTEX (BẢN 25.12)

### 8.1. Thiết lập trình biên dịch và môi trường
- Hệ thống máy trạm đã cài đặt sẵn MiKTeX 25.12 tại đường dẫn:  
  `C:\Users\ASUS\AppData\Local\Programs\MiKTeX\miktex\bin\x64\`
- Lệnh biên dịch chuẩn:
  ```powershell
  # Biên dịch lần 1
  pdflatex -synctex=1 -interaction=nonstopmode main.tex
  # Biên dịch tài liệu tham khảo (nếu dùng bibtex)
  bibtex main
  # Biên dịch lần 2 & 3 để hoàn thiện mục lục và cross-ref
  pdflatex -synctex=1 -interaction=nonstopmode main.tex
  pdflatex -synctex=1 -interaction=nonstopmode main.tex
  ```
- *Lưu ý Sandbox Windows:* Khi thực thi lệnh biên dịch `pdflatex` thông qua agent terminal, cần thiết lập `BypassSandbox: true` để tránh xung đột quyền truy cập Registry của MiKTeX (`Software\MiKTeX.org\MiKTeX\2.9\Core`).

### 8.2. Danh mục các gói lệnh LaTeX (Packages) bắt buộc
- **Ngôn ngữ và bảng mã:**
  ```latex
  \usepackage[utf8]{inputenc}
  \usepackage[vietnamese]{babel} % Hỗ trợ tiếng Việt chuẩn
  \usepackage[T5]{fontenc}       % Bảng mã font tiếng Việt T5
  ```
- **Toán học và ký hiệu:**
  ```latex
  \usepackage{amsmath, amsfonts, amssymb}
  \usepackage{mathtools}
  ```
- **Chèn hình ảnh và định dạng đồ họa:**
  ```latex
  \usepackage{graphicx}
  \usepackage{subcaption}
  \graphicspath{{../runs/verification/visualizations/}} % Đường dẫn trực tiếp đến ảnh
  ```
- **Bảng biểu chuẩn mực học thuật:**
  ```latex
  \usepackage{booktabs}
  \usepackage{multirow}
  \usepackage{tabularx}
  ```
- **Định dạng lề và căn lề trang:**
  ```latex
  \usepackage[a4paper, top=2.5cm, bottom=2.5cm, left=3.0cm, right=2.0cm]{geometry}
  ```
- **Thuật toán (Pseudocode):**
  ```latex
  \usepackage[ruled, vlined, linesnumbered]{algorithm2e}
  ```
- **Liên kết và mục lục điện tử:**
  ```latex
  \usepackage{hyperref}
  \hypersetup{
      colorlinks=true,
      linkcolor=blue,
      citecolor=blue,
      urlcolor=cyan
  }
  ```
- **Tùy chỉnh định dạng Caption:**
  ```latex
  \usepackage{caption}
  \captionsetup[figure]{name=Hình, labelsep=period} % Đảm bảo hiển thị dạng "Hình X.Y."
  \captionsetup[table]{name=Bảng, labelsep=period}  % Đảm bảo hiển thị dạng "Bảng X."
  ```

---
*Tài liệu STYLE_RULES.md này là kim chỉ nam bắt buộc tuân thủ xuyên suốt quá trình thiết kế đề cương và viết chi tiết toàn bộ các file LaTeX của báo cáo học phần.*
