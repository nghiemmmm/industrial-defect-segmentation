---
name: github-code-mining
description: >-
  Quy trình tìm kiếm, trích xuất và tái cấu trúc thuật toán nghiên cứu từ các repository mã nguồn mở
  thông qua GitHub MCP Server thành code thuần NumPy/OpenCV cho pipeline xử lý ảnh.
---

# GitHub Code Mining & Algorithm Refactoring Guide

Hướng dẫn chi tiết cách sử dụng `github-mcp-server` để truy vấn paper code, đọc tệp và trích xuất lõi thuật toán.

## 1. Cấu trúc Lệnh Chuẩn của GitHub MCP

### A. Tìm kiếm mã nguồn (`search_code`)
Luôn sử dụng tham số `query` (KHÔNG dùng `q`):
- Tìm hàm cụ thể trong repo chỉ định:
  `query: "<tên_hàm> repo:<owner>/<repo>"`
- Tìm kết hợp nhiều hàm/từ khóa theo ngôn ngữ:
  `query: "\"<keyword1>\" \"<keyword2>\" language:python"`
- Tìm định nghĩa hàm:
  `query: "def <function_name> language:python"`

### B. Tải nội dung tệp (`get_file_contents`)
Yêu cầu đủ 3 tham số:
- `owner`: Tên chủ repo (vd: `VitjanZ`, `hmsch`)
- `repo`: Tên repository (vd: `DRAEM`, `natural-synthetic-anomalies`)
- `path`: Đường dẫn tệp tính từ root repo, không có `/` ở đầu (vd: `perlin.py`, `self_sup_data/self_sup_tasks.py`)

## 2. Xử lý Output Tệp Lớn
Khi GitHub MCP trả về tệp dài, nội dung sẽ được ghi vào file tạm:
`file:///.../.system_generated/steps/<step_id>/output.txt`
-> Sử dụng `read_file` với `StartLine` và `EndLine` (tối đa 150-200 dòng/lần) để đọc trọn vẹn logic thuật toán.

## 3. Quy Tắc Refactor "Clean Core" vào Data Engine
1. **Loại bỏ Framework Bloat**:
   - Loại bỏ `torch.utils.data.Dataset`, `DataLoader`, tensor conversions nếu chỉ phục vụ nạp dữ liệu.
   - Thay thế `iaa` (imgaug) hoặc `torchvision.transforms` bằng toán tử NumPy / OpenCV tương đương.
2. **Bảo đảm tính tương thích NumPy 2.x**:
   - Ép kiểu rõ ràng: `.astype(np.uint8)` cho ảnh và mặt nạ.
   - Mặt nạ nhị phân luôn chuẩn hóa strictly `{0, 255}`.
3. **Bảo toàn giao diện Pipeline**:
   - Nhận vào `Sample` và trả về `Sample` với không gian ảnh $(H, W, 3)$ và mặt nạ $(H, W)$ được căn chỉnh tuyệt đối.

## 4. Khắc Phục Lỗi Giả Định Kích Thước Ảnh Trong Paper Code
Mã nguồn nghiên cứu (như DRAEM Perlin noise) thường fix cứng kích thước lũy thừa 2 (256x256). Khi áp dụng cho ảnh công nghiệp thực tế với kích thước bất kỳ (900x900, 840x840), phép chia lưới `d = shape // res` sẽ sinh lỗi broadcast gradient:
- **Giải pháp chuẩn**: Luôn sinh ma trận tần số / nhiễu ngẫu nhiên trên kích thước lũy thừa 2 cố định (vd: 512x512) nơi mọi tỷ lệ `res` chia hết, sau đó dùng `cv2.resize(..., interpolation=cv2.INTER_LINEAR)` nội suy về kích thước `(W, H)` của ảnh đầu vào.

## 5. Tải Dataset Dự Phòng Chọn Lọc qua HuggingFace Hub
Khi link máy chủ trường đại học hoặc mirror chính thức của dataset bị 404:
- Dùng `huggingface_hub.snapshot_download` với tham số `allow_patterns=[f"{category}/**" for category in categories]`.
- Giúp tải định dạng thư mục giải nén sẵn, lọc bỏ các class không cần thiết, tiết kiệm băng thông và tự động resume.
