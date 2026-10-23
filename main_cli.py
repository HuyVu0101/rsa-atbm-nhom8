"""
main.py  --  PHẦN CỦA TV5: giao diện dòng lệnh để demo.

Chạy:  python main.py
Cần đặt cùng thư mục với so_hoc.py, sinh_khoa.py, ma_hoa.py.

Luồng demo gợi ý: 1 -> 2 -> 3 -> 4 -> 5 (mục 6 dùng để lấy số liệu cho báo cáo).
Lưu ý: hashlib chỉ dùng ở mục 5 để KIỂM TRA tệp giải mã trùng tệp gốc;
phần lõi RSA vẫn do so_hoc.py, sinh_khoa.py, ma_hoa.py tự cài đặt.
"""
import csv
import hashlib
import os
import sys
import time

from so_hoc import euclid_mo_rong, luy_thua_modulo
from sinh_khoa import sinh_khoa, khoa_tu_p_q, miller_rabin
from ma_hoa import (ma_hoa_so, giai_ma_so, ma_hoa_van_ban, giai_ma_van_ban,
                    ma_hoa_bytes, giai_ma_bytes, _kich_thuoc_khoi)

# Hiển thị tiếng Việt có dấu đúng trên console Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

khoa_nho = None   # khoá ví dụ nhỏ (dict n, e, d, p, q)
khoa_lon = None   # khoá lớn vừa tạo
VAN_BAN_MAU = "Thương mại điện tử an toàn nhờ mật mã khoá công khai RSA"
GIOI_HAN_TEP = 200 * 1024   # cảnh báo nếu tệp lớn hơn 200 KB (giải mã sẽ chậm)


# ===================== TIỆN ÍCH HIỂN THỊ =====================

def tieu_de(noi_dung):
    print("\n" + "=" * 64)
    print(noi_dung)
    print("=" * 64)


def rut_gon(so, dau=24, cuoi=8):
    """Rút gọn số rất dài để in cho gọn: 1234...5678 (còn N chữ số)."""
    s = str(so)
    if len(s) <= dau + cuoi + 12:
        return s
    return f"{s[:dau]}...{s[-cuoi:]}  ({len(s)} chữ số)"


def dung_man_hinh():
    input("\nNhấn Enter để quay lại menu...")


def nhap_so_nguyen(loi_nhac, mac_dinh=None, toi_thieu=None):
    while True:
        s = input(loi_nhac).strip()
        if s == "" and mac_dinh is not None:
            return mac_dinh
        try:
            v = int(s)
            if toi_thieu is not None and v < toi_thieu:
                print(f"  Giá trị phải >= {toi_thieu}.")
                continue
            return v
        except ValueError:
            print("  Vui lòng nhập một số nguyên.")


# ===================== CÁC BƯỚC TRUNG GIAN (CHO KHOÁ NHỎ) =====================

def euclid_tung_buoc(phi, e):
    """
    In bảng Euclid mở rộng để tìm d (e*d = 1 mod phi), từng dòng một.
    Giữ  r = phi*x + e*y  ở mỗi dòng; khi r = 1 thì y chính là d (mod phi).
    Trả về d.
    """
    print(f"\nTìm d bằng Euclid mở rộng: giải  {phi}*x + {e}*y = 1")
    print(f"{'q':>6} | {'r':>8} | {'x':>8} | {'y':>8}")
    print("-" * 40)
    r0, x0, y0 = phi, 1, 0
    r1, x1, y1 = e, 0, 1
    print(f"{'':>6} | {r0:>8} | {x0:>8} | {y0:>8}")
    print(f"{'':>6} | {r1:>8} | {x1:>8} | {y1:>8}")
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
        print(f"{q:>6} | {r1:>8} | {x1:>8} | {y1:>8}")
    # Khi r1 = 0 thì dòng liền trước (r0, x0, y0) chứa gcd
    print(f"=> gcd = {r0};  {phi}*({x0}) + {e}*({y0}) = {r0}")
    d = y0 % phi
    print(f"=> d = y mod phi = {y0} mod {phi} = {d}")
    # Đối chiếu với hàm của TV2
    g, _, y_tv2 = euclid_mo_rong(phi, e)
    assert g == r0 and y_tv2 % phi == d, "Kết quả không khớp với so_hoc.euclid_mo_rong!"
    return d


