"""
test_rsa.py  --  PHẦN CỦA TV4: kiểm thử.

Chạy toàn bộ kiểm thử :  python -m unittest test_rsa -v
Chạy minh hoạ tấn công :  python test_rsa.py tan_cong
Thư viện chuẩn (pow, math.gcd) chỉ được dùng Ở ĐÂY để đối chiếu.
"""
import math
import random
import sys
import time
import unittest

from so_hoc import euclid_mo_rong, uoc_chung_lon_nhat, nghich_dao_modulo, luy_thua_modulo
from sinh_khoa import miller_rabin, sinh_so_nguyen_to, sinh_khoa, khoa_tu_p_q
from ma_hoa import ma_hoa_so, giai_ma_so, ma_hoa_van_ban, giai_ma_van_ban, ma_hoa_bytes, giai_ma_bytes


class TestSoHoc(unittest.TestCase):
    def test_euclid_mo_rong(self):
        d, x, y = euclid_mo_rong(30, 18)
        self.assertEqual(d, 6)
        self.assertEqual(30 * x + 18 * y, 6)

    def test_euclid_ngau_nhien(self):
        for _ in range(50):
            a, b = random.randint(1, 10**6), random.randint(1, 10**6)
            d, x, y = euclid_mo_rong(a, b)
            self.assertEqual(d, math.gcd(a, b))
            self.assertEqual(a * x + b * y, d)

    def test_gcd(self):
        self.assertEqual(uoc_chung_lon_nhat(48, 36), 12)

    def test_nghich_dao(self):
        self.assertEqual(nghich_dao_modulo(7, 40), 23)
        with self.assertRaises(ValueError):
            nghich_dao_modulo(6, 9)   # gcd = 3, không có nghịch đảo

    def test_luy_thua_modulo(self):
        self.assertEqual(luy_thua_modulo(4, 13, 497), 445)
        for _ in range(50):
            a, b, n = random.randint(1, 10**9), random.randint(1, 10**9), random.randint(2, 10**9)
            self.assertEqual(luy_thua_modulo(a, b, n), pow(a, b, n))


class TestSinhKhoa(unittest.TestCase):
    def test_miller_rabin(self):
        for p in [2, 3, 5, 97, 7919, 104729]:
            self.assertTrue(miller_rabin(p), p)
        for h in [1, 4, 91, 561, 1105, 104730]:   # 561, 1105 là số Carmichael
            self.assertFalse(miller_rabin(h), h)

    def test_sinh_so_nguyen_to(self):
        p = sinh_so_nguyen_to(64)
        self.assertEqual(p.bit_length(), 64)
        self.assertTrue(miller_rabin(p))

    def test_khoa_nho(self):
        k = khoa_tu_p_q(11, 13, 7)
        self.assertEqual((k["n"], k["e"], k["d"]), (143, 7, 103))

    def test_sinh_khoa_lon(self):
        k = sinh_khoa(256)
        phi = (k["p"] - 1) * (k["q"] - 1)
        self.assertEqual(k["e"] * k["d"] % phi, 1)


class TestMaHoa(unittest.TestCase):
    def test_vi_du_tinh_tay(self):
        # n=143, e=7, d=103: bản rõ 9 -> bản mã 48
        self.assertEqual(ma_hoa_so(9, 143, 7), 48)
        self.assertEqual(giai_ma_so(48, 143, 103), 9)

    def test_van_ban_tieng_viet(self):
        k = sinh_khoa(512)
        van_ban = "An toàn và bảo mật thông tin mạng"
        ban_ma, do_dai = ma_hoa_van_ban(van_ban, k["n"], k["e"])
        self.assertEqual(giai_ma_van_ban(ban_ma, do_dai, k["n"], k["d"]), van_ban)

    def test_chuoi_rong(self):
        k = sinh_khoa(512)
        van_ban = ""
        ban_ma, do_dai = ma_hoa_van_ban(van_ban, k["n"], k["e"])
        self.assertEqual(giai_ma_van_ban(ban_ma, do_dai, k["n"], k["d"]), van_ban)

    def test_ky_tu_dac_biet_va_emoji(self):
        k = sinh_khoa(512)
        van_ban = "Test @#$*^% 🚀 Tiếng Việt: Ă Â Đ Ê Ô Ơ Ư - 123456789"
        ban_ma, do_dai = ma_hoa_van_ban(van_ban, k["n"], k["e"])
        self.assertEqual(giai_ma_van_ban(ban_ma, do_dai, k["n"], k["d"]), van_ban)

    def test_van_ban_sieu_dai(self):
        k = sinh_khoa(512)
        van_ban = "Học phần An toàn và bảo mật thông tin mạng - NEU. " * 20
        ban_ma, do_dai = ma_hoa_van_ban(van_ban, k["n"], k["e"])
        self.assertEqual(giai_ma_van_ban(ban_ma, do_dai, k["n"], k["d"]), van_ban)


