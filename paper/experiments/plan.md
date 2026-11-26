# SECTION IV: EXPERIMENTAL EVALUATION — KẾ HOẠCH TRIỂN KHAI (ACTION PLAN)

1. Tạo tệp mô-đun `paper/sections/experiments.tex` theo Phương án A (kết hợp số liệu thật `extra_eval` + `Table I` và khung bảng Ablation 12 kịch bản sạch chờ nạp kết quả Colab).
2. Thay thế Section IV nội tuyến trong `paper/paper.tex` bằng `\input{sections/experiments}`.
3. Kiểm chứng toán học các giá trị trung bình 6 lớp (`0.854 / 0.524` cho `yolo11l-seg@640`; `0.873 / 0.520` cho `yolo11x-seg@1024`) và FAR trên 467 ảnh lành (`4.50% / 2.14%` và `8.78% / 2.36%`).
4. Biên dịch `pdflatex` + `bibtex` + `pdflatex`, xác nhận 0 lỗi, 0 `Overfull \hbox` trong Section IV.
5. Cập nhật `paper/experiments/validation.md` và `paper/RoadMap.md`.