def luy_thua_tung_buoc(co_so, so_mu, modulo, ten):
    """
    In từng bước bình phương và nhân khi tính  co_so^so_mu mod modulo.
    Duyệt bit số mũ từ TRÁI sang phải (dễ giải thích hơn); kết quả luôn
    được đối chiếu với luy_thua_modulo của TV2 (duyệt từ phải sang trái).
    """
    bits = bin(so_mu)[2:]
    print(f"\n{ten}: {co_so}^{so_mu} mod {modulo}")
    print(f"Số mũ {so_mu} = {bits} (nhị phân)")
    print(f"{'bit':>4} | {'bình phương':>22} | {'nhân thêm cơ số':>22}")
    print("-" * 56)
    kq = 1
    for b in bits:
        truoc = kq
        kq = kq * kq % modulo
        bp = f"{truoc}^2 mod {modulo} = {kq}"
        nhan = "-"
        if b == "1":
            truoc2 = kq
            kq = kq * co_so % modulo
            nhan = f"{truoc2}*{co_so} mod {modulo} = {kq}"
        print(f"{b:>4} | {bp:>22} | {nhan:>22}")
    print(f"=> Kết quả: {kq}")
    assert kq == luy_thua_modulo(co_so, so_mu, modulo), "Không khớp luy_thua_modulo!"
    return kq


# ===================== MỤC 1: TẠO KHOÁ NHỎ =====================

def chon_tao_khoa_nho():
    global khoa_nho
    tieu_de("1. TẠO KHOÁ RSA VÍ DỤ NHỎ (tính tay được)")
    print("Nhấn Enter để dùng ví dụ chuẩn p=11, q=13, e=7,")
    print("hoặc nhập 3 số cách nhau bởi dấu cách (ví dụ: 17 11 7).")
    s = input("p q e = ").strip()
    try:
        p, q, e = (11, 13, 7) if s == "" else tuple(int(x) for x in s.split())
        if not (miller_rabin(p) and miller_rabin(q)):
            print("p và q phải là số nguyên tố.")
            return dung_man_hinh()
        if p == q:
            print("p và q phải khác nhau.")
            return dung_man_hinh()
    except ValueError:
        print("Dữ liệu không hợp lệ.")
        return dung_man_hinh()

    print(f"\nBước 1: chọn hai số nguyên tố  p = {p},  q = {q}")
    n, phi = p * q, (p - 1) * (q - 1)
    print(f"Bước 2: n = p*q = {n}")
    print(f"Bước 3: phi(n) = (p-1)*(q-1) = {p-1}*{q-1} = {phi}")
    print(f"Bước 4: chọn e = {e}, kiểm tra gcd(e, phi) = 1")
    try:
        khoa = khoa_tu_p_q(p, q, e)
    except ValueError as loi:
        print("  Lỗi:", loi)
        return dung_man_hinh()
    print("        gcd hợp lệ.")
    print("Bước 5: tính khoá riêng d (nghịch đảo của e theo modulo phi)")
    d = euclid_tung_buoc(phi, e)
    print(f"\nKiểm tra: e*d mod phi = {e}*{d} mod {phi} = {e * d % phi}  (phải bằng 1)")
    khoa_nho = khoa
    print(f"\n>>> Khoá công khai KU = {{e={e}, n={n}}}")
    print(f">>> Khoá riêng    KR = {{d={d}, p={p}, q={q}}}")
    dung_man_hinh()


# ===================== MỤC 2: MÃ HOÁ / GIẢI MÃ VỚI KHOÁ NHỎ =====================