class TestDoiChieuQuyMo(unittest.TestCase):
    """Đối chiếu số lượng lớn với hàm chuẩn của Python (số ngẫu nhiên cố định để lặp lại được)."""

    def setUp(self):
        random.seed(8)

    def test_nghich_dao_1000_cap(self):
        dem = loi = 0
        while dem < 1000:
            n = random.randint(2, 10**6) if dem < 500 else random.getrandbits(1024) | 1
            a = random.randint(1, n - 1)
            if math.gcd(a, n) == 1:
                dem += 1
                self.assertEqual(nghich_dao_modulo(a, n), pow(a, -1, n))
            else:
                with self.assertRaises(ValueError):
                    nghich_dao_modulo(a, n)
                loi += 1
        self.assertGreater(loi, 0)

    def test_luy_thua_1000_bo(self):
        for i in range(1000):
            bit = 16 if i < 500 else 1024
            a, b, n = random.getrandbits(bit), random.getrandbits(bit), random.getrandbits(bit) | 1
            self.assertEqual(luy_thua_modulo(a, b, n), pow(a, b, n))

    def test_miller_rabin_den_9999(self):
        def nt_chuan(n):
            return n > 1 and all(n % i for i in range(2, int(n ** 0.5) + 1))
        for n in range(2, 10000):
            self.assertEqual(miller_rabin(n), nt_chuan(n), n)
        for c in [561, 1105, 1729, 2465, 2821, 6601, 8911]:      # số Carmichael
            self.assertFalse(miller_rabin(c), c)
        for p in [2**127 - 1, 2**521 - 1]:
            self.assertTrue(miller_rabin(p))
        for h in [(2**61 - 1) * (2**89 - 1), (2**127 - 1) * (2**107 - 1)]:
            self.assertFalse(miller_rabin(h))

    def test_khoi_phuc_byte_ngau_nhien(self):
        for bits in (512, 1024):
            k = sinh_khoa(bits)
            for i in range(25):
                du = bytes(random.getrandbits(8) for _ in range(random.randint(0, 600)))
                if i % 5 == 0:
                    du = b"\x00\x00" + du                        # byte 0 ở đầu dữ liệu
                ban_ma, do_dai = ma_hoa_bytes(du, k["n"], k["e"])
                self.assertEqual(giai_ma_bytes(ban_ma, do_dai, k["n"], k["d"]), du)


# ---------- MINH HOẠ TẤN CÔNG: phân tích n bằng phép chia thử ----------

def chia_thu(n):
    """Trả về (thừa số nhỏ nhất, số phép chia thử)."""
    if n % 2 == 0:
        return 2, 1
    so_thu, i = 1, 3
    while i * i <= n:
        so_thu += 1
        if n % i == 0:
            return i, so_thu
        i += 2
    return n, so_thu


class TestTanCong(unittest.TestCase):
    def test_be_khoa_nho(self):
        random.seed(8)
        k = sinh_khoa(40)
        ban_ma, do_dai = ma_hoa_van_ban("Giao dich 123", k["n"], k["e"])
        p, _ = chia_thu(k["n"])
        q = k["n"] // p
        d = nghich_dao_modulo(k["e"], (p - 1) * (q - 1))
        self.assertEqual(d, k["d"])
        self.assertEqual(giai_ma_van_ban(ban_ma, do_dai, k["n"], d), "Giao dich 123")


def tan_cong():
    """Chạy: python test_rsa.py tan_cong  (dùng để chụp ảnh minh hoạ cho báo cáo)."""
    random.seed(8)
    print("PHAN 1: Ke tan cong chi co khoa cong khai (n, e) va ban ma")
    k = sinh_khoa(40)
    n, e = k["n"], k["e"]
    ban_ro = "Giao dich 123"
    ban_ma, do_dai = ma_hoa_van_ban(ban_ro, n, e)
    print("  n = %d (%d bit), e = %d" % (n, n.bit_length(), e))
    p, so_thu = chia_thu(n)
    q = n // p
    d = nghich_dao_modulo(e, (p - 1) * (q - 1))
    print("  Phan tich duoc: p = %d, q = %d sau %d phep chia thu" % (p, q, so_thu))
    print("  Tinh lai d = %d (khoa rieng that: d = %d, %s)" % (d, k["d"], "TRUNG" if d == k["d"] else "KHAC"))
    kq = giai_ma_van_ban(ban_ma, do_dai, n, d)
    print("  Giai ma ban ma bang d tim duoc: '%s' -> %s" % (kq, "KHOP ban ro goc" if kq == ban_ro else "SAI"))

    print("\nPHAN 2: So phep chia thu theo do dai N")
    print("%-12s %-22s %-16s %s" % ("Do dai N", "Thua so nho nhat p", "So phep chia thu", "Thoi gian (s)"))
    toc_do = None
    for bits in (24, 32, 40, 48):
        k = sinh_khoa(bits)
        t = time.perf_counter()
        p, so_thu = chia_thu(k["n"])
        dt = time.perf_counter() - t
        if bits == 48:
            toc_do = so_thu / dt
        print("%-12s %-22d %-16d %.3f" % ("%d bit" % k["n"].bit_length(), min(k["p"], k["q"]), so_thu, dt))

    print("\nPHAN 3: Uoc luong voi khoa that")
    for bits in (512, 1024, 2048):
        nam = 2 ** (bits // 2 - 1) / toc_do / (365 * 24 * 3600)
        print("  N %4d bit: can toi da khoang 2^%d phep chia thu, tuc khoang 10^%d nam voi toc do %.1e phep/giay cua may nay"
              % (bits, bits // 2 - 1, len(str(int(nam))) - 1, toc_do))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "tan_cong":
        tan_cong()
    else:
        unittest.main()