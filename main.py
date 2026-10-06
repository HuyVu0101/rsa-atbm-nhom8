"""
main.py  --  PHẦN CỦA TV5: giao diện dòng lệnh để demo.

Chạy:  python main.py
Menu mẫu đã nối sẵn với các module; TV5 chỉnh lời nhắc, thêm in các bước
trung gian, đo thời gian, v.v. cho phù hợp với kịch bản demo.
"""
import time

from sinh_khoa import sinh_khoa, khoa_tu_p_q
from ma_hoa import ma_hoa_van_ban, giai_ma_van_ban

khoa = None


def chon_tao_khoa_nho():
    global khoa
    khoa = khoa_tu_p_q(11, 13, 7)
    print("Khoá ví dụ nhỏ:", khoa)
    # TODO (TV5): in rõ n, phi(n), e, d để đối chiếu với bảng tính tay của TV4


def chon_tao_khoa_lon():
    global khoa
    so_bit = int(input("Độ dài khoá (512 / 1024 / 2048): "))
    bat_dau = time.time()
    khoa = sinh_khoa(so_bit)
    print(f"Sinh khoá xong trong {time.time() - bat_dau:.2f} giây")
    print("n =", khoa["n"])
    # TODO (TV5): in e, d; ghi lại thời gian vào bảng đo của báo cáo


def chon_ma_hoa_giai_ma():
    if khoa is None:
        print("Hãy tạo khoá trước.")
        return
    van_ban = input("Nhập văn bản: ")
    ban_ma, do_dai = ma_hoa_van_ban(van_ban, khoa["n"], khoa["e"])
    print("Bản mã (danh sách số):", ban_ma)
    print("Giải mã:", giai_ma_van_ban(ban_ma, do_dai, khoa["n"], khoa["d"]))
    # TODO (TV5): thêm mã hoá tệp (đọc bytes từ tệp rồi gọi ma_hoa_bytes)


def main():
    menu = {
        "1": ("Tạo khoá ví dụ nhỏ (p=11, q=13)", chon_tao_khoa_nho),
        "2": ("Tạo khoá lớn", chon_tao_khoa_lon),
        "3": ("Mã hoá và giải mã văn bản", chon_ma_hoa_giai_ma),
        "0": ("Thoát", None),
    }
    while True:
        print("\n=== DEMO RSA ===")
        for phim, (ten, _) in menu.items():
            print(f"{phim}. {ten}")
        lua_chon = input("Chọn: ").strip()
        if lua_chon == "0":
            break
        if lua_chon in menu:
            menu[lua_chon][1]()
        else:
            print("Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()