def chon_ma_hoa_khoa_nho():
    global khoa_nho
    if khoa_nho is None:
        print("(Chưa có khoá nhỏ, tự tạo khoá ví dụ p=11, q=13, e=7)")
        khoa_nho = khoa_tu_p_q(11, 13, 7)
    n, e, d = khoa_nho["n"], khoa_nho["e"], khoa_nho["d"]
    tieu_de(f"2. MÃ HOÁ / GIẢI MÃ VỚI KHOÁ NHỎ  (n={n}, e={e}, d={d})")
    print(f"Khoá nhỏ chỉ mã hoá được số M với 0 <= M < {n}.")
    print("Nhập một số, hoặc một từ viết hoa không dấu (A=1, B=2, ..., Z=26).")
    s = input("M = ").strip().upper()
    if s == "":
        s = "9"

    if s.isdigit():
        m = int(s)
        if m >= n:
            print(f"M phải nhỏ hơn n = {n}.")
            return dung_man_hinh()
        c = luy_thua_tung_buoc(m, e, n, "MÃ HOÁ   C = M^e mod n")
        assert c == ma_hoa_so(m, n, e)
        m2 = luy_thua_tung_buoc(c, d, n, "GIẢI MÃ  M = C^d mod n")
        assert m2 == giai_ma_so(c, n, d)
        print(f"\n>>> Bản rõ {m}  ->  bản mã {c}  ->  giải mã lại {m2}",
              "(ĐÚNG)" if m2 == m else "(SAI!)")
    elif s.isalpha() and s.isascii():
        gia_tri = [ord(ch) - 64 for ch in s]
        if max(gia_tri) >= n:
            print(f"Khoá quá nhỏ cho các chữ cái này (n = {n}).")
            return dung_man_hinh()
        print(f"\n{'chữ':>4} | {'M':>4} | {'C = M^e mod n':>14} | {'M giải mã':>10}")
        print("-" * 44)
        ban_ma, ban_giai = [], []
        for ch, m in zip(s, gia_tri):
            c = ma_hoa_so(m, n, e)
            m2 = giai_ma_so(c, n, d)
            ban_ma.append(c)
            ban_giai.append(chr(m2 + 64))
            print(f"{ch:>4} | {m:>4} | {c:>14} | {m2:>10}")
        print(f"\n>>> Bản mã: {ban_ma}")
        print(f">>> Giải mã lại: {''.join(ban_giai)}")
    else:
        print("Chỉ nhập số nguyên hoặc chữ cái A-Z không dấu.")
    dung_man_hinh()


# ===================== MỤC 3: TẠO KHOÁ LỚN =====================

def chon_tao_khoa_lon():
    global khoa_lon
    tieu_de("3. TẠO KHOÁ LỚN VÀ ĐO THỜI GIAN")
    so_bit = nhap_so_nguyen("Độ dài khoá n (bit) [Enter = 1024; gợi ý 512/1024/2048]: ",
                            mac_dinh=1024, toi_thieu=64)
    print(f"Đang sinh khoá {so_bit} bit (hai số nguyên tố mỗi số ~{so_bit // 2} bit)...")
    bat_dau = time.perf_counter()
    khoa = sinh_khoa(so_bit)
    giay = time.perf_counter() - bat_dau
    khoa_lon = khoa
    phi = (khoa["p"] - 1) * (khoa["q"] - 1)
    print(f"\nThời gian sinh khoá: {giay:.3f} giây")
    print(f"p ({khoa['p'].bit_length()} bit) = {rut_gon(khoa['p'])}")
    print(f"q ({khoa['q'].bit_length()} bit) = {rut_gon(khoa['q'])}")
    print(f"n ({khoa['n'].bit_length()} bit) = {rut_gon(khoa['n'])}")
    print(f"e = {khoa['e']}")
    print(f"d ({khoa['d'].bit_length()} bit) = {rut_gon(khoa['d'])}")
    print(f"Kiểm tra e*d mod phi(n) = {khoa['e'] * khoa['d'] % phi}  (phải bằng 1)")
    dung_man_hinh()


def lay_khoa_lon():
    """Trả về khoá lớn hiện có; nếu chưa có thì sinh khoá 1024 bit."""
    global khoa_lon
    if khoa_lon is None:
        print("(Chưa có khoá lớn, tự sinh khoá 1024 bit...)")
        khoa_lon = sinh_khoa(1024)
    return khoa_lon


# ===================== MỤC 4: MÃ HOÁ VĂN BẢN =====================

