# Hệ mã RSA – Bài tập nhóm An toàn và bảo mật thông tin mạng (Nhóm 8)

Chương trình cài đặt **hệ mã khoá công khai RSA** bằng Python, kèm các thuật toán nền: **Euclid mở rộng**, **tìm phần tử nghịch đảo theo modulo**, **bình phương và nhân**, **kiểm tra số nguyên tố Miller – Rabin**. Toàn bộ phần lõi do nhóm tự viết, **không dùng thư viện mật mã** và không gọi `pow(a, b, n)` hay `math.gcd`. Các hàm chuẩn của Python chỉ dùng trong `test_rsa.py` để đối chiếu kết quả.

| STT | Thành viên | Phần mã nguồn | Phần báo cáo và việc khác |
|:-:|---|---|---|
| 1 | Phan Thảo Phương | `README.md` | Phần mở đầu, Chương 1 (cơ sở lý thuyết); tổng hợp và trình bày báo cáo |
| 2 | Lại Phương Thúy | `so_hoc.py` | Mục 2.2.1 – 2.2.3 và sơ đồ khối Hình 2.1 – 2.3 |
| 3 | Nguyễn Như Phát | `sinh_khoa.py`, `ma_hoa.py` | Mục 2.2.4, 2.3 – 2.5 |
| 4 | Ngô Hương Trà | `test_rsa.py` (kiểm thử, minh hoạ tấn công) | Ví dụ tính tay (2.6), phân tích độ an toàn (2.7), đo hiệu năng (3.4.2) |
| 5 | Vũ Trường Huy – Nhóm trưởng | `main.py` (giao diện đồ hoạ) | Điều phối nhóm, quản lý kho GitHub; Chương 4; slide và demo |

Tỉ lệ đóng góp của mỗi thành viên là 100%, đã được cả nhóm xác nhận trong Bảng phân công nhiệm vụ của báo cáo.

**Sử dụng công cụ AI:** nhóm dùng Claude (Anthropic) để dựng khung mã, rà soát và bổ sung ca kiểm thử đối chiếu, và Google Antigravity để hỗ trợ viết giao diện `main.py`. Các thuật toán lõi trong `so_hoc.py`, `sinh_khoa.py`, `ma_hoa.py` do thành viên được phân công tự cài đặt. Chi tiết xem mục "Khai báo sử dụng công cụ trí tuệ nhân tạo (AI)" trong báo cáo.

---

## Mục lục

