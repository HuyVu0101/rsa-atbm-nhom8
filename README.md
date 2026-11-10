## Mục lục

1. [Cần chuẩn bị gì?](#1-cần-chuẩn-bị-gì)
2. [Bước 1 – Cài Python](#bước-1--cài-python)
3. [Bước 2 – Lấy thư mục chương trình](#bước-2--lấy-thư-mục-chương-trình)
4. [Bước 3 – Mở cửa sổ dòng lệnh đúng chỗ](#bước-3--mở-cửa-sổ-dòng-lệnh-đúng-chỗ)
5. [Bước 4 – Chạy giao diện đồ hoạ](#bước-4--chạy-giao-diện-đồ-hoạ)
6. [Bước 5 – Chạy kiểm thử tự động](#bước-5--chạy-kiểm-thử-tự-động)
7. [Giải thích thuật ngữ](#giải-thích-thuật-ngữ)
8. [Gặp lỗi? Xem ở đây](#gặp-lỗi-xem-ở-đây)
9. [Giới hạn đã biết của chương trình](#giới-hạn-đã-biết-của-chương-trình)
10. [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## 1. Cần chuẩn bị gì?

| Cần có | Ghi chú |
|---|---|
| Máy tính Windows, macOS hoặc Linux | Loại nào cũng được |
| Python **3.8 trở lên** (khuyến nghị 3.10+) | Cài ở Bước 1 (miễn phí) |
| Thư viện `tkinter` | **Chỉ cần cho giao diện đồ hoạ.** Có sẵn khi cài Python trên Windows/macOS; Linux có thể phải cài thêm (xem Bước 1) |
| Thư mục `rsa_project` | Gồm các file `.py` của nhóm, thường gửi dưới dạng `.zip` |
| Internet | Chỉ cần để tải Python. **Chạy chương trình không cần mạng** |

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

## Bước 2 – Lấy thư mục chương trình

1. Nếu nhận được file **`.zip`**: bấm chuột phải → **Extract All… / Giải nén** (Windows) hoặc bấm đúp (macOS). Bạn sẽ có thư mục **`rsa_project`**.
2. Đặt thư mục ở nơi dễ nhớ, ví dụ `Desktop` hoặc `Documents`.
3. Mở thư mục ra xem, bên trong phải thấy `main.py`, `main_cli.py`, `so_hoc.py`... **trực tiếp** (không nằm trong thư mục con). Nếu bên trong chỉ có thêm một thư mục `rsa_project` nữa, hãy mở tiếp vào đó.

Cấu trúc đúng:

```
rsa_project/
├── README.md          ← file hướng dẫn này
├── main.py            ← CHẠY: giao diện đồ hoạ (Tkinter)
├── main_cli.py        ← CHẠY: giao diện dòng lệnh (menu 6 mục)
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

## Bước 4 – Chạy giao diện đồ hoạ

```
python main.py
```

(nhớ thay `python` bằng `python3` hoặc `py` nếu cần). Một **cửa sổ** hiện ra với tiêu đề "Chương trình Demo Hệ mã RSA", gồm **5 tab** ở phía trên. Làm lần lượt từ tab 1 đến tab 5. Thanh dưới cùng của cửa sổ báo trạng thái ("Sẵn sàng", "Đã tạo khoá nhỏ…").

> Để thoát: đóng cửa sổ như bình thường. Khoá tạo ra **chỉ sống trong lúc cửa sổ còn mở** (xem [Giới hạn](#giới-hạn-đã-biết-của-chương-trình)).

### Tab 1 – "Khoá nhỏ & Từng bước" (tính tay được)

Dùng để **xem từng bước tạo khoá** với số nhỏ.

1. Ô **p, q, e** đã điền sẵn `11`, `13`, `7`. Bấm **⚡ Bắt đầu tạo khoá** (hoặc bấm nút mẫu **Mẫu (11, 13, 7)** / **Mẫu (17, 11, 7)**).
2. Phía trên bảng hiện các bước: kiểm tra p, q nguyên tố, n = p × q, φ(n), kiểm tra e, tính d.
3. Bảng **Euclid mở rộng** ban đầu để trống. Bấm **⏭ Bước tiếp theo** để hiện từng dòng, **⏩ Hiện tất cả** để hiện hết, **🔄 Làm lại** để xoá và xem lại từ đầu.
4. Hai ô màu hiện **Khoá công khai KU = { e, n }** và **Khoá bí mật KR = { d, p, q }**. Với bộ mẫu: e = 7, n = 143, d = 103.
5. Phần dưới của tab: gõ một **số M** (0 ≤ M < n, ví dụ `9`) hoặc **chữ A–Z viết không dấu** (ví dụ `HELLO`), rồi bấm **🔒 Mã hoá & Giải mã**. Một dòng kết quả hiện ra, màu xanh nếu **ĐÚNG**: `9 → 48 → 9`.
6. Bảng **Bình phương và nhân** bên dưới cho thấy cách tính lũy thừa từng bước, cũng có nút **Bước tiếp theo / Hiện tất cả / Làm lại**.

Nếu nhập sai (p không nguyên tố, p = q, e không hợp lệ, M ≥ n...), chương trình hiện hộp thông báo lỗi bằng tiếng Việt.

### Tab 2 – "Khoá lớn (512 – 2048 bit)"

1. Chọn độ dài khoá trong hộp (512, 1024 hoặc 2048; cũng có thể gõ số khác, tối thiểu 64). Mặc định **1024**.
2. Bấm **🚀 Sinh cặp khoá RSA**. Thanh chạy cho biết chương trình đang tính (cửa sổ không bị đứng). Khi xong, hiện thời gian.
3. Các ô **p, q, n, e, d** hiện dạng rút gọn (đầu…cuối kèm số chữ số). Bấm **🔍 Xem đầy đủ** để xem cả số dài, **📋 Sao chép** để chép vào bộ nhớ tạm, hoặc **📋 Sao chép toàn bộ khoá (KU & KR)**.
4. Dòng xanh phía dưới xác nhận **e × d mod φ(n) = 1**.

> Khoá 2048 bit có thể mất từ 1 đến hơn chục giây, tuỳ lần chạy.

### Tab 3 – "Mã hoá văn bản"

1. Ô trên cùng có sẵn câu mẫu; bạn có thể xoá và gõ **câu tiếng Việt có dấu** bất kỳ (nút **Mẫu** để trả về câu mẫu, **Xoá** để xoá).
2. Bấm **🔒 Thực hiện Mã hoá**. Nếu chưa có khoá lớn, chương trình báo "Tự động sinh khoá" và tạo khoá 1024 bit (bấm OK, cửa sổ có thể đứng hình trong chốc lát).
3. Ô giữa hiện **bản mã** theo từng khối `[Khối 01]: …` (số viết hệ 16), cùng dòng thông tin: số byte, kích thước khối, số khối, thời gian mã hoá.
4. Bấm **🔓 Thực hiện Giải mã**. Ô dưới hiện **văn bản giải mã**, thời gian giải mã và kết luận **✓ ĐÚNG: Khớp 100% với văn bản gốc**.

### Tab 4 – "Mã hoá tệp & Ảnh"

1. Bấm **📁 Chọn tệp...**, chọn một tệp **nhỏ** (vài KB là đẹp; ảnh `.png` hoặc `.gif` sẽ được xem trước). Tệp lớn hơn 200 KB sẽ có hộp cảnh báo vì giải mã khá lâu.
2. Bấm **🔒 Mã hoá tệp**. Chương trình tạo tệp **`<tên tệp>.rsa`** cạnh tệp gốc (ví dụ `anh.png.rsa`) và hiện mã băm SHA-256 của tệp gốc.
3. Bấm **🔓 Giải mã tệp**. Chương trình tạo tệp **`<tên>_giaima<đuôi>`** (ví dụ `anh_giaima.png`), tính SHA-256 của tệp giải mã và so sánh: **✓ ĐÚNG** nghĩa là hai tệp giống hệt nhau. Với ảnh PNG/GIF, ảnh gốc và ảnh sau giải mã hiện cạnh nhau.
4. Thanh tiến độ cho biết khối đã xử lý.

> ⚠️ Giải mã tệp `.rsa` cần **đúng khoá đã dùng khi mã hoá**. Khoá chỉ nằm trong bộ nhớ, nên **đừng đóng chương trình** giữa lúc mã hoá và giải mã; nếu đóng rồi mở lại, khoá mới sẽ khác và tệp `.rsa` cũ **không giải mã được nữa**.

### Tab 5 – "Đo thời gian & Biểu đồ"

1. Chọn **số lần lặp** (1–10, mặc định 3). Số lần càng lớn kết quả càng ổn định nhưng càng lâu.
2. Bấm **⏱ Bắt đầu đo nghiệm**. Chương trình đo sinh khoá, mã hoá, giải mã ở **512, 1024, 2048 bit**; thanh tiến độ chạy, bảng kết quả điền dần.
3. Chọn kiểu xem biểu đồ cột: **Tất cả chỉ số**, **Chỉ Sinh khoá**, hoặc **Chỉ Mã hoá & Giải mã**.
4. Bấm **📥 Xuất file CSV** để lưu bảng (mặc định tên `thoi_gian_rsa.csv`, mở được bằng Excel).

### Nút và phím tắt chung

| Thao tác | Tác dụng |
|---|---|
| Nút **ℹ Giới thiệu** (góc trên phải) | Mở hộp thoại giới thiệu nguyên lý RSA và lưu ý an toàn |
| Nút **⛶ Toàn màn hình (F11)** hoặc phím **F11** | Bật/tắt toàn màn hình; phím **Esc** để thoát toàn màn hình |
| **Ctrl + 1 … Ctrl + 5** (hoặc **Alt + 1 … Alt + 5**) | Chuyển sang tab 1…5 |
| **Ctrl + Tab** | Sang tab kế tiếp |
| **Enter** | Thực hiện thao tác chính của tab đang mở (không áp dụng khi đang gõ trong ô văn bản nhiều dòng) |

---



## Bước 5 – Chạy kiểm thử tự động

Kiểm thử tự động giúp xác nhận phần tính toán lõi chạy đúng. Gõ:

```
python -m unittest test_rsa test_bo_sung
```

Chờ khoảng 1–2 giây. Cuối kết quả phải có:

```
Ran 28 tests in 0.9s

OK
```

Chữ **`OK`** nghĩa là mọi kiểm thử đều đạt (11 ca của nhóm trong `test_rsa.py` và 17 ca bổ sung trong `test_bo_sung.py`). Nếu muốn xem chi tiết từng ca, thêm `-v` vào cuối lệnh. Kiểm thử dùng số ngẫu nhiên nên số giây mỗi lần hơi khác nhau, không sao. (Bộ kiểm thử chỉ phủ phần lõi; hai giao diện được kiểm tra bằng cách chạy thử trực tiếp.)

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
| `ModuleNotFoundError: No module named 'tkinter'` | Python chưa có `tkinter` (cần cho `main.py`) | Linux: `sudo apt install python3-tk`. Windows: cài lại Python và giữ mục "tcl/tk and IDLE". Hoặc dùng `python main_cli.py` thay thế |
| `_tkinter.TclError: no display name and no $DISPLAY environment variable` | Máy/phiên làm việc không có màn hình đồ hoạ (ví dụ SSH, một số WSL) | Dùng giao diện dòng lệnh: `python main_cli.py` |
| `ModuleNotFoundError: No module named 'so_hoc'` (hoặc `sinh_khoa`, `ma_hoa`) | Thiếu file hoặc các file `.py` không nằm chung một thư mục | Kiểm tra đủ các file ở Bước 2 và đặt chung một chỗ |
| `Ran 1 test ... FAILED (errors=1)` khi chạy kiểm thử | Đang đứng sai thư mục nên không tìm thấy `test_rsa.py` | `cd` vào `rsa_project` rồi chạy lại |
| `'python' is not recognized...` (Windows) | Python chưa cài hoặc chưa tick "Add to PATH" | Thử `py` thay cho `python`; nếu vẫn lỗi, cài lại Python và **tick ô "Add python.exe to PATH"** |
| `python: command not found` (macOS/Linux) | Máy dùng tên lệnh `python3` | Gõ `python3` thay cho `python` |
| Tab 4/mục 5: `Không tìm thấy tệp` / "Chưa chọn tệp" | Sai đường dẫn hoặc chưa chọn tệp | Chép tệp vào thư mục `rsa_project`; gõ đúng tên kể cả đuôi (`anh.png`) |
| Tab 4: "Chưa tìm thấy tệp mã hoá .rsa để giải mã" | Chưa mã hoá tệp đó, hoặc tệp `.rsa` đã bị xoá/di chuyển | Mã hoá trước; giữ tệp `.rsa` cạnh tệp gốc |
| Tab 4: kết quả "✗ SAI" hoặc báo lỗi khi giải mã | Khoá đã đổi (đã đóng/mở lại chương trình hoặc sinh khoá mới ở tab 2 sau khi mã hoá) | Mã hoá lại bằng khoá hiện tại rồi giải mã ngay, **không** sinh khoá mới ở giữa chừng |
| Cửa sổ "đứng hình" vài giây khi bấm Mã hoá ở tab 3/4 lần đầu | Chương trình đang tự sinh khoá 1024 bit | Chờ vài giây; hoặc sinh khoá trước ở tab 2 |
| `Có lỗi: ...` ở dòng lệnh | Một mục gặp lỗi bất ngờ nhưng chương trình vẫn chạy tiếp | Đọc nội dung lỗi; thử lại mục đó với dữ liệu khác |
| Chữ tiếng Việt hiện thành ký tự lạ (Windows, dòng lệnh) | Cửa sổ chưa dùng bảng mã UTF-8 | Gõ `chcp 65001` rồi Enter, hoặc dùng **Windows Terminal / PowerShell** |
| Tạo khoá 2048 bit lâu | Khoá càng dài càng lâu; tìm số nguyên tố là ngẫu nhiên nên có lần nhanh, có lần chậm | Chờ thêm hoặc dùng 512 / 1024 bit |

Mẹo: hầu hết lỗi của người mới đến từ việc **đứng sai thư mục** hoặc **gõ thiếu/sai lệnh**. Hãy sao chép nguyên văn lệnh từ README này.

---

## Giới hạn đã biết của chương trình

Những điều dưới đây được phát hiện khi kiểm thử và đo đạc; chúng cũng được ghi trong báo cáo (mục 4.4):

- **Khoá không được lưu ra tệp**: thoát chương trình là mất khoá, nên tệp `.rsa` đã tạo **không giải mã được** sau đó. (Giao diện đồ hoạ chỉ cho "Sao chép" khoá vào bộ nhớ tạm.)
- **Không có "đệm" OAEP/PSS**: cùng một câu và cùng một khoá luôn cho **cùng một bản mã** (ví dụ hai chữ `L` trong `HELLO` đều thành `12`), và bản mã có thể bị biến đổi có chủ đích. Phần mềm thực tế bắt buộc có lớp đệm này (theo chuẩn RFC 8017). Tệp `.rsa` cũng không có xác thực toàn vẹn.
- **Bộ sinh số ngẫu nhiên không dành cho mật mã**: chương trình dùng mô-đun `random`; mật mã thật cần `secrets`.
- **Khoá có thể ngắn hơn yêu cầu 1 bit**: do chỉ ép 1 bit cao nhất, nên yêu cầu 512 bit đôi khi cho khoá 511 bit (khoảng 32–41% số lần trong các lần đo).
- **Hàm Euclid mở rộng dùng đệ quy**: với hai số ngẫu nhiên cỡ 2048 bit trở lên sẽ báo `RecursionError`. Việc sinh khoá không bị ảnh hưởng vì e nhỏ.
- **Giải mã không dùng định lý phần dư Trung Hoa (CRT)** nên chậm hơn mức có thể (khoảng 25 KB/giây với khoá 1024 bit).
- **Bảng Euclid ở tab 1 của giao diện đồ hoạ** hiển thị lệch một dòng (dòng thứ ba lặp lại dòng thứ hai, thiếu dòng cuối có số dư 0), nhưng kết quả gcd và d vẫn **đúng**; bản dòng lệnh (mục 1) in đúng.
- **Khoá ngắn không an toàn**: khoá dưới 2048 bit chỉ dùng để minh hoạ; khoá cỡ vài chục bit có thể bị phá trong tích tắc.
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