def chon_ma_hoa_van_ban():
    tieu_de("4. MÃ HOÁ VÀ GIẢI MÃ VĂN BẢN (khoá lớn)")
    khoa = lay_khoa_lon()
    n, e, d = khoa["n"], khoa["e"], khoa["d"]
    print(f"Đang dùng khoá {n.bit_length()} bit. Nhấn Enter để dùng câu mẫu:")
    print(f'  "{VAN_BAN_MAU}"')
    van_ban = input("Nhập văn bản: ").strip() or VAN_BAN_MAU

    du_lieu = van_ban.encode("utf-8")
    k = _kich_thuoc_khoi(n)
    print(f"\nVăn bản: {len(van_ban)} ký tự = {len(du_lieu)} byte (UTF-8)")
    print(f"Kích thước khối: {k} byte  (đảm bảo mỗi khối < n)")

    t0 = time.perf_counter()
    ban_ma, do_dai = ma_hoa_van_ban(van_ban, n, e)
    t_mh = time.perf_counter() - t0
    print(f"Số khối bản mã: {len(ban_ma)}")
    for i, c in enumerate(ban_ma[:3], 1):
        print(f"  Khối {i}: {rut_gon(c, 30, 10)}")
    if len(ban_ma) > 3:
        print(f"  ... ({len(ban_ma) - 3} khối nữa)")

    t0 = time.perf_counter()
    giai = giai_ma_van_ban(ban_ma, do_dai, n, d)
    t_gm = time.perf_counter() - t0

    print(f"\nBản giải mã: {giai}")
    print("Khớp với bản gốc:", "ĐÚNG" if giai == van_ban else "SAI!")
    print(f"Thời gian mã hoá : {t_mh * 1000:.2f} ms  (khoá công khai e = {e}, nhỏ nên nhanh)")
    print(f"Thời gian giải mã: {t_gm * 1000:.2f} ms  (khoá riêng d dài {d.bit_length()} bit nên chậm hơn)")
    dung_man_hinh()


# ===================== MỤC 5: MÃ HOÁ TỆP =====================

def chon_ma_hoa_tep():
    tieu_de("5. MÃ HOÁ VÀ GIẢI MÃ TỆP (văn bản, ảnh nhỏ...)")
    duong_dan = input("Đường dẫn tệp (nên chọn tệp nhỏ, vài KB): ").strip().strip('"')
    if not os.path.isfile(duong_dan):
        print("Không tìm thấy tệp.")
        return dung_man_hinh()
    kich_thuoc = os.path.getsize(duong_dan)
    if kich_thuoc > GIOI_HAN_TEP:
        tra_loi = input(f"Tệp {kich_thuoc // 1024} KB khá lớn, giải mã sẽ lâu. Tiếp tục? (c/k): ")
        if tra_loi.strip().lower() != "c":
            return dung_man_hinh()

    khoa = lay_khoa_lon()
    n, e, d = khoa["n"], khoa["e"], khoa["d"]
    with open(duong_dan, "rb") as f:
        du_lieu = f.read()
    print(f"\nTệp gốc: {kich_thuoc} byte. Khoá {n.bit_length()} bit, khối {_kich_thuoc_khoi(n)} byte.")

    t0 = time.perf_counter()
    ban_ma, do_dai = ma_hoa_bytes(du_lieu, n, e)
    t_mh = time.perf_counter() - t0
    tep_ma = duong_dan + ".rsa"
    with open(tep_ma, "w") as f:
        f.write(f"{do_dai}\n")                      # dòng 1: độ dài tệp gốc
        f.write("\n".join(format(c, "x") for c in ban_ma))   # mỗi dòng một khối (hex)
    print(f"Đã mã hoá -> {tep_ma}  ({os.path.getsize(tep_ma)} byte, {len(ban_ma)} khối, {t_mh:.3f} giây)")

    # Đọc lại tệp .rsa và giải mã
    with open(tep_ma) as f:
        dong = f.read().split("\n")
    do_dai_doc = int(dong[0])
    ban_ma_doc = [int(x, 16) for x in dong[1:] if x]
    t0 = time.perf_counter()
    giai = giai_ma_bytes(ban_ma_doc, do_dai_doc, n, d)
    t_gm = time.perf_counter() - t0
    goc, duoi = os.path.splitext(duong_dan)
    tep_giai = f"{goc}_giaima{duoi}"
    with open(tep_giai, "wb") as f:
        f.write(giai)
    print(f"Đã giải mã -> {tep_giai}  ({t_gm:.3f} giây)")

    # hashlib chỉ để kiểm tra tệp trùng khớp, không dùng trong phần lõi RSA
    trung = hashlib.sha256(du_lieu).hexdigest() == hashlib.sha256(giai).hexdigest()
    print("Tệp giải mã trùng tệp gốc:", "ĐÚNG" if trung else "SAI!")
    dung_man_hinh()


