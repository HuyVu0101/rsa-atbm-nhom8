"""
QUY ƯỚC: tất cả tham số và kết quả đều là số nguyên (int) của Python.
Không dùng pow(a, b, n) hay math.gcd cho phần lõi; phải tự cài đặt.
"""


def euclid_mo_rong(a, b):
    """
    Thuật toán Euclid mở rộng.

    Trả về bộ ba (d, x, y) sao cho:
        d = gcd(a, b)
        a*x + b*y = d

    Ví dụ:
        euclid_mo_rong(30, 18) -> (6, -1, 2)
        vì 30*(-1) + 18*2 = 6.
    """
    # Bước 1: điều kiện dừng của thuật toán Euclid.
    # Khi b = 0 thì gcd(a, 0) = |a|.
    if b == 0:
        # Chọn hệ số x sao cho a*x = |a|, giúp gcd luôn không âm.
        if a >= 0:
            return a, 1, 0
        return -a, -1, 0

    # Bước 2: giải bài toán nhỏ hơn với (b, a mod b).
    d, x1, y1 = euclid_mo_rong(b, a % b)

    # Bước 3: thế ngược để tìm hệ số Bézout của cặp (a, b).
    # Từ: d = b*x1 + (a % b)*y1
    # và a % b = a - (a // b)*b
    # suy ra: d = a*y1 + b*(x1 - (a // b)*y1)
    x = y1
    y = x1 - (a // b) * y1

    return d, x, y


def uoc_chung_lon_nhat(a, b):
    """
    Trả về gcd(a, b) bằng cách gọi Euclid mở rộng.
    """
    # Euclid mở rộng đã tính gcd ở phần tử đầu tiên của bộ ba kết quả.
    d, _, _ = euclid_mo_rong(a, b)
    return d


def nghich_dao_modulo(a, n):
    """
    Tìm x sao cho (a * x) % n == 1, với 0 < x < n.

    Nếu gcd(a, n) != 1 thì a không có nghịch đảo modulo n và hàm
    sẽ raise ValueError.

    Ví dụ:
        nghich_dao_modulo(7, 40) -> 23
        vì 7*23 = 161 = 4*40 + 1.
    """
    # Trong RSA, modulo phải là số nguyên dương lớn hơn 1.
    if n <= 1:
        raise ValueError("Modulo n phải lớn hơn 1")

    # Bước 1: tìm d, x, y sao cho a*x + n*y = d = gcd(a, n).
    d, x, _ = euclid_mo_rong(a, n)

    # Bước 2: nghịch đảo chỉ tồn tại khi a và n nguyên tố cùng nhau.
    if d != 1:
        raise ValueError(f"{a} không có nghịch đảo modulo {n}")

    # Bước 3: x có thể âm, nên đưa về đại diện chuẩn trong [0, n-1].
    return x % n


def luy_thua_modulo(co_so, so_mu, modulo):
    """
    Tính (co_so ** so_mu) % modulo bằng thuật toán BÌNH PHƯƠNG VÀ NHÂN
    (square-and-multiply), không tính co_so ** so_mu rồi mới lấy dư.

    Ví dụ:
        luy_thua_modulo(4, 13, 497) -> 445
    """
    # RSA dùng số mũ không âm và modulo dương.
    if so_mu < 0:
        raise ValueError("Số mũ phải không âm")
    if modulo <= 0:
        raise ValueError("Modulo phải là số nguyên dương")

    # Bước 1: khởi tạo kết quả và rút gọn cơ số ngay từ đầu.
    ket_qua = 1 % modulo
    co_so = co_so % modulo

    # Bước 2: duyệt các bit của số mũ từ phải sang trái.
    while so_mu > 0:
        # Nếu bit cuối là 1, nhân cơ số hiện tại vào kết quả.
        if so_mu % 2 == 1:
            ket_qua = (ket_qua * co_so) % modulo

        # Bỏ bit cuối của số mũ.
        so_mu = so_mu // 2

        # Bình phương cơ số để chuẩn bị cho bit tiếp theo.
        co_so = (co_so * co_so) % modulo

    return ket_qua
