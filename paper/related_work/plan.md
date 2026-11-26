# SECTION II: RELATED WORK — KẾ HOẠCH TRIỂN KHAI (ACTION PLAN)

1. Tạo tệp mô-đun `paper/sections/related_work.tex` với 3 tiểu mục II-A, II-B, II-C và đoạn tổng kết định vị (*Positioning*).
2. Thay thế khối Section II nội tuyến trong `paper/paper.tex` bằng `\input{sections/related_work}`.
3. Liên kết đầy đủ các trích dẫn học thuật đã xác thực: `bergmann2019mvtec`, `czimmermann2020visual`, `defard2021padim`, `roth2022towards`, `li2021cutpaste`, `zavrtanik2021draem`, `perlin1985image`, `schluter2022natural`, `perez2003poisson`, `gonzalez2018digital`, `mallat2008wavelet`, `hendrycks2019robustness`, `chen2023mvtecadc`, `ultralytics2024yolo11`.
4. Biên dịch `pdflatex` + `bibtex` + `pdflatex`, kiểm tra 0 lỗi, 0 warning BibTeX, 0 `Overfull \hbox` trong Section II.
5. Cập nhật `paper/related_work/validation.md` và `paper/RoadMap.md` (`VERIFIED`).
