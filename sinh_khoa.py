"""
sinh_khoa.py -- Kiểm tra số nguyên tố (Miller-Rabin) và sinh cặp khoá RSA.

Dùng các hàm số học nền trong so_hoc.py:
  - uoc_chung_lon_nhat : kiểm tra e nguyên tố cùng nhau với phi(n)
  - nghich_dao_modulo  : tính khoá riêng d
  - luy_thua_modulo    : tính nhanh a^d mod n trong Miller-Rabin
"""
import random

from so_hoc import uoc_chung_lon_nhat, nghich_dao_modulo, luy_thua_modulo


def miller_rabin(n, so_vong=20):
    """
    Kiểm tra n có phải số nguyên tố hay không bằng thuật toán Miller-Rabin
    (theo bài giảng Chương 3, mục 2.3).

    Bài giảng mô tả một lần thử với một số a ngẫu nhiên; ở đây lặp lại
    so_vong lần với các a khác nhau để giảm xác suất kết luận sai.

    Trả về:
      - False: n chắc chắn là hợp số.
      - True : n "có thể là số nguyên tố", xác suất sai không quá (1/4)^so_vong.
               Với so_vong = 20, xác suất sai <= 1/4^20 (khoảng 1 phần nghìn tỷ).

    Ví dụ: miller_rabin(97) -> True,  miller_rabin(561) -> False (561 là số Carmichael).
    """
    # Bước 1: loại nhanh các trường hợp đặc biệt
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Bước 2: biểu diễn n - 1 = 2^k * q với q lẻ (chia 2 liên tục cho đến khi lẻ)
    k, q = 0, n - 1
    while q % 2 == 0:
        q //= 2
        k += 1

    # Bước 3: thử với so_vong cơ số a chọn ngẫu nhiên
    for _ in range(so_vong):
        a = random.randint(2, n - 2)          # chọn a với 1 < a < n-1
        x = luy_thua_modulo(a, q, n)          # x = a^q mod n
        if x == 1 or x == n - 1:
            continue                  # a^q mod n = 1 hoặc = n-1: a không chứng minh được n là hợp số
        for _ in range(k - 1):
            x = x * x % n             # lần lượt tính a^(2q), a^(4q), ..., a^(2^(k-1) q) mod n
            if x == n - 1:
                break                 # gặp n-1 -> vòng này qua
        else:
            return False              # không bao giờ gặp n-1: a là "nhân chứng", n là hợp số

    # Bước 4: qua hết các vòng -> coi n là số nguyên tố
    return True


def sinh_so_nguyen_to(so_bit):
    """
    Sinh một số nguyên tố ngẫu nhiên có đúng `so_bit` bit.

    Ví dụ: sinh_so_nguyen_to(64).bit_length() == 64
    """
    while True:
        # Ép bit cao nhất = 1 (đủ độ dài so_bit) và bit thấp nhất = 1 (số lẻ)
        so = random.getrandbits(so_bit) | (1 << (so_bit - 1)) | 1
        if miller_rabin(so):
            return so


def sinh_khoa(so_bit=1024, e=65537):
    """
    Tạo cặp khoá RSA với modulo N = p*q dài khoảng `so_bit` bit.

    Trả về dict {"n", "e", "d", "p", "q"}, trong đó (theo bài giảng):
      - Khoá công khai: KU = {e, N}
      - Khoá riêng    : KR = {d, p, q}

    Về khoá mã hoá e: bài giảng yêu cầu 1 < e < Phi(N) và gcd(e, Phi(N)) = 1.
    Nhóm chọn mặc định e = 65537 (= 2^16 + 1) vì đây là số nguyên tố, có ít
    bit 1 nên phép mã hoá nhanh, và là giá trị được dùng phổ biến trong thực tế.
    """
    while True:
        # Bước 1: sinh hai số nguyên tố khác nhau, mỗi số dài một nửa số bit
        p = sinh_so_nguyen_to(so_bit // 2)
        q = sinh_so_nguyen_to(so_bit // 2)
        if p == q:
            continue
        # Bước 2: tính n và phi(n)
        n = p * q
        phi = (p - 1) * (q - 1)
        # Bước 3: e phải nguyên tố cùng nhau với phi(n), nếu không thì sinh lại p, q
        if uoc_chung_lon_nhat(e, phi) != 1:
            continue
        # Bước 4: khoá riêng d là nghịch đảo của e modulo phi(n), tức e*d mod phi = 1
        d = nghich_dao_modulo(e, phi)
        return {"n": n, "e": e, "d": d, "p": p, "q": q}


def khoa_tu_p_q(p, q, e):
    """
    Tạo khoá RSA từ p, q, e cho trước (dùng cho các ví dụ tính tay).

    Ví dụ:
      khoa_tu_p_q(11, 13, 7) -> N = 143, Phi(N) = 120, d = 103
      khoa_tu_p_q(17, 11, 7) -> N = 187, Phi(N) = 160, d = 23   (ví dụ trong bài giảng)
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    if uoc_chung_lon_nhat(e, phi) != 1:
        raise ValueError(f"e = {e} không nguyên tố cùng nhau với phi(n) = {phi}")
    d = nghich_dao_modulo(e, phi)
    return {"n": n, "e": e, "d": d, "p": p, "q": q}


if __name__ == "__main__":
    # Chỉ chạy khi bấm Run trực tiếp file này (khi file khác import thì không chạy)
    print("=== CHẠY THỬ sinh_khoa.py ===")
    for so in (11, 13, 561, 104729):
        print(f"miller_rabin({so}) = {miller_rabin(so)}")
    print("Khoá từ p=11, q=13, e=7:", khoa_tu_p_q(11, 13, 7))
    k = sinh_khoa(512)
    print("Khoá 512 bit: n có", k["n"].bit_length(), "bit")
