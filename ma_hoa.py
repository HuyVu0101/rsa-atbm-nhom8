"""
ma_hoa.py  --  PHẦN CỦA TV3: mã hoá và giải mã RSA.

Hai hàm lõi ma_hoa_so / giai_ma_so để TV3 điền (mỗi hàm chỉ 1 dòng).
Phần chia khối văn bản và tệp đã được viết sẵn, chỉ cần đọc hiểu để
giải thích khi bảo vệ.

Lưu ý: đây là RSA "sách giáo khoa" (không có padding như OAEP) nên chỉ
dùng để học tập, không dùng cho hệ thống thật.
"""
from so_hoc import luy_thua_modulo


# ---------- PHẦN LÕI (TV3 điền) ----------

def ma_hoa_so(m, n, e):
    """
    Mã hoá một số nguyên m (0 <= m < n):  c = m^e mod n
    Gợi ý: dùng luy_thua_modulo.
    """
    # TODO (TV3)
    raise NotImplementedError("TV3: chưa cài ma_hoa_so")


def giai_ma_so(c, n, d):
    """
    Giải mã một số nguyên c:  m = c^d mod n
    Gợi ý: dùng luy_thua_modulo.
    """
    # TODO (TV3)
    raise NotImplementedError("TV3: chưa cài giai_ma_so")


# ---------- PHẦN VIẾT SẴN (chia khối, chuyển byte <-> số) ----------

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