1. [Cấu trúc mã nguồn](#1-cấu-trúc-mã-nguồn)
2. [Cần chuẩn bị gì?](#2-cần-chuẩn-bị-gì)
3. [Bước 1 – Cài Python](#bước-1--cài-python)
4. [Bước 2 – Tải mã nguồn](#bước-2--tải-mã-nguồn)
5. [Bước 3 – Mở cửa sổ dòng lệnh đúng chỗ](#bước-3--mở-cửa-sổ-dòng-lệnh-đúng-chỗ)
6. [Bước 4 – Chạy giao diện đồ hoạ](#bước-4--chạy-giao-diện-đồ-hoạ)
7. [Bước 5 – Chạy kiểm thử tự động](#bước-5--chạy-kiểm-thử-tự-động)
8. [Bước 6 – Chạy minh hoạ tấn công](#bước-6--chạy-minh-hoạ-tấn-công)
9. [Giải thích thuật ngữ](#giải-thích-thuật-ngữ)
10. [Gặp lỗi? Xem ở đây](#gặp-lỗi-xem-ở-đây)
11. [Giới hạn đã biết của chương trình](#giới-hạn-đã-biết-của-chương-trình)
12. [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## 1. Cấu trúc mã nguồn

```
rsa-atbm-nhom8/
├── README.md       ← file hướng dẫn này
├── so_hoc.py       ← số học nền: Euclid mở rộng, gcd, nghịch đảo modulo, bình phương và nhân
├── sinh_khoa.py    ← kiểm tra nguyên tố Miller–Rabin, sinh số nguyên tố, sinh cặp khoá RSA
├── ma_hoa.py       ← mã hoá / giải mã: một số, dãy byte (chia khối), văn bản UTF-8
├── main.py         ← CHẠY: giao diện đồ hoạ Tkinter (5 mục), chỉ gọi các hàm ở 3 file trên
└── test_rsa.py     ← kiểm thử tự động (19 ca) + minh hoạ tấn công phân tích n
```

Phần thuật toán (3 file `so_hoc.py`, `sinh_khoa.py`, `ma_hoa.py`) tách riêng khỏi phần giao diện (`main.py`). Các file gọi lẫn nhau theo thứ tự:

```
so_hoc.py  →  sinh_khoa.py  →  ma_hoa.py  →  main.py / test_rsa.py
```

> ⚠️ Các file `.py` **phải nằm chung một thư mục** vì chúng gọi lẫn nhau. Đừng tách riêng từng file ra chỗ khác.

---

## 2. Cần chuẩn bị gì?

| Cần có | Ghi chú |
|---|---|
| Máy tính Windows, macOS hoặc Linux | Loại nào cũng được |
| Python **3.8 trở lên** (khuyến nghị 3.10+) | Cài ở Bước 1 (miễn phí) |
| Thư viện `tkinter` | **Chỉ cần cho giao diện đồ hoạ.** Có sẵn khi cài Python trên Windows/macOS; Linux có thể phải cài thêm (xem Bước 1) |
| Thư viện `Pillow` | **Không bắt buộc.** Nếu có, mục 4 xem trước được nhiều định dạng ảnh hơn (JPG, BMP, WEBP); nếu không có vẫn xem được PNG và GIF |
| Internet | Chỉ cần để tải Python và mã nguồn. **Chạy chương trình không cần mạng** |

Bạn **không cần `pip install`** gì cả: chương trình chỉ dùng thư viện có sẵn của Python.

---

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
2. Mở file vừa tải. **Quan trọng:** ở màn hình đầu tiên, **tick vào ô "Add python.exe to PATH"** (phía dưới) rồi mới bấm **Install Now** (bản cài mặc định đã kèm `tkinter`).
3. Cài xong, bấm **Close**. Đóng hết cửa sổ dòng lệnh đang mở, mở lại cửa sổ mới rồi gõ `python --version` để kiểm tra.

**macOS**

1. Vào https://www.python.org/downloads/macos/ , tải bản cài đặt, mở file và bấm Continue cho đến khi xong (bản này kèm `tkinter`).
2. Mở **Terminal** (nhấn `Cmd + Space`, gõ "Terminal", Enter), gõ `python3 --version` để kiểm tra.

**Linux (Ubuntu/Debian)**

```
sudo apt update
sudo apt install python3 python3-tk
python3 --version
```

(`python3-tk` chỉ cần nếu muốn dùng giao diện đồ hoạ.)

> 📌 **Ghi nhớ:** trên macOS và Linux, hãy gõ **`python3`** thay cho `python` trong mọi lệnh bên dưới. Trên Windows nếu `python` không chạy thì thay bằng **`py`**.

---

## Bước 2 – Tải mã nguồn

Chọn **một** trong hai cách.

**Cách 1 – Tải file ZIP (không cần cài gì thêm)**

1. Mở https://github.com/HuyVu0101/rsa-atbm-nhom8
2. Bấm nút xanh **Code** → **Download ZIP**.
3. Giải nén: bấm chuột phải → **Extract All… / Giải nén** (Windows) hoặc bấm đúp (macOS). Bạn sẽ có thư mục **`rsa-atbm-nhom8-main`**.

**Cách 2 – Dùng Git**

```
git clone https://github.com/HuyVu0101/rsa-atbm-nhom8.git
```

Lệnh này tạo thư mục **`rsa-atbm-nhom8`**.

Mở thư mục vừa có, bên trong phải thấy `main.py`, `so_hoc.py`, `test_rsa.py`... **trực tiếp** (không nằm trong thư mục con). Nếu bên trong chỉ có thêm một thư mục cùng tên nữa, hãy mở tiếp vào đó. Bên dưới, "thư mục chương trình" là thư mục chứa các file này.

---

## Bước 3 – Mở cửa sổ dòng lệnh đúng chỗ

"Cửa sổ dòng lệnh" là cửa sổ để gõ lệnh. Quan trọng nhất: **nó phải đang "đứng" trong thư mục chương trình**.

**Windows 10/11**
1. Mở thư mục chương trình bằng File Explorer (nhìn thấy các file `main.py`, `so_hoc.py`...).
2. Bấm chuột phải vào **khoảng trống** → **"Open in Terminal"**. Nếu không thấy mục này: bấm vào **thanh địa chỉ** phía trên, xoá hết chữ, gõ `cmd` rồi nhấn Enter.

**macOS**
1. Mở **Terminal**, gõ `cd ` (có một dấu cách sau chữ cd).
2. **Kéo thư mục chương trình từ Finder thả vào cửa sổ Terminal**, rồi nhấn Enter.

**Linux**
- Bấm chuột phải vào khoảng trống trong thư mục → **Open in Terminal**. Nếu vừa dùng `git clone`, chỉ cần gõ `cd rsa-atbm-nhom8`.

### Kiểm tra bạn đang ở đúng chỗ

- Windows (cmd): gõ `dir`
- Windows PowerShell / macOS / Linux: gõ `ls`

Phải thấy **`main.py`** trong danh sách. Nếu không thấy → bạn đang ở sai thư mục, hãy làm lại Bước 3.

> 💡 Chỉ gõ (hoặc dán) phần lệnh rồi nhấn **Enter**, **không gõ** dấu `$` hay `>` ở đầu dòng. Dán trong cửa sổ Terminal của Windows: bấm **chuột phải** hoặc `Ctrl + V`.

---

## Bước 4 – Chạy giao diện đồ hoạ

```
python main.py
```

(nhớ thay `python` bằng `python3` hoặc `py` nếu cần). Một **cửa sổ** hiện ra với tiêu đề "Hệ mã hoá RSA - An toàn và bảo mật thông tin mạng (Nhóm 8 TMĐT)". **Thanh menu bên trái** có 5 mục: **1. Khoá nhỏ**, **2. Khoá lớn**, **3. Văn bản**, **4. Tệp & Ảnh**, **5. Thời gian**. Làm lần lượt từ mục 1 đến mục 5. Thanh dưới cùng của cửa sổ báo trạng thái; góc trên phải cho biết đã có khoá lớn hay chưa.

> Để thoát: đóng cửa sổ như bình thường. Khoá tạo ra **chỉ sống trong lúc cửa sổ còn mở** (xem [Giới hạn](#giới-hạn-đã-biết-của-chương-trình)).

### Mục 1 – Khoá nhỏ & minh hoạ từng bước (tính tay được)

Dùng để **xem từng bước tạo khoá và mã hoá** với số nhỏ, khớp với ví dụ tính tay trong báo cáo.

1. Ô **p, q, e** đã điền sẵn `11`, `13`, `7`. Bấm **⚡ Tạo khoá** (hoặc bấm nút mẫu **Mẫu (11,13,7)** / **Mẫu (17,11,7)**).
2. Phía trên bảng hiện kết quả: n, φ(n), gcd(e, φ(n)) = 1 và d.
3. Bảng **Euclid mở rộng** ban đầu để trống. Bấm **⏭ Bước tiếp** để hiện từng dòng, **⏩ Hiện hết** để hiện hết, **🔄 Làm lại** để xoá và xem lại từ đầu.
4. Hai ô màu hiện **Khoá công khai KU = { e, n }** và **Khoá bí mật KR = { d, p, q }**. Với bộ (11, 13, 7): n = 143, d = 103. Với bộ (17, 11, 7): n = 187, d = 23.
5. Phần dưới: gõ một **số M** (0 ≤ M < n, ví dụ `9` hoặc `88`) hoặc **chữ A–Z viết không dấu** (ví dụ `HELLO`, quy ước A = 1, …, Z = 26), rồi bấm **🔒 Mã hoá & Giải mã** (hoặc nút **Thử 'HELLO'**). Một dòng kết quả hiện ra, màu xanh nếu **ĐÚNG**. Ví dụ: `M=9 → C=48 → M'=9` (khoá 11, 13, 7); `M=88 → C=11 → M'=88` (khoá 17, 11, 7).
6. Hai bảng **Bình phương và nhân** bên dưới cho thấy cách tính C = M^e mod n và M = C^d mod n từng bit, cũng có nút **Bước tiếp / Hiện hết / Làm lại**.

Nếu nhập sai (p không nguyên tố, p = q, e không hợp lệ, M ≥ n...), chương trình hiện hộp thông báo lỗi bằng tiếng Việt.

### Mục 2 – Khoá lớn (512 – 2048 bit)

1. Chọn độ dài khoá trong hộp (512, 1024 hoặc 2048; cũng có thể gõ số khác, tối thiểu 64). Mặc định **1024**.
2. Bấm **🚀 Sinh cặp khoá RSA**. Thanh chạy cho biết chương trình đang tính (cửa sổ không bị đứng). Khi xong, hiện thời gian.
3. Các ô **p, q, n, e, d** hiện dạng rút gọn (đầu…cuối kèm số chữ số). Bấm **🔍 Xem đầy đủ** để xem cả số dài, **📋 Sao chép** để chép vào bộ nhớ tạm, hoặc **📋 Sao chép toàn bộ khoá**.
4. Dòng xanh phía dưới xác nhận **e × d mod φ(n) = 1**.

> Khoá 2048 bit có thể mất từ 1 đến hơn chục giây, tuỳ lần chạy.

### Mục 3 – Mã hoá văn bản

1. Ô trên cùng có sẵn câu mẫu; bạn có thể xoá và gõ **câu tiếng Việt có dấu** bất kỳ. Nút **Dùng câu mẫu** trả về câu mẫu, **Dùng văn bản dài** điền đoạn khoảng 600 ký tự (chia thành nhiều khối), **Xoá** để xoá.
2. Bấm **🔒 Mã hoá văn bản**. Nếu chưa có khoá lớn, chương trình tự sinh khoá 1024 bit (chạy nền, chờ vài giây).
3. Ô giữa hiện **bản mã** theo từng khối `[Khối 01]: …` (số viết hệ 16), cùng dòng thông tin: số byte, kích thước khối, số khối, thời gian mã hoá. Nút **📋 Sao chép bản mã** để chép ra ngoài.
4. Bấm **🔓 Giải mã bản mã**. Ô dưới hiện **văn bản giải mã**, thời gian giải mã và kết luận có khớp 100% với văn bản gốc hay không.

### Mục 4 – Mã hoá tệp & ảnh

1. Bấm **📁 Chọn tệp...**, chọn một tệp **nhỏ** (vài KB là đẹp). Ảnh sẽ được xem trước. Tệp lớn hơn 200 KB sẽ có hộp cảnh báo vì giải mã khá lâu.
2. Bấm **🔒 Mã hoá tệp**. Chương trình tạo tệp **`<tên tệp>.rsa`** cạnh tệp gốc (ví dụ `anh.png.rsa`) và hiện mã băm SHA-256 của tệp gốc.
3. Bấm **🔓 Giải mã tệp**. Chương trình tạo tệp **`<tên>_giaima<đuôi>`** (ví dụ `anh_giaima.png`), tính SHA-256 của tệp giải mã và so sánh: **✓ ĐÚNG** nghĩa là hai tệp giống hệt nhau. Với ảnh, ảnh gốc và ảnh sau giải mã hiện cạnh nhau.
4. Thanh tiến độ cho biết số khối đã xử lý.

> SHA-256 (thư viện `hashlib`) chỉ dùng để **kiểm tra** tệp giải mã có giống hệt tệp gốc hay không, không thuộc phần lõi RSA.

> ⚠️ Giải mã tệp `.rsa` cần **đúng khoá đã dùng khi mã hoá**. Khoá chỉ nằm trong bộ nhớ, nên **đừng đóng chương trình** giữa lúc mã hoá và giải mã; nếu đóng rồi mở lại, khoá mới sẽ khác và tệp `.rsa` cũ **không giải mã được nữa**.

### Mục 5 – Đo thời gian & biểu đồ

Mục này có 2 thẻ con:

**📊 Đo theo độ dài khoá (512 / 1024 / 2048 bit)**
1. Chọn **số lần lặp** cho mỗi độ dài khoá (1–10). Số lần càng lớn kết quả càng ổn định nhưng càng lâu.
2. Bấm **⏱ Bắt đầu đo nghiệm**. Chương trình đo thời gian sinh khoá, mã hoá, giải mã; bảng kết quả điền dần.
3. Chọn kiểu xem biểu đồ cột: **Mã hoá & Giải mã (ms)** hoặc **Chỉ Sinh khoá (giây)**.
4. Bấm **📥 Xuất CSV** để lưu bảng (mặc định `thoi_gian_rsa_khoa.csv`, mở được bằng Excel).

**📈 Đo theo kích thước dữ liệu (1 KB – 50 KB)**
1. Chọn độ dài khoá cố định (512, 1024 hoặc 2048 bit) và số lần lặp mỗi mức.
2. Bấm **⏱ Bắt đầu đo kích thước**. Chương trình đo mã hoá, giải mã ở các mức 1, 5, 10, 25, 50 KB, kèm số khối RSA.
3. Bấm **📥 Xuất CSV** để lưu (mặc định `thoi_gian_rsa_kich_thuoc.csv`).

### Nút và phím tắt chung

| Thao tác | Tác dụng |
|---|---|
| Nút **ℹ Giới thiệu** (cuối thanh menu trái) | Mở hộp thoại giới thiệu nguyên lý RSA và lưu ý an toàn |
| Nút **⛶ Toàn màn hình (F11)** hoặc phím **F11** | Bật/tắt toàn màn hình; phím **Esc** để thoát toàn màn hình |
| **Ctrl + 1 … Ctrl + 5** (hoặc **Alt + 1 … Alt + 5**) | Chuyển sang mục 1…5 |
| **Ctrl + Tab** | Sang mục kế tiếp |
| **Enter** | Thực hiện thao tác chính của mục đang mở (không áp dụng khi đang gõ trong ô văn bản nhiều dòng) |

---

## Bước 5 – Chạy kiểm thử tự động

Kiểm thử tự động giúp xác nhận phần tính toán lõi chạy đúng. Gõ:

```
python -m unittest test_rsa -v
```

Chờ khoảng 5–15 giây (tuỳ máy). Mỗi ca hiện một dòng kết thúc bằng `ok`, cuối cùng phải có:

```
Ran 19 tests in ...s

OK
```

Chữ **`OK`** nghĩa là cả 19 ca đều đạt. Các nhóm kiểm thử:

| Nhóm (lớp) | Số ca | Nội dung |
|---|---|---|
| `TestSoHoc` | 5 | Euclid mở rộng, gcd, nghịch đảo modulo, bình phương và nhân; đối chiếu với `math.gcd` và `pow` trên dữ liệu ngẫu nhiên |
| `TestSinhKhoa` | 4 | Miller–Rabin (gồm số Carmichael 561, 1105), sinh số nguyên tố đúng số bit, khoá nhỏ (11, 13, 7) → d = 103, khoá lớn thoả e·d mod φ(n) = 1 |
| `TestMaHoa` | 5 | Ví dụ tính tay 9 → 48 → 9; văn bản tiếng Việt, chuỗi rỗng, ký tự đặc biệt và emoji, văn bản dài nhiều khối |
| `TestDoiChieuQuyMo` | 4 | Đối chiếu với hàm chuẩn của Python: 1000 cặp nghịch đảo (`pow(a, -1, n)`), 1000 bộ luỹ thừa đến 1024 bit (`pow`), Miller–Rabin với mọi số từ 2 đến 9999 + số Carmichael + số Mersenne; khôi phục dãy byte ngẫu nhiên (có byte 0 ở đầu) với khoá 512 và 1024 bit |
| `TestTanCong` | 1 | Phá khoá 40 bit bằng phép chia thử, tính lại d và giải mã đúng bản rõ |

Bỏ `-v` ở cuối lệnh nếu chỉ muốn xem kết quả tổng. Thời gian mỗi lần chạy hơi khác nhau vì có dùng số ngẫu nhiên, không sao. (Bộ kiểm thử phủ phần lõi; giao diện được kiểm tra bằng cách chạy thử trực tiếp.)

---

## Bước 6 – Chạy minh hoạ tấn công

```
python test_rsa.py tan_cong
```

Chương trình minh hoạ kẻ tấn công chỉ biết khoá công khai (n, e) và bản mã:

1. **Phần 1:** phân tích n (khoá 40 bit) thành p × q bằng phép chia thử, tính lại khoá bí mật d và giải mã được bản rõ `Giao dich 123`.
2. **Phần 2:** bảng số phép chia thử và thời gian theo độ dài n (24 – 48 bit).
3. **Phần 3:** ước lượng thời gian cần để phá khoá thật 512 / 1024 / 2048 bit bằng cách này (cỡ 10^62 năm trở lên với tốc độ của máy đang chạy).

---

## Giải thích thuật ngữ

| Thuật ngữ | Giải thích đơn giản |
|---|---|
| **Mã hoá** | Biến câu chữ/tệp thành các số không đọc được |
| **Giải mã** | Biến các số đó trở lại như ban đầu |
| **Bản rõ / Bản mã** | Nội dung gốc, đọc được / nội dung sau khi mã hoá |
| **Khoá công khai** KU = {e, n} | "Ổ khoá": ai cũng có thể dùng để khoá tin nhắn gửi cho chủ khoá |
| **Khoá bí mật** KR = {d, p, q} | "Chìa khoá": chỉ chủ khoá giữ, dùng để mở tin nhắn |
| **Số bit (độ dài khoá)** | Độ lớn của n; càng lớn càng khó bị phá nhưng chạy càng lâu |
| **n, e, d, p, q** | Các số trong RSA: n = p × q; (e, n) công khai; d bí mật |
| **φ(n)** | "Phi của n" = (p − 1) × (q − 1), dùng để tính d |
| **Số nguyên tố** | Số chỉ chia hết cho 1 và chính nó (ví dụ 11, 13) |
| **Miller–Rabin** | Cách kiểm tra nhanh một số có phải số nguyên tố hay không |
| **Euclid mở rộng** | Cách tìm nghịch đảo để tính d từ e |
| **Bình phương và nhân** | Cách tính lũy thừa lớn nhanh (a^b mod n) |
| **Khối** | Dữ liệu dài được cắt thành các đoạn nhỏ, mỗi đoạn mã hoá riêng |
| **SHA-256** | "Dấu vân tay" của tệp: hai tệp giống hệt nhau thì cùng dấu vân tay |
| **Tệp `.rsa`** | Tệp do chương trình tạo ra chứa nội dung đã mã hoá |
| **Terminal / dòng lệnh** | Cửa sổ để gõ lệnh cho máy tính |

---

## Gặp lỗi? Xem ở đây

| Thông báo / hiện tượng | Nguyên nhân | Cách sửa |
|---|---|---|
| `can't open file '...main.py': [Errno 2] No such file or directory` | Cửa sổ dòng lệnh **đang ở sai thư mục** | Làm lại Bước 3; kiểm tra bằng `dir`/`ls` phải thấy `main.py` |
| `ModuleNotFoundError: No module named 'tkinter'` | Python chưa có `tkinter` (cần cho `main.py`) | Linux: `sudo apt install python3-tk`. Windows: cài lại Python và giữ mục "tcl/tk and IDLE". Kiểm thử (Bước 5) và minh hoạ tấn công (Bước 6) vẫn chạy được mà không cần `tkinter` |
| `_tkinter.TclError: no display name and no $DISPLAY environment variable` | Máy/phiên làm việc không có màn hình đồ hoạ (ví dụ SSH, một số WSL) | Chạy giao diện trên máy có màn hình; trên máy không có màn hình vẫn chạy được Bước 5 và Bước 6 |
| `ModuleNotFoundError: No module named 'so_hoc'` (hoặc `sinh_khoa`, `ma_hoa`) | Thiếu file hoặc các file `.py` không nằm chung một thư mục | Kiểm tra đủ các file ở mục 1 và đặt chung một chỗ |
| `ModuleNotFoundError: No module named 'test_rsa'` hoặc `Ran 0 tests` khi chạy kiểm thử | Đang đứng sai thư mục nên không tìm thấy `test_rsa.py` | Làm lại Bước 3 rồi chạy lại |
| `'python' is not recognized...` (Windows) | Python chưa cài hoặc chưa tick "Add to PATH" | Thử `py` thay cho `python`; nếu vẫn lỗi, cài lại Python và **tick ô "Add python.exe to PATH"** |
| `python: command not found` (macOS/Linux) | Máy dùng tên lệnh `python3` | Gõ `python3` thay cho `python` |
| Mục 4: "Chưa chọn tệp" / không thấy tệp | Chưa chọn tệp hoặc tệp đã bị xoá/di chuyển | Bấm **📁 Chọn tệp...** và chọn lại |
| Mục 4: không tìm thấy tệp `.rsa` để giải mã | Chưa mã hoá tệp đó, hoặc tệp `.rsa` đã bị xoá/di chuyển | Mã hoá trước; giữ tệp `.rsa` cạnh tệp gốc |
| Mục 4: kết quả "✗ SAI" hoặc báo "Sai khoá" khi giải mã | Khoá đã mất (đã đóng/mở lại chương trình) | Mã hoá lại bằng khoá hiện tại rồi giải mã ngay, không đóng chương trình giữa chừng |
| Bấm Mã hoá ở mục 3/4 lần đầu phải chờ vài giây | Chương trình đang tự sinh khoá 1024 bit | Chờ vài giây; hoặc sinh khoá trước ở mục 2 |
| Chữ tiếng Việt hiện thành ký tự lạ (Windows, dòng lệnh) | Cửa sổ chưa dùng bảng mã UTF-8 | Gõ `chcp 65001` rồi Enter, hoặc dùng **Windows Terminal / PowerShell** |
| Tạo khoá 2048 bit lâu | Khoá càng dài càng lâu; tìm số nguyên tố là ngẫu nhiên nên có lần nhanh, có lần chậm | Chờ thêm hoặc dùng 512 / 1024 bit |

Mẹo: hầu hết lỗi của người mới đến từ việc **đứng sai thư mục** hoặc **gõ thiếu/sai lệnh**. Hãy sao chép nguyên văn lệnh từ README này.

---

## Giới hạn đã biết của chương trình

Những điều dưới đây được phát hiện khi kiểm thử và đo đạc; chúng cũng được ghi trong báo cáo (mục 4.4):

- **Khoá không được lưu ra tệp**: thoát chương trình là mất khoá, nên tệp `.rsa` đã tạo **không giải mã được** sau đó. (Giao diện chỉ cho "Sao chép" khoá vào bộ nhớ tạm.)
- **Không có "đệm" OAEP/PSS**: cùng một bản rõ và cùng một khoá luôn cho **cùng một bản mã**, và bản mã có thể bị biến đổi có chủ đích. Phần mềm thực tế bắt buộc có lớp đệm này (theo chuẩn RFC 8017). Tệp `.rsa` cũng không có xác thực toàn vẹn.
- **Mã hoá từng chữ cái ở mục 1 chỉ để minh hoạ**: mỗi chữ luôn cho cùng một số, nên thực chất giống mã thay thế đơn bảng và có thể bị phân tích tần suất. Một số giá trị còn cho bản mã trùng bản rõ: với n = 143, e = 7 thì `A` (= 1) → 1 và `L` (= 12) → 12.
- **Bộ sinh số ngẫu nhiên không dành cho mật mã**: chương trình dùng mô-đun `random`; mật mã thật cần `secrets`.
- **Khoá có thể ngắn hơn yêu cầu 1 bit**: do chỉ ép 1 bit cao nhất của p và q, nên yêu cầu 512 bit đôi khi cho n dài 511 bit (khoảng 32–41% số lần trong các lần đo).
- **Hàm Euclid mở rộng dùng đệ quy**: với hai số ngẫu nhiên cỡ 2048 bit trở lên sẽ báo `RecursionError`. Việc sinh khoá không bị ảnh hưởng vì e nhỏ.
- **Giải mã không dùng định lý phần dư Trung Hoa (CRT)** nên chậm hơn mức có thể (khoảng 25 KB/giây với khoá 1024 bit).
- **Bảng Euclid ở mục 1** dừng ở dòng có số dư bằng 1 (gcd), không hiện dòng cuối có số dư 0.
- **Khoá ngắn không an toàn**: khoá dưới 2048 bit chỉ dùng để minh hoạ; khoá cỡ vài chục bit có thể bị phá trong tích tắc (xem Bước 6).
- RSA có thể bị thuật toán Shor đe doạ nếu có máy tính lượng tử đủ lớn; NIST đang xây dựng lộ trình chuyển sang mật mã hậu lượng tử (bản dự thảo NIST IR 8547).

Muốn mã hoá thông tin thật, hãy dùng các công cụ đã được kiểm định như OpenSSL, GnuPG hoặc các thư viện mật mã chuẩn.

---

## Tài liệu tham khảo

- R. L. Rivest, A. Shamir, L. Adleman (1978), *A Method for Obtaining Digital Signatures and Public-Key Cryptosystems*: https://doi.org/10.1145/359340.359342
- RFC 8017, *PKCS #1: RSA Cryptography Specifications Version 2.2*: https://www.rfc-editor.org/rfc/rfc8017
- NIST FIPS 186-5, *Digital Signature Standard*: https://doi.org/10.6028/NIST.FIPS.186-5
- NIST IR 8547 (bản dự thảo), *Transition to Post-Quantum Cryptography Standards*: https://csrc.nist.gov/pubs/ir/8547/ipd
- Python `tkinter`: https://docs.python.org/3/library/tkinter.html
- Python `random` (cảnh báo không dùng cho bảo mật): https://docs.python.org/3/library/random.html
- Tải Python: https://www.python.org/downloads/