# ===================== MỤC 6: BẢNG ĐO THỜI GIAN (CHO BÁO CÁO) =====================

def chon_bang_do():
    tieu_de("6. BẢNG ĐO THỜI GIAN THEO ĐỘ DÀI KHOÁ")
    so_lan = nhap_so_nguyen("Số lần đo mỗi độ dài khoá [Enter = 3]: ", mac_dinh=3, toi_thieu=1)
    mau = (VAN_BAN_MAU * 20).encode("utf-8")[:1000].decode("utf-8", errors="ignore")
    print(f"Dữ liệu đo: văn bản mẫu ~{len(mau.encode('utf-8'))} byte. Đang đo, vui lòng chờ...\n")
    ket_qua = []
    for so_bit in (512, 1024, 2048):
        t_khoa = t_mh = t_gm = 0.0
        for _ in range(so_lan):
            t0 = time.perf_counter()
            k = sinh_khoa(so_bit)
            t_khoa += time.perf_counter() - t0
            t0 = time.perf_counter()
            bm, dd = ma_hoa_van_ban(mau, k["n"], k["e"])
            t_mh += time.perf_counter() - t0
            t0 = time.perf_counter()
            giai_ma_van_ban(bm, dd, k["n"], k["d"])
            t_gm += time.perf_counter() - t0
        ket_qua.append((so_bit, t_khoa / so_lan, t_mh / so_lan * 1000, t_gm / so_lan * 1000))
        print(f"  xong {so_bit} bit")

    print(f"\n{'Khoá (bit)':>10} | {'Sinh khoá (s)':>14} | {'Mã hoá (ms)':>12} | {'Giải mã (ms)':>13}")
    print("-" * 58)
    for so_bit, a, b, c in ket_qua:
        print(f"{so_bit:>10} | {a:>14.3f} | {b:>12.2f} | {c:>13.2f}")
    print(f"(Trung bình {so_lan} lần đo. Sinh khoá dao động mạnh vì chọn số nguyên tố ngẫu nhiên.)")

    ten_tep = "thoi_gian_rsa.csv"
    with open(ten_tep, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Khoá (bit)", "Sinh khoá (s)", "Mã hoá (ms)", "Giải mã (ms)", "Số lần đo"])
        for so_bit, a, b, c in ket_qua:
            w.writerow([so_bit, round(a, 3), round(b, 2), round(c, 2), so_lan])
    print(f"Đã lưu bảng vào {ten_tep} (mở bằng Excel, ghi cấu hình máy vào báo cáo).")
    dung_man_hinh()


# ===================== MENU CHÍNH =====================

def main():
    menu = {
        "1": ("Tạo khoá ví dụ nhỏ (in từng bước)", chon_tao_khoa_nho),
        "2": ("Mã hoá/giải mã với khoá nhỏ (in từng bước)", chon_ma_hoa_khoa_nho),
        "3": ("Tạo khoá lớn và đo thời gian", chon_tao_khoa_lon),
        "4": ("Mã hoá/giải mã văn bản (khoá lớn)", chon_ma_hoa_van_ban),
        "5": ("Mã hoá/giải mã tệp", chon_ma_hoa_tep),
        "6": ("Bảng đo thời gian 512/1024/2048 bit (cho báo cáo)", chon_bang_do),
        "0": ("Thoát", None),
    }
    while True:
        print("\n" + "=" * 64)
        print("                    DEMO HỆ MÃ RSA")
        print("=" * 64)
        for phim, (ten, _) in menu.items():
            print(f"  {phim}. {ten}")
        lua_chon = input("Chọn: ").strip()
        if lua_chon == "0":
            print("Tạm biệt!")
            break
        if lua_chon in menu:
            try:
                menu[lua_chon][1]()
            except KeyboardInterrupt:
                print("\nĐã dừng.")
            except Exception as loi:   # tránh sập chương trình giữa buổi demo
                print(f"\nCó lỗi: {type(loi).__name__}: {loi}")
        else:
            print("Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()
