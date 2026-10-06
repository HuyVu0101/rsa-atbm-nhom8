"""
test_rsa.py  --  PHẦN CỦA TV4: kiểm thử.

Chạy toàn bộ:  python -m unittest test_rsa -v
Ban đầu các test sẽ lỗi (NotImplementedError); khi TV2, TV3 cài xong
thì phải chuyển dần sang OK. TV4 bổ sung thêm ca kiểm thử của riêng mình.
Thư viện chuẩn (pow, math.gcd) chỉ được dùng Ở ĐÂY để đối chiếu.
"""
import math
import random
import unittest

from so_hoc import euclid_mo_rong, uoc_chung_lon_nhat, nghich_dao_modulo, luy_thua_modulo
from sinh_khoa import miller_rabin, sinh_so_nguyen_to, sinh_khoa, khoa_tu_p_q
from ma_hoa import ma_hoa_so, giai_ma_so, ma_hoa_van_ban, giai_ma_van_ban


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


if __name__ == "__main__":
    unittest.main()
