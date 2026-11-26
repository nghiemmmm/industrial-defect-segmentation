---
name: ieee-citation-formatting
description: >-
  Quy chuẩn gộp trích dẫn liền kề trong bài báo khoa học LaTeX/IEEE (từ [7],[8] thành [7, 8]
  hoặc [7--9] bằng gói cite và cú pháp \cite{key1, key2}). Kích hoạt khi viết, rà soát hoặc
  định dạng trích dẫn tài liệu tham khảo trong bài báo khoa học.
---

# IEEE Merged Citation Formatting Skill

Quy chuẩn định dạng và gộp trích dẫn nhiều tài liệu tham khảo trong cùng một vị trí câu cho bài báo khoa học LaTeX (`IEEEtran`).

---

## 1. Quy Tắc Cốt Lõi (Core Citation Rules)

1. **Bắt buộc gộp nhiều nguồn trong MỘT lệnh `\cite{...}` duy nhất:**
   - **SAI:** `\cite{ref1}, \cite{ref2}` hoặc `\cite{ref1}\cite{ref2}` (tạo ra `[7], [8]` hoặc `[7][8]`).
   - **ĐÚNG:** `\cite{ref1, ref2}` (tạo ra `[7, 8]` khi cấu hình gói `cite`).
   - Với 3 nguồn trở lên liên tiếp: `\cite{ref1, ref2, ref3}` sẽ tự động rút gọn thành `[7--9]`.

2. **Cấu hình Preamble bắt buộc trong `paper.tex` (`IEEEtran`):**
   - Trong `IEEEtran.cls` gốc (dòng 4380), macro `\@citex` hardcode `\def\@citea{], [}` nên kể cả khi viết `\cite{a, b}` vẫn bị tách thành **`[7], [8]`**.
   - **Cách chuẩn không cần cài thêm gói (chạy 100% offline trên MiKTeX/TeXLive/Overleaf):** Ghi đè `\@citea` trong preamble của `paper.tex`:
     ```latex
     \makeatletter
     \def\@citex[#1]#2{%
       \let\@citea\@empty
       \@cite{\@for\@citeb:=#2\do
         {\@citea\def\@citea{, }%
          \edef\@citeb{\expandafter\@firstofone\@citeb\@empty}%
          \if@filesw\immediate\write\@auxout{\string\citation{\@citeb}}\fi
          \@ifundefined{b@\@citeb}{\mbox{\reset@font\bfseries ?}%
            \G@refundefinedtrue
            \@latex@warning
              {Citation `\@citeb' on page \thepage \space undefined}}%
            {\hbox{\csname b@\@citeb\endcsname}}}}{#1}}
     \makeatother
     ```
   - *(Tùy chọn nếu môi trường có sẵn `cite.sty` và cần tự động nén dải 3+ nguồn `[7--9]`: dùng `\usepackage{cite}` kèm `\renewcommand\citepunct{, }` và `\renewcommand\citedash{--}`).*
   - Kết quả hiển thị trên PDF: `\cite{a, b}` $\rightarrow$ **`[7, 8]`**.

3. **Ngữ cảnh áp dụng trong câu:**
   - Khi nhiều tài liệu cùng chứng minh cho **một mệnh đề chung** (đặt ở cuối cụm/câu), luôn gộp chung vào một lệnh `\cite{k1, k2}`:
     - *Ví dụ:* `...as shown in recent robustness benchmarks \cite{hendrycks2019robustness, chen2023mvtecadc}.` $\rightarrow$ `[7, 8]`.
   - Khi mỗi tài liệu gắn trực tiếp với **tên riêng của phương pháp tương ứng** trong câu liệt kê, vẫn đặt sát tên phương pháp đó:
     - *Ví dụ:* `CutPaste \cite{li2021cutpaste}, DRAEM \cite{zavrtanik2021draem}, and NSA \cite{schluter2022natural}`.

---

## 2. Quy Trình Kiểm Tra Tự Động (Audit & Fix Workflow)

Mỗi khi rà soát hoặc chuẩn hóa trích dẫn trong các tệp `.tex`:

1. **Quét lỗi tách lệnh `\cite` liền kề:**
   - Tìm mọi mẫu `\cite{...}\s*,?\s*\cite{...}` trong toàn bộ `paper/**/*.tex`.
   - Gộp thành `\cite{key1, key2}`.
2. **Kiểm tra cấu hình `\usepackage{cite}` trong `paper/paper.tex`:**
   - Xác nhận có `\usepackage{cite}` kèm `\renewcommand\citepunct{, }` và `\renewcommand\citedash{--}`.
3. **Biên dịch kiểm chứng:**
   - Chạy `pdflatex` + `bibtex` + `pdflatex` × 2, kiểm tra `0` lỗi, `0` undefined citations và xác nhận trên PDF các trích dẫn gộp hiển thị đúng dạng `[7, 8]`.
