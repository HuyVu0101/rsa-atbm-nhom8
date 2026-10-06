"""
so_hoc.py  --  PHẦN CỦA TV2: các thuật toán số học nền cho RSA.

QUY ƯỚC: tất cả tham số và kết quả đều là số nguyên (int) của Python.
Không dùng pow(a, b, n) hay math.gcd cho phần lõi; bạn phải tự cài đặt.
(Chỉ được dùng các hàm có sẵn trong tests để đối chiếu kết quả.)
"""


def euclid_mo_rong(a, b):
    """
    Thuật toán Euclid mở rộng.

    Trả về bộ ba (d, x, y) sao cho:  d = gcd(a, b)  và  a*x + b*y = d

    Ví dụ: euclid_mo_rong(30, 18) -> (6, -1, 2)   vì 30*(-1) + 18*2 = 6

    Gợi ý: có thể làm bằng vòng lặp hoặc đệ quy.
      - Điều kiện dừng: nếu b == 0 thì gcd = a, với x = 1, y = 0.
      - Ngược lại: gọi đệ quy với (b, a % b) rồi suy ra x, y của (a, b)
        từ x', y' vừa nhận:  x = y',  y = x' - (a // b) * y'
    """
    # TODO (TV2): viết thuật toán ở đây
    raise NotImplementedError("TV2: chưa cài euclid_mo_rong")


def uoc_chung_lon_nhat(a, b):
    """
    Trả về gcd(a, b).
    Gợi ý: chỉ cần gọi euclid_mo_rong và lấy phần tử đầu tiên.
    """
    # TODO (TV2)
    raise NotImplementedError("TV2: chưa cài uoc_chung_lon_nhat")


def nghich_dao_modulo(a, n):
    """
    Tìm x sao cho (a * x) % n == 1, với 0 < x < n.
    Nếu gcd(a, n) != 1 thì không tồn tại nghịch đảo: raise ValueError.

    Ví dụ: nghich_dao_modulo(7, 40) -> 23   vì 7*23 = 161 = 4*40 + 1

    Gợi ý: dùng euclid_mo_rong(a, n) được (d, x, y).
      Nếu d == 1 thì x chính là nghịch đảo, nhưng x có thể âm, nên lấy x % n.
    """
    # TODO (TV2)
    raise NotImplementedError("TV2: chưa cài nghich_dao_modulo")


def luy_thua_modulo(co_so, so_mu, modulo):
    """
    Tính (co_so ** so_mu) % modulo bằng thuật toán BÌNH PHƯƠNG VÀ NHÂN
    (square-and-multiply), KHÔNG được tính co_so ** so_mu rồi mới lấy dư
    (vì số sẽ quá lớn).

    Ví dụ: luy_thua_modulo(4, 13, 497) -> 445

    Gợi ý (duyệt từng bit của so_mu từ phải sang trái):
      ket_qua = 1
      co_so = co_so % modulo
      trong khi so_mu > 0:
          nếu bit cuối của so_mu là 1 (so_mu % 2 == 1): ket_qua = ket_qua * co_so % modulo
          so_mu = so_mu // 2
          co_so = co_so * co_so % modulo
    """
    # TODO (TV2)
    raise NotImplementedError("TV2: chưa cài luy_thua_modulo")
