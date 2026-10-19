"""
ma_hoa.py -- Mã hoá và giải mã RSA.

Công thức:
  - Mã hoá : C = M^e mod N, với 0 <= M < N   (dùng khoá công khai KU = {e, N})
  - Giải mã: M = C^d mod N                   (dùng khoá riêng     KR = {d, p, q})

Vì bản rõ M phải nhỏ hơn N, văn bản dài cần được chia khối: văn bản được đổi
sang dãy byte (mã UTF-8, hỗ trợ tiếng Việt có dấu), chia thành các khối nhỏ,
mỗi khối đổi thành một số nguyên M < N rồi mã hoá riêng.

Lưu ý: chương trình cài đặt RSA ở dạng cơ bản, chưa bổ sung
kỹ thuật đệm (padding, ví dụ OAEP) mà các hệ thống thực tế sử dụng, vì vậy chỉ
phục vụ mục đích học tập.
"""
from so_hoc import luy_thua_modulo


# ---------- MÃ HOÁ / GIẢI MÃ MỘT SỐ ----------

def ma_hoa_so(m, n, e):
    """
    Mã hoá một số nguyên m (0 <= m < n):  C = M^e mod N

    Ví dụ: ma_hoa_so(9, 143, 7)  -> 48
           ma_hoa_so(88, 187, 7) -> 11
    """
    return luy_thua_modulo(m, e, n)


def giai_ma_so(c, n, d):
    """
    Giải mã một số nguyên c:  M = C^d mod N

    Ví dụ: giai_ma_so(48, 143, 103) -> 9
           giai_ma_so(11, 187, 23)  -> 88
    """
    return luy_thua_modulo(c, d, n)


# ---------- CHIA KHỐI VÀ CHUYỂN BYTE <-> SỐ ----------

def _kich_thuoc_khoi(n):
    """Số byte tối đa của một khối plaintext sao cho giá trị khối < n."""
    kich_thuoc = (n.bit_length() - 1) // 8
    if kich_thuoc < 1:
        raise ValueError("n quá nhỏ để mã hoá dữ liệu byte (cần n > 255)")
    return kich_thuoc


def ma_hoa_bytes(du_lieu, n, e):
    """
    Mã hoá chuỗi bytes: chia thành khối, mỗi khối thành một số, mã hoá từng số.
    Trả về (danh_sach_ban_ma, do_dai_goc).
    do_dai_goc cần để cắt bỏ phần đệm khi giải mã.
    """
    k = _kich_thuoc_khoi(n)
    ban_ma = []
    for i in range(0, len(du_lieu), k):
        khoi = du_lieu[i:i + k]
        m = int.from_bytes(khoi, "big")
        ban_ma.append(ma_hoa_so(m, n, e))
    return ban_ma, len(du_lieu)


def giai_ma_bytes(ban_ma, do_dai_goc, n, d):
    """Giải mã danh sách số về lại chuỗi bytes ban đầu."""
    k = _kich_thuoc_khoi(n)
    ket_qua = bytearray()
    con_lai = do_dai_goc
    for c in ban_ma:
        m = giai_ma_so(c, n, d)
        do_dai_khoi = min(k, con_lai)   # khối cuối có thể ngắn hơn
        ket_qua += m.to_bytes(do_dai_khoi, "big")
        con_lai -= do_dai_khoi
    return bytes(ket_qua)


def ma_hoa_van_ban(van_ban, n, e):
    """Mã hoá chuỗi văn bản (UTF-8, hỗ trợ tiếng Việt có dấu)."""
    return ma_hoa_bytes(van_ban.encode("utf-8"), n, e)


def giai_ma_van_ban(ban_ma, do_dai_goc, n, d):
    """Giải mã về lại chuỗi văn bản."""
    return giai_ma_bytes(ban_ma, do_dai_goc, n, d).decode("utf-8")


if __name__ == "__main__":
    # Chỉ chạy khi bấm Run trực tiếp file này (khi file khác import thì không chạy)
    print("=== CHẠY THỬ ma_hoa.py ===")
    n, e, d = 143, 7, 103
    c = ma_hoa_so(9, n, e)
    print("Mã hoá 9  ->", c)
    print("Giải mã", c, "->", giai_ma_so(c, n, d))
