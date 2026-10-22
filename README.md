# rsa-atbm-nhom8
## Bước 1 – Cài Python

### Kiểm tra máy đã có Python chưa

Mở cửa sổ dòng lệnh (cách mở ở Bước 3) rồi gõ:

```
python --version
```

- Hiện ra dạng `Python 3.12.3` (số đầu là 3, số thứ hai từ **8** trở lên) → **đã đủ, sang Bước 2**.
- Báo `command not found` hoặc `'python' is not recognized` → thử `python3 --version` (macOS/Linux) hoặc `py --version` (Windows). Nếu vẫn không được → cài Python như bên dưới.

### Cài Python

**Windows**

1. Vào https://www.python.org/downloads/ và bấm nút **Download Python 3.x.x**.
2. Mở file vừa tải. **Quan trọng:** ở màn hình đầu tiên, **tick vào ô "Add python.exe to PATH"** (phía dưới) rồi mới bấm **Install Now**.
3. Cài xong, bấm **Close**. Đóng hết cửa sổ dòng lệnh đang mở, mở lại cửa sổ mới rồi gõ `python --version` để kiểm tra.

**macOS**

1. Vào https://www.python.org/downloads/macos/ , tải bản cài đặt, mở file và bấm Continue cho đến khi xong.
2. Mở **Terminal** (nhấn `Cmd + Space`, gõ "Terminal", Enter), gõ `python3 --version` để kiểm tra.

**Linux (Ubuntu/Debian)**

```
sudo apt update
sudo apt install python3
python3 --version
```

> 📌 **Ghi nhớ:** trên macOS và Linux, hãy gõ **`python3`** thay cho `python` trong mọi lệnh bên dưới. Trên Windows nếu `python` không chạy thì thay bằng **`py`**.

---

## Bước 2 – Lấy thư mục chương trình