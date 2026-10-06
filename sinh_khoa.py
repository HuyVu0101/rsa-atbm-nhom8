"""
sinh_khoa.py  --  PHẦN CỦA TV3: kiểm tra số nguyên tố và sinh khoá RSA.

Phụ thuộc vào so_hoc.py của TV2. Trong lúc chờ TV2, có thể thử với
bộ số nhỏ viết tay (p=11, q=13, e=7) để kiểm tra logic của mình.
"""
import random

from so_hoc import uoc_chung_lon_nhat, nghich_dao_modulo, luy_thua_modulo


def miller_rabin(n, so_vong=20):
    """
    Kiểm tra n có phải số nguyên tố hay không (xác suất).
    Trả về True nếu n "có thể là nguyên tố", False nếu chắc chắn là hợp số.

    Gợi ý:
      1. Loại nhanh các trường hợp: n < 2 -> False; n là 2 hoặc 3 -> True;
         n chẵn -> False.
      2. Viết n - 1 = 2^s * d  với d lẻ (chia 2 liên tục cho đến khi lẻ).
      3. Lặp so_vong lần:
           - chọn ngẫu nhiên a trong [2, n-2]
           - x = luy_thua_modulo(a, d, n)
           - nếu x == 1 hoặc x == n-1: bỏ qua, sang vòng sau
           - lặp s-1 lần: x = x*x % n; nếu x == n-1 thì thoát vòng lặp, sang vòng sau
           - nếu không gặp n-1: trả về False (hợp số)
      4. Qua hết mọi vòng: trả về True.
    """
    # TODO (TV3)
    raise NotImplementedError("TV3: chưa cài miller_rabin")


def sinh_so_nguyen_to(so_bit):
    """
    Sinh một số nguyên tố ngẫu nhiên có đúng `so_bit` bit.

    Gợi ý:
      - Lấy số ngẫu nhiên: random.getrandbits(so_bit)
      - Ép bit cao nhất = 1 (để đủ độ dài) và bit thấp nhất = 1 (để là số lẻ):
            so = random.getrandbits(so_bit) | (1 << (so_bit - 1)) | 1
      - Lặp đến khi miller_rabin(so) trả về True.
    """
    # TODO (TV3)
    raise NotImplementedError("TV3: chưa cài sinh_so_nguyen_to")


def sinh_khoa(so_bit=1024, e=65537):
    """
    Sinh cặp khoá RSA với modulus n khoảng `so_bit` bit.

    Trả về dict:
        {"n": ..., "e": ..., "d": ..., "p": ..., "q": ...}
    Khoá công khai = (n, e), khoá riêng = (n, d).

    Gợi ý:
      1. p = sinh_so_nguyen_to(so_bit // 2);  q = sinh_so_nguyen_to(so_bit // 2)
         (lặp lại nếu p == q)
      2. n = p * q;   phi = (p - 1) * (q - 1)
      3. Kiểm tra uoc_chung_lon_nhat(e, phi) == 1; nếu không thì sinh lại p, q.
      4. d = nghich_dao_modulo(e, phi)
    """
    # TODO (TV3)
    raise NotImplementedError("TV3: chưa cài sinh_khoa")


def khoa_tu_p_q(p, q, e):
    """
    Dựng khoá từ p, q, e cho trước (dùng cho ví dụ tính tay: p=11, q=13, e=7).
    Trả về dict giống sinh_khoa. Ví dụ: khoa_tu_p_q(11, 13, 7) -> n=143, d=103.

    Gợi ý: làm giống bước 2-4 của sinh_khoa nhưng không sinh ngẫu nhiên.
    """
    # TODO (TV3)
    raise NotImplementedError("TV3: chưa cài khoa_tu_p_q")
