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

1. Nếu nhận được file **`.zip`**: bấm chuột phải → **Extract All… / Giải nén** (Windows) hoặc bấm đúp (macOS). Bạn sẽ có thư mục **`rsa_project`**.
2. Đặt thư mục ở nơi dễ nhớ, ví dụ `Desktop` hoặc `Documents`.
3. Mở thư mục ra xem, bên trong phải thấy các file `main.py`, `so_hoc.py`, `sinh_khoa.py`, `ma_hoa.py`... **trực tiếp** (không nằm trong thư mục con). Nếu bên trong chỉ có thêm một thư mục `rsa_project` nữa, hãy mở tiếp vào đó.

Cấu trúc đúng:

```
rsa_project/
├── README.md          ← file hướng dẫn này
├── main.py            ← CHẠY FILE NÀY: menu demo
├── so_hoc.py          ← số học nền: Euclid mở rộng, nghịch đảo, bình phương và nhân
├── sinh_khoa.py       ← kiểm tra nguyên tố Miller–Rabin, sinh khoá RSA
├── ma_hoa.py          ← mã hoá / giải mã (số, dãy byte, văn bản)
├── test_rsa.py        ← kiểm thử tự động của nhóm (11 ca)
└── test_bo_sung.py    ← kiểm thử bổ sung các trường hợp biên (17 ca)
```

> ⚠️ Các file `.py` **phải nằm chung một thư mục** vì chúng gọi lẫn nhau. Đừng tách riêng từng file ra chỗ khác.

---

## Bước 3 – Mở cửa sổ dòng lệnh đúng chỗ

"Cửa sổ dòng lệnh" là cửa sổ để gõ lệnh. Quan trọng nhất: **nó phải đang "đứng" trong thư mục `rsa_project`**.

**Windows 10/11**
1. Mở thư mục `rsa_project` bằng File Explorer (nhìn thấy các file `main.py`, `so_hoc.py`...).
2. Bấm chuột phải vào **khoảng trống** → **"Open in Terminal"**. Nếu không thấy mục này: bấm vào **thanh địa chỉ** phía trên, xoá hết chữ, gõ `cmd` rồi nhấn Enter.

**macOS**
1. Mở **Terminal**, gõ `cd ` (có một dấu cách sau chữ cd).
2. **Kéo thư mục `rsa_project` từ Finder thả vào cửa sổ Terminal**, rồi nhấn Enter.

**Linux**
- Bấm chuột phải vào khoảng trống trong thư mục → **Open in Terminal**.

### Kiểm tra bạn đang ở đúng chỗ

- Windows (cmd): gõ `dir`
- Windows PowerShell / macOS / Linux: gõ `ls`

Phải thấy **`main.py`** trong danh sách. Nếu không thấy → bạn đang ở sai thư mục, hãy làm lại Bước 3.

> 💡 Chỉ gõ (hoặc dán) phần lệnh rồi nhấn **Enter**, **không gõ** dấu `$` hay `>` ở đầu dòng. Dán trong cửa sổ Terminal của Windows: bấm **chuột phải** hoặc `Ctrl + V`.

---

## Bước 4 – Chạy chương trình (menu demo)