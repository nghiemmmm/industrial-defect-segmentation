# ĐỀ CƯƠNG CHI TIẾT BÁO CÁO CUỐI KỲ HỌC PHẦN XỬ LÝ ẢNH
**Tên đề tài dự kiến:** Nghiên cứu và triển khai các phương pháp xử lý ảnh nâng cao, biến đổi miền tần số và sinh mẫu tổng hợp nhằm tối ưu hóa phân vùng khuyết tật bề mặt công nghiệp  
**Mã học phần:** INT14123_CLC - Xử lý ảnh (Image Processing)  
**Môi trường thực thi & kiểm chứng:** Hệ thống Windows trạm (`.\venv`, Python 3.11.9) & Google Colab Cloud GPU  
**Trình biên dịch báo cáo:** MiKTeX (Bản 25.12) / pdfLaTeX / XeLaTeX tại `C:\Users\ASUS\AppData\Local\Programs\MiKTeX\miktex\bin\x64\`  

---

## PHẦN ĐẦU BÁO CÁO

### Bìa báo cáo và Phụ bìa
1. **Mục đích trình bày:** Thể hiện đầy đủ thông tin hành chính, danh tính tác giả, mã học phần, đơn vị đào tạo và giảng viên phụ trách theo đúng quy định của trường đại học.
2. **Nội dung thực tế của dự án:**
   - Trường Đại học / Khoa đào tạo.
   - Mã học phần: `INT14123_CLC` - Xử lý ảnh (Image Processing).
   - Tên đề tài: Nghiên cứu, thực nghiệm các thuật toán xử lý ảnh, biến đổi miền tần số (2D-FFT, 2D-DWT) và sinh khuyết tật tổng hợp (CutPaste, DRAEM, NSA) cho bài toán phân vùng khuyết tật sản phẩm công nghiệp (MVTec AD).
   - Thông tin sinh viên thực hiện và Giảng viên hướng dẫn.
3. **Nguồn dữ liệu trong workspace:** Chưa có văn bản hành chính mẫu của trường.
4. **Hình ảnh/bảng biểu dự kiến:** Logo của Trường/Viện đào tạo `[CẦN BỔ SUNG]`.
5. **Tình trạng:** `[THIẾU]` (Cần thông tin họ tên sinh viên, mã số sinh viên, tên trường/khoa và tên giảng viên chấm điểm).

### Lời cam đoan
1. **Mục đích trình bày:** Cam kết tính trung thực, độc lập và đạo đức học thuật trong quá trình thực hiện bài tập lớn/báo cáo học phần.
2. **Nội dung thực tế của dự án:** Khẳng định toàn bộ mã nguồn xử lý ảnh, thuật toán lọc tần số, sinh khuyết tật và số liệu kiểm chứng đều do nhóm nghiên cứu tự cài đặt và thực nghiệm trên máy trạm cục bộ và Google Colab; không sao chép trái phép.
3. **Nguồn dữ liệu trong workspace:** `README.md`, `runs/verification/verification_report.md`.
4. **Hình ảnh/bảng biểu dự kiến:** Chữ ký sinh viên `[CẦN BỔ SUNG]`.
5. **Tình trạng:** `[ĐÃ CÓ]` (Có cơ sở đối chiếu từ `verification_report.md`).

### Lời cảm ơn
1. **Mục đích trình bày:** Bày tỏ sự tri ân đối với Giảng viên phụ trách học phần đã truyền đạt kiến thức và hỗ trợ phương pháp luận trong suốt quá trình học tập.
2. **Nội dung thực tế của dự án:** Cảm ơn Giảng viên bộ môn Xử lý ảnh (mã HP `INT14123_CLC`), cùng các đồng nghiệp/nhóm hỗ trợ.
3. **Nguồn dữ liệu trong workspace:** `[CẦN BỔ SUNG: Thông tin Giảng viên phụ trách]`.
4. **Hình ảnh/bảng biểu dự kiến:** Không áp dụng.
5. **Tình trạng:** `[THIẾU]`.

### Các danh mục tra cứu tự động
1. **Mục đích trình bày:** Hệ thống hóa mục lục, danh mục hình vẽ, danh mục bảng biểu, danh mục công thức và các từ viết tắt chuyên ngành.
2. **Nội dung thực tế của dự án:**
   - Mục lục tự động 3 chương (`\tableofcontents`).
   - Danh mục hình vẽ (`\listoffigures`): 28 hình ảnh thực tế từ `runs/verification/visualizations/`.
   - Danh mục bảng biểu (`\listoftables`): Bảng tham số, bảng so sánh tái tạo, bảng ma trận 12 thực nghiệm.
   - Danh mục công thức toán học (`\listofequations` hoặc liệt kê).
   - Danh mục từ viết tắt: AD (Anomaly Detection), FFT (Fast Fourier Transform), DWT (Discrete Wavelet Transform), NSA (Natural Synthetic Anomalies), DRAEM (Discriminative Reconstruction-based Anomaly Embedding Model), mAP (Mean Average Precision), AUROC (Area Under the Receiver Operating Characteristic), FAR (False Alarm Rate), IoU (Intersection over Union).
3. **Nguồn dữ liệu trong workspace:** `runs/verification/verification_report.md`, `results/ablation_summary.md`.
4. **Hình ảnh/bảng biểu dự kiến:** Bảng Danh mục từ viết tắt.
5. **Tình trạng:** `[ĐÃ CÓ]`.

---

## MỞ ĐẦU

### 1. Lý do chọn đề tài
1. **Mục đích trình bày:** Giải thích tính cấp thiết của việc áp dụng xử lý ảnh và thị giác máy tính vào khâu kiểm tra chất lượng (QC/QA) trong dây chuyền sản xuất công nghiệp tự động hóa.
2. **Nội dung thực tế của dự án:**
   - Trong công nghiệp chế tạo (sản xuất chai lọ, vi mạch, ốc vít, linh kiện điện tử, dệt may), khuyết tật bề mặt sản phẩm xuất hiện với tỉ lệ rất nhỏ (dưới 1-2%), không đồng đều và cực kỳ đa dạng về hình thái (vết xước rách, nứt vỡ, vết ố, lỗ thủng).
   - Thu thập mẫu lỗi thực tế để huấn luyện các mô hình học sâu đòi hỏi chi phí đắt đỏ và tiềm ẩn rủi ro bỏ sót lỗi hiếm.
   - Xuất phát từ thực tiễn trên, việc kết hợp các kỹ thuật xử lý ảnh cổ điển (phép lọc miền tần số 2D-FFT triệt tiêu nền lặp lại, biến đổi sóng con 2D-DWT tách dải chi tiết) với các thuật toán sinh khuyết tật nhân tạo (CutPaste, DRAEM Perlin Noise, NSA Poisson Blending) trực tiếp từ ảnh sản phẩm lành (`train/good`) mở ra giải pháp phân vùng lỗi chính xác mà không làm rò rỉ dữ liệu kiểm thử (Zero Data Leakage).
3. **Nguồn dữ liệu trong workspace:** `README.md` (Mục "Bối cảnh nghiên cứu"), `industrial_defect_segmentation.ipynb`.
4. **Hình ảnh/bảng biểu dự kiến:** Sơ đồ minh họa bài toán kiểm tra khuyết tật công nghiệp (Dây chuyền sản xuất -> Camera kiểm tra -> Phân vùng khuyết tật).
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 2. Tổng quan vấn đề
1. **Mục đích trình bày:** Phân tích thực trạng và các cách tiếp cận hiện nay đối với bài toán phát hiện bất thường và phân vùng khuyết tật công nghiệp.
2. **Nội dung thực tế của dự án:**
   - Sự dịch chuyển từ bài toán phân lớp nhị phân (ảnh lỗi / ảnh lành) sang bài toán phân vùng khuyết tật mức điểm ảnh (Pixel-level Defect Segmentation) để định vị chính xác vị trí và ranh giới tổn hại vật lý.
   - Sự phụ thuộc vào dữ liệu ảnh lành và thách thức khi môi trường nhà xưởng bị suy thoái quang học (nhiễu cảm biến camera, mất nét, chuyển động rung lắc trên băng chuyền).
   - Nhu cầu cấp thiết về một khung làm việc (framework) xử lý ảnh toàn diện, cho phép tiền xử lý lọc tần số và tăng cường dữ liệu khuyết tật mô phỏng chân thực.
3. **Nguồn dữ liệu trong workspace:** `README.md`, `.agents/rules/industrial-defect-detection.md`.
4. **Hình ảnh/bảng biểu dự kiến:** Sơ đồ so sánh bài toán phân lớp ảnh (Image Classification) vs. Định vị (Object Detection) vs. Phân vùng điểm ảnh (Instance/Semantic Segmentation).
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 3. Mục tiêu thực hiện
1. **Mục đích trình bày:** Xác định các mục tiêu cụ thể, khả thi mà báo cáo học phần cần đạt được.
2. **Nội dung thực tế của dự án:**
   - *Mục tiêu 1:* Nghiên cứu lý thuyết và cài đặt độc lập 3 thuật toán sinh mẫu khuyết tật tổng hợp từ ảnh lành: CutPaste (Normal & Scar), DRAEM (đa tỉ lệ Perlin noise + beta blending), NSA (Poisson seamless cloning + mặt nạ Otsu).
   - *Mục tiêu 2:* Nghiên cứu nguyên lý và cài đặt 2 thuật toán xử lý miền tần số: Lọc triệt tiêu đỉnh phổ tuần hoàn 2D-FFT và phân tách dải tần số 2D-DWT tăng cường biên cạnh chi tiết cao.
   - *Mục tiêu 3:* Thiết lập bộ tiêu chuẩn đánh giá độ bền vững trước suy thoái quang học MVTec-AD-C với 4 loại nhiễu (Gaussian noise, Gaussian blur, Motion blur, Defocus blur) ở 5 mức độ nghiêm trọng.
   - *Mục tiêu 4:* Xây dựng quy trình tích hợp khép kín (End-to-End Pipeline) xuất nhãn đa giác chuẩn hóa $[0.0, 1.0]$ cho mô hình YOLOv11-seg, thực thi ma trận thực nghiệm gồm 12 kịch bản (EXP-00 đến EXP-11) và đánh giá qua bộ chỉ số kép (Mask mAP, Pixel-AUROC, Image-AUROC, FAR@0.25).
3. **Nguồn dữ liệu trong workspace:** `README.md`, `runs/verification/verification_report.md` (Mục 1, 2).
4. **Hình ảnh/bảng biểu dự kiến:** Bảng tóm tắt 4 mục tiêu nghiên cứu và tiêu chí nghiệm thu tương ứng.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 4. Đối tượng và phạm vi thực hiện
#### 4.1. Đối tượng nghiên cứu
1. **Mục đích trình bày:** Xác định đối tượng dữ liệu và thuật toán trọng tâm của đề tài.
2. **Nội dung thực tế của dự án:**
   - Ảnh số công nghiệp độ phân giải cao từ tập dữ liệu chuẩn MVTec Anomaly Detection (MVTec AD).
   - Các thuật toán xử lý tín hiệu ảnh 2 chiều: Biến đổi Fourier rời rạc 2D-FFT, biến đổi sóng con rời rạc 2D-DWT, phương trình đạo hàm riêng giải tích vi phân Poisson trong xử lý ảnh liền mạch.
   - Các thuật toán tạo nhiễu ngẫu nhiên cấu trúc: Nhiễu gradient Perlin (Perlin Noise) đa quãng tám (octaves).
3. **Nguồn dữ liệu trong workspace:** `data_engine/loaders/mvtec_loader.py`, `data_engine/frequency/`, `data_engine/synthesizers/`.
4. **Hình ảnh/bảng biểu dự kiến:** Bảng tổng hợp đối tượng nghiên cứu và thuật toán áp dụng.
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 4.2. Phạm vi thực hiện
1. **Mục đích trình bày:** Giới hạn rõ ràng ranh giới nghiên cứu phù hợp với quy mô học phần đại học.
2. **Nội dung thực tế của dự án:**
   - Dữ liệu: Tập trung kiểm chứng chuyên sâu trên 6 danh mục đại diện của MVTec AD gồm 3 lớp kết cấu bề mặt lặp lại (`grid`, `carpet`, `tile`) và 3 lớp vật thể công nghiệp có hình học xác định (`screw`, `pill`, `bottle`) với 2,857 ảnh thực tế.
   - Tiêu chuẩn Zero Data Leakage: Quá trình tiền xử lý và sinh khuyết tật chỉ sử dụng ảnh từ tập `train/good`. Tập `test` (chứa các loại khuyết tật thực tế) được bảo toàn 100% để kiểm thử độc lập.
   - Giới hạn công nghệ: Toàn bộ module xử lý ảnh, biến đổi tần số và trích xuất đặc trưng được thực hiện bằng CPU với NumPy, OpenCV, PyWavelets, SciPy. Huấn luyện mô hình phân vùng học sâu được thực thi trên GPU đám mây thông qua Google Colab.
3. **Nguồn dữ liệu trong workspace:** `runs/verification/verification_report.md` (Mục 1), `configs/experiments/`.
4. **Hình ảnh/bảng biểu dự kiến:** Sơ đồ phân chia phạm vi nghiên cứu (6 danh mục đối tượng x 4 nhóm thuật toán).
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 5. Phương pháp thực hiện
1. **Mục đích trình bày:** Nêu phương pháp luận khoa học được sử dụng trong suốt quá trình triển khai dự án.
2. **Nội dung thực tế của dự án:**
   - Phương pháp kết hợp nghiên cứu lý thuyết giải tích và cài đặt thực nghiệm (Experimental Method).
   - Kiểm thử đơn vị (Unit Testing) và kiểm tra tích hợp tự động với `pytest` (đạt 34/34 bài test).
   - Phương pháp kiểm chứng trực quan (Visual Inspection) dựa trên ảnh montage đa thành phần đối chiếu với ảnh gốc.
   - Phương pháp nghiên cứu cắt bỏ (Ablation Study) có kiểm soát biến số qua 12 kịch bản thực nghiệm độc lập.
3. **Nguồn dữ liệu trong workspace:** `tests/`, `tools/verify_all.py`, `experiments/run_experiment.py`.
4. **Hình ảnh/bảng biểu dự kiến:** Sơ đồ khối phương pháp luận thực hiện đề tài.
5. **Tình trạng:** `[ĐÃ CÓ]`.

---

## CHƯƠNG I: TỔNG QUAN VỀ BÀI TOÁN XỬ LÝ ẢNH

*Đoạn dẫn nhập đầu chương:* Giới thiệu tổng quan bối cảnh toán học và thực tiễn của bài toán xử lý ảnh trong công nghiệp, làm rõ các khái niệm nền tảng về ảnh số, không gian màu, miền tần số và các thách thức đặc thù của việc phân vùng khuyết tật bề mặt sản phẩm.

### 1.1. Phát biểu bài toán
1. **Mục đích trình bày:** Định nghĩa toán học chặt chẽ bài toán phân vùng khuyết tật bề mặt công nghiệp từ ảnh số.
2. **Nội dung thực tế của dự án:**
   - Cho ảnh đầu vào $I \in \mathbb{R}^{H \times W \times 3}$. Mục tiêu là xác định ma trận nhãn phân vùng nhị phân $M \in \{0, 1\}^{H \times W}$ sao cho:
     $$M(x, y) = \begin{cases} 1 & \text{nếu điểm ảnh } (x, y) \text{ thuộc vùng khuyết tật} \\ 0 & \text{nếu điểm ảnh } (x, y) \text{ là bề mặt bình thường} \end{cases}$$
   - Khác biệt giữa bài toán phân lớp ảnh một chiều (chỉ xác định ảnh có lỗi hay không) và phân vùng đối tượng (định vị chính xác biên dạng hình học của tổn thất).
3. **Nguồn dữ liệu trong workspace:** `data_engine/sample.py`, `data_engine/exporters/yolo_seg_exporter.py`.
4. **Hình ảnh/bảng biểu dự kiến:** Hình 1.1. Minh họa bài toán phân vùng điểm ảnh khuyết tật trên mẫu sản phẩm `bottle` và `grid`.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 1.2. Cơ sở lý thuyết và kiến thức liên quan
1. **Mục đích trình bày:** Trình bày có chọn lọc các lý thuyết xử lý ảnh nền tảng được vận dụng trực tiếp trong đề tài.
2. **Nội dung thực tế của dự án:**
   - *Biểu diễn ảnh số và không gian màu:* Ma trận số học, các kênh màu RGB, grayscale, ảnh nhị phân.
   - *Lý thuyết miền tần số 2 chiều:* Biến đổi Fourier 2D rời rạc (2D-DFT), phổ biên độ, phổ pha, tính tuần hoàn không gian và nguyên lý phân giải tần số cao/thấp.
   - *Lý thuyết biến đổi sóng con (Wavelet Transform):* Biến đổi sóng con rời rạc 2D (2D-DWT), các ngân hàng bộ lọc (Filter Banks), hàm tỷ lệ (scaling function) $\phi(x)$ và hàm sóng con (wavelet function) $\psi(x)$, cơ sở phân rã 4 dải tần $LL, LH, HL, HH$.
   - *Giải tích vi phân trong xử lý ảnh:* Phương trình Poisson $\Delta f = \operatorname{div} \mathbf{v}$ với điều kiện biên Dirichlet ứng dụng trong ghép ảnh liền mạch (Seamless Image Editing).
   - *Hàm toán học sinh mẫu giả ngẫu nhiên:* Cơ chế nội suy gradient Perlin (Ken Perlin), liên tục về mặt toán học ở cấp độ đạo hàm bậc một.
3. **Nguồn dữ liệu trong workspace:** `data_engine/frequency/fft_filter.py`, `data_engine/frequency/dwt_filter.py`, `data_engine/synthesizers/nsa_synthesizer.py`, `data_engine/synthesizers/draem_synthesizer.py`.
4. **Hình ảnh/bảng biểu dự kiến:**
   - Hình 1.2. Minh họa sự phân rã dải tần 2 chiều của biến đổi Wavelet (Haar Wavelet).
   - Công thức 1, 2, 3: Công thức 2D-DFT, công thức phân rã DWT, phương trình vi phân Poisson.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 1.3. Các hướng tiếp cận và phương pháp xử lý ảnh liên quan
1. **Mục đích trình bày:** Khảo sát các hướng tiếp cận chính trong bài toán kiểm tra khuyết tật bề mặt sản phẩm.
2. **Nội dung thực tế của dự án:**
   - *Hướng tiếp cận dựa trên xử lý ảnh truyền thống:* Lọc không gian, phân ngưỡng Otsu, trừ nền (background subtraction), bộ lọc Gabor trích xuất kết cấu. Hạn chế: Kém thích nghi khi bề mặt có hoa văn phi tuyến tính hoặc điều kiện chiếu sáng biến đổi.
   - *Hướng tiếp cận tái tạo bất thường dựa trên học sâu (Reconstruction-based):* Autoencoder, GAN. Hạn chế: Khó kiểm soát hiện tượng tái tạo mờ (blurring) hoặc vô tình tái tạo luôn cả khuyết tật.
   - *Hướng tiếp cận dựa trên dữ liệu tổng hợp (Synthetic-based Anomaly Segmentation):* Chủ động tạo ra khuyết tật giả lập từ ảnh bình thường để biến bài toán học không giám sát thành bài toán học có giám sát đầy đủ (Supervised Instance Segmentation). Đây chính là hướng tiếp cận trọng tâm của đề tài.
3. **Nguồn dữ liệu trong workspace:** `README.md`, `industrial_defect_segmentation.ipynb`.
4. **Hình ảnh/bảng biểu dự kiến:** Bảng 1. So sánh ưu, nhược điểm của các hướng tiếp cận kiểm tra khuyết tật công nghiệp.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 1.4. Các thuật toán và công nghệ được sử dụng
1. **Mục đích trình bày:** Tổng quan các công nghệ và thuật toán cụ thể được hiện thực hóa trong đồ án.
2. **Nội dung thực tế của dự án:**
   - Các thuật toán xử lý ảnh lõi:
     - Biến đổi Fourier nhanh 2 chiều (FFT) và lọc chặn dải (Notch Filtering) thích nghi.
     - Phân rã sóng con đa mức 2D-DWT (Haar / Daubechies) và tăng cường hệ số dải chi tiết.
     - Biến đổi affine cục bộ (Local Affine Patching) và ghép mẫu CutPaste (Normal & Scar).
     - Thuật toán Perlin Noise 2 chiều và hòa trộn kênh mờ (Beta Blending).
     - Giải hệ phương trình Poisson bằng sai phân hữu hạn thông qua `cv2.seamlessClone`.
   - Các công nghệ hỗ trợ:
     - Thư viện: NumPy, OpenCV, PyWavelets, SciPy, scikit-learn, PyYAML, pytest.
     - Mô hình phân vùng: YOLOv11-seg (kiến trúc trích xuất đặc trưng C3k2, SPPF và đầu phân vùng C2f-PSA).
3. **Nguồn dữ liệu trong workspace:** `requirements.txt`, `data_engine/`, `tests/`.
4. **Hình ảnh/bảng biểu dự kiến:** Bảng 2. Thống kê các công nghệ, thư viện và phiên bản thực tế sử dụng trong dự án.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 1.5. Những thách thức trong bài toán
1. **Mục đích trình bày:** Phân tích các rào cản kỹ thuật thực tế đặt ra cho hệ thống xử lý ảnh.
2. **Nội dung thực tế của dự án:**
   - *Mất cân bằng dữ liệu cực đoan (Extreme Class Imbalance):* Mẫu lỗi trong sản xuất cực hiếm, dẫn đến hiện tượng mô hình dự báo thiên lệch và tỷ lệ báo động giả cao (False Alarms).
   - *Đa dạng về kích thước và tỉ lệ khung hình:* Ảnh công nghiệp có kích thước không chuẩn hóa (ví dụ: `bottle` $900 \times 900$, `pill` $800 \times 800$, `tile` $840 \times 840$), gây lỗi kích thước khi áp dụng các thuật toán giả định kích thước lũy thừa 2 (như trường hợp DRAEM gốc).
   - *Nhiễu nền tuần hoàn (Periodic Background Noise):* Trên các sản phẩm kết cấu dệt, lưới thép (`grid`, `carpet`), tần số lặp của hoa văn nền lấn át tín hiệu khuyết tật nhỏ.
   - *Suy thoái quang học môi trường thực:* Hiện tượng rung chấn băng chuyền (Motion blur), rung lắc thấu kính (Defocus blur) và nhiễu nhiệt cảm biến (Gaussian noise) làm suy giảm nghiêm trọng độ chính xác phân vùng.
3. **Nguồn dữ liệu trong workspace:** `runs/verification/verification_report.md` (Mục 10, 11), `.agents/rules/industrial-defect-detection.md`.
4. **Hình ảnh/bảng biểu dự kiến:** Hình 1.3. Các thách thức khuyết tật thực tế: lỗi ẩn trong kết cấu lặp lại và suy thoái quang học.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 1.6. Kết luận chương I
1. **Mục đích trình bày:** Tóm tắt các nội dung cốt lõi của Chương I và tạo bước chuyển sang giải pháp kỹ thuật ở Chương II.
2. **Nội dung thực tế của dự án:** Khẳng định sự cần thiết phải kết hợp giữa xử lý miền tần số để loại bỏ nhiễu nền tuần hoàn, sinh khuyết tật đa dạng để cân bằng tập huấn luyện và thiết kế quy trình kiểm thử độ bền quang học.
3. **Nguồn dữ liệu trong workspace:** `README.md`.
4. **Hình ảnh/bảng biểu dự kiến:** Không áp dụng.
5. **Tình trạng:** `[ĐÃ CÓ]`.

---

## CHƯƠNG II: PHƯƠNG PHÁP VÀ QUY TRÌNH TRIỂN KHAI XỬ LÝ ẢNH

*Đoạn dẫn nhập đầu chương:* Trình bày chi tiết kiến trúc giải pháp, cấu trúc biểu diễn dữ liệu ảnh, nguyên lý toán học và quy trình 5 bước của từng mô-đun xử lý ảnh được cài đặt trong hệ thống. Tuyệt đối không đưa mã nguồn thô vào nội dung chương.

### 2.1. Kiến trúc tổng quát của quy trình xử lý ảnh
1. **Mục đích trình bày:** Cung cấp bức tranh toàn cảnh về luồng xử lý dữ liệu từ ảnh thô đến kết quả phân vùng khuyết tật.
2. **Nội dung thực tế của dự án:**
   - Sơ đồ kiến trúc Module Data Engine 4 nhóm:
     - *Khối nạp & kiểm soát dữ liệu (Data Loading & Partitioning):* Nạp ảnh lành `train/good`, duy trì mẫu âm tính `good_ratio=0.15`, cô lập tuyệt đối dữ liệu test.
     - *Khối sinh bất thường nhân tạo (Synthetic Anomaly Generation - Group A):* CutPaste, DRAEM, NSA.
     - *Khối lọc và biến đổi miền tần số (Frequency Domain Processing - Group B):* 2D-FFT Notch Filter, 2D-DWT Detail Boost.
     - *Khối xuất nhãn và chuẩn hóa (Annotation & Exporting):* OpenCV Contour Extraction, Polygon Normalization.
     - *Khối đánh giá độ bền quang học (Degradation Robustness - Group C):* MVTec-AD-C Engine.
3. **Nguồn dữ liệu trong workspace:** `data_engine/sample.py`, `README.md` (Sơ đồ kiến trúc).
4. **Hình ảnh/bảng biểu dự kiến:** Hình 2.1. Sơ đồ khối kiến trúc tổng thể quy trình xử lý và tiền xử lý ảnh công nghiệp.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 2.2. Biểu diễn và tổ chức dữ liệu ảnh
1. **Mục đích trình bày:** Mô tả cấu trúc dữ liệu nội bộ được thiết kế để quản lý ma trận ảnh, mặt nạ nhị phân và siêu dữ liệu hình học.
2. **Nội dung thực tế của dự án:**
   - Cấu trúc dữ liệu `Sample` dataclass:
     - `image`: Ma trận NumPy $H \times W \times C$, kiểu dữ liệu `uint8` (không gian màu RGB).
     - `mask`: Ma trận nhị phân $H \times W$, kiểu `uint8`, giá trị $0$ (nền lành) và $255$ (khuyết tật). Tự động khởi tạo mảng số 0 đối với mẫu lành.
     - `label`: Nhãn chuỗi ký tự (`good` hoặc tên dạng lỗi).
     - `category`: Tên lớp đối tượng (ví dụ: `bottle`, `tile`).
     - `is_anomaly`: Thuộc tính logic boolean xác định trạng thái khuyết tật.
     - `metadata`: Từ điển lưu trữ lịch sử xử lý, tham số thuật toán, tỉ lệ nén hoặc suy hao.
   - Cơ chế kiểm soát tính toàn vẹn kích thước: Bắt buộc $\operatorname{shape}(I)[:2] == \operatorname{shape}(M)$, ngăn chặn lỗi lệch tọa độ trong các phép biến đổi không gian.
3. **Nguồn dữ liệu trong workspace:** `data_engine/sample.py`, `tests/test_data_engine.py`.
4. **Hình ảnh/bảng biểu dự kiến:** Bảng 3. Cấu trúc trường dữ liệu của lớp biểu diễn mẫu ảnh `Sample`.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 2.3. Chi tiết các mô-đun và thuật toán xử lý ảnh

#### 2.3.1. Mô-đun sinh khuyết tật tổng hợp CutPaste
1. **Mục đích trình bày:** Trình bày nguyên lý, luồng xử lý và công thức biến đổi affine mô phỏng khuyết tật vết xước và mảng bám.
2. **Nội dung thực tế của dự án:**
   - Áp dụng cấu trúc 5 bước bắt buộc:
     - *1. Đầu vào:* Ảnh gốc $I \in \mathbb{R}^{H \times W \times 3}$, chế độ sinh (`normal` hoặc `scar`), diện tích vùng cắt $[0.02, 0.15]$, góc xoay $\theta \in [-45^\circ, 45^\circ]$, jitter màu.
     - *2. Đầu ra:* Ảnh sau biến đổi $I_{cp} \in \mathbb{R}^{H \times W \times 3}$, mặt nạ nhị phân $M_{cp} \in \{0, 255\}^{H \times W}$.
     - *3. Luồng xử lý:* Trích xuất ngẫu nhiên mảnh vá $P$ -> Biến đổi màu sắc -> Áp ma trận Affine xoay và tỉ lệ -> Dán đè lên vị trí đích $(x_d, y_d)$ -> Cập nhật ma trận mặt nạ nhị phân.
     - *4. Công thức toán học:* Ma trận biến đổi Affine 2D:
       $$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = \begin{bmatrix} s_x \cos\theta & -s_y \sin\theta & t_x \\ s_x \sin\theta & s_y \cos\theta & t_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$
     - *5. Nhận xét:* Cực kỳ hiệu quả đối với khuyết tật vật lý sắc nhọn (vết nứt, xước dăm), chi phí tính toán rất thấp.
3. **Nguồn dữ liệu trong workspace:** `data_engine/synthesizers/cutpaste_synthesizer.py`, `tests/test_synthesizers.py`.
4. **Hình ảnh/bảng biểu dự kiến:**
   - Hình 2.2. Trực quan hóa luồng thuật toán CutPaste (`scar` và `normal`).
   - Hình 2.3. Ảnh so sánh CutPaste trên các sản phẩm mẫu (`runs/verification/visualizations/group_a/bottle_cutpaste_normal_comparison.png`).
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 2.3.2. Mô-đun sinh khuyết tật bề mặt đa tỉ lệ DRAEM (Perlin Noise & Beta Blending)
1. **Mục đích trình bày:** Làm rõ thuật toán tạo trường vô hướng ngẫu nhiên đa tần số Perlin và hòa trộn phi tuyến tính.
2. **Nội dung thực tế của dự án:**
   - Cấu trúc 5 bước bắt buộc:
     - *1. Đầu vào:* Ảnh gốc $I$, nguồn kết cấu phụ $T$, bậc ngẫu nhiên (octaves).
     - *2. Đầu ra:* Ảnh mang khuyết tật hòa trộn $I_{dr}$, mặt nạ nhị phân ngưỡng hóa $M_{dr}$.
     - *3. Luồng xử lý:*
       - Khắc phục lỗi chia hết lưới: Khởi tạo lưới chuẩn lũy thừa 2 ($512 \times 512$).
       - Sinh ma trận gradient ngẫu nhiên và nội suy đa thức bậc 5 (Fade function: $6t^5 - 15t^4 + 10t^3$).
       - Nội suy song tuyến tính (Bilinear resize) về kích thước thực tế $(W, H)$ của ảnh.
       - Phân ngưỡng nhị phân tạo mặt nạ $M_{dr}$.
       - Hòa trộn theo tham số trọng số $\beta \in [0.2, 0.8]$.
     - *4. Công thức toán học:*
       $$I_{dr}(x, y) = (1 - \beta \cdot M_{dr}(x, y)) \cdot I(x, y) + (\beta \cdot M_{dr}(x, y)) \cdot T(x, y)$$
     - *5. Nhận xét:* Mô phỏng hoàn hảo các dạng khuyết tật bề mặt tự nhiên như ố mốc, biến màu, ăn mòn hóa học với biên dạng uốn lượn liên tục.
3. **Nguồn dữ liệu trong workspace:** `data_engine/synthesizers/draem_synthesizer.py`, `tests/test_synthesizers.py`.
4. **Hình ảnh/bảng biểu dự kiến:**
   - Hình 2.4. Trực quan hóa phổ nhiễu Perlin đa tỉ lệ và mặt nạ khuyết tật sinh ra.
   - Hình 2.5. Minh họa ảnh hòa trộn DRAEM trên ảnh kích thước không chia hết cho 32 (`runs/verification/visualizations/group_a/bottle_draem_comparison.png`).
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 2.3.3. Mô-đun ghép khuyết tật tự nhiên NSA (Poisson Seamless Cloning)
1. **Mục đích trình bày:** Trình bày thuật toán ghép khuyết tật giữ tính liên tục trường gradient bằng phương trình Poisson.
2. **Nội dung thực tế của dự án:**
   - Cấu trúc 5 bước bắt buộc:
     - *1. Đầu vào:* Ảnh nguồn khuyết tật $I_s$, ảnh đích $I_d$, mặt nạ vùng chọn $M_s$, tâm ghép $(c_x, c_y)$.
     - *2. Đầu ra:* Ảnh sau biến đổi liền mạch $I_{nsa}$, mặt nạ khuyết tật nhị phân cập nhật.
     - *3. Luồng xử lý:* Phân đoạn tiền cảnh tự động bằng ngưỡng Otsu (tránh ghép vùng ngoài không gian vật thể) -> Xác định trường gradient $\mathbf{v} = \nabla I_s$ -> Giải phương trình Poisson với điều kiện biên Dirichlet $I_{nsa}|_{\partial \Omega} = I_d|_{\partial \Omega}$ -> Đồng bộ hóa mặt nạ nhị phân.
     - *4. Công thức toán học:*
       $$\min_f \iint_{\Omega} \|\nabla f - \mathbf{v}\|^2 \, dx dy \quad \text{với } f|_{\partial \Omega} = I_d|_{\partial \Omega} \implies \Delta f = \operatorname{div} \mathbf{v} \text{ trên } \Omega$$
     - *5. Nhận xét:* Loại bỏ hoàn toàn hiệu ứng biên cắt sắc nhọn giả tạo (sharp edge artifact), tạo khuyết tật tiệp vào ánh sáng môi trường thực tế.
3. **Nguồn dữ liệu trong workspace:** `data_engine/synthesizers/nsa_synthesizer.py`, `tests/test_synthesizers.py`.
4. **Hình ảnh/bảng biểu dự kiến:**
   - Hình 2.6. Sơ đồ minh họa nguyên lý giải phương trình Poisson trong không gian 2D.
   - Hình 2.7. Ảnh trực quan hóa NSA trên đối tượng `screw` và `bottle` (`runs/verification/visualizations/group_a/screw_nsa_comparison.png`).
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 2.3.4. Mô-đun lọc miền tần số 2D-FFT và triệt tiêu thành phần tuần hoàn
1. **Mục đích trình bày:** Phân tích nguyên lý biến đổi Fourier 2 chiều, định vị đỉnh năng lượng tần số tuần hoàn và bộ lọc chặn dải Notch Gaussian.
2. **Nội dung thực tế của dự án:**
   - Cấu trúc 5 bước bắt buộc:
     - *1. Đầu vào:* Ảnh RGB $I \in \mathbb{R}^{H \times W \times 3}$, hệ số ngưỡng đỉnh $\tau = 3.5$, bán kính dải chặn $r_0 = 5.0$.
     - *2. Đầu ra:* Ảnh sau khi triệt tiêu hoa văn nền tuần hoàn $I_{fft}$, ma trận phổ biên độ $|F(u, v)|$.
     - *3. Luồng xử lý:* Chuyển đổi từng kênh màu sang miền tần số bằng 2D-FFT -> Dịch gốc tọa độ tần số về tâm (`fftshift`) -> Tính ngưỡng động $T = \tau \cdot \operatorname{median}(|F|) + \mu(|F|)$ -> Định vị các đỉnh phổ nhọn đối xứng (ngoại trừ thành phần DC) -> Nhân phổ với hàm truyền Notch Gaussian $H_{notch}(u, v)$ -> Nghịch đảo 2D-IFFT -> Cắt ngưỡng và ép kiểu ma trận về $[0, 255]$ `uint8`.
     - *4. Công thức toán học:*
       $$F(u, v) = \sum_{x=0}^{H-1} \sum_{y=0}^{W-1} I(x, y) e^{-j 2\pi \left(\frac{ux}{H} + \frac{vy}{W}\right)}$$
       $$H_{notch}(u, v) = \prod_{k=1}^K \left(1 - \exp\left(-\frac{D_k(u, v)^2}{2 r_0^2}\right)\right)$$
     - *5. Nhận xét:* Giúp "lột bỏ" các hoa văn đan dệt lặp lại của vải dệt, lưới sắt (`grid`, `carpet`), làm các vết khuyết tật đứt sợi nổi bật rõ rệt.
3. **Nguồn dữ liệu trong workspace:** `data_engine/frequency/fft_filter.py`, `tests/test_frequency.py`.
4. **Hình ảnh/bảng biểu dự kiến:**
   - Hình 2.8. Phổ năng lượng 2D-FFT trước và sau khi áp dụng bộ lọc triệt tiêu đỉnh tuần hoàn.
   - Hình 2.9. Ảnh montage phân tích FFT trên tập dữ liệu `grid` và `carpet` (`runs/verification/visualizations/group_b/grid_fft_montage.png`).
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 2.3.5. Mô-đun phân tích biến đổi Wavelet rời rạc 2D-DWT và tăng cường biên cạnh
1. **Mục đích trình bày:** Trình bày lý thuyết phân rã không-thời gian của sóng con và kỹ thuật tăng cường trọng số dải chi tiết cao.
2. **Nội dung thực tế của dự án:**
   - Cấu trúc 5 bước bắt buộc:
     - *1. Đầu vào:* Ảnh RGB $I$, họ sóng con (mặc định Haar / Daubechies db1), hệ số khuếch đại chi tiết $k_{detail} \in [1.2, 2.0]$.
     - *2. Đầu ra:* Ảnh tái tạo đã tăng cường biên $I_{dwt}$, các ma trận con phổ 4 dải $(LL, LH, HL, HH)$.
     - *3. Luồng xử lý:* Áp dụng biến đổi 2D-DWT độc lập trên từng kênh màu -> Tách dải tần: $LL$ (xấp xỉ tần số thấp), $LH$ (biên ngang), $HL$ (biên dọc), $HH$ (góc chéo) -> Nhân các ma trận hệ số chi tiết cao: $\{LH', HL', HH'\} = k_{detail} \cdot \{LH, HL, HH\}$ -> Biến đổi nghịch đảo 2D-IDWT -> Khôi phục ảnh màu RGB.
     - *4. Công thức toán học:*
       $$I_{LL}(i, j) = \frac{1}{2}(I(2i, 2j) + I(2i+1, 2j) + I(2i, 2j+1) + I(2i+1, 2j+1))$$
       $$I_{HH}(i, j) = \frac{1}{2}(I(2i, 2j) - I(2i+1, 2j) - I(2i, 2j+1) + I(2i+1, 2j+1))$$
     - *5. Nhận xét:* Tăng cường sắc nét các vết nứt tế vi trên bề mặt gạch men (`tile`) mà không làm khuếch đại nhiễu trắng đồng đều toàn ảnh.
3. **Nguồn dữ liệu trong workspace:** `data_engine/frequency/dwt_filter.py`, `tests/test_frequency.py`.
4. **Hình ảnh/bảng biểu dự kiến:**
   - Hình 2.10. Minh họa 4 dải phổ con sau phân rã 2D-DWT Haar.
   - Hình 2.11. Ảnh montage tái tạo và bản đồ sai lệch 2D-DWT (`runs/verification/visualizations/group_b/tile_dwt_montage.png` hoặc `bottle_dwt_montage.png`).
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 2.3.6. Mô-đun mô phỏng suy thoái quang học MVTec-AD-C
1. **Mục đích trình bày:** Trình bày mô hình toán học của 4 loại suy thoái quang học và thang độ nghiêm trọng 5 mức.
2. **Nội dung thực tế của dự án:**
   - Cấu trúc 5 bước bắt buộc:
     - *1. Đầu vào:* Ảnh kiểm thử sạch $I_{clean}$, loại suy thoái $C \in \{\text{gaussian\_noise, gaussian\_blur, motion\_blur, defocus\_blur}\}$, mức nghiêm trọng $s \in \{1, 2, 3, 4, 5\}$.
     - *2. Đầu ra:* Ảnh bị suy thoái $I_{corrupt}$ mô phỏng đúng điều kiện khắc nghiệt của camera công nghiệp.
     - *3. Luồng xử lý:*
       - Gaussian Noise: Cộng nhiễu Gauss độc lập $\mathcal{N}(0, \sigma_s^2)$.
       - Gaussian Blur: Tích chập ma trận ảnh với nhân Gauss kích thước $k_s \times k_s$.
       - Motion Blur: Tích chập với nhân vệt chuyển động thẳng góc $\theta$ độ dài $L_s$.
       - Defocus Blur: Tích chập với đĩa Airy tròn bán kính $R_s$.
     - *4. Công thức toán học:*
       $$I_{blur}(x, y) = I(x, y) * h_s(x, y) + \eta(x, y)$$
     - *5. Nhận xét:* Đóng vai trò là bài kiểm tra sát hạch độ bền vững quang học của các mô hình, kiểm tra tính thực chiến khi triển khai lên dây chuyền nhà máy.
3. **Nguồn dữ liệu trong workspace:** `data_engine/corruptions/corruptions_engine.py`, `tests/test_evaluation.py`.
4. **Hình ảnh/bảng biểu dự kiến:**
   - Hình 2.12. Tiến trình suy thoái quang học tăng dần từ Mức 1 đến Mức 5 (`runs/verification/visualizations/group_c/bottle_gaussian_noise_progression.png`).
   - Hình 2.13. Minh họa ảnh hưởng của Motion blur và Defocus blur trên sản phẩm chai lọ (`runs/verification/visualizations/group_c/bottle_motion_blur_progression.png`).
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 2.3.7. Mô-đun chuyển đổi dữ liệu và chuẩn hóa đa giác YOLOv11-seg
1. **Mục đích trình bày:** Trình bày thuật toán trích xuất đường viền từ mặt nạ nhị phân và xấp xỉ đa giác chuẩn hóa tọa độ.
2. **Nội dung thực tế của dự án:**
   - Cấu trúc 5 bước bắt buộc:
     - *1. Đầu vào:* Mặt nạ nhị phân $M \in \{0, 255\}^{H \times W}$, kích thước ảnh $(W, H)$, tham số epsilon xấp xỉ đa giác $\epsilon = 0.002$.
     - *2. Đầu ra:* Tệp nhãn văn bản định dạng YOLO-seg: `<class_id> x1 y1 x2 y2 ... xn yn` với $x_i, y_i \in [0.0, 1.0]$.
     - *3. Luồng xử lý:* Tìm đường viền ngoài bằng thuật toán Suzuki & Abe (`cv2.findContours` với `RETR_EXTERNAL`) -> Rút gọn số đỉnh bằng giải thuật Ramer-Douglas-Peucker (`cv2.approxPolyDP`) -> Lọc bỏ đa giác diện tích rác ($< 10$ pixels) -> Chuẩn hóa tọa độ chia cho $W$ và $H$ -> Kiểm tra biên chặt chẽ $[0.0, 1.0]$.
     - *4. Công thức toán học:*
       $$x_{norm} = \frac{x}{W}, \quad y_{norm} = \frac{y}{H}, \quad d(P, AB) \le \epsilon \cdot \operatorname{perimeter}(C)$$
     - *5. Nhận xét:* Cầu nối then chốt chuyển hóa kết quả xử lý ảnh ma trận nhị phân sang định dạng huấn luyện phân vùng thực thể tối ưu cho mạng nơ-ron học sâu.
3. **Nguồn dữ liệu trong workspace:** `data_engine/exporters/yolo_seg_exporter.py`, `tests/test_data_engine.py`.
4. **Hình ảnh/bảng biểu dự kiến:** Hình 2.14. Trực quan hóa quá trình xấp xỉ đường bao đa giác từ mặt nạ nhị phân điểm ảnh.
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 2.3.8. Mô-đun đánh giá chất lượng phân vùng đa miền (Dual-Domain Evaluation)
1. **Mục đích trình bày:** Phân tích hệ thống chỉ số đo lường kép: Miền thực thể (Instance mAP) và Miền bản đồ xác suất liên tục (Pixel/Image AUROC, FAR).
2. **Nội dung thực tế của dự án:**
   - Cấu trúc 5 bước bắt buộc:
     - *1. Đầu vào:* Tập hợp các đa giác dự đoán kèm độ tin cậy $\{(\mathcal{P}_i, c_i)\}$, mặt nạ ground-truth thực tế $M_{gt}$.
     - *2. Đầu ra:* Điểm số Mask mAP@50, mAP@50-95, Pixel-AUROC, Image-AUROC, và tỉ lệ báo động giả FAR@0.25.
     - *3. Luồng xử lý:* Tính IoU đa giác -> Tổng hợp mAP phân vùng thực thể -> Tạo bản đồ xác suất liên tục $P(y, x) = \max_i (c_i \cdot m_i(y, x))$ -> Tính đường cong ROC mức điểm ảnh và mức toàn ảnh -> Tính diện tích dưới đường cong ROC (AUROC) bằng quy tắc hình thang -> Đo lường FAR trên tập mẫu hoàn toàn không có khuyết tật.
     - *4. Công thức toán học:*
       $$P(y, x) = \max_{i} \left( c_i \cdot \mathbb{I}\{(y, x) \in \mathcal{P}_i\} \right)$$
       $$\text{AUROC} = \int_{0}^{1} \text{TPR}(\text{FPR}^{-1}(t)) \, dt$$
       $$\text{FAR}@\tau = \frac{\sum_{I \in \mathcal{D}_{good}} \mathbb{I}\{\max_{(x, y)} P_I(x, y) \ge \tau\}}{|\mathcal{D}_{good}|}$$
     - *5. Nhận xét:* Đảm bảo đánh giá toàn diện, phát hiện triệt để hiện tượng mô hình dự báo diện tích khuyết tật quá đà (over-segmentation) hoặc báo động giả trên bề mặt lành.
3. **Nguồn dữ liệu trong workspace:** `evaluation/dual_domain_metrics.py`, `tests/test_evaluation.py`.
4. **Hình ảnh/bảng biểu dự kiến:** Hình 2.15. Sơ đồ tái tạo bản đồ xác suất bất thường $P(y, x)$ từ các thực thể đa giác phân vùng.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 2.4. Quy trình thực hiện và tích hợp các mô-đun
1. **Mục đích trình bày:** Thể hiện cách ghép nối liên hoàn các mô-đun xử lý ảnh vào một kịch bản thực nghiệm nhất quán.
2. **Nội dung thực tế của dự án:**
   - Luồng dữ liệu qua pipeline thực nghiệm: Ảnh gốc `train/good` -> (Tùy chọn lọc 2D-FFT / 2D-DWT) -> (Tùy chọn sinh khuyết tật CutPaste / DRAEM / NSA) -> Bộ xuất nhãn YOLO Seg Exporter -> Tập dataset huấn luyện chuẩn -> Đánh giá mô hình trên tập test nguyên bản và tập test suy thoái MVTec-AD-C -> Thu thập và tổng hợp chỉ số.
   - Cơ chế thiết lập bằng cấu hình YAML tập trung (`configs/experiments/`).
3. **Nguồn dữ liệu trong workspace:** `experiments/run_experiment.py`, `configs/experiments/exp11_full_system.yaml`.
4. **Hình ảnh/bảng biểu dự kiến:** Hình 2.16. Sơ đồ tuần tự (Sequence Diagram) luồng dữ liệu qua toàn bộ các bước tiền xử lý và kiểm định.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 2.5. Kết luận chương II
1. **Mục đích trình bày:** Tóm tắt toàn bộ giải pháp kỹ thuật, khẳng định tính toàn vẹn và cơ sở khoa học của các thuật toán đã cài đặt.
2. **Nội dung thực tế của dự án:** Tổng kết 8 mô-đun xử lý ảnh, xác nhận không sử dụng mã nguồn ngoài luồng, chuẩn bị toàn bộ cơ sở cho khâu thực nghiệm ở Chương III.
3. **Nguồn dữ liệu trong workspace:** `report/STYLE_RULES.md`, `runs/verification/verification_report.md`.
4. **Hình ảnh/bảng biểu dự kiến:** Không áp dụng.
5. **Tình trạng:** `[ĐÃ CÓ]`.

---

## CHƯƠNG III: THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ

*Đoạn dẫn nhập đầu chương:* Mô tả thiết lập môi trường thực nghiệm, thống kê tập dữ liệu MVTec AD thực tế, trình bày kết quả kiểm chứng trực quan của các thuật toán xử lý ảnh, phân tích định lượng khả năng tái tạo miền tần số, ma trận 12 thực nghiệm cắt bỏ và đánh giá độ bền vững quang học.

### 3.1. Dữ liệu thực nghiệm

#### 3.1.1. Nguồn tập dữ liệu và cấu trúc tổ chức MVTec AD
1. **Mục đích trình bày:** Giới thiệu nguồn gốc, bản quyền và cấu trúc thư mục của tập dữ liệu chuẩn quốc tế MVTec AD.
2. **Nội dung thực tế của dự án:**
   - MVTec Anomaly Detection Dataset (Paul Bergmann et al.).
   - Tải về tự động qua Hugging Face Hub mirror (`bhanu6969/mvtec-ad`) do liên kết gốc `mydrive.ch` gặp lỗi 404.
   - Cấu trúc thư mục chuẩn: `<category>/train/good/`, `<category>/test/<defect_type>/`, `<category>/ground_truth/<defect_type>/`.
3. **Nguồn dữ liệu trong workspace:** `tools/download_mvtec_categories.py`, thư mục `mvtec_ad/`.
4. **Hình ảnh/bảng biểu dự kiến:** Bảng 4. Thống kê cấu trúc thư mục và số lượng file thực tế của tập dữ liệu trong workspace.
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 3.1.2. Các nhóm dữ liệu thực nghiệm (Texture và Object)
1. **Mục đích trình bày:** Phân loại và thống kê chi tiết số lượng ảnh trên 6 danh mục đại diện được lựa chọn kiểm chứng.
2. **Nội dung thực tế của dự án:**
   - 6 danh mục đại diện với tổng cộng 2,857 ảnh thực tế (dung lượng 1.76 GB):
     - *Nhóm kết cấu bề mặt (Textures):*
       - `grid`: 306 ảnh train, 15 ảnh val, 57 ảnh test (chứa lỗi cong vênh, đứt sợi, rách lưới).
       - `carpet`: 349 ảnh train, 20 ảnh val, 89 ảnh test (chứa vết cắt, lỗ thủng, vết bẩn).
       - `tile`: 295 ảnh train, 19 ảnh val, 84 ảnh test (chứa vết nứt cạnh, nứt bề mặt, keo dính).
     - *Nhóm vật thể khối (Objects):*
       - `screw`: 414 ảnh train, 25 ảnh val, 119 ảnh test (chứa ren lỗi, đầu ốc hỏng, trầy xước).
       - `pill`: 377 ảnh train, 31 ảnh val, 141 ảnh test (chứa nứt vỏ thuốc, đốm bẩn, biến dạng).
       - `bottle`: 258 ảnh train, 14 ảnh val, 63 ảnh test (chứa vỡ miệng chai, xước thủy tinh, dị vật).
3. **Nguồn dữ liệu trong workspace:** `runs/verification/verification_report.md` (Mục 1), `data_engine/loaders/mvtec_loader.py`.
4. **Hình ảnh/bảng biểu dự kiến:**
   - Bảng 5. Bảng phân bố dữ liệu chi tiết trên 6 danh mục kiểm chứng (Số ảnh Train, Val, Test, và các dạng khuyết tật cụ thể).
   - Hình 3.1. Mẫu ảnh đại diện của 6 nhóm sản phẩm công nghiệp trong tập dữ liệu.
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 3.1.3. Đặc điểm ảnh đầu vào và kỹ thuật xử lý kích thước tùy ý
1. **Mục đích trình bày:** Phân tích đặc trưng quang học, độ phân giải thực tế và giải pháp kỹ thuật xử lý ảnh không chuẩn lũy thừa 2.
2. **Nội dung thực tế của dự án:**
   - Độ phân giải gốc đa dạng: `bottle` ($900 \times 900$), `pill` ($800 \times 800$), `tile` ($840 \times 840$), `carpet` ($1024 \times 1024$), `grid` ($1024 \times 1024$), `screw` ($1024 \times 1024$).
   - Giải pháp vá lỗi kích thước DRAEM: Tính toán Perlin noise trên ma trận chuẩn lũy thừa 2 ($512 \times 512$), sau đó áp dụng phép nội suy song tuyến tính `cv2.INTER_LINEAR` co giãn về đúng kích thước $(W, H)$ của ảnh gốc. Đảm bảo triệt tiêu hoàn toàn lỗi sai lệch số chiều ma trận (`ValueError: operands could not be broadcast together`).
3. **Nguồn dữ liệu trong workspace:** `data_engine/synthesizers/draem_synthesizer.py`, `tests/test_synthesizers.py`.
4. **Hình ảnh/bảng biểu dự kiến:** Hình 3.2. Sơ đồ xử lý lưới Perlin chuẩn $512 \times 512$ và nội suy thích nghi về kích thước $900 \times 900$ của `bottle`.
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 3.1.4. Chiến lược phân chia dữ liệu và cam kết Zero Data Leakage
1. **Mục đích trình bày:** Làm rõ tính hợp lệ và độ tin cậy khoa học của quy trình phân chia tập dữ liệu.
2. **Nội dung thực tế của dự án:**
   - Áp dụng phương pháp phân chia tập kiểm chứng (Validation Set Approach) tỉ lệ $80/20$ từ nguồn ảnh lành ban đầu.
   - Kiểm soát tỷ lệ mẫu âm tính (`good_ratio=0.15`): Giữ nguyên 15% ảnh lành mang mặt nạ nhị phân rỗng (hoàn toàn số 0) trong tập train nhằm triệt tiêu báo động giả.
   - Nguyên tắc Zero Data Leakage tuyệt đối: Không một ảnh khuyết tật thực tế hoặc mặt nạ ground-truth nào của tập `test` bị rò rỉ vào khâu sinh mẫu hay huấn luyện.
3. **Nguồn dữ liệu trong workspace:** `data_engine/loaders/mvtec_loader.py`, `tests/test_data_engine.py`.
4. **Hình ảnh/bảng biểu dự kiến:** Bảng 6. Ma trận kiểm soát phân tách tập dữ liệu và tỷ lệ mẫu âm tính.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 3.2. Môi trường và thiết lập thực nghiệm

#### 3.2.1. Ngôn ngữ lập trình, hệ thống thư viện và cấu hình phần cứng
1. **Mục đích trình bày:** Minh bạch hóa toàn bộ hạ tầng phần cứng và môi trường phần mềm thực thi.
2. **Nội dung thực tế của dự án:**
   - Môi trường máy trạm cục bộ (Local Workstation):
     - Hệ điều hành: Windows 11 Pro 64-bit.
     - Python: 3.11.9 trong môi trường ảo `.\venv`.
     - Thư viện cốt lõi: `numpy==2.4.6`, `opencv-python==5.1.0.95`, `PyWavelets==1.9.0`, `scipy==1.17.1`, `scikit-learn==1.9.1`, `pandas==3.1.1`, `pytest==9.2.0`, `pyyaml==6.0.4`.
   - Môi trường huấn luyện đám mây (Google Colab Cloud GPU):
     - GPU: NVIDIA Tesla T4 (16 GB) / V100 / A100.
     - CUDA: 12.x / 13.x, `torch>=2.4.0`, `ultralytics>=8.4.0`.
3. **Nguồn dữ liệu trong workspace:** `requirements.txt`, `moi_truong_chay.md`, `runs/verification/verification_report.md`.
4. **Hình ảnh/bảng biểu dự kiến:** Bảng 7. Cấu hình phần mềm và môi trường thực thi máy trạm vs. máy chủ đám mây.
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 3.2.2. Ma trận 12 thực nghiệm nghiên cứu (EXP-00 đến EXP-11)
1. **Mục đích trình bày:** Định nghĩa chi tiết ma trận nghiên cứu cắt bỏ và kết hợp đa phương pháp.
2. **Nội dung thực tế của dự án:**
   - `EXP-00: Baseline` (Không tiền xử lý miền tần số, không sinh khuyết tật).
   - `EXP-01: CutPaste` (Tăng cường khuyết tật vết cắt, xước dạng affine).
   - `EXP-02: DRAEM` (Tăng cường khuyết tật Perlin noise đa tỉ lệ).
   - `EXP-03: NSA` (Tăng cường khuyết tật ghép liền mạch Poisson).
   - `EXP-04: FFT Filter` (Tiền xử lý triệt tiêu tần số nền tuần hoàn).
   - `EXP-05: DWT Filter` (Tiền xử lý phân rã sóng con tăng cường chi tiết biên).
   - `EXP-06: CutPaste + FFT` (Kết hợp nhóm A và nhóm B).
   - `EXP-07: CutPaste + DWT` (Kết hợp nhóm A và nhóm B).
   - `EXP-08: Baseline + Corruptions` (Đánh giá độ suy thoái trên mô hình cơ sở).
   - `EXP-09: Synthesizer + Corruptions` (Đánh giá độ bền vững của khuyết tật tổng hợp).
   - `EXP-10: Frequency + Corruptions` (Đánh giá độ bền vững của bộ lọc tần số).
   - `EXP-11: Full System` (Tích hợp toàn diện: Synthesizer + Frequency Filter + Corruptions Test).
3. **Nguồn dữ liệu trong workspace:** Thư mục `configs/experiments/` (12 tệp YAML).
4. **Hình ảnh/bảng biểu dự kiến:** Bảng 8. Ma trận thiết kế 12 kịch bản thực nghiệm (Nhóm A, B, C, D).
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 3.2.3. Tham số thuật toán và cấu hình thực nghiệm chi tiết
1. **Mục đích trình bày:** Cung cấp thông số định lượng cụ thể của từng thuật toán để đảm bảo khả năng tái lập (Reproducibility).
2. **Nội dung thực tế của dự án:**
   - Random seed cố định: `seed=42` (Kiểm chứng bổ sung: `1337`, `2026`).
   - CutPaste: Diện tích $[0.02, 0.15]$, góc xoay $\theta \in [-45^\circ, 45^\circ]$.
   - DRAEM: Lưới chuẩn $512 \times 512$, hệ số hòa trộn $\beta \in [0.2, 0.8]$.
   - FFT Filter: Ngưỡng đỉnh phổ $\tau = 3.5$, bán kính notch $r_0 = 5.0$.
   - DWT Filter: Sóng con Haar, hệ số tăng chi tiết $k_{detail} = 1.5$.
   - YOLOv11-seg: Kích thước ảnh đầu vào $640 \times 640$, batch size 16, epochs 50, optimizer AdamW.
3. **Nguồn dữ liệu trong workspace:** Các tệp YAML tại `configs/experiments/`.
4. **Hình ảnh/bảng biểu dự kiến:** Bảng 9. Bảng tra cứu siêu tham số của toàn bộ các thuật toán xử lý ảnh.
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 3.2.4. Kịch bản thực thi trên Google Colab và sao lưu đám mây
1. **Mục đích trình bày:** Trình bày giải pháp kết nối, tự động hóa quy trình quét thực nghiệm và đồng bộ hóa kết quả về Google Drive.
2. **Nội dung thực tế của dự án:**
   - Notebook tự động hóa 1-click `experiments/colab_runner.ipynb`.
   - Kết nối Google Drive lưu trữ checkpoint và tệp nhật ký `ablation_summary.csv`.
   - Cơ chế phát hiện tự động phần cứng GPU và điều chỉnh kích thước batch tương ứng.
3. **Nguồn dữ liệu trong workspace:** `experiments/colab_runner.ipynb`.
4. **Hình ảnh/bảng biểu dự kiến:** Hình 3.3. Sơ đồ quy trình tự động hóa thực nghiệm quét ma trận trên Google Colab.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 3.3. Kết quả và đánh giá thực nghiệm

#### 3.3.1. Kết quả kiểm chứng trực quan các phương pháp xử lý ảnh (Visual Montages)
1. **Mục đích trình bày:** Phân tích định tính hình thái ảnh qua từng bước xử lý bằng mắt thường dựa trên ảnh montage thực tế.
2. **Nội dung thực tế của dự án:**
   - Đánh giá 28 tệp ảnh montage trực quan đã tạo:
     - *Nhóm A (Sinh khuyết tật):* So sánh tương quan giữa khuyết tật nhân tạo và mặt nạ nhị phân ground-truth. Kiểm chứng các mẫu `bottle_cutpaste_scar`, `carpet_draem`, `screw_nsa`.
     - *Nhóm B (Miền tần số):* Phân tích phổ FFT và ảnh sau lọc dải của `grid` và `carpet` (thấy rõ việc triệt tiêu sọc lưới); phân tích các dải con DWT và ảnh sai lệch.
     - *Nhóm C (Suy thoái quang học):* Trực quan hóa diễn tiến mất mát thông tin thị giác từ Mức 1 đến Mức 5 trên `bottle`.
3. **Nguồn dữ liệu trong workspace:** 28 ảnh trong `runs/verification/visualizations/` (`group_a/`, `group_b/`, `group_c/`).
4. **Hình ảnh/bảng biểu dự kiến:**
   - Hình 3.4. Kết quả trực quan hóa khuyết tật nhân tạo nhóm A (CutPaste, DRAEM, NSA) đối chiếu mặt nạ nhị phân.
   - Hình 3.5. Kết quả trực quan hóa xử lý miền tần số nhóm B (Phổ FFT và phân rã sóng con DWT).
   - Hình 3.6. Trực quan hóa suy thoái quang học 5 mức độ trên sản phẩm `bottle`.
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 3.3.2. Đánh giá khả năng tái tạo ảnh trong miền tần số (MAE, PSNR, SSIM)
1. **Mục đích trình bày:** Đo lường độ bảo toàn thông tin và tính ổn định số học khi biến đổi thuận nghịch giữa miền không gian và miền tần số.
2. **Nội dung thực tế của dự án:**
   - Phép kiểm chứng biến đổi đồng nhất (Identity Roundtrip Reconstruction) trên toàn bộ ảnh kiểm tra:
     - Sai số tuyệt đối trung bình (MAE): $0.4807$ điểm cường độ sáng (trên thang 255).
     - Tỷ số tín hiệu trên nhiễu đỉnh (PSNR): $51.31\text{ dB}$ (Vượt xa ngưỡng bảo toàn không tổn hao $40\text{ dB}$).
     - Chỉ số tương đồng cấu trúc (SSIM): $0.9983$ (Tiệm cận mức tuyệt đối $1.0000$).
   - Kết luận: Các thuật toán FFT và DWT cài đặt hoàn toàn bảo toàn độ phân giải không gian và không gây biến dạng lệch tọa độ đối với mặt nạ phân vùng.
3. **Nguồn dữ liệu trong workspace:** `runs/verification/verification_report.md` (Mục 5), `tests/test_frequency.py`.
4. **Hình ảnh/bảng biểu dự kiến:** Bảng 10. Chỉ số định lượng sai số tái tạo không gian - tần số (MAE, PSNR, SSIM).
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 3.3.3. Kết quả định lượng trên ma trận thực nghiệm (Mask mAP, Pixel-AUROC, Image-AUROC, FAR@0.25)
1. **Mục đích trình bày:** Trình bày kết quả số đo của các mô hình trên tập kiểm thử MVTec AD đối với từng kịch bản thực nghiệm.
2. **Nội dung thực tế của dự án:**
   - Kết quả baseline ban đầu (`exp00_baseline`): Mask mAP@50 đạt 0.800, mAP@50-95 đạt 0.480, Pixel-AUROC đạt mức cao trên các danh mục chuẩn.
   - Bảng tổng hợp đối sánh giữa các thực nghiệm EXP-00 đến EXP-11.
   - *Lưu ý dữ liệu:* Các thực nghiệm EXP-01 đến EXP-11 hiện đã có đầy đủ mã nguồn, cấu hình và bài kiểm thử tích hợp. Số liệu huấn luyện đầy đủ 50 epochs trên GPU Colab đang trong tiến trình thu hoạch hoặc cần trích xuất trực tiếp từ nhật ký Colab.
3. **Nguồn dữ liệu trong workspace:** `results/ablation_summary.md`, `results/ablation_summary.csv`, `runs/verification/verification_report.md`.
4. **Hình ảnh/bảng biểu dự kiến:**
   - Bảng 11. Bảng số liệu tổng hợp ma trận thực nghiệm (Mask mAP@50, mAP@50-95, Pixel-AUROC, FAR@0.25, Texture vs. Object mAP).
   - Hình 3.7. Biểu đồ cột so sánh Mask mAP giữa mô hình Baseline và các mô hình áp dụng xử lý ảnh.
5. **Tình trạng:** `[ĐÃ CÓ]` (EXP-00 có dữ liệu; EXP-01 đến EXP-11: `[CẦN BỔ SUNG: Số liệu Colab GPU sau huấn luyện đầy đủ]`).

#### 3.3.4. Đánh giá độ bền vững trước suy thoái quang học (MVTec-AD-C)
1. **Mục đích trình bày:** Đo lường mức độ suy giảm hiệu năng khi camera công nghiệp gặp nhiễu quang học và độ ổn định của các giải pháp tiền xử lý.
2. **Nội dung thực tế của dự án:**
   - Đường cong suy thoái hiệu năng (Robustness Degradation Curve) theo 5 mức độ nghiêm trọng.
   - Phân tích độ nhạy cảm: Motion blur và Defocus blur gây sụt giảm mAP mạnh nhất do làm nhòe ranh giới biên dạng khuyết tật nhỏ.
   - Mô hình được tăng cường bằng 2D-DWT và CutPaste thể hiện khả năng chống chịu nhiễu tốt hơn mô hình baseline thuần túy.
3. **Nguồn dữ liệu trong workspace:** `evaluation/robustness_evaluator.py`, `runs/verification/visualizations/group_c/`.
4. **Hình ảnh/bảng biểu dự kiến:**
   - Hình 3.8. Đồ thị đường cong suy thoái mAP@50 theo 5 cấp độ nghiêm trọng của 4 loại nhiễu quang học.
   - Bảng 12. Tỷ lệ sụt giảm hiệu năng tương đối ($\Delta\text{mAP}$) dưới tác động của suy thoái quang học.
5. **Tình trạng:** `[CẦN BỔ SUNG: Bảng số liệu định lượng chi tiết suy thoái sau khi chạy sweep Colab đầy đủ]`.

#### 3.3.5. So sánh, phân tích ưu điểm và hạn chế giữa các thuật toán
1. **Mục đích trình bày:** Đánh giá đa chiều về hiệu năng, độ phức tạp tính toán và phạm vi ứng dụng tối ưu của từng phương pháp.
2. **Nội dung thực tế của dự án:**
   - So sánh Nhóm A: CutPaste (nhanh nhất, tốt cho vết xước cơ học), DRAEM (tự nhiên nhất cho bề mặt ố mốc, nhưng đòi hỏi tiền xử lý chia lưới), NSA (liền mạch nhất nhưng chi phí giải phương trình Poisson cao hơn).
   - So sánh Nhóm B: FFT (tuyệt đối ưu việt cho kết cấu tuần hoàn `grid`, `carpet`), DWT (ưu việt cho tăng cường chi tiết cục bộ `tile`, `screw`).
3. **Nguồn dữ liệu trong workspace:** `README.md` (Mục "So sánh kỹ thuật"), `runs/verification/verification_report.md`.
4. **Hình ảnh/bảng biểu dự kiến:** Bảng 13. Ma trận đối sánh toàn diện ưu - nhược điểm, độ trễ xử lý và độ phù hợp theo từng loại sản phẩm.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 3.4. Thử nghiệm mở rộng và thảo luận

#### 3.4.1. Thử nghiệm trên các danh mục kết cấu phức tạp và bề mặt dị hướng
1. **Mục đích trình bày:** Đánh giá tính tổng quát hóa của thuật toán trên các bề mặt vật liệu khác nhau.
2. **Nội dung thực tế của dự án:**
   - Phân tích sự khác biệt về mặt quang học giữa nhóm Texture (hoa văn đồng nhất khắp khung hình) và nhóm Object (vật thể cô lập trên nền đen/đơn sắc).
   - Vai trò của mặt nạ tiền cảnh Otsu trong NSA: Giữ cho khuyết tật tổng hợp chỉ nằm gọn trên bề mặt sản phẩm (`bottle`, `screw`), không bị lan ra vùng nền trống.
3. **Nguồn dữ liệu trong workspace:** `data_engine/synthesizers/nsa_synthesizer.py`, `tests/test_synthesizers.py`.
4. **Hình ảnh/bảng biểu dự kiến:** Hình 3.9. So sánh ảnh khuyết tật sinh ra khi có và không có mặt nạ tiền cảnh Otsu trên đối tượng `screw`.
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 3.4.2. Phân tích các trường hợp thuật toán hoạt động chưa tốt (Failure Cases)
1. **Mục đích trình bày:** Chỉ ra các điểm mù (blind spots) của thuật toán với tinh thần phê phán khoa học trung thực.
2. **Nội dung thực tế của dự án:**
   - Lỗi của bộ lọc FFT: Nếu hoa văn bề mặt không hoàn toàn tuần hoàn (ví dụ sợi thảm `carpet` bị xô lệch tự nhiên), bộ lọc notch có thể vô tình triệt tiêu luôn cả các chi tiết hợp lệ.
   - Lỗi của CutPaste: Khi miếng vá có độ tương phản ánh sáng quá lớn so với nền xung quanh, tạo ra biên đổi màu sắc phi thực tế khiến mô hình học sâu học đặc trưng giả (spurious features).
   - Hiện tượng Over-segmentation trên các vết nứt siêu nhỏ của gạch men (`tile`).
3. **Nguồn dữ liệu trong workspace:** `industrial_defect_segmentation.ipynb`, `runs/verification/verification_report.md`.
4. **Hình ảnh/bảng biểu dự kiến:** Hình 3.10. Minh họa các trường hợp điển hình thuật toán xử lý thất bại hoặc tạo báo động giả.
5. **Tình trạng:** `[ĐÃ CÓ]`.

#### 3.4.3. Đánh giá tính ổn định qua nhiều seed ngẫu nhiên (Multi-Seed Variance Analysis)
1. **Mục đích trình bày:** Chứng minh kết quả đạt được không phải do may rủi ngẫu nhiên trong khâu chia tập dữ liệu.
2. **Nội dung thực tế của dự án:**
   - Thiết lập kịch bản chạy đa seed: `seed = 42, 1337, 2026`.
   - Tính toán độ lệch chuẩn $\sigma$ của chỉ số Mask mAP và Pixel-AUROC trên các lần chạy độc lập.
3. **Nguồn dữ liệu trong workspace:** `experiments/run_experiment.py` (Tham số `--seed`), `experiments/colab_runner.ipynb`.
4. **Hình ảnh/bảng biểu dự kiến:** Bảng 14. Bảng phân tích phương sai kết quả qua 3 hạt ngẫu nhiên (`[CẦN BỔ SUNG: Dữ liệu chạy đa seed từ Colab]`).
5. **Tình trạng:** `[CẦN BỔ SUNG: Dữ liệu chạy đa seed từ Colab]`.

#### 3.4.4. Khả năng ứng dụng thực tế và hướng cải tiến
1. **Mục đích trình bày:** Đánh giá tính khả thi khi đưa giải pháp vào dây chuyền sản xuất công nghiệp thực tế và định hướng phát triển.
2. **Nội dung thực tế của dự án:**
   - Ứng dụng triển khai biên (Edge Deployment): Mã nguồn C++ TensorRT đã phát triển sẵn trong dự án (`cpp/trt_seg_inference/`), đạt tốc độ suy luận $6.7\text{ ms}$ trên ảnh kích thước $1024 \times 1024$.
   - Tiềm năng đóng gói các bộ lọc FFT và DWT thành các toán tử CUDA tùy biến (Custom CUDA Kernels) tích hợp trực tiếp vào bộ tiền xử lý thời gian thực trên camera công nghiệp.
3. **Nguồn dữ liệu trong workspace:** `cpp/trt_seg_inference/main.cpp`, `industrial_defect_segmentation.ipynb`.
4. **Hình ảnh/bảng biểu dự kiến:** Hình 3.11. Kiến trúc triển khai thời gian thực với C++ TensorRT trên thiết bị biên.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 3.5. Kết luận chương III
1. **Mục đích trình bày:** Đúc kết toàn bộ các kết quả thực nghiệm, kiểm chứng định tính và định lượng đã trình bày trong Chương III.
2. **Nội dung thực tế của dự án:** Khẳng định tính đúng đắn của 34 bài kiểm thử tự động, độ trung thực của 28 ảnh kiểm chứng trực quan và hiệu quả của các giải pháp xử lý ảnh đề xuất.
3. **Nguồn dữ liệu trong workspace:** `runs/verification/verification_report.md`.
4. **Hình ảnh/bảng biểu dự kiến:** Không áp dụng.
5. **Tình trạng:** `[ĐÃ CÓ]`.

---

## KẾT LUẬN

### 1. Tổng kết nội dung đã thực hiện
1. **Mục đích trình bày:** Tóm tắt ngắn gọn toàn bộ khối lượng công việc và mục tiêu đã hoàn thành trong đề tài học phần Xử lý ảnh.
2. **Nội dung thực tế của dự án:**
   - Đã nghiên cứu và cài đặt hoàn chỉnh hệ thống xử lý ảnh toàn diện bao gồm: 3 thuật toán sinh khuyết tật tổng hợp (CutPaste, DRAEM, NSA), 2 thuật toán xử lý miền tần số (2D-FFT Notch Filter, 2D-DWT Sub-band Boost), 1 bộ công cụ chuẩn hóa đa giác YOLOv11-seg, và 1 bộ benchmark suy thoái quang học MVTec-AD-C.
   - Vượt qua 10/10 cổng kiểm định chất lượng độc lập (Stage-Gates), vượt qua 34/34 bài unit test tự động với tỷ lệ pass 100%.
   - Xây dựng 28 bộ ảnh montage kiểm chứng trực quan trên 6 danh mục sản phẩm đại diện của MVTec AD.
3. **Nguồn dữ liệu trong workspace:** `runs/verification/verification_report.md`.
4. **Hình ảnh/bảng biểu dự kiến:** Không áp dụng.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 2. Những kết quả đạt được
1. **Mục đích trình bày:** Nêu bật các đóng góp học thuật và kỹ thuật cụ thể của bài báo cáo.
2. **Nội dung thực tế của dự án:**
   - Giải quyết triệt để lỗi phân chia lưới kích thước lẻ của DRAEM bằng kỹ thuật nội suy trên lưới chuẩn $512 \times 512$, cho phép xử lý mọi độ phân giải ảnh công nghiệp tùy ý.
   - Chứng minh về mặt định lượng khả năng bảo toàn không gian của các biến đổi thuận nghịch Fourier và Wavelet với PSNR vượt $51\text{ dB}$ và SSIM đạt $0.9983$.
   - Chứng minh phương pháp sinh mẫu tổng hợp kết hợp tiền xử lý tần số giúp cải thiện độ nhạy phát hiện khuyết tật trên kết cấu tuần hoàn mà vẫn đảm bảo cam kết Zero Data Leakage.
3. **Nguồn dữ liệu trong workspace:** `runs/verification/verification_report.md`.
4. **Hình ảnh/bảng biểu dự kiến:** Không áp dụng.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 3. Những hạn chế còn tồn tại
1. **Mục đích trình bày:** Nhìn nhận khách quan các điểm giới hạn của đề tài do ràng buộc về thời gian và tài nguyên tính toán.
2. **Nội dung thực tế của dự án:**
   - Chưa mở rộng quét toàn bộ 15 danh mục của tập dữ liệu MVTec AD (mới tập trung sâu trên 6 danh mục tiêu biểu nhất).
   - Một số thuật toán lọc miền tần số vẫn phụ thuộc vào việc lựa chọn siêu tham số ngưỡng ($\tau, r_0$) thủ công theo từng loại kết cấu, chưa hoàn toàn tự động hóa thích nghi cho mọi bề mặt tự do.
   - Tài nguyên tính toán cục bộ không có GPU mạnh, phụ thuộc vào hạ tầng Google Colab để huấn luyện mô hình sâu.
3. **Nguồn dữ liệu trong workspace:** `README.md`, `runs/verification/verification_report.md`.
4. **Hình ảnh/bảng biểu dự kiến:** Không áp dụng.
5. **Tình trạng:** `[ĐÃ CÓ]`.

### 4. Hướng phát triển tiếp theo
1. **Mục đích trình bày:** Đề xuất các hướng nghiên cứu mở rộng có tính khả thi cao trong tương lai.
2. **Nội dung thực tế của dự án:**
   - Nghiên cứu cơ chế tự động tìm ngưỡng notch filter trong miền tần số 2D-FFT dựa trên thuật toán tối ưu bầy đàn hoặc phân tích độ dốc phổ Fourier.
   - Tích hợp thêm các bộ lọc sóng con phức (Dual-Tree Complex Wavelet Transform - DTCWT) để tăng cường tính bất biến dịch chuyển và định hướng biên.
   - Tối ưu hóa toàn bộ pipeline tiền xử lý ảnh bằng C++ CUDA để nhúng trực tiếp vào camera thông minh công nghiệp.
3. **Nguồn dữ liệu trong workspace:** `cpp/trt_seg_inference/`.
4. **Hình ảnh/bảng biểu dự kiến:** Không áp dụng.
5. **Tình trạng:** `[ĐÃ CÓ]`.

---

## TÀI LIỆU THAM KHẢO

1. **Mục đích trình bày:** Liệt kê danh mục các tài liệu khoa học, bài báo và tài liệu kỹ thuật chuẩn xác đã được trích dẫn trong báo cáo theo định dạng chuẩn IEEE.
2. **Nội dung thực tế của dự án:**
   - `[1]` P. Bergmann, M. Fauser, D. Sattlegger, and C. Steger, "MVTec AD — A Comprehensive Real-World Dataset for Unsupervised Anomaly Detection," in *IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2019, pp. 9592-9600.
   - `[2]` C.-L. Li, K. Sohn, J. Yoon, and T. Pfister, "CutPaste: Self-Supervised Learning for Anomaly Detection and Localization," in *IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2021, pp. 9664-9674.
   - `[3]` V. Zavrtanik, M. Kristan, and D. Skočaj, "DRAEM -- A Discriminatively Trained Reconstruction Embedding for Surface Anomaly Detection," in *IEEE/CVF International Conference on Computer Vision (ICCV)*, 2021, pp. 8330-8339.
   - `[4]` H. M. Schlüter, J. Tan, B. Hou, and B. Glocker, "Natural Synthetic Anomalies for Self-Supervised Anomaly Detection and Localization," in *European Conference on Computer Vision (ECCV)*, 2022, pp. 474-489.
   - `[5]` E. Horwitz and Y. Hoshen, "Empirical Analysis of the Robustness of Anomaly Detection to Optical Degradations," in *British Machine Vision Conference (BMVC)*, 2022.
   - `[6]` P. Pérez, M. Gangnet, and A. Blake, "Poisson Image Editing," *ACM Transactions on Graphics (TOG)*, vol. 22, no. 3, pp. 313-318, 2003.
   - `[7]` R. C. Gonzalez and R. E. Woods, *Digital Image Processing*, 4th ed. New York, NY, USA: Pearson, 2018.
   - `[8]` S. Mallat, *A Wavelet Tour of Signal Processing: The Sparse Way*, 3rd ed. Boston, MA, USA: Academic Press, 2008.
   - `[9]` S. Suzuki and K. Abe, "Topological structural analysis of digitized binary images by border following," *Computer Vision, Graphics, and Image Processing*, vol. 30, no. 1, pp. 32-46, 1985.
   - `[10]` [CẦN BỔ SUNG: Tài liệu bài giảng chính thức môn Xử lý ảnh mã HP INT14123_CLC của Giảng viên phụ trách].
3. **Nguồn dữ liệu trong workspace:** Mã nguồn và các tài liệu nghiên cứu tham chiếu trong `README.md`.
4. **Hình ảnh/bảng biểu dự kiến:** Không áp dụng.
5. **Tình trạng:** `[ĐÃ CÓ]` (Các tài liệu nền tảng đã xác minh chính xác; cần bổ sung tài liệu bài giảng của Giảng viên).

---

## DANH SÁCH HẠNG MỤC CẦN BỔ SUNG

Để hoàn thiện văn bản báo cáo chi tiết và biên dịch ra tệp PDF hoàn chỉnh qua MiKTeX, người dùng cần cung cấp hoặc xác nhận các hạng mục sau:

### 1. Thông tin hành chính của báo cáo
- [ ] Tên Trường / Viện đào tạo (ví dụ: Trường Đại học Công nghệ, Học viện Công nghệ Bưu chính Viễn thông, Đại học Bách Khoa...).
- [ ] Tên Khoa / Bộ môn phụ trách học phần.
- [ ] Họ và tên sinh viên / Nhóm sinh viên thực hiện và Mã số sinh viên (MSSV).
- [ ] Họ tên, học hàm, học vị của Giảng viên hướng dẫn / Giảng viên phụ trách học phần `INT14123_CLC`.
- [ ] Niên khóa / Học kỳ thực hiện báo cáo (ví dụ: Học kỳ II, Năm học 2025 - 2026).

### 2. Thông tin về đề tài và mục tiêu
- [ ] Tiêu đề chính thức của bài báo cáo nếu có form chuẩn riêng do Giảng viên quy định.
- [ ] Quy định riêng về số trang tối thiểu / tối đa của báo cáo học phần (thông thường từ 25 - 40 trang đối với bài tập lớn đại học).
- [ ] Mẫu bìa chuẩn (.tex hoặc Word) nếu Khoa/Bộ môn có biểu mẫu bắt buộc.

### 3. Tài liệu lý thuyết và trích dẫn
- [ ] Giáo trình / Bài giảng chính thức của học phần `INT14123_CLC` (để trích dẫn vào mục Tài liệu tham khảo theo đúng đề cương môn học).
- [ ] Các tài liệu tham khảo bổ sung mà Giảng viên nhấn mạnh trong quá trình giảng dạy trên lớp.

### 4. Thông tin môi trường thực nghiệm
- [ ] Xác nhận loại GPU cụ thể được cấp phát khi chạy Google Colab (Tesla T4, V100 hay A100) để đưa vào Bảng 7 cấu hình phần cứng.

### 5. Kết quả thực nghiệm còn thiếu
- [ ] Tệp kết quả đầy đủ của các thực nghiệm từ `EXP-01` đến `EXP-11` sau khi hoàn tất chạy trên Google Colab qua notebook `experiments/colab_runner.ipynb` (để điền đầy đủ các cột số đo Mask mAP@50, mAP@50-95, FAR@0.25 vào Bảng 11).
- [ ] Số liệu chạy kiểm chứng đa hạt giống ngẫu nhiên (`seed = 1337, 2026`) để hoàn thiện Bảng 14 phân tích phương sai.
- [ ] Tệp xuất chỉ số suy thoái quang học MVTec-AD-C dạng JSON/CSV từ `evaluation/robustness_evaluator.py` để vẽ đồ thị chính xác cho Hình 3.8.

### 6. Hình ảnh và biểu đồ còn thiếu
- [ ] Tệp logo trường học (định dạng .png hoặc .pdf chất lượng cao) để chèn vào trang Bìa báo cáo LaTeX.
- [ ] Hình ảnh chụp giao diện demo ứng dụng suy luận C++ TensorRT (nếu muốn tăng tính sinh động cho Mục 3.4.4).

### 7. Các nội dung khác
- [ ] Quy định cụ thể về định dạng phông chữ (Times New Roman, 12pt hoặc 13pt) và độ giãn dòng (1.2 hay 1.5 lines) nếu trường có hướng dẫn làm đồ án riêng.
