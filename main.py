"""
main.py -- Giao diện đồ hoạ Hiện đại (Modern Dashboard UI) Demo Hệ mã RSA.
Học phần: An toàn và bảo mật thông tin mạng
Tên nhóm: Cấu hình tại hằng số NHOM bên dưới.

Phong cách thiết kế:
- Giao diện Dashboard hiện đại (Sidebar Navigation + Card-based Layout)
- 100% Thư viện chuẩn Python (tkinter, ttk, threading, queue, time, os, csv, hashlib, sys)
- Phông chữ Segoe UI / Consolas phân cấp rõ ràng, dễ nhìn khi chiếu màn hình lớn
- Tuyệt đối không can thiệp hay sửa đổi các file thuật toán:
  so_hoc.py, sinh_khoa.py, ma_hoa.py, test_rsa.py, main_cli.py.

Chạy chương trình:
    python main.py
"""

import csv
import hashlib
import os
import queue
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Import các hàm lõi RSA từ các module trong nhóm (giữ nguyên quy ước không sửa các file này)
from ma_hoa import (
    _kich_thuoc_khoi,
    giai_ma_bytes,
    giai_ma_so,
    giai_ma_van_ban,
    ma_hoa_bytes,
    ma_hoa_so,
    ma_hoa_van_ban,
)
from sinh_khoa import khoa_tu_p_q, miller_rabin, sinh_khoa, sinh_so_nguyen_to
from so_hoc import (
    euclid_mo_rong,
    luy_thua_modulo,
    nghich_dao_modulo,
    uoc_chung_lon_nhat,
)

# Thiết lập encoding hiển thị tiếng Việt trên console Windows nếu có in log
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ==============================================================================
# HẰNG SỐ TOÀN CỤC & TÊN NHÓM (SỬA TÊN NHÓM TẠI ĐÂY)
# ==============================================================================
NHOM = "Nhóm 8"  # Đổi tên nhóm tại đây để cập nhật toàn bộ ứng dụng

VAN_BAN_MAU = "Thương mại điện tử an toàn nhờ mật mã khoá công khai RSA"

VAN_BAN_DAI = (
    "Hệ thống thanh toán trực tuyến và thương mại điện tử hiện đại đòi hỏi mức độ bảo mật "
    "thông tin tối đa nhằm bảo vệ quyền riêng tư và dữ liệu giao dịch của người dùng. "
    "Mật mã khoá công khai RSA đóng vai trò nền tảng trong việc thiết lập kết nối an toàn "
    "thông qua giao thức HTTPS, chữ ký số và xác thực điện tử. Bằng việc phân tách thành hai "
    "khoá công khai và bí mật dựa trên độ khó của bài toán phân tích thừa số nguyên tố của số lớn, "
    "RSA đảm bảo rằng thông tin chỉ có thể được giải mã bởi người sở hữu khoá bí mật tương ứng, "
    "ngăn chặn hoàn toàn các nguy cơ tấn công nghe lén và giả mạo trên không gian mạng."
)

GIOI_HAN_TEP = 200 * 1024  # Cảnh báo nếu tệp lớn hơn 200 KB

# Hệ màu Slate & Indigo lấy cảm hứng từ Tailwind CSS
CLR_SIDEBAR_BG = "#0F172A"      # Slate 900 (Sidebar nền tối sang trọng)
CLR_SIDEBAR_HOVER = "#1E293B"   # Slate 800 (Hover menu)
CLR_SIDEBAR_ACTIVE = "#2563EB"  # Blue 600 (Mục menu đang chọn)
CLR_SIDEBAR_TEXT = "#94A3B8"    # Slate 400 (Chữ menu thường)
CLR_SIDEBAR_TEXT_ACT = "#FFFFFF"# Trắng (Chữ menu active)

CLR_APP_BG = "#F8FAFC"          # Slate 50 (Nền ứng dụng xám sáng tinh tế)
CLR_TOPBAR_BG = "#FFFFFF"       # Nền thanh tiêu đề trên
CLR_CARD_BG = "#FFFFFF"         # Nền các thẻ nội dung
CLR_CARD_BORDER = "#E2E8F0"     # Slate 200 (Viền mỏng 1px phẳng)

CLR_TEXT_MAIN = "#0F172A"       # Slate 900 (Chữ chính đậm rõ)
CLR_TEXT_MUTED = "#64748B"      # Slate 500 (Chữ phụ / mô tả)

CLR_PRIMARY = "#2563EB"         # Blue 600 (Nút chính)
CLR_PRIMARY_HOVER = "#1D4ED8"   # Blue 700
CLR_ACCENT = "#0284C7"          # Sky 600

CLR_SUCCESS_TEXT = "#15803D"    # Green 700 (Thành công / ĐÚNG)
CLR_SUCCESS_BG = "#DCFCE7"      # Green 100 (Nền xanh nhạt)
CLR_SUCCESS_BORDER = "#86EFAC"  # Green 300

CLR_DANGER_TEXT = "#B91C1C"     # Red 700 (Lỗi / SAI)
CLR_DANGER_BG = "#FEE2E2"       # Red 100 (Nền đỏ nhạt)
CLR_DANGER_BORDER = "#FCA5A5"   # Red 300

CLR_INFO_TEXT = "#0369A1"       # Sky 700 (Thông tin / KU)
CLR_INFO_BG = "#E0F2FE"         # Sky 100
CLR_INFO_BORDER = "#7DD3FC"

CLR_WARN_TEXT = "#B45309"       # Amber 700 (Cảnh báo / KR)
CLR_WARN_BG = "#FEF3C7"         # Amber 100
CLR_WARN_BORDER = "#FCD34D"

# Phông chữ hệ thống hiện đại
FONT_BRAND = ("Segoe UI", 12, "bold")
FONT_TITLE_PAGE = ("Segoe UI", 13, "bold")
FONT_CARD_TITLE = ("Segoe UI", 11, "bold")
FONT_BODY = ("Segoe UI", 9)
FONT_BODY_BOLD = ("Segoe UI", 9, "bold")
FONT_SMALL = ("Segoe UI", 8)
FONT_CODE = ("Consolas", 9)
FONT_CODE_BOLD = ("Consolas", 9, "bold")


# ==============================================================================
# TIỆN ÍCH TOÁN HỌC VÀ HIỂN THỊ
# ==============================================================================
def rut_gon(so, dau=22, cuoi=10):
    """Rút gọn số nguyên lớn để hiển thị gọn gàng."""
    s = str(so)
    if len(s) <= dau + cuoi + 8:
        return s
    return f"{s[:dau]}...{s[-cuoi:]}  ({len(s)} chữ số)"


def tinh_euclid_cac_buoc(phi, e):
    """Sinh danh sách các bước của thuật toán Euclid mở rộng."""
    r0, x0, y0 = phi, 1, 0
    r1, x1, y1 = e, 0, 1

    cac_buoc = []
    buoc = 1
    cac_buoc.append((buoc, "-", r0, x0, y0, f"{r0} = {phi}*(1) + {e}*(0)"))
    buoc += 1
    cac_buoc.append((buoc, "-", r1, x1, y1, f"{r1} = {phi}*(0) + {e}*(1)"))

    while r1 != 0:
        q = r0 // r1
        r_moi = r0 - q * r1
        x_moi = x0 - q * x1
        y_moi = y0 - q * y1

        r0, r1 = r1, r_moi
        x0, x1 = x1, x_moi
        y0, y1 = y1, y_moi

        buoc += 1
        he_thuc = f"{r0} = {phi}*({x0}) + {e}*({y0})"
        cac_buoc.append((buoc, q, r0, x0, y0, he_thuc))

    gcd = r0
    d = y0 % phi
    g, _, y_tv2 = euclid_mo_rong(phi, e)
    assert g == gcd and y_tv2 % phi == d, "Không khớp so_hoc.euclid_mo_rong!"
    return cac_buoc, gcd, d


def tinh_luy_thua_cac_buoc(co_so, so_mu, modulo):
    """Sinh danh sách các bước của thuật toán Bình phương và nhân."""
    bits = bin(so_mu)[2:]
    cac_buoc = []
    kq = 1

    for idx, b in enumerate(bits, 1):
        truoc = kq
        kq = (kq * kq) % modulo
        bp_str = f"{truoc}² mod {modulo} = {kq}"

        if b == "1":
            truoc2 = kq
            kq = (kq * co_so) % modulo
            nhan_str = f"{truoc2} * {co_so} mod {modulo} = {kq}"
        else:
            nhan_str = "-"

        cac_buoc.append((idx, b, bp_str, nhan_str, kq))

    assert kq == luy_thua_modulo(co_so, so_mu, modulo), "Không khớp so_hoc.luy_thua_modulo!"
    return cac_buoc, kq


# ==============================================================================
# QUẢN LÝ TRẠNG THÁI TOÀN CỤC (STATE MANAGEMENT)
# ==============================================================================
class TrangThai:
    def __init__(self):
        self.khoa_nho = None
        self.khoa_lon = None
        self.thoi_gian_sinh_lon = 0.0
        self._listeners = []

    def dang_ky(self, callback):
        self._listeners.append(callback)

    def thong_bao(self):
        for cb in self._listeners:
            try:
                cb(self)
            except Exception:
                pass


# ==============================================================================
# CÁC WIDGET PHONG CÁCH HIỆN ĐẠI (CUSTOM FLAT COMPONENTS)
# ==============================================================================
class ModernCard(tk.Frame):
    """Thẻ nội dung trắng phẳng bo viền 1px tinh tế."""
    def __init__(self, parent, tieu_de=None, **kwargs):
        super().__init__(parent, bg=CLR_CARD_BG, bd=1, relief="solid",
                         highlightthickness=1, highlightbackground=CLR_CARD_BORDER,
                         highlightcolor=CLR_CARD_BORDER, **kwargs)
        if tieu_de:
            f_head = tk.Frame(self, bg=CLR_CARD_BG)
            f_head.pack(fill="x", padx=10, pady=(6, 2))
            tk.Label(f_head, text=tieu_de, font=FONT_CARD_TITLE,
                     fg=CLR_TEXT_MAIN, bg=CLR_CARD_BG).pack(anchor="w")
            tk.Frame(self, bg=CLR_CARD_BORDER, height=1).pack(fill="x", padx=8, pady=(2, 4))


class ModernButton(tk.Label):
    """Nút bấm phẳng hiện đại với hiệu ứng hover mượt mà."""
    def __init__(self, parent, text, command=None, bg_color=CLR_PRIMARY,
                 hover_color=CLR_PRIMARY_HOVER, fg_color="white", font=FONT_BODY_BOLD,
                 padx=10, pady=4, **kwargs):
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.fg_color = fg_color
        self._state = "normal"

        super().__init__(parent, text=text, font=font, bg=bg_color, fg=fg_color,
                         padx=padx, pady=pady, cursor="hand2", **kwargs)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _on_enter(self, e):
        if self._state == "normal":
            self.configure(bg=self.hover_color)

    def _on_leave(self, e):
        if self._state == "normal":
            self.configure(bg=self.bg_color)

    def _on_click(self, e):
        if self._state == "normal" and self.command:
            self.command()

    def config_state(self, state):
        self._state = state
        if state == "disabled":
            self.configure(bg="#CBD5E1", fg="#94A3B8", cursor="arrow")
        else:
            self.configure(bg=self.bg_color, fg=self.fg_color, cursor="hand2")


class StatusBadge(tk.Frame):
    """Thẻ trạng thái dạng Pill bo mềm mại."""
    def __init__(self, parent, text="", status_type="info", **kwargs):
        super().__init__(parent, bd=1, relief="solid", **kwargs)
        self.lbl = tk.Label(self, text=text, font=FONT_BODY_BOLD, padx=8, pady=3)
        self.lbl.pack(fill="x", expand=True)
        self.set_status(text, status_type)

    def set_status(self, text, status_type="info"):
        self.lbl.config(text=text)
        if status_type == "success":
            bg, fg, border = CLR_SUCCESS_BG, CLR_SUCCESS_TEXT, CLR_SUCCESS_BORDER
        elif status_type == "danger":
            bg, fg, border = CLR_DANGER_BG, CLR_DANGER_TEXT, CLR_DANGER_BORDER
        elif status_type == "warn":
            bg, fg, border = CLR_WARN_BG, CLR_WARN_TEXT, CLR_WARN_BORDER
        else:
            bg, fg, border = CLR_INFO_BG, CLR_INFO_TEXT, CLR_INFO_BORDER

        self.config(bg=bg, highlightbackground=border, highlightthickness=1)
        self.lbl.config(bg=bg, fg=fg)


# ==============================================================================
# HỘP THOẠI XEM CHI TIẾT SỐ LỚN
# ==============================================================================
class HopThoaiXemChiTiet(tk.Toplevel):
    def __init__(self, parent, ten_bien, gia_tri, so_bit=None):
        super().__init__(parent)
        self.title(f"Chi tiết tham số: {ten_bien}")
        self.geometry("700x440")
        self.minsize(550, 340)
        self.configure(bg=CLR_APP_BG)
        self.transient(parent)
        self.grab_set()

        f_head = tk.Frame(self, bg=CLR_SIDEBAR_BG, padx=16, pady=12)
        f_head.pack(fill="x")
        tk.Label(f_head, text=f"Tham số: {ten_bien}", font=FONT_BRAND,
                 fg="white", bg=CLR_SIDEBAR_BG).pack(anchor="w")
        info = f"Độ dài: {len(str(gia_tri))} chữ số thập phân"
        if so_bit:
            info += f" | {so_bit} bit nhị phân"
        tk.Label(f_head, text=info, font=FONT_SMALL, fg=CLR_SIDEBAR_TEXT,
                 bg=CLR_SIDEBAR_BG).pack(anchor="w")

        f_body = tk.Frame(self, bg=CLR_APP_BG, padx=16, pady=12)
        f_body.pack(fill="both", expand=True)

        txt = tk.Text(f_body, font=FONT_CODE, wrap="char", bd=1, relief="solid",
                      bg="#FFFFFF", fg=CLR_TEXT_MAIN, padx=8, pady=8)
        txt.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(f_body, orient="vertical", command=txt.yview)
        sb.pack(side="right", fill="y")
        txt.configure(yscrollcommand=sb.set)
        txt.insert("1.0", str(gia_tri))
        txt.configure(state="disabled")

        f_btn = tk.Frame(self, bg=CLR_APP_BG, padx=16, pady=10)
        f_btn.pack(fill="x")

        self.lbl_msg = tk.Label(f_btn, text="", font=FONT_BODY_BOLD,
                                fg=CLR_SUCCESS_TEXT, bg=CLR_APP_BG)
        self.lbl_msg.pack(side="left")

        ModernButton(f_btn, "Đóng", command=self.destroy,
                     bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN).pack(side="right", padx=4)
        ModernButton(f_btn, "📋 Sao chép", command=lambda: self.sao_chep(str(gia_tri))).pack(side="right", padx=4)

    def sao_chep(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.lbl_msg.config(text="✓ Đã sao chép vào bộ nhớ tạm!")
        self.after(2000, lambda: self.lbl_msg.config(text=""))


# ==============================================================================
# TAB 1: KHOÁ NHỎ & CÁC BƯỚC TÍNH TOÁN (ĐÃ TĂNG CHIỀU CAO BẢNG)
# ==============================================================================
class TabKhoaNho(tk.Frame):
    def __init__(self, parent, trang_thai, status_cb):
        super().__init__(parent, bg=CLR_APP_BG, padx=12, pady=6)
        self.trang_thai = trang_thai
        self.set_status = status_cb

        self.euclid_steps = []
        self.euclid_idx = 0
        self.sq_steps = []
        self.sq_idx = 0
        self.sq_kq = None

        self._tao_giao_dien()

    def _tao_giao_dien(self):
        # Bố cục 2 Card: Card 1 trên (hiện đủ 6 dòng Euclid), Card 2 dưới (hiện đủ 8 dòng Bình phương)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # ----------------- CARD 1: TẠO KHOÁ NHỎ -----------------
        c1 = ModernCard(self, tieu_de="1. Khởi tạo khoá nhỏ (p, q, e) & Thuật toán Euclid mở rộng")
        c1.grid(row=0, column=0, sticky="nsew", pady=(0, 6))

        f_in = tk.Frame(c1, bg=CLR_CARD_BG)
        f_in.pack(fill="x", padx=10, pady=2)

        tk.Label(f_in, text="Số p:", font=FONT_BODY_BOLD, bg=CLR_CARD_BG).pack(side="left")
        self.ent_p = ttk.Entry(f_in, width=6, font=FONT_CODE)
        self.ent_p.insert(0, "11")
        self.ent_p.pack(side="left", padx=(3, 8))
        self.ent_p.bind("<Return>", lambda e: self.thuc_hien_tao_khoa())

        tk.Label(f_in, text="Số q:", font=FONT_BODY_BOLD, bg=CLR_CARD_BG).pack(side="left")
        self.ent_q = ttk.Entry(f_in, width=6, font=FONT_CODE)
        self.ent_q.insert(0, "13")
        self.ent_q.pack(side="left", padx=(3, 8))
        self.ent_q.bind("<Return>", lambda e: self.thuc_hien_tao_khoa())

        tk.Label(f_in, text="Số e:", font=FONT_BODY_BOLD, bg=CLR_CARD_BG).pack(side="left")
        self.ent_e = ttk.Entry(f_in, width=6, font=FONT_CODE)
        self.ent_e.insert(0, "7")
        self.ent_e.pack(side="left", padx=(3, 10))
        self.ent_e.bind("<Return>", lambda e: self.thuc_hien_tao_khoa())

        ModernButton(f_in, "⚡ Tạo khoá", command=self.thuc_hien_tao_khoa).pack(side="left", padx=2)
        ModernButton(f_in, "Mẫu (11,13,7)", command=lambda: self._dat_mau(11, 13, 7),
                     bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN).pack(side="left", padx=2)
        ModernButton(f_in, "Mẫu (17,11,7)", command=lambda: self._dat_mau(17, 11, 7),
                     bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN).pack(side="left", padx=2)

        # Điều khiển trình chiếu Euclid
        f_ctrl_e = tk.Frame(c1, bg=CLR_CARD_BG)
        f_ctrl_e.pack(fill="x", padx=10, pady=2)

        self.lbl_ly_thuyet = tk.Label(
            f_ctrl_e, text="Nhấn 'Tạo khoá' để kiểm tra nguyên tố & tìm d.",
            font=FONT_BODY, bg=CLR_CARD_BG, fg=CLR_TEXT_MUTED, anchor="w"
        )
        self.lbl_ly_thuyet.pack(side="left", fill="x", expand=True)

        self.btn_e_next = ModernButton(f_ctrl_e, "⏭ Bước tiếp", command=self.euclid_buoc_tiep,
                                       bg_color="#0284C7", hover_color="#0369A1", padx=8, pady=2)
        self.btn_e_next.pack(side="right", padx=2)
        self.btn_e_next.config_state("disabled")

        self.btn_e_all = ModernButton(f_ctrl_e, "⏩ Hiện hết", command=self.euclid_hien_tat_ca,
                                      bg_color="#475569", hover_color="#334155", padx=8, pady=2)
        self.btn_e_all.pack(side="right", padx=2)
        self.btn_e_all.config_state("disabled")

        self.btn_e_reset = ModernButton(f_ctrl_e, "🔄 Làm lại", command=self.euclid_lam_lai,
                                        bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN, padx=8, pady=2)
        self.btn_e_reset.pack(side="right", padx=2)
        self.btn_e_reset.config_state("disabled")

        # Treeview Euclid (hiện đủ ít nhất 6 dòng)
        f_tv_e = tk.Frame(c1, bg=CLR_CARD_BG)
        f_tv_e.pack(fill="both", expand=True, padx=10, pady=2)

        cols_e = ("buoc", "q", "r", "x", "y", "he_thuc")
        self.tree_euclid = ttk.Treeview(f_tv_e, columns=cols_e, show="headings", height=6)
        self.tree_euclid.heading("buoc", text="Bước")
        self.tree_euclid.heading("q", text="q (Thương)")
        self.tree_euclid.heading("r", text="r (Số dư)")
        self.tree_euclid.heading("x", text="x")
        self.tree_euclid.heading("y", text="y")
        self.tree_euclid.heading("he_thuc", text="Hệ thức đồng dư Bézout (r = phi*x + e*y)")

        self.tree_euclid.column("buoc", width=45, anchor="center")
        self.tree_euclid.column("q", width=75, anchor="center")
        self.tree_euclid.column("r", width=75, anchor="center")
        self.tree_euclid.column("x", width=75, anchor="center")
        self.tree_euclid.column("y", width=75, anchor="center")
        self.tree_euclid.column("he_thuc", width=340, anchor="w")
        self.tree_euclid.pack(side="left", fill="both", expand=True)

        sb_e = ttk.Scrollbar(f_tv_e, orient="vertical", command=self.tree_euclid.yview)
        sb_e.pack(side="right", fill="y")
        self.tree_euclid.configure(yscrollcommand=sb_e.set)

        # Cặp khoá kết quả KU & KR
        f_ku_kr = tk.Frame(c1, bg=CLR_CARD_BG)
        f_ku_kr.pack(fill="x", padx=10, pady=(2, 6))

        self.box_ku = StatusBadge(f_ku_kr, "Khoá công khai KU = { e, n } (Mã hoá)", "info")
        self.box_ku.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.box_kr = StatusBadge(f_ku_kr, "Khoá bí mật KR = { d, p, q } (Giải mã)", "warn")
        self.box_kr.pack(side="left", fill="x", expand=True, padx=(4, 0))

        # ----------------- CARD 2: MÃ HOÁ KHOÁ NHỎ -----------------
        c2 = ModernCard(self, tieu_de="2. Mã hoá & Giải mã từng bước (Bình phương và nhân)")
        c2.grid(row=1, column=0, sticky="nsew")

        f_in_m = tk.Frame(c2, bg=CLR_CARD_BG)
        f_in_m.pack(fill="x", padx=10, pady=2)

        tk.Label(f_in_m, text="Số M hoặc từ A-Z:", font=FONT_BODY_BOLD, bg=CLR_CARD_BG).pack(side="left", padx=(0, 4))
        self.ent_m = ttk.Entry(f_in_m, width=12, font=FONT_CODE)
        self.ent_m.insert(0, "9")
        self.ent_m.pack(side="left", padx=(0, 8))
        self.ent_m.bind("<Return>", lambda e: self.thuc_hien_ma_hoa_nho())

        ModernButton(f_in_m, "🔒 Mã hoá & Giải mã", command=self.thuc_hien_ma_hoa_nho).pack(side="left", padx=2)
        ModernButton(f_in_m, "Thử 'HELLO'", command=lambda: self._dat_m_chu("HELLO"),
                     bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN).pack(side="left", padx=2)

        self.badge_mh = StatusBadge(f_in_m, "Chưa có dữ liệu tính toán.", "info")
        self.badge_mh.pack(side="left", fill="x", expand=True, padx=(8, 0))

        # Điều khiển trình chiếu Bình phương & nhân
        f_ctrl_sq = tk.Frame(c2, bg=CLR_CARD_BG)
        f_ctrl_sq.pack(fill="x", padx=10, pady=2)

        self.lbl_sq_title = tk.Label(f_ctrl_sq, text="Bảng Bình phương và nhân:",
                                     font=FONT_BODY_BOLD, bg=CLR_CARD_BG)
        self.lbl_sq_title.pack(side="left")

        self.btn_sq_next = ModernButton(f_ctrl_sq, "⏭ Bước tiếp", command=self.sq_buoc_tiep,
                                        bg_color="#0284C7", hover_color="#0369A1", padx=8, pady=2)
        self.btn_sq_next.pack(side="right", padx=2)
        self.btn_sq_next.config_state("disabled")

        self.btn_sq_all = ModernButton(f_ctrl_sq, "⏩ Hiện hết", command=self.sq_hien_tat_ca,
                                       bg_color="#475569", hover_color="#334155", padx=8, pady=2)
        self.btn_sq_all.pack(side="right", padx=2)
        self.btn_sq_all.config_state("disabled")

        self.btn_sq_reset = ModernButton(f_ctrl_sq, "🔄 Làm lại", command=self.sq_lam_lai,
                                         bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN, padx=8, pady=2)
        self.btn_sq_reset.pack(side="right", padx=2)
        self.btn_sq_reset.config_state("disabled")

        # Treeview Square and Multiply (hiện đủ ít nhất 8 dòng)
        f_tv_sq = tk.Frame(c2, bg=CLR_CARD_BG)
        f_tv_sq.pack(fill="both", expand=True, padx=10, pady=(2, 6))

        cols_sq = ("buoc", "bit", "bp", "nhan", "kq")
        self.tree_sq = ttk.Treeview(f_tv_sq, columns=cols_sq, show="headings", height=8)
        self.tree_sq.heading("buoc", text="Bước")
        self.tree_sq.heading("bit", text="Bit số mũ")
        self.tree_sq.heading("bp", text="Bình phương (x² mod n)")
        self.tree_sq.heading("nhan", text="Nhân cơ số (nếu bit=1)")
        self.tree_sq.heading("kq", text="Kết quả sau bước")

        self.tree_sq.column("buoc", width=45, anchor="center")
        self.tree_sq.column("bit", width=75, anchor="center")
        self.tree_sq.column("bp", width=220, anchor="w")
        self.tree_sq.column("nhan", width=220, anchor="w")
        self.tree_sq.column("kq", width=110, anchor="center")
        self.tree_sq.pack(side="left", fill="both", expand=True)

        sb_sq = ttk.Scrollbar(f_tv_sq, orient="vertical", command=self.tree_sq.yview)
        sb_sq.pack(side="right", fill="y")
        self.tree_sq.configure(yscrollcommand=sb_sq.set)

    def _dat_mau(self, p, q, e):
        self.ent_p.delete(0, "end"); self.ent_p.insert(0, str(p))
        self.ent_q.delete(0, "end"); self.ent_q.insert(0, str(q))
        self.ent_e.delete(0, "end"); self.ent_e.insert(0, str(e))
        self.thuc_hien_tao_khoa()

    def _dat_m_chu(self, s):
        self.ent_m.delete(0, "end"); self.ent_m.insert(0, s)
        self.thuc_hien_ma_hoa_nho()

    def thuc_hien_tao_khoa(self):
        try:
            p_s, q_s, e_s = self.ent_p.get().strip(), self.ent_q.get().strip(), self.ent_e.get().strip()
            if not p_s or not q_s or not e_s:
                messagebox.showwarning("Thiếu tham số", "Vui lòng nhập đầy đủ p, q, e!")
                return
            p, q, e = int(p_s), int(q_s), int(e_s)

            if p <= 1 or q <= 1:
                messagebox.showerror("Giá trị không hợp lệ", "p và q phải là số nguyên > 1!")
                return
            if p == q:
                messagebox.showerror("Trùng số", "p và q phải là hai số nguyên tố khác nhau!")
                return
            if not miller_rabin(p):
                messagebox.showerror("Hợp số", f"p = {p} không phải là số nguyên tố!")
                return
            if not miller_rabin(q):
                messagebox.showerror("Hợp số", f"q = {q} không phải là số nguyên tố!")
                return

            n = p * q
            phi = (p - 1) * (q - 1)
            if uoc_chung_lon_nhat(e, phi) != 1:
                messagebox.showerror("gcd ≠ 1", f"e = {e} không nguyên tố cùng nhau với phi(n) = {phi}!")
                return

            steps, gcd, d = tinh_euclid_cac_buoc(phi, e)
            khoa = khoa_tu_p_q(p, q, e)
            self.trang_thai.khoa_nho = khoa
            self.trang_thai.thong_bao()

            txt_ly_thuyet = (
                f"✓ n = {n} | phi(n) = {phi} | gcd({e},{phi})=1 ==> d = {d}  (e*d mod phi = {e*d % phi})"
            )
            self.lbl_ly_thuyet.config(text=txt_ly_thuyet, fg=CLR_TEXT_MAIN)

            self.euclid_steps = steps
            self.euclid_idx = 0
            for item in self.tree_euclid.get_children():
                self.tree_euclid.delete(item)

            self.btn_e_next.config_state("normal")
            self.btn_e_all.config_state("normal")
            self.btn_e_reset.config_state("normal")

            self.box_ku.set_status(f"Khoá công khai KU = {{ e = {e}, n = {n} }}", "info")
            self.box_kr.set_status(f"Khoá bí mật KR = {{ d = {d}, p = {p}, q = {q} }}", "warn")

            self.set_status(f"Đã tạo khoá nhỏ n={n}, e={e}, d={d}")

        except ValueError:
            messagebox.showerror("Sai kiểu", "p, q, e phải là số nguyên!")
        except Exception as ex:
            messagebox.showerror("Lỗi", str(ex))

    def euclid_buoc_tiep(self):
        if self.euclid_idx < len(self.euclid_steps):
            self.tree_euclid.insert("", "end", values=self.euclid_steps[self.euclid_idx])
            self.euclid_idx += 1
            if self.euclid_idx == len(self.euclid_steps):
                self.btn_e_next.config_state("disabled")

    def euclid_hien_tat_ca(self):
        while self.euclid_idx < len(self.euclid_steps):
            self.euclid_buoc_tiep()

    def euclid_lam_lai(self):
        for item in self.tree_euclid.get_children():
            self.tree_euclid.delete(item)
        self.euclid_idx = 0
        self.btn_e_next.config_state("normal")

    def thuc_hien_ma_hoa_nho(self):
        if self.trang_thai.khoa_nho is None:
            self.thuc_hien_tao_khoa()
        if self.trang_thai.khoa_nho is None:
            return

        n = self.trang_thai.khoa_nho["n"]
        e = self.trang_thai.khoa_nho["e"]
        d = self.trang_thai.khoa_nho["d"]

        raw = self.ent_m.get().strip()
        if not raw:
            messagebox.showwarning("Trống", "Vui lòng nhập một số hoặc chữ cái A-Z!")
            return

        if raw.isdigit():
            m = int(raw)
            if m < 0 or m >= n:
                messagebox.showerror("M quá lớn", f"0 ≤ M < n (tức 0 ≤ M < {n})!")
                return
            c = ma_hoa_so(m, n, e)
            m_giai = giai_ma_so(c, n, d)
            dung = (m == m_giai)

            self.badge_mh.set_status(
                f"M={m} → C={c} → M'={m_giai} ({'✓ ĐÚNG' if dung else '✗ SAI'})",
                "success" if dung else "danger"
            )

            self.sq_steps, self.sq_kq = tinh_luy_thua_cac_buoc(m, e, n)
            self.lbl_sq_title.config(text=f"Bình phương & nhân C = {m}^{e} mod {n}:")
            self.sq_lam_lai()

        elif raw.isalpha() and raw.isascii():
            raw_upper = raw.upper()
            gia_tri = [ord(ch) - 64 for ch in raw_upper]
            if max(gia_tri) >= n:
                messagebox.showerror("Khoá nhỏ", f"Khoá n = {n} không đủ cho chữ cái này!")
                return

            ban_ma, ban_giai = [], []
            for ch, m_val in zip(raw_upper, gia_tri):
                c_val = ma_hoa_so(m_val, n, e)
                m2_val = giai_ma_so(c_val, n, d)
                ban_ma.append(c_val)
                ban_giai.append(chr(m2_val + 64))

            chuoi_giai = "".join(ban_giai)
            dung = (raw_upper == chuoi_giai)

            self.badge_mh.set_status(
                f"'{raw_upper}' → Mã: {ban_ma} → Giải: '{chuoi_giai}' ({'✓ ĐÚNG' if dung else '✗ SAI'})",
                "success" if dung else "danger"
            )

            self.sq_steps, self.sq_kq = tinh_luy_thua_cac_buoc(gia_tri[0], e, n)
            self.lbl_sq_title.config(text=f"Bình phương & nhân '{raw_upper[0]}' (M={gia_tri[0]}):")
            self.sq_lam_lai()
        else:
            messagebox.showerror("Dữ liệu không hợp lệ", "Nhập số nguyên không âm hoặc chữ A-Z không dấu!")

    def sq_buoc_tiep(self):
        if self.sq_idx < len(self.sq_steps):
            self.tree_sq.insert("", "end", values=self.sq_steps[self.sq_idx])
            self.sq_idx += 1
            if self.sq_idx == len(self.sq_steps):
                self.btn_sq_next.config_state("disabled")

    def sq_hien_tat_ca(self):
        while self.sq_idx < len(self.sq_steps):
            self.sq_buoc_tiep()

    def sq_lam_lai(self):
        for item in self.tree_sq.get_children():
            self.tree_sq.delete(item)
        self.sq_idx = 0
        self.btn_sq_next.config_state("normal")
        self.btn_sq_all.config_state("normal")
        self.btn_sq_reset.config_state("normal")


# ==============================================================================
# TAB 2: KHOÁ LỚN (512 - 2048 BIT)
# ==============================================================================
class TabKhoaLon(tk.Frame):
    def __init__(self, parent, trang_thai, status_cb):
        super().__init__(parent, bg=CLR_APP_BG, padx=14, pady=10)
        self.trang_thai = trang_thai
        self.set_status = status_cb
        self.dang_sinh = False
        self.msg_queue = queue.Queue()

        self._tao_giao_dien()
        self._kiem_tra_queue()

    def _tao_giao_dien(self):
        c_top = ModernCard(self, tieu_de="Thiết lập tham số sinh cặp khoá RSA")
        c_top.pack(fill="x", pady=(0, 8))

        f_ctrl = tk.Frame(c_top, bg=CLR_CARD_BG)
        f_ctrl.pack(fill="x", padx=12, pady=(2, 8))

        tk.Label(f_ctrl, text="Độ dài Modulo N (bit):", font=FONT_BODY_BOLD, bg=CLR_CARD_BG).pack(side="left", padx=(0, 6))

        self.cbo_bit = ttk.Combobox(f_ctrl, values=["512", "1024", "2048"], width=8, font=FONT_CODE)
        self.cbo_bit.set("1024")
        self.cbo_bit.pack(side="left", padx=(0, 12))
        self.cbo_bit.bind("<Return>", lambda e: self.bat_dau_sinh_khoa())

        self.btn_sinh = ModernButton(f_ctrl, "🚀 Sinh cặp khoá RSA", command=self.bat_dau_sinh_khoa)
        self.btn_sinh.pack(side="left", padx=4)

        self.progress = ttk.Progressbar(f_ctrl, mode="indeterminate", length=180)
        self.progress.pack(side="left", padx=(14, 8))

        self.lbl_time = tk.Label(f_ctrl, text="", font=FONT_BODY_BOLD, fg=CLR_PRIMARY, bg=CLR_CARD_BG)
        self.lbl_time.pack(side="left", padx=4)

        c_body = ModernCard(self, tieu_de="Chi tiết các tham số của cặp khoá RSA")
        c_body.pack(fill="both", expand=True)

        self.entries = {}
        fields = [
            ("p", "Số nguyên tố bí mật p (~k/2 bit):"),
            ("q", "Số nguyên tố bí mật q (~k/2 bit):"),
            ("n", "Modulo công khai N = p * q (k bit):"),
            ("e", "Số mũ công khai e (thường chọn 65537):"),
            ("d", "Số mũ bí mật d = e⁻¹ mod phi(n):"),
        ]

        f_params = tk.Frame(c_body, bg=CLR_CARD_BG)
        f_params.pack(fill="both", expand=True, padx=12, pady=4)

        for key, title in fields:
            f_r = tk.Frame(f_params, bg=CLR_CARD_BG)
            f_r.pack(fill="x", pady=3)

            tk.Label(f_r, text=title, font=FONT_BODY_BOLD, width=30, anchor="w", bg=CLR_CARD_BG).pack(side="left")

            ent = ttk.Entry(f_r, font=FONT_CODE)
            ent.pack(side="left", fill="x", expand=True, padx=(4, 6))
            ent.configure(state="readonly")
            self.entries[key] = ent

            ModernButton(f_r, "🔍 Xem đầy đủ", command=lambda k=key, n=title: self.xem_day_du(k, n),
                         bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN, padx=6, pady=2).pack(side="left", padx=2)
            ModernButton(f_r, "📋 Sao chép", command=lambda k=key: self.sao_chep_thanh_phan(k),
                         bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN, padx=6, pady=2).pack(side="left", padx=2)

        f_bot = tk.Frame(c_body, bg=CLR_CARD_BG)
        f_bot.pack(fill="x", padx=12, pady=(4, 8))

        self.badge_kiem_tra = StatusBadge(f_bot, "Trạng thái: Chưa sinh khoá lớn.", "info")
        self.badge_kiem_tra.pack(side="left", fill="x", expand=True)

        ModernButton(f_bot, "📋 Sao chép toàn bộ khoá", command=self.sao_chep_tat_ca,
                     bg_color="#334155", hover_color="#1E293B", padx=8, pady=3).pack(side="right", padx=(8, 0))

    def bat_dau_sinh_khoa(self):
        if self.dang_sinh:
            return
        try:
            s_bit = int(self.cbo_bit.get().strip())
            if s_bit < 64:
                messagebox.showerror("Độ dài nhỏ", "Độ dài khoá phải ≥ 64 bit!")
                return
            if s_bit > 4096:
                messagebox.showwarning("Cảnh báo", "Độ dài > 4096 bit sẽ rất lâu!")
        except ValueError:
            messagebox.showerror("Sai kiểu", "Độ dài bit phải là số nguyên dương!")
            return

        self.dang_sinh = True
        self.btn_sinh.config_state("disabled")
        self.progress.start(10)
        self.lbl_time.config(text="Đang sinh p, q...")
        self.set_status(f"Đang sinh cặp khoá {s_bit} bit...")

        thread = threading.Thread(target=self._worker_sinh, args=(s_bit,), daemon=True)
        thread.start()

    def _worker_sinh(self, s_bit):
        try:
            t0 = time.perf_counter()
            khoa = sinh_khoa(s_bit)
            thoi_gian = time.perf_counter() - t0
            self.msg_queue.put(("DONE", khoa, thoi_gian, s_bit))
        except Exception as ex:
            self.msg_queue.put(("ERROR", str(ex)))

    def _kiem_tra_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                if msg[0] == "DONE":
                    _, khoa, t, s_bit = msg
                    self.progress.stop()
                    self.btn_sinh.config_state("normal")
                    self.dang_sinh = False

                    self.trang_thai.khoa_lon = khoa
                    self.trang_thai.thoi_gian_sinh_lon = t
                    self.trang_thai.thong_bao()

                    for k in ("p", "q", "n", "e", "d"):
                        ent = self.entries[k]
                        ent.configure(state="normal")
                        ent.delete(0, "end")
                        if k == "e":
                            ent.insert(0, str(khoa[k]))
                        else:
                            ent.insert(0, rut_gon(khoa[k]))
                        ent.configure(state="readonly")

                    self.lbl_time.config(text=f"Thời gian: {t:.3f}s ({s_bit} bit)")

                    phi = (khoa["p"] - 1) * (khoa["q"] - 1)
                    if (khoa["e"] * khoa["d"]) % phi == 1:
                        self.badge_kiem_tra.set_status(
                            f"✓ Đã xác minh: e * d mod phi(n) = 1  |  KU={{e, n}}, KR={{d, p, q}}", "success"
                        )
                    else:
                        self.badge_kiem_tra.set_status("✗ CẢNH BÁO: e * d mod phi(n) ≠ 1", "danger")

                    self.set_status(f"Sinh khoá {s_bit} bit hoàn tất trong {t:.3f}s.")

                elif msg[0] == "ERROR":
                    self.progress.stop()
                    self.btn_sinh.config_state("normal")
                    self.dang_sinh = False
                    messagebox.showerror("Lỗi sinh khoá", msg[1])
        except queue.Empty:
            pass

        self.after(50, self._kiem_tra_queue)

    def xem_day_du(self, k, title):
        if self.trang_thai.khoa_lon is None:
            messagebox.showinfo("Chưa có khoá", "Vui lòng sinh khoá trước!")
            return
        val = self.trang_thai.khoa_lon[k]
        so_bit = val.bit_length() if isinstance(val, int) else None
        HopThoaiXemChiTiet(self, title, val, so_bit)

    def sao_chep_thanh_phan(self, k):
        if self.trang_thai.khoa_lon is None:
            return
        self.clipboard_clear()
        self.clipboard_append(str(self.trang_thai.khoa_lon[k]))
        self.set_status(f"Đã sao chép tham số '{k}'.")

    def sao_chep_tat_ca(self):
        if self.trang_thai.khoa_lon is None:
            messagebox.showinfo("Chưa có khoá", "Chưa có cặp khoá lớn để sao chép!")
            return
        k = self.trang_thai.khoa_lon
        noi_dung = (
            f"=== CẶP KHOÁ RSA ({k['n'].bit_length()} BIT) ===\n"
            f"Khoá công khai KU:\n  e = {k['e']}\n  n = {k['n']}\n\n"
            f"Khoá bí mật KR:\n  d = {k['d']}\n  p = {k['p']}\n  q = {k['q']}\n"
        )
        self.clipboard_clear()
        self.clipboard_append(noi_dung)
        messagebox.showinfo("Đã sao chép", "Đã sao chép toàn bộ cặp khoá vào Clipboard!")


# ==============================================================================
# TAB 3: MÃ HOÁ VĂN BẢN (KHÓA LƯU CÙNG BẢN MÃ, BỐ CỤC KHÔNG BỊ CHE, SINH NỀN)
# ==============================================================================
class TabMaHoaVanBan(tk.Frame):
    def __init__(self, parent, trang_thai, status_cb):
        super().__init__(parent, bg=CLR_APP_BG, padx=14, pady=8)
        self.trang_thai = trang_thai
        self.set_status = status_cb

        self.ban_ma_hien_tai = None
        self.do_dai_goc = 0
        self.van_ban_goc = ""
        self.khoa_da_ma_hoa = None  # Lưu khoá lúc mã hoá

        self.dang_sinh_nen = False
        self.msg_queue = queue.Queue()

        self._tao_giao_dien()
        self._kiem_tra_queue()

    def _tao_giao_dien(self):
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.columnconfigure(0, weight=1)

        # 1. Plaintext
        c1 = ModernCard(self, tieu_de="1. Văn bản nguồn (Plaintext) - Tiếng Việt UTF-8")
        c1.grid(row=0, column=0, sticky="nsew", pady=(0, 6))

        f_txt1 = tk.Frame(c1, bg=CLR_CARD_BG)
        f_txt1.pack(fill="both", expand=True, padx=12, pady=2)

        self.txt_ro = tk.Text(f_txt1, height=3, font=FONT_BODY, wrap="word",
                              bd=1, relief="solid", bg="#FFFFFF", padx=6, pady=4)
        self.txt_ro.pack(side="left", fill="both", expand=True)
        sb1 = ttk.Scrollbar(f_txt1, orient="vertical", command=self.txt_ro.yview)
        sb1.pack(side="right", fill="y")
        self.txt_ro.configure(yscrollcommand=sb1.set)
        self.txt_ro.insert("1.0", VAN_BAN_MAU)

        f_act1 = tk.Frame(c1, bg=CLR_CARD_BG)
        f_act1.pack(fill="x", padx=12, pady=(2, 6))
        ModernButton(f_act1, "Dùng câu mẫu", command=self._dat_cau_mau,
                     bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN, padx=8, pady=2).pack(side="left", padx=2)
        ModernButton(f_act1, "Dùng văn bản dài (nhiều khối ~600 ký tự)", command=self._dat_cau_dai,
                     bg_color="#E0E7FF", hover_color="#C7D2FE", fg_color="#3730A3", padx=8, pady=2).pack(side="left", padx=2)
        ModernButton(f_act1, "Xoá", command=lambda: self.txt_ro.delete("1.0", "end"),
                     bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN, padx=8, pady=2).pack(side="left", padx=2)

        # 2. Ciphertext
        c2 = ModernCard(self, tieu_de="2. Bản mã RSA & Phân khối (Ciphertext)")
        c2.grid(row=1, column=0, sticky="nsew", pady=(0, 6))

        f_top2 = tk.Frame(c2, bg=CLR_CARD_BG)
        f_top2.pack(fill="x", padx=12, pady=2)

        self.btn_mh = ModernButton(f_top2, "🔒 Mã hoá văn bản", command=self.thuc_hien_ma_hoa, padx=10, pady=3)
        self.btn_mh.pack(side="left", padx=(0, 8))

        self.progress_mh = ttk.Progressbar(f_top2, mode="indeterminate", length=140)

        ModernButton(f_top2, "📋 Sao chép bản mã", command=self._sao_chep_ma,
                     bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN, padx=8, pady=2).pack(side="right", padx=2)

        # Dòng thông tin & DÒNG RIÊNG CHO THỜI GIAN MÃ HOÁ (không bị che nút)
        f_info2 = tk.Frame(c2, bg=CLR_CARD_BG)
        f_info2.pack(fill="x", padx=12, pady=(1, 2))

        self.lbl_info_khoi = tk.Label(f_info2, text="Kích thước: 0 byte | Khối k: 0 byte | Số khối: 0",
                                      font=FONT_BODY_BOLD, fg=CLR_TEXT_MAIN, bg=CLR_CARD_BG)
        self.lbl_info_khoi.pack(side="left")

        self.lbl_time_mh = tk.Label(f_info2, text="", font=FONT_BODY_BOLD, fg=CLR_ACCENT, bg=CLR_CARD_BG)
        self.lbl_time_mh.pack(side="right")

        f_txt2 = tk.Frame(c2, bg=CLR_CARD_BG)
        f_txt2.pack(fill="both", expand=True, padx=12, pady=(2, 6))

        self.txt_ma = tk.Text(f_txt2, height=3, font=FONT_CODE, wrap="char",
                              bd=1, relief="solid", bg="#F8FAFC", padx=6, pady=4)
        self.txt_ma.pack(side="left", fill="both", expand=True)
        sb2 = ttk.Scrollbar(f_txt2, orient="vertical", command=self.txt_ma.yview)
        sb2.pack(side="right", fill="y")
        self.txt_ma.configure(yscrollcommand=sb2.set)

        # 3. Decrypted Text
        c3 = ModernCard(self, tieu_de="3. Kết quả giải mã & Đối chiếu tính toàn vẹn")
        c3.grid(row=2, column=0, sticky="nsew")

        f_top3 = tk.Frame(c3, bg=CLR_CARD_BG)
        f_top3.pack(fill="x", padx=12, pady=2)

        self.btn_gm = ModernButton(f_top3, "🔓 Giải mã bản mã", command=self.thuc_hien_giai_ma,
                                   bg_color="#0D9488", hover_color="#0F766E", padx=10, pady=3)
        self.btn_gm.pack(side="left", padx=(0, 8))

        self.lbl_time_gm = tk.Label(f_top3, text="", font=FONT_BODY_BOLD, fg=CLR_ACCENT, bg=CLR_CARD_BG)
        self.lbl_time_gm.pack(side="left", padx=4)

        self.badge_ket_luan = StatusBadge(f_top3, "", "info")
        self.badge_ket_luan.pack(side="right")

        f_txt3 = tk.Frame(c3, bg=CLR_CARD_BG)
        f_txt3.pack(fill="both", expand=True, padx=12, pady=(2, 6))

        self.txt_giai = tk.Text(f_txt3, height=3, font=FONT_BODY, wrap="word",
                                bd=1, relief="solid", bg="#FFFFFF", padx=6, pady=4)
        self.txt_giai.pack(side="left", fill="both", expand=True)
        sb3 = ttk.Scrollbar(f_txt3, orient="vertical", command=self.txt_giai.yview)
        sb3.pack(side="right", fill="y")
        self.txt_giai.configure(yscrollcommand=sb3.set)

    def _dat_cau_mau(self):
        self.txt_ro.delete("1.0", "end")
        self.txt_ro.insert("1.0", VAN_BAN_MAU)

    def _dat_cau_dai(self):
        self.txt_ro.delete("1.0", "end")
        self.txt_ro.insert("1.0", VAN_BAN_DAI)

    def _sao_chep_ma(self):
        raw = self.txt_ma.get("1.0", "end-1c")
        if raw:
            self.clipboard_clear()
            self.clipboard_append(raw)
            self.set_status("Đã sao chép các khối bản mã.")

    def thuc_hien_ma_hoa(self):
        vb = self.txt_ro.get("1.0", "end-1c")
        if not vb:
            messagebox.showwarning("Trống", "Vui lòng nhập văn bản!")
            return

        # Nếu chưa có khoá lớn: sinh khoá trong luồng nền
        if self.trang_thai.khoa_lon is None:
            if self.dang_sinh_nen:
                return
            self.dang_sinh_nen = True
            self.progress_mh.pack(side="left", padx=6)
            self.progress_mh.start(10)
            self.lbl_info_khoi.config(text="Đang tự động sinh cặp khoá RSA 1024 bit trong nền...")
            self.set_status("Đang tự động sinh khoá 1024 bit trong luồng nền...")

            thread = threading.Thread(target=self._worker_sinh_khoa_tu_dong, args=("MA_HOA",), daemon=True)
            thread.start()
            return

        self._chay_ma_hoa_voi_khoa(self.trang_thai.khoa_lon, vb)

    def _worker_sinh_khoa_tu_dong(self, tiep_tuc_tac_vu):
        try:
            t0 = time.perf_counter()
            k = sinh_khoa(1024)
            tg = time.perf_counter() - t0
            self.msg_queue.put(("DONE_AUTO_KEY", k, tg, tiep_tuc_tac_vu))
        except Exception as ex:
            self.msg_queue.put(("ERR_AUTO_KEY", str(ex)))

    def _chay_ma_hoa_voi_khoa(self, khoa, vb):
        try:
            n, e = khoa["n"], khoa["e"]
            du_lieu = vb.encode("utf-8")
            k_khoi = _kich_thuoc_khoi(n)

            t0 = time.perf_counter()
            ban_ma, do_dai = ma_hoa_van_ban(vb, n, e)
            t_mh = time.perf_counter() - t0

            self.ban_ma_hien_tai = ban_ma
            self.do_dai_goc = do_dai
            self.van_ban_goc = vb
            self.khoa_da_ma_hoa = dict(khoa)  # Lưu khoá lúc mã hoá

            self.lbl_info_khoi.config(
                text=f"Dữ liệu: {len(du_lieu)} byte UTF-8 | Khối k: {k_khoi} byte | Số khối: {len(ban_ma)} khối"
            )
            self.lbl_time_mh.config(text=f"Thời gian mã hoá: {t_mh * 1000:.2f} ms")

            self.txt_ma.delete("1.0", "end")
            lines = [f"[Khối {i:02d}]: {format(c, 'x')}" for i, c in enumerate(ban_ma, 1)]
            self.txt_ma.insert("1.0", "\n".join(lines))

            self.txt_giai.delete("1.0", "end")
            self.badge_ket_luan.set_status("", "info")
            self.set_status(f"Mã hoá văn bản thành công: {len(ban_ma)} khối ({t_mh*1000:.2f} ms).")
        except Exception as ex:
            messagebox.showerror("Lỗi mã hoá", str(ex))

    def thuc_hien_giai_ma(self):
        try:
            if not self.ban_ma_hien_tai or not self.khoa_da_ma_hoa:
                messagebox.showwarning("Chưa mã hoá", "Vui lòng thực hiện mã hoá trước!")
                return

            # Dùng đúng khoá lúc mã hoá
            khoa_giai = self.khoa_da_ma_hoa
            n, d = khoa_giai["n"], khoa_giai["d"]

            # Kiểm tra nếu khoá lớn hiện tại đã bị thay đổi
            khoa_doi = False
            if self.trang_thai.khoa_lon is not None:
                if (self.trang_thai.khoa_lon.get("n") != khoa_giai.get("n") or
                        self.trang_thai.khoa_lon.get("d") != khoa_giai.get("d")):
                    khoa_doi = True

            t0 = time.perf_counter()
            giai = giai_ma_van_ban(self.ban_ma_hien_tai, self.do_dai_goc, n, d)
            t_gm = time.perf_counter() - t0

            self.txt_giai.delete("1.0", "end")
            self.txt_giai.insert("1.0", giai)
            self.lbl_time_gm.config(text=f"Thời gian giải mã: {t_gm * 1000:.2f} ms")

            if giai == self.van_ban_goc:
                if khoa_doi:
                    self.badge_ket_luan.set_status(
                        "⚠️ Cảnh báo: Khoá lớn hiện tại đã đổi! Đã giải mã bằng khoá lúc mã hoá để bảo toàn kết quả (ĐÚNG).", "warn"
                    )
                else:
                    self.badge_ket_luan.set_status("✓ ĐÚNG: Khớp 100% bản rõ ban đầu!", "success")
            else:
                self.badge_ket_luan.set_status("✗ SAI: Bản giải mã không khớp!", "danger")

            self.set_status(f"Giải mã hoàn tất trong {t_gm*1000:.2f} ms.")
        except Exception as ex:
            messagebox.showerror("Lỗi giải mã", str(ex))

    def _kiem_tra_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                if msg[0] == "DONE_AUTO_KEY":
                    _, k, tg, task = msg
                    self.dang_sinh_nen = False
                    self.progress_mh.stop()
                    self.progress_mh.pack_forget()

                    self.trang_thai.khoa_lon = k
                    self.trang_thai.thoi_gian_sinh_lon = tg
                    self.trang_thai.thong_bao()

                    if task == "MA_HOA":
                        vb = self.txt_ro.get("1.0", "end-1c")
                        self._chay_ma_hoa_voi_khoa(k, vb)

                elif msg[0] == "ERR_AUTO_KEY":
                    self.dang_sinh_nen = False
                    self.progress_mh.stop()
                    self.progress_mh.pack_forget()
                    messagebox.showerror("Lỗi sinh khoá nền", msg[1])
        except queue.Empty:
            pass

        self.after(50, self._kiem_tra_queue)


# ==============================================================================
# TAB 4: MÃ HOÁ TỆP & ẢNH (KHÓA LƯU CÙNG TỆP, KHÔNG HỘP THOẠI THÀNH CÔNG, SINH NỀN)
# ==============================================================================
class TabMaHoaTep(tk.Frame):
    def __init__(self, parent, trang_thai, status_cb):
        super().__init__(parent, bg=CLR_APP_BG, padx=14, pady=8)
        self.trang_thai = trang_thai
        self.set_status = status_cb

        self.duong_dan_tep = None
        self.duong_dan_rsa = None
        self.khoa_da_ma_hoa_tep = None  # Lưu khoá lúc mã hoá tệp

        self.img_goc_tk = None
        self.img_giai_tk = None
        self.dang_sinh_nen = False
        self.msg_queue = queue.Queue()

        self._tao_giao_dien()
        self._kiem_tra_queue()

    def _tao_giao_dien(self):
        c1 = ModernCard(self, tieu_de="1. Chọn tệp nguồn & Thao tác Mã hoá (.rsa) / Giải mã (_giaima)")
        c1.pack(fill="x", pady=(0, 6))

        f_f1 = tk.Frame(c1, bg=CLR_CARD_BG)
        f_f1.pack(fill="x", padx=12, pady=2)

        ModernButton(f_f1, "📁 Chọn tệp...", command=self.chon_tep,
                     bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN, padx=8, pady=2).pack(side="left", padx=(0, 6))

        self.lbl_path = tk.Label(f_f1, text="Chưa chọn tệp nào.", font=FONT_CODE, fg=CLR_TEXT_MUTED, bg=CLR_CARD_BG)
        self.lbl_path.pack(side="left", fill="x", expand=True)

        self.lbl_size = tk.Label(f_f1, text="", font=FONT_BODY_BOLD, fg=CLR_PRIMARY, bg=CLR_CARD_BG)
        self.lbl_size.pack(side="right")

        f_act = tk.Frame(c1, bg=CLR_CARD_BG)
        f_act.pack(fill="x", padx=12, pady=(4, 8))

        self.btn_mh = ModernButton(f_act, "🔒 Mã hoá tệp", command=self.bat_dau_ma_hoa, padx=8, pady=3)
        self.btn_mh.pack(side="left", padx=(0, 6))

        self.btn_gm = ModernButton(f_act, "🔓 Giải mã tệp", command=self.bat_dau_giai_ma,
                                   bg_color="#0D9488", hover_color="#0F766E", padx=8, pady=3)
        self.btn_gm.pack(side="left", padx=(0, 10))

        self.progress = ttk.Progressbar(f_act, orient="horizontal", mode="determinate", length=200)
        self.progress.pack(side="left", padx=(0, 8))

        self.lbl_tien_do = tk.Label(f_act, text="Sẵn sàng", font=FONT_BODY, bg=CLR_CARD_BG, fg=CLR_TEXT_MUTED)
        self.lbl_tien_do.pack(side="left")

        # 2. Toàn vẹn SHA-256 & Cảnh báo khoá
        c2 = ModernCard(self, tieu_de="2. Kiểm định toàn vẹn dữ liệu (Băm SHA-256 đối chiếu)")
        c2.pack(fill="x", pady=(0, 6))

        f_h = tk.Frame(c2, bg=CLR_CARD_BG)
        f_h.pack(fill="x", padx=12, pady=2)

        tk.Label(f_h, text="SHA-256 tệp gốc:      ", font=FONT_BODY_BOLD, bg=CLR_CARD_BG).grid(row=0, column=0, sticky="w")
        self.lbl_h_goc = tk.Label(f_h, text="-", font=FONT_CODE, bg=CLR_CARD_BG)
        self.lbl_h_goc.grid(row=0, column=1, sticky="w")

        tk.Label(f_h, text="SHA-256 tệp giải mã:", font=FONT_BODY_BOLD, bg=CLR_CARD_BG).grid(row=1, column=0, sticky="w", pady=(2, 0))
        self.lbl_h_giai = tk.Label(f_h, text="-", font=FONT_CODE, bg=CLR_CARD_BG)
        self.lbl_h_giai.grid(row=1, column=1, sticky="w", pady=(2, 0))

        self.badge_hash = StatusBadge(c2, "Trạng thái so sánh: Chưa thực hiện.", "info")
        self.badge_hash.pack(fill="x", padx=12, pady=(3, 6))

        # 3. So sánh trực quan hình ảnh
        c3 = ModernCard(self, tieu_de="3. So sánh trực quan hình ảnh (Xem trước PNG / GIF)")
        c3.pack(fill="both", expand=True)

        f_imgs = tk.Frame(c3, bg=CLR_CARD_BG)
        f_imgs.pack(fill="both", expand=True, padx=12, pady=(2, 6))
        f_imgs.columnconfigure(0, weight=1)
        f_imgs.columnconfigure(1, weight=1)
        f_imgs.rowconfigure(0, weight=1)

        b1 = tk.LabelFrame(f_imgs, text=" [ Ảnh gốc ban đầu ] ", bg=CLR_CARD_BG, font=FONT_BODY_BOLD, fg=CLR_TEXT_MAIN)
        b1.grid(row=0, column=0, sticky="nsew", padx=4)
        self.lbl_pv_goc = tk.Label(b1, text="(Chưa có ảnh gốc)", bg=CLR_CARD_BG, fg=CLR_TEXT_MUTED)
        self.lbl_pv_goc.pack(fill="both", expand=True)

        b2 = tk.LabelFrame(f_imgs, text=" [ Ảnh sau giải mã ] ", bg=CLR_CARD_BG, font=FONT_BODY_BOLD, fg=CLR_TEXT_MAIN)
        b2.grid(row=0, column=1, sticky="nsew", padx=4)
        self.lbl_pv_giai = tk.Label(b2, text="(Chưa có ảnh giải mã)", bg=CLR_CARD_BG, fg=CLR_TEXT_MUTED)
        self.lbl_pv_giai.pack(fill="both", expand=True)

    def chon_tep(self):
        path = filedialog.askopenfilename(
            title="Chọn tệp để mã hoá hoặc giải mã",
            filetypes=[
                ("Tất cả tệp", "*.*"),
                ("Tệp văn bản", "*.txt"),
                ("Tệp hình ảnh", "*.png;*.gif"),
                ("Tệp mã hoá RSA", "*.rsa"),
            ]
        )
        if not path:
            return
        self.duong_dan_tep = path
        size = os.path.getsize(path)
        name = os.path.basename(path)

        self.lbl_path.config(text=f"{name} ({path})")
        size_str = f"{size} B" if size < 1024 else f"{size/1024:.1f} KB"
        self.lbl_size.config(text=f"Dung lượng: {size_str}")

        self.lbl_h_goc.config(text="-")
        self.lbl_h_giai.config(text="-")
        self.badge_hash.set_status("Đã chọn tệp mới, sẵn sàng thao tác.", "info")
        self._hien_thi_anh_goc(path)

        if size > GIOI_HAN_TEP and not path.endswith(".rsa"):
            ok = messagebox.askyesno("Cảnh báo tệp lớn", f"Tệp {size//1024} KB (>200 KB) giải mã sẽ lâu. Bạn muốn tiếp tục?")
            if not ok:
                self.duong_dan_tep = None
                self.lbl_path.config(text="Đã huỷ chọn tệp.")
                self.lbl_size.config(text="")
                return
        self.set_status(f"Đã chọn tệp: {name}")

    def _hien_thi_anh_goc(self, path):
        if path.lower().endswith((".png", ".gif")):
            try:
                img = tk.PhotoImage(file=path)
                w, h = img.width(), img.height()
                if w > 240 or h > 180:
                    ti_le = max((w + 239) // 240, (h + 179) // 180)
                    img = img.subsample(ti_le, ti_le)
                self.img_goc_tk = img
                self.lbl_pv_goc.config(image=self.img_goc_tk, text="")
            except Exception:
                self.lbl_pv_goc.config(image="", text="(Không đọc được ảnh)")
        else:
            self.lbl_pv_goc.config(image="", text="(Không hỗ trợ xem trước)")

    def _hien_thi_anh_giai(self, path):
        if path.lower().endswith((".png", ".gif")):
            try:
                img = tk.PhotoImage(file=path)
                w, h = img.width(), img.height()
                if w > 240 or h > 180:
                    ti_le = max((w + 239) // 240, (h + 179) // 180)
                    img = img.subsample(ti_le, ti_le)
                self.img_giai_tk = img
                self.lbl_pv_giai.config(image=self.img_giai_tk, text="")
            except Exception:
                self.lbl_pv_giai.config(image="", text="(Không đọc được ảnh)")
        else:
            self.lbl_pv_giai.config(image="", text="(Không hỗ trợ xem trước)")

    def bat_dau_ma_hoa(self):
        if not self.duong_dan_tep or not os.path.isfile(self.duong_dan_tep):
            messagebox.showwarning("Chưa chọn tệp", "Vui lòng chọn tệp hợp lệ trước!")
            return

        if self.trang_thai.khoa_lon is None:
            if self.dang_sinh_nen:
                return
            self.dang_sinh_nen = True
            self.progress.configure(mode="indeterminate")
            self.progress.start(10)
            self.lbl_tien_do.config(text="Đang sinh khoá 1024 bit trong nền...")
            self.set_status("Đang sinh cặp khoá 1024 bit trong luồng nền...")

            thread = threading.Thread(target=self._worker_sinh_khoa_tep, daemon=True)
            thread.start()
            return

        self._chay_luong_ma_hoa(self.trang_thai.khoa_lon)

    def _worker_sinh_khoa_tep(self):
        try:
            t0 = time.perf_counter()
            k = sinh_khoa(1024)
            tg = time.perf_counter() - t0
            self.msg_queue.put(("DONE_AUTO_KEY_TEP", k, tg))
        except Exception as ex:
            self.msg_queue.put(("ERR_AUTO_KEY_TEP", str(ex)))

    def _chay_luong_ma_hoa(self, khoa):
        self.btn_mh.config_state("disabled")
        self.btn_gm.config_state("disabled")
        self.progress.configure(mode="determinate")
        self.progress["value"] = 0
        self.lbl_tien_do.config(text="Đang mã hoá...")

        thread = threading.Thread(target=self._worker_mh, args=(self.duong_dan_tep, khoa), daemon=True)
        thread.start()

    def _worker_mh(self, path, khoa):
        try:
            with open(path, "rb") as f:
                data = f.read()
            h_goc = hashlib.sha256(data).hexdigest()
            n, e = khoa["n"], khoa["e"]
            k = _kich_thuoc_khoi(n)
            tong = (len(data) + k - 1) // k
            ban_ma = []
            t0 = time.perf_counter()

            for i in range(0, len(data), k):
                khoi = data[i:i + k]
                m = int.from_bytes(khoi, "big")
                ban_ma.append(ma_hoa_so(m, n, e))
                pct = int((len(ban_ma) / max(tong, 1)) * 100)
                self.msg_queue.put(("P_MH", pct, len(ban_ma), tong))

            t_mh = time.perf_counter() - t0
            out_file = path + ".rsa"
            with open(out_file, "w", encoding="ascii") as f:
                f.write(f"{len(data)}\n")
                f.write("\n".join(format(c, "x") for c in ban_ma))

            self.msg_queue.put(("DONE_MH", out_file, h_goc, t_mh, len(ban_ma), dict(khoa)))
        except Exception as ex:
            self.msg_queue.put(("ERR_MH", str(ex)))

    def bat_dau_giai_ma(self):
        if not self.duong_dan_tep:
            messagebox.showwarning("Chưa chọn tệp", "Vui lòng chọn tệp để giải mã!")
            return
        tep_rsa = self.duong_dan_tep if self.duong_dan_tep.endswith(".rsa") else (self.duong_dan_rsa or self.duong_dan_tep + ".rsa")
        if not os.path.isfile(tep_rsa):
            messagebox.showwarning("Không thấy file", f"Không tìm thấy tệp:\n{tep_rsa}")
            return

        # Dùng khoá lúc mã hoá tệp nếu có, nếu không thì dùng khoá lớn hiện tại
        if self.khoa_da_ma_hoa_tep is not None:
            khoa_giai = self.khoa_da_ma_hoa_tep
            if (self.trang_thai.khoa_lon is not None and
                    (self.trang_thai.khoa_lon.get("n") != khoa_giai.get("n") or
                     self.trang_thai.khoa_lon.get("d") != khoa_giai.get("d"))):
                self.set_status("⚠️ Khoá lớn hiện tại đã đổi! Đang giải mã tệp bằng khoá lúc mã hoá.")
        elif self.trang_thai.khoa_lon is not None:
            khoa_giai = self.trang_thai.khoa_lon
        else:
            messagebox.showwarning("Chưa có khoá", "Chưa có cặp khoá để giải mã tệp!")
            return

        self.btn_mh.config_state("disabled")
        self.btn_gm.config_state("disabled")
        self.progress.configure(mode="determinate")
        self.progress["value"] = 0
        self.lbl_tien_do.config(text="Đang giải mã...")

        thread = threading.Thread(target=self._worker_gm, args=(tep_rsa, khoa_giai), daemon=True)
        thread.start()

    def _worker_gm(self, tep_rsa, khoa):
        try:
            with open(tep_rsa, "r", encoding="ascii") as f:
                lines = f.read().split("\n")
            do_dai = int(lines[0])
            ban_ma = [int(x, 16) for x in lines[1:] if x.strip()]

            n, d = khoa["n"], khoa["d"]
            k = _kich_thuoc_khoi(n)
            tong = len(ban_ma)
            res = bytearray()
            con_lai = do_dai
            t0 = time.perf_counter()

            for idx, c in enumerate(ban_ma, 1):
                m = giai_ma_so(c, n, d)
                dk = min(k, con_lai)
                res += m.to_bytes(dk, "big")
                con_lai -= dk
                pct = int((idx / max(tong, 1)) * 100)
                self.msg_queue.put(("P_GM", pct, idx, tong))

            t_gm = time.perf_counter() - t0
            giai_bytes = bytes(res)
            h_giai = hashlib.sha256(giai_bytes).hexdigest()

            if tep_rsa.endswith(".rsa"):
                tien_to = tep_rsa[:-4]
                goc, ext = os.path.splitext(tien_to)
                out_path = f"{goc}_giaima{ext}"
                orig_file = tien_to
            else:
                goc, ext = os.path.splitext(tep_rsa)
                out_path = f"{goc}_giaima{ext}"
                orig_file = None

            with open(out_path, "wb") as f:
                f.write(giai_bytes)

            h_orig = None
            if orig_file and os.path.isfile(orig_file):
                with open(orig_file, "rb") as fg:
                    h_orig = hashlib.sha256(fg.read()).hexdigest()

            self.msg_queue.put(("DONE_GM", out_path, h_giai, t_gm, h_orig))
        except Exception as ex:
            self.msg_queue.put(("ERR_GM", str(ex)))

    def _kiem_tra_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                loai = msg[0]

                if loai == "DONE_AUTO_KEY_TEP":
                    _, k, tg = msg
                    self.dang_sinh_nen = False
                    self.progress.stop()
                    self.trang_thai.khoa_lon = k
                    self.trang_thai.thoi_gian_sinh_lon = tg
                    self.trang_thai.thong_bao()
                    self._chay_luong_ma_hoa(k)

                elif loai == "ERR_AUTO_KEY_TEP":
                    self.dang_sinh_nen = False
                    self.progress.stop()
                    messagebox.showerror("Lỗi sinh khoá nền", msg[1])

                elif loai == "P_MH":
                    self.progress["value"] = msg[1]
                    self.lbl_tien_do.config(text=f"Mã hoá: {msg[2]}/{msg[3]} khối ({msg[1]}%)")

                elif loai == "DONE_MH":
                    _, out, h_goc, t, so_khoi, khoa_dung = msg
                    self.duong_dan_rsa = out
                    self.khoa_da_ma_hoa_tep = khoa_dung
                    self.lbl_h_goc.config(text=h_goc)
                    self.progress["value"] = 100
                    # THAY HỘP THOẠI THÀNH CÔNG BẰNG NHÃN & THANH TRẠNG THÁI
                    self.lbl_tien_do.config(text=f"✓ Đã mã hoá {so_khoi} khối ({t:.2f}s) -> {os.path.basename(out)}")
                    self.btn_mh.config_state("normal")
                    self.btn_gm.config_state("normal")
                    self.set_status(f"✓ Đã mã hoá tệp thành công: {os.path.basename(out)} ({t:.2f}s).")

                elif loai == "P_GM":
                    self.progress["value"] = msg[1]
                    self.lbl_tien_do.config(text=f"Giải mã: {msg[2]}/{msg[3]} khối ({msg[1]}%)")

                elif loai == "DONE_GM":
                    _, out, h_giai, t, h_orig = msg
                    self.lbl_h_giai.config(text=h_giai)
                    if h_orig:
                        self.lbl_h_goc.config(text=h_orig)
                    self.progress["value"] = 100
                    # THAY HỘP THOẠI THÀNH CÔNG BẰNG NHÃN & THANH TRẠNG THÁI
                    self.lbl_tien_do.config(text=f"✓ Đã giải mã xong ({t:.2f}s) -> {os.path.basename(out)}")
                    self.btn_mh.config_state("normal")
                    self.btn_gm.config_state("normal")

                    h_g = self.lbl_h_goc.cget("text")
                    if h_g != "-" and h_g == h_giai:
                        self.badge_hash.set_status("✓ ĐÚNG: Tệp giải mã trùng khớp 100% tệp gốc (SHA-256 trùng khớp)!", "success")
                    elif h_g != "-" and h_g != h_giai:
                        self.badge_hash.set_status("✗ SAI: Mã băm SHA-256 không trùng khớp!", "danger")
                    else:
                        self.badge_hash.set_status(f"✓ Đã giải mã thành công ra {os.path.basename(out)}.", "info")

                    self._hien_thi_anh_giai(out)
                    self.set_status(f"✓ Đã giải mã tệp thành công: {os.path.basename(out)} ({t:.2f}s).")

                elif loai in ("ERR_MH", "ERR_GM"):
                    self.progress["value"] = 0
                    self.btn_mh.config_state("normal")
                    self.btn_gm.config_state("normal")
                    messagebox.showerror("Lỗi", msg[1])
        except queue.Empty:
            pass

        self.after(50, self._kiem_tra_queue)


# ==============================================================================
# TAB 5: ĐO THỜI GIAN (THEO ĐỘ DÀI KHOÁ & THEO KÍCH THƯỚC DỮ LIỆU)
# ==============================================================================
class TabDoThoiGian(tk.Frame):
    def __init__(self, parent, trang_thai, status_cb):
        super().__init__(parent, bg=CLR_APP_BG, padx=14, pady=8)
        self.trang_thai = trang_thai
        self.set_status = status_cb

        # Kết quả đo phần 1 (theo độ dài khoá)
        self.ket_qua_do_khoa = []
        self.dang_do_khoa = False

        # Kết quả đo phần 2 (theo kích thước dữ liệu)
        self.ket_qua_do_kt = []
        self.dang_do_kt = False

        self.msg_queue = queue.Queue()

        self._tao_giao_dien()
        self._kiem_tra_queue()

    def _tao_giao_dien(self):
        # Tạo Notebook con chuyển đổi 2 chế độ đo
        self.sub_nb = ttk.Notebook(self)
        self.sub_nb.pack(fill="both", expand=True)

        self.sub_tab_khoa = tk.Frame(self.sub_nb, bg=CLR_APP_BG, padx=8, pady=6)
        self.sub_tab_kt = tk.Frame(self.sub_nb, bg=CLR_APP_BG, padx=8, pady=6)

        self.sub_nb.add(self.sub_tab_khoa, text="  📊 Đo theo Độ dài khoá (512 / 1024 / 2048 bit)  ")
        self.sub_nb.add(self.sub_tab_kt, text="  📈 Đo theo Kích thước dữ liệu (1 KB - 50 KB)  ")

        self._tao_giao_dien_do_khoa()
        self._tao_giao_dien_do_kich_thuoc()

    # ----------------- PHẦN 1: ĐO THEO ĐỘ DÀI KHOÁ -----------------
    def _tao_giao_dien_do_khoa(self):
        c1 = ModernCard(self.sub_tab_khoa, tieu_de="1. Thiết lập tham số đo lường theo độ dài khoá")
        c1.pack(fill="x", pady=(0, 6))

        f_ctrl = tk.Frame(c1, bg=CLR_CARD_BG)
        f_ctrl.pack(fill="x", padx=10, pady=(2, 6))

        tk.Label(f_ctrl, text="Số lần lặp mỗi độ dài khoá:", font=FONT_BODY_BOLD, bg=CLR_CARD_BG).pack(side="left", padx=(0, 6))
        self.spn_so_lan_khoa = ttk.Spinbox(f_ctrl, from_=1, to=10, width=4, font=FONT_CODE)
        self.spn_so_lan_khoa.set("3")
        self.spn_so_lan_khoa.pack(side="left", padx=(0, 10))
        self.spn_so_lan_khoa.bind("<Return>", lambda e: self.bat_dau_do_khoa())

        self.btn_do_khoa = ModernButton(f_ctrl, "⏱ Bắt đầu đo nghiệm", command=self.bat_dau_do_khoa, padx=8, pady=3)
        self.btn_do_khoa.pack(side="left", padx=3)

        self.btn_csv_khoa = ModernButton(f_ctrl, "📥 Xuất CSV", command=self.xuat_csv_khoa,
                                         bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN, padx=8, pady=3)
        self.btn_csv_khoa.pack(side="left", padx=3)
        self.btn_csv_khoa.config_state("disabled")

        self.progress_khoa = ttk.Progressbar(f_ctrl, orient="horizontal", mode="determinate", length=160)
        self.progress_khoa.pack(side="left", padx=(10, 6))

        self.lbl_tien_do_khoa = tk.Label(f_ctrl, text="Sẵn sàng đo (512 / 1024 / 2048 bit)",
                                         font=FONT_BODY, bg=CLR_CARD_BG, fg=CLR_TEXT_MUTED)
        self.lbl_tien_do_khoa.pack(side="left")

        # Bảng kết quả độ dài khoá
        c2 = ModernCard(self.sub_tab_khoa, tieu_de="2. Bảng kết quả đo theo độ dài khoá")
        c2.pack(fill="x", pady=(0, 6))

        f_tv = tk.Frame(c2, bg=CLR_CARD_BG)
        f_tv.pack(fill="x", padx=10, pady=(1, 6))

        cols = ("bit", "sinh_khoa", "ma_hoa", "giai_ma", "so_lan")
        self.tree_bm_khoa = ttk.Treeview(f_tv, columns=cols, show="headings", height=3)
        self.tree_bm_khoa.heading("bit", text="Độ dài khoá (bit)")
        self.tree_bm_khoa.heading("sinh_khoa", text="Sinh khoá TB (giây)")
        self.tree_bm_khoa.heading("ma_hoa", text="Mã hoá TB (ms)")
        self.tree_bm_khoa.heading("giai_ma", text="Giải mã TB (ms)")
        self.tree_bm_khoa.heading("so_lan", text="Số lần đo")

        self.tree_bm_khoa.column("bit", width=110, anchor="center")
        self.tree_bm_khoa.column("sinh_khoa", width=150, anchor="center")
        self.tree_bm_khoa.column("ma_hoa", width=150, anchor="center")
        self.tree_bm_khoa.column("giai_ma", width=150, anchor="center")
        self.tree_bm_khoa.column("so_lan", width=80, anchor="center")
        self.tree_bm_khoa.pack(fill="x")

        # Biểu đồ cột Canvas (mặc định Mã hoá & Giải mã ms)
        c3 = ModernCard(self.sub_tab_khoa, tieu_de="3. Biểu đồ cột hiệu năng (Canvas Flat)")
        c3.pack(fill="both", expand=True)

        f_opt = tk.Frame(c3, bg=CLR_CARD_BG)
        f_opt.pack(fill="x", padx=10, pady=(1, 3))
        tk.Label(f_opt, text="Xem chỉ số:", font=FONT_BODY_BOLD, bg=CLR_CARD_BG).pack(side="left", padx=(0, 8))

        # MẶC ĐỊNH LÀ "ma_giai" (tách đơn vị, tránh nhãn số đè lên nhau)
        self.var_opt_khoa = tk.StringVar(value="ma_giai")
        ttk.Radiobutton(f_opt, text="Mã hoá & Giải mã (ms) [Khuyên dùng]", variable=self.var_opt_khoa,
                        value="ma_giai", command=self.ve_bieu_do_khoa).pack(side="left", padx=4)
        ttk.Radiobutton(f_opt, text="Chỉ Sinh khoá (giây)", variable=self.var_opt_khoa,
                        value="sinh_khoa", command=self.ve_bieu_do_khoa).pack(side="left", padx=4)

        self.canvas_khoa = tk.Canvas(c3, bg="#FFFFFF", bd=0, highlightthickness=0)
        self.canvas_khoa.pack(fill="both", expand=True, padx=10, pady=(2, 6))
        self.canvas_khoa.bind("<Configure>", lambda e: self.ve_bieu_do_khoa())

    def bat_dau_do_khoa(self):
        if self.dang_do_khoa:
            return
        try:
            sl = int(self.spn_so_lan_khoa.get().strip())
            sl = max(1, sl)
        except ValueError:
            sl = 3

        self.dang_do_khoa = True
        self.btn_do_khoa.config_state("disabled")
        self.btn_csv_khoa.config_state("disabled")
        self.progress_khoa["value"] = 0

        for it in self.tree_bm_khoa.get_children():
            self.tree_bm_khoa.delete(it)
        self.canvas_khoa.delete("all")

        thread = threading.Thread(target=self._worker_do_khoa, args=(sl,), daemon=True)
        thread.start()

    def _worker_do_khoa(self, sl):
        try:
            mau = (VAN_BAN_MAU * 20).encode("utf-8")[:1000].decode("utf-8", errors="ignore")
            bits = [512, 1024, 2048]
            tong = len(bits) * sl
            cur = 0
            res = []

            for s_bit in bits:
                t_k = t_mh = t_gm = 0.0
                for lan in range(1, sl + 1):
                    cur += 1
                    pct = int((cur / tong) * 100)
                    self.msg_queue.put(("P_KHOA", pct, f"Đang đo {s_bit} bit (lần {lan}/{sl})..."))

                    t0 = time.perf_counter()
                    k = sinh_khoa(s_bit)
                    t_k += (time.perf_counter() - t0)

                    t0 = time.perf_counter()
                    bm, dd = ma_hoa_van_ban(mau, k["n"], k["e"])
                    t_mh += (time.perf_counter() - t0)

                    t0 = time.perf_counter()
                    giai_ma_van_ban(bm, dd, k["n"], k["d"])
                    t_gm += (time.perf_counter() - t0)

                row = (s_bit, t_k / sl, (t_mh / sl) * 1000, (t_gm / sl) * 1000, sl)
                res.append(row)
                self.msg_queue.put(("ROW_KHOA", row))

            self.msg_queue.put(("DONE_KHOA", res))
        except Exception as ex:
            self.msg_queue.put(("ERR_KHOA", str(ex)))

    def ve_bieu_do_khoa(self):
        self.canvas_khoa.delete("all")
        if not self.ket_qua_do_khoa:
            self.canvas_khoa.create_text(
                self.canvas_khoa.winfo_width() // 2 or 300,
                self.canvas_khoa.winfo_height() // 2 or 100,
                text="Chưa có số liệu. Bấm 'Bắt đầu đo nghiệm' ở trên.",
                font=FONT_BODY, fill=CLR_TEXT_MUTED
            )
            return

        w = self.canvas_khoa.winfo_width()
        h = self.canvas_khoa.winfo_height()
        if w < 100:
            w = max(self.canvas_khoa.winfo_reqwidth(), 700)
        if h < 100:
            h = max(self.canvas_khoa.winfo_reqheight(), 220)

        opt = self.var_opt_khoa.get()
        pad_l, pad_r, pad_t, pad_b = 55, 30, 25, 30
        pw = w - pad_l - pad_r
        ph = h - pad_t - pad_b

        # Trục toạ độ
        self.canvas_khoa.create_line(pad_l, pad_t + ph, pad_l + pw, pad_t + ph, fill="#CBD5E1", width=1.5)
        self.canvas_khoa.create_line(pad_l, pad_t, pad_l, pad_t + ph, fill="#CBD5E1", width=1.5)

        colors = {
            "sinh_khoa": ("#F59E0B", "Sinh khoá (giây)"),
            "ma_hoa": ("#10B981", "Mã hoá (ms)"),
            "giai_ma": ("#3B82F6", "Giải mã (ms)")
        }

        # Legend
        lx = pad_l + pw - 220
        ly = pad_t - 14
        if opt == "sinh_khoa":
            self.canvas_khoa.create_rectangle(lx, ly, lx + 10, ly + 10, fill=colors["sinh_khoa"][0], outline="")
            self.canvas_khoa.create_text(lx + 14, ly + 5, text="Sinh khoá (giây)", font=FONT_SMALL, anchor="w", fill=CLR_TEXT_MAIN)
        else:
            self.canvas_khoa.create_rectangle(lx, ly, lx + 10, ly + 10, fill=colors["ma_hoa"][0], outline="")
            self.canvas_khoa.create_text(lx + 14, ly + 5, text="Mã hoá (ms)", font=FONT_SMALL, anchor="w", fill=CLR_TEXT_MAIN)
            lx += 95
            self.canvas_khoa.create_rectangle(lx, ly, lx + 10, ly + 10, fill=colors["giai_ma"][0], outline="")
            self.canvas_khoa.create_text(lx + 14, ly + 5, text="Giải mã (ms)", font=FONT_SMALL, anchor="w", fill=CLR_TEXT_MAIN)

        max_v = 0.001
        for row in self.ket_qua_do_khoa:
            _, a, b, c, _ = row
            if opt == "sinh_khoa":
                max_v = max(max_v, a)
            else:
                max_v = max(max_v, b, c)

        y_max = max_v * 1.25
        for i in range(5):
            vg = y_max * (i / 4)
            yp = pad_t + ph - (vg / y_max) * ph
            self.canvas_khoa.create_line(pad_l, yp, pad_l + pw, yp, fill="#F1F5F9", width=1)
            unit_str = "s" if opt == "sinh_khoa" else "ms"
            self.canvas_khoa.create_text(pad_l - 6, yp, text=f"{vg:.1f} {unit_str}", font=FONT_SMALL, anchor="e", fill=CLR_TEXT_MUTED)

        num_groups = len(self.ket_qua_do_khoa)
        gw = pw / num_groups

        for g_idx, row in enumerate(self.ket_qua_do_khoa):
            s_bit, a, b, c, _ = row
            cx = pad_l + g_idx * gw + gw / 2
            self.canvas_khoa.create_text(cx, pad_t + ph + 14, text=f"{s_bit} bit", font=FONT_BODY_BOLD, fill=CLR_TEXT_MAIN)

            if opt == "sinh_khoa":
                items = [(a, colors["sinh_khoa"][0], f"{a:.3f} s")]
            else:
                items = [
                    (b, colors["ma_hoa"][0], f"{b:.1f} ms"),
                    (c, colors["giai_ma"][0], f"{c:.1f} ms")
                ]

            bw = min(36, (gw * 0.6) / len(items))
            sx = cx - (len(items) * bw) / 2

            for bi, (val, clr, lbl_t) in enumerate(items):
                bx = sx + bi * bw
                bh = (val / y_max) * ph
                by = pad_t + ph - bh
                self.canvas_khoa.create_rectangle(bx, by, bx + bw - 2, pad_t + ph, fill=clr, outline="")
                # Nhãn số hiển thị rõ ràng trên đầu cột, không bị đè nhau
                self.canvas_khoa.create_text(bx + bw / 2, by - 8, text=lbl_t, font=("Segoe UI", 8, "bold"), fill=CLR_TEXT_MAIN)

    def xuat_csv_khoa(self):
        if not self.ket_qua_do_khoa:
            messagebox.showwarning("Trống", "Chưa có số liệu để xuất CSV!")
            return
        path = filedialog.asksaveasfilename(
            title="Lưu kết quả đo độ dài khoá", initialfile="thoi_gian_rsa_khoa.csv",
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(["Khoá (bit)", "Sinh khoá (s)", "Mã hoá (ms)", "Giải mã (ms)", "Số lần đo"])
                for s_bit, a, b, c, sl in self.ket_qua_do_khoa:
                    w.writerow([s_bit, round(a, 3), round(b, 2), round(c, 2), sl])
            messagebox.showinfo("Thành công", f"Đã lưu CSV:\n{path}")
            self.set_status(f"Đã xuất file: {os.path.basename(path)}")
        except Exception as ex:
            messagebox.showerror("Lỗi", str(ex))

    # ----------------- PHẦN 2: ĐO THEO KÍCH THƯỚC DỮ LIỆU (1KB - 50KB) -----------------
    def _tao_giao_dien_do_kich_thuoc(self):
        c1 = ModernCard(self.sub_tab_kt, tieu_de="1. Thiết lập đo lường theo kích thước dữ liệu (1 KB, 5 KB, 10 KB, 25 KB, 50 KB)")
        c1.pack(fill="x", pady=(0, 6))

        f_ctrl = tk.Frame(c1, bg=CLR_CARD_BG)
        f_ctrl.pack(fill="x", padx=10, pady=(2, 6))

        tk.Label(f_ctrl, text="Cố định khoá (bit):", font=FONT_BODY_BOLD, bg=CLR_CARD_BG).pack(side="left", padx=(0, 4))
        self.cbo_bit_kt = ttk.Combobox(f_ctrl, values=["512", "1024", "2048"], width=6, font=FONT_CODE)
        self.cbo_bit_kt.set("1024")
        self.cbo_bit_kt.pack(side="left", padx=(0, 8))

        tk.Label(f_ctrl, text="Số lần lặp mỗi mức:", font=FONT_BODY_BOLD, bg=CLR_CARD_BG).pack(side="left", padx=(0, 4))
        self.spn_so_lan_kt = ttk.Spinbox(f_ctrl, from_=1, to=10, width=4, font=FONT_CODE)
        self.spn_so_lan_kt.set("3")
        self.spn_so_lan_kt.pack(side="left", padx=(0, 10))
        self.spn_so_lan_kt.bind("<Return>", lambda e: self.bat_dau_do_kich_thuoc())

        self.btn_do_kt = ModernButton(f_ctrl, "⏱ Bắt đầu đo kích thước", command=self.bat_dau_do_kich_thuoc, padx=8, pady=3)
        self.btn_do_kt.pack(side="left", padx=3)

        self.btn_csv_kt = ModernButton(f_ctrl, "📥 Xuất CSV", command=self.xuat_csv_kich_thuoc,
                                       bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN, padx=8, pady=3)
        self.btn_csv_kt.pack(side="left", padx=3)
        self.btn_csv_kt.config_state("disabled")

        self.progress_kt = ttk.Progressbar(f_ctrl, orient="horizontal", mode="determinate", length=140)
        self.progress_kt.pack(side="left", padx=(8, 6))

        self.lbl_tien_do_kt = tk.Label(f_ctrl, text="Sẵn sàng đo (1 KB - 50 KB)",
                                       font=FONT_BODY, bg=CLR_CARD_BG, fg=CLR_TEXT_MUTED)
        self.lbl_tien_do_kt.pack(side="left")

        # Bảng dữ liệu kích thước
        c2 = ModernCard(self.sub_tab_kt, tieu_de="2. Bảng kết quả theo kích thước dữ liệu")
        c2.pack(fill="x", pady=(0, 6))

        f_tv = tk.Frame(c2, bg=CLR_CARD_BG)
        f_tv.pack(fill="x", padx=10, pady=(1, 6))

        cols = ("size_str", "bytes", "blocks", "ma_hoa", "giai_ma", "so_lan")
        self.tree_bm_kt = ttk.Treeview(f_tv, columns=cols, show="headings", height=5)
        self.tree_bm_kt.heading("size_str", text="Kích thước")
        self.tree_bm_kt.heading("bytes", text="Số byte UTF-8")
        self.tree_bm_kt.heading("blocks", text="Số khối RSA")
        self.tree_bm_kt.heading("ma_hoa", text="Mã hoá TB (ms)")
        self.tree_bm_kt.heading("giai_ma", text="Giải mã TB (ms)")
        self.tree_bm_kt.heading("so_lan", text="Số lần đo")

        self.tree_bm_kt.column("size_str", width=100, anchor="center")
        self.tree_bm_kt.column("bytes", width=110, anchor="center")
        self.tree_bm_kt.column("blocks", width=100, anchor="center")
        self.tree_bm_kt.column("ma_hoa", width=140, anchor="center")
        self.tree_bm_kt.column("giai_ma", width=140, anchor="center")
        self.tree_bm_kt.column("so_lan", width=80, anchor="center")
        self.tree_bm_kt.pack(fill="x")

        # Biểu đồ đường Canvas (Line chart)
        c3 = ModernCard(self.sub_tab_kt, tieu_de="3. Biểu đồ đường (Line Chart) thời gian theo kích thước dữ liệu (ms)")
        c3.pack(fill="both", expand=True)

        self.canvas_kt = tk.Canvas(c3, bg="#FFFFFF", bd=0, highlightthickness=0)
        self.canvas_kt.pack(fill="both", expand=True, padx=10, pady=(4, 6))
        self.canvas_kt.bind("<Configure>", lambda e: self.ve_bieu_do_kich_thuoc())

    def bat_dau_do_kich_thuoc(self):
        if self.dang_do_kt:
            return
        try:
            sl = int(self.spn_so_lan_kt.get().strip())
            sl = max(1, sl)
        except ValueError:
            sl = 3

        try:
            s_bit = int(self.cbo_bit_kt.get().strip())
            s_bit = max(64, s_bit)
        except ValueError:
            s_bit = 1024

        self.dang_do_kt = True
        self.btn_do_kt.config_state("disabled")
        self.btn_csv_kt.config_state("disabled")
        self.progress_kt["value"] = 0

        for it in self.tree_bm_kt.get_children():
            self.tree_bm_kt.delete(it)
        self.canvas_kt.delete("all")

        thread = threading.Thread(target=self._worker_do_kich_thuoc, args=(s_bit, sl), daemon=True)
        thread.start()

    def _worker_do_kich_thuoc(self, s_bit, sl):
        try:
            self.msg_queue.put(("P_KT", 5, "Đang chuẩn bị cặp khoá RSA..."))
            # Dùng khoá cố định cho bài test
            khoa = sinh_khoa(s_bit)
            n, e, d = khoa["n"], khoa["e"], khoa["d"]
            k_khoi = _kich_thuoc_khoi(n)

            # Danh sách kích thước: 1 KB, 5 KB, 10 KB, 25 KB, 50 KB
            cac_muc = [
                ("1 KB", 1 * 1024),
                ("5 KB", 5 * 1024),
                ("10 KB", 10 * 1024),
                ("25 KB", 25 * 1024),
                ("50 KB", 50 * 1024),
            ]

            tong = len(cac_muc) * sl
            cur = 0
            res = []

            for size_name, b_len in cac_muc:
                # Tạo văn bản tiếng Việt đúng kích thước byte
                raw_bytes = (VAN_BAN_DAI * 150).encode("utf-8")[:b_len]
                vb = raw_bytes.decode("utf-8", errors="ignore")
                so_byte_that = len(vb.encode("utf-8"))
                so_khoi = (so_byte_that + k_khoi - 1) // k_khoi

                t_mh_tong = t_gm_tong = 0.0

                for lan in range(1, sl + 1):
                    cur += 1
                    pct = int((cur / tong) * 100)
                    self.msg_queue.put(("P_KT", pct, f"Đang đo {size_name} ({so_byte_that} B, lần {lan}/{sl})..."))

                    t0 = time.perf_counter()
                    bm, dd = ma_hoa_van_ban(vb, n, e)
                    t_mh_tong += (time.perf_counter() - t0)

                    t0 = time.perf_counter()
                    giai_ma_van_ban(bm, dd, n, d)
                    t_gm_tong += (time.perf_counter() - t0)

                tb_mh = (t_mh_tong / sl) * 1000
                tb_gm = (t_gm_tong / sl) * 1000

                row = (size_name, so_byte_that, so_khoi, tb_mh, tb_gm, sl)
                res.append(row)
                self.msg_queue.put(("ROW_KT", row))

            self.msg_queue.put(("DONE_KT", res))
        except Exception as ex:
            self.msg_queue.put(("ERR_KT", str(ex)))

    def ve_bieu_do_kich_thuoc(self):
        """Vẽ biểu đồ đường (Line chart) cho thời gian theo kích thước dữ liệu."""
        self.canvas_kt.delete("all")
        if not self.ket_qua_do_kt:
            self.canvas_kt.create_text(
                self.canvas_kt.winfo_width() // 2 or 300,
                self.canvas_kt.winfo_height() // 2 or 100,
                text="Chưa có số liệu. Bấm 'Bắt đầu đo kích thước' ở trên.",
                font=FONT_BODY, fill=CLR_TEXT_MUTED
            )
            return

        w = self.canvas_kt.winfo_width()
        h = self.canvas_kt.winfo_height()
        if w < 100:
            w = max(self.canvas_kt.winfo_reqwidth(), 700)
        if h < 100:
            h = max(self.canvas_kt.winfo_reqheight(), 220)

        pad_l, pad_r, pad_t, pad_b = 60, 35, 25, 30
        pw = w - pad_l - pad_r
        ph = h - pad_t - pad_b

        # Trục toạ độ
        self.canvas_kt.create_line(pad_l, pad_t + ph, pad_l + pw, pad_t + ph, fill="#CBD5E1", width=1.5)
        self.canvas_kt.create_line(pad_l, pad_t, pad_l, pad_t + ph, fill="#CBD5E1", width=1.5)

        # Legend
        lx = pad_l + pw - 220
        ly = pad_t - 14
        self.canvas_kt.create_line(lx, ly + 5, lx + 20, ly + 5, fill="#10B981", width=2.5)
        self.canvas_kt.create_oval(lx + 8, ly + 3, lx + 12, ly + 7, fill="#10B981", outline="")
        self.canvas_kt.create_text(lx + 24, ly + 5, text="Mã hoá (ms)", font=FONT_SMALL, anchor="w", fill=CLR_TEXT_MAIN)

        lx += 95
        self.canvas_kt.create_line(lx, ly + 5, lx + 20, ly + 5, fill="#3B82F6", width=2.5)
        self.canvas_kt.create_oval(lx + 8, ly + 3, lx + 12, ly + 7, fill="#3B82F6", outline="")
        self.canvas_kt.create_text(lx + 24, ly + 5, text="Giải mã (ms)", font=FONT_SMALL, anchor="w", fill=CLR_TEXT_MAIN)

        max_v = 0.001
        for row in self.ket_qua_do_kt:
            _, _, _, tb_mh, tb_gm, _ = row
            max_v = max(max_v, tb_mh, tb_gm)

        y_max = max_v * 1.25

        # Lưới ngang
        for i in range(5):
            vg = y_max * (i / 4)
            yp = pad_t + ph - (vg / y_max) * ph
            self.canvas_kt.create_line(pad_l, yp, pad_l + pw, yp, fill="#F1F5F9", width=1)
            self.canvas_kt.create_text(pad_l - 6, yp, text=f"{vg:.0f} ms", font=FONT_SMALL, anchor="e", fill=CLR_TEXT_MUTED)

        num_points = len(self.ket_qua_do_kt)
        step_x = pw / max(1, num_points - 1)

        pts_mh = []
        pts_gm = []

        for idx, row in enumerate(self.ket_qua_do_kt):
            size_name, _, _, tb_mh, tb_gm, _ = row
            cx = pad_l + idx * step_x

            # Nhãn trục X
            self.canvas_kt.create_text(cx, pad_t + ph + 14, text=size_name, font=FONT_BODY_BOLD, fill=CLR_TEXT_MAIN)

            cy_mh = pad_t + ph - (tb_mh / y_max) * ph
            cy_gm = pad_t + ph - (tb_gm / y_max) * ph

            pts_mh.append((cx, cy_mh, tb_mh))
            pts_gm.append((cx, cy_gm, tb_gm))

        # Vẽ đường nối Mã hoá
        for i in range(len(pts_mh) - 1):
            self.canvas_kt.create_line(pts_mh[i][0], pts_mh[i][1], pts_mh[i+1][0], pts_mh[i+1][1],
                                      fill="#10B981", width=2.5, smooth=True)

        # Vẽ đường nối Giải mã
        for i in range(len(pts_gm) - 1):
            self.canvas_kt.create_line(pts_gm[i][0], pts_gm[i][1], pts_gm[i+1][0], pts_gm[i+1][1],
                                      fill="#3B82F6", width=2.5, smooth=True)

        # Vẽ điểm tròn & nhãn giá trị
        for cx, cy, val in pts_mh:
            self.canvas_kt.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill="#10B981", outline="white", width=1.5)
            self.canvas_kt.create_text(cx, cy - 10, text=f"{val:.1f} ms", font=("Segoe UI", 8, "bold"), fill="#047857")

        for cx, cy, val in pts_gm:
            self.canvas_kt.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill="#3B82F6", outline="white", width=1.5)
            self.canvas_kt.create_text(cx, cy + 10, text=f"{val:.1f} ms", font=("Segoe UI", 8, "bold"), fill="#1D4ED8")

    def xuat_csv_kich_thuoc(self):
        if not self.ket_qua_do_kt:
            messagebox.showwarning("Trống", "Chưa có số liệu để xuất CSV!")
            return
        path = filedialog.asksaveasfilename(
            title="Lưu kết quả đo kích thước", initialfile="thoi_gian_rsa_kich_thuoc.csv",
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(["Kích thước", "Số byte UTF-8", "Số khối RSA", "Mã hoá TB (ms)", "Giải mã TB (ms)", "Số lần đo"])
                for size_name, b_len, so_khoi, tb_mh, tb_gm, sl in self.ket_qua_do_kt:
                    w.writerow([size_name, b_len, so_khoi, round(tb_mh, 2), round(tb_gm, 2), sl])
            messagebox.showinfo("Thành công", f"Đã lưu CSV:\n{path}")
            self.set_status(f"Đã xuất file: {os.path.basename(path)}")
        except Exception as ex:
            messagebox.showerror("Lỗi", str(ex))

    # ----------------- XỬ LÝ QUEUE TAB 5 -----------------
    def _kiem_tra_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                loai = msg[0]

                # Queue cho phần 1
                if loai == "P_KHOA":
                    self.progress_khoa["value"] = msg[1]
                    self.lbl_tien_do_khoa.config(text=msg[2])
                elif loai == "ROW_KHOA":
                    s_bit, a, b, c, sl = msg[1]
                    self.tree_bm_khoa.insert("", "end", values=(
                        f"{s_bit} bit", f"{a:.3f} s", f"{b:.2f} ms", f"{c:.2f} ms", f"{sl}"
                    ))
                elif loai == "DONE_KHOA":
                    self.ket_qua_do_khoa = msg[1]
                    self.dang_do_khoa = False
                    self.btn_do_khoa.config_state("normal")
                    self.btn_csv_khoa.config_state("normal")
                    self.progress_khoa["value"] = 100
                    self.lbl_tien_do_khoa.config(text="✓ Đã hoàn tất đo lường theo độ dài khoá!")
                    self.ve_bieu_do_khoa()
                    self.set_status("Đo thời gian theo độ dài khoá hoàn tất.")
                elif loai == "ERR_KHOA":
                    self.dang_do_khoa = False
                    self.btn_do_khoa.config_state("normal")
                    messagebox.showerror("Lỗi đo khoá", msg[1])

                # Queue cho phần 2
                elif loai == "P_KT":
                    self.progress_kt["value"] = msg[1]
                    self.lbl_tien_do_kt.config(text=msg[2])
                elif loai == "ROW_KT":
                    size_name, b_len, so_khoi, tb_mh, tb_gm, sl = msg[1]
                    self.tree_bm_kt.insert("", "end", values=(
                        size_name, f"{b_len:,} B", f"{so_khoi}", f"{tb_mh:.2f} ms", f"{tb_gm:.2f} ms", f"{sl}"
                    ))
                elif loai == "DONE_KT":
                    self.ket_qua_do_kt = msg[1]
                    self.dang_do_kt = False
                    self.btn_do_kt.config_state("normal")
                    self.btn_csv_kt.config_state("normal")
                    self.progress_kt["value"] = 100
                    self.lbl_tien_do_kt.config(text="✓ Đã hoàn tất đo lường theo kích thước dữ liệu!")
                    self.ve_bieu_do_kich_thuoc()
                    self.set_status("Đo thời gian theo kích thước hoàn tất.")
                elif loai == "ERR_KT":
                    self.dang_do_kt = False
                    self.btn_do_kt.config_state("normal")
                    messagebox.showerror("Lỗi đo kích thước", msg[1])

        except queue.Empty:
            pass

        self.after(50, self._kiem_tra_queue)


# ==============================================================================
# CỬA SỔ GIỚI THIỆU
# ==============================================================================
class CuaSoGioiThieu(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title(f"Giới thiệu Đề tài RSA - {NHOM}")
        self.geometry("640x510")
        self.resizable(False, False)
        self.configure(bg=CLR_APP_BG)
        self.transient(parent)
        self.grab_set()

        f_head = tk.Frame(self, bg=CLR_SIDEBAR_BG, padx=20, pady=16)
        f_head.pack(fill="x")
        tk.Label(f_head, text="HỆ MÃ HOÁ KHOÁ CÔNG KHAI RSA", font=FONT_BRAND, fg="white", bg=CLR_SIDEBAR_BG).pack(anchor="w")
        tk.Label(f_head, text=f"Học phần: An toàn và bảo mật thông tin mạng | {NHOM} (Thương mại điện tử)",
                 font=FONT_SMALL, fg=CLR_SIDEBAR_TEXT, bg=CLR_SIDEBAR_BG).pack(anchor="w", pady=(3, 0))

        f_body = tk.Frame(self, bg=CLR_APP_BG, padx=20, pady=14)
        f_body.pack(fill="both", expand=True)

        txt = (
            "📌 NGUYÊN LÝ HOẠT ĐỘNG:\n"
            "1. Sinh khoá: Chọn hai số nguyên tố ngẫu nhiên p và q (kiểm tra bằng Miller-Rabin).\n"
            "2. Tính modulo n = p * q và phi(n) = (p - 1) * (q - 1).\n"
            "3. Chọn e nguyên tố cùng nhau với phi(n) (mặc định e = 65537).\n"
            "4. Tìm số mũ bí mật d = e⁻¹ mod phi(n) nhờ thuật toán Euclid mở rộng.\n"
            "5. Khoá công khai KU = {e, n} dùng để Mã hoá: C = M^e mod n.\n"
            "6. Khoá riêng KR = {d, p, q} dùng để Giải mã: M = C^d mod n.\n"
            "   (Cả hai phép luỹ thừa lớn đều dùng thuật toán Bình phương và nhân).\n\n"
            f"👥 NHÓM THỰC HIỆN:\n"
            f"• {NHOM} - 5 sinh viên chuyên ngành Thương mại điện tử\n"
            "• Đề tài: Cài đặt và mô phỏng trực quan hệ mã RSA thuần Python\n\n"
            "⚠️ LƯU Ý MẬT MÃ QUAN TRỌNG:\n"
            "Chương trình cài đặt RSA ở dạng toán học cơ bản (Textbook RSA), chưa tích hợp chuẩn đệm "
            "OAEP (Optimal Asymmetric Encryption Padding) như trong thực tế, chỉ phục vụ mục đích học tập."
        )
        tk.Label(f_body, text=txt, font=FONT_BODY, justify="left", bg=CLR_APP_BG, fg=CLR_TEXT_MAIN).pack(fill="both", expand=True)

        ModernButton(self, "Đóng", command=self.destroy,
                     bg_color="#E2E8F0", hover_color="#CBD5E1", fg_color=CLR_TEXT_MAIN, padx=16).pack(pady=(0, 16))


# ==============================================================================
# CỬA SỔ CHÍNH ỨNG DỤNG (MODERN DASHBOARD SHELL)
# ==============================================================================
class UngDungRSA(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"Hệ mã hoá RSA - An toàn và bảo mật thông tin mạng ({NHOM} TMĐT)")

        # Đặt kích thước ban đầu theo kích thước màn hình: tối đa 90% chiều cao màn hình, tối thiểu 1050x640
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        init_w = max(1050, min(1200, int(screen_w * 0.9)))
        init_h = max(640, min(int(screen_h * 0.9), 780))
        self.geometry(f"{init_w}x{init_h}")
        self.minsize(1050, 640)
        self.configure(bg=CLR_APP_BG)

        self.trang_thai = TrangThai()
        self.is_fullscreen = False
        self.current_tab = 0

        self._cau_hinh_ttk_style()
        self._tao_bo_cuc_chinh()
        self._dang_ky_phim_tat()

        # Đăng ký lắng nghe thay đổi khoá lớn để cập nhật badge ở Topbar
        self.trang_thai.dang_ky(self._cap_nhat_badge_khoa)

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _cau_hinh_ttk_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Treeview", font=FONT_BODY, rowheight=24, background="#FFFFFF", fieldbackground="#FFFFFF", borderwidth=0)
        style.configure("Treeview.Heading", font=FONT_BODY_BOLD, background="#F1F5F9", foreground=CLR_TEXT_MAIN, borderwidth=0)
        style.map("Treeview.Heading", background=[("active", "#E2E8F0")])
        style.map("Treeview", background=[("selected", CLR_PRIMARY)], foreground=[("selected", "white")])

    def _tao_bo_cuc_chinh(self):
        # 1. SIDEBAR BÊN TRÁI
        self.sidebar = tk.Frame(self, bg=CLR_SIDEBAR_BG, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand Logo Header
        f_brand = tk.Frame(self.sidebar, bg=CLR_SIDEBAR_BG, padx=14, pady=14)
        f_brand.pack(fill="x")
        tk.Label(f_brand, text="🛡️  RSA CIPHER", font=FONT_BRAND, fg="white", bg=CLR_SIDEBAR_BG).pack(anchor="w")
        tk.Label(f_brand, text=f"ATBM Mạng • {NHOM}", font=FONT_SMALL, fg=CLR_SIDEBAR_TEXT, bg=CLR_SIDEBAR_BG).pack(anchor="w", pady=(1, 0))

        tk.Frame(self.sidebar, bg=CLR_SIDEBAR_HOVER, height=1).pack(fill="x", padx=10, pady=(0, 8))

        # Menu Items (Tên các tab rút gọn cho khỏi bị cắt chữ)
        self.menu_buttons = []
        menu_defs = [
            ("🔑 1. Khoá nhỏ", 0),
            ("🛡️ 2. Khoá lớn", 1),
            ("📝 3. Văn bản", 2),
            ("📁 4. Tệp & Ảnh", 3),
            ("📊 5. Thời gian", 4),
        ]

        for text, idx in menu_defs:
            btn = tk.Label(self.sidebar, text=text, font=FONT_BODY_BOLD,
                           fg=CLR_SIDEBAR_TEXT, bg=CLR_SIDEBAR_BG,
                           padx=14, pady=10, anchor="w", cursor="hand2")
            btn.pack(fill="x", padx=6, pady=2)
            btn.bind("<Button-1>", lambda e, i=idx: self.chuyen_tab(i))
            btn.bind("<Enter>", lambda e, b=btn, i=idx: self._menu_enter(b, i))
            btn.bind("<Leave>", lambda e, b=btn, i=idx: self._menu_leave(b, i))
            self.menu_buttons.append(btn)

        # Sidebar Footer
        f_sb_foot = tk.Frame(self.sidebar, bg=CLR_SIDEBAR_BG, padx=10, pady=10)
        f_sb_foot.pack(side="bottom", fill="x")

        ModernButton(f_sb_foot, "ℹ Giới thiệu", command=self.mo_gioi_thieu,
                     bg_color=CLR_SIDEBAR_HOVER, hover_color="#334155", fg_color="white", font=FONT_SMALL).pack(fill="x", pady=2)
        ModernButton(f_sb_foot, "⛶ Toàn màn hình (F11)", command=self.toggle_fullscreen,
                     bg_color=CLR_SIDEBAR_HOVER, hover_color="#334155", fg_color="white", font=FONT_SMALL).pack(fill="x", pady=2)

        # 2. KHU VỰC NỘI DUNG CHÍNH (MAIN AREA)
        self.main_area = tk.Frame(self, bg=CLR_APP_BG)
        self.main_area.pack(side="left", fill="both", expand=True)

        # Top Bar
        self.topbar = tk.Frame(self.main_area, bg=CLR_TOPBAR_BG, height=48, padx=16, pady=8,
                               bd=1, relief="solid", highlightthickness=1,
                               highlightbackground=CLR_CARD_BORDER, highlightcolor=CLR_CARD_BORDER)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        self.lbl_page_title = tk.Label(self.topbar, text="1. Khoá nhỏ & Minh hoạ từng bước",
                                       font=FONT_TITLE_PAGE, fg=CLR_TEXT_MAIN, bg=CLR_TOPBAR_BG)
        self.lbl_page_title.pack(side="left")

        self.badge_top_key = StatusBadge(self.topbar, "🔑 Khoá lớn: Chưa tạo", "info")
        self.badge_top_key.pack(side="right")

        # Container chứa các view Tab
        self.view_container = tk.Frame(self.main_area, bg=CLR_APP_BG)
        self.view_container.pack(fill="both", expand=True)

        # Khởi tạo 5 View
        self.tab1 = TabKhoaNho(self.view_container, self.trang_thai, self.set_status)
        self.tab2 = TabKhoaLon(self.view_container, self.trang_thai, self.set_status)
        self.tab3 = TabMaHoaVanBan(self.view_container, self.trang_thai, self.set_status)
        self.tab4 = TabMaHoaTep(self.view_container, self.trang_thai, self.set_status)
        self.tab5 = TabDoThoiGian(self.view_container, self.trang_thai, self.set_status)

        self.views = [self.tab1, self.tab2, self.tab3, self.tab4, self.tab5]
        self.tab_titles = [
            "1. Khoá nhỏ (Euclid mở rộng & Bình phương-và-nhân từng bước)",
            "2. Sinh khoá lớn RSA (512, 1024, 2048 bit ngẫu nhiên)",
            "3. Mã hoá & Giải mã văn bản Tiếng Việt UTF-8",
            "4. Mã hoá & Giải mã tệp nhị phân / Hình ảnh",
            "5. Đo thời gian thực tế & Biểu đồ hiệu năng",
        ]

        # Status Bar dưới đáy (Sửa chữ theo mục 9)
        self.statusbar = tk.Frame(self.main_area, bg="#F1F5F9", padx=14, pady=3,
                                  bd=1, relief="solid", highlightthickness=1,
                                  highlightbackground=CLR_CARD_BORDER)
        self.statusbar.pack(fill="x", side="bottom")

        self.lbl_status = tk.Label(self.statusbar, text="Sẵn sàng.", font=FONT_SMALL, bg="#F1F5F9", fg=CLR_TEXT_MAIN)
        self.lbl_status.pack(side="left")

        tk.Label(self.statusbar, text="Ctrl+1…5 / Alt+1…5: chuyển tab  |  F11: Toàn màn hình",
                 font=FONT_SMALL, bg="#F1F5F9", fg=CLR_TEXT_MUTED).pack(side="right")

        # Hiển thị tab đầu tiên
        self.chuyen_tab(0)

    def _menu_enter(self, btn, idx):
        if idx != self.current_tab:
            btn.config(bg=CLR_SIDEBAR_HOVER, fg="white")

    def _menu_leave(self, btn, idx):
        if idx != self.current_tab:
            btn.config(bg=CLR_SIDEBAR_BG, fg=CLR_SIDEBAR_TEXT)

    def chuyen_tab(self, idx):
        self.current_tab = idx
        for i, b in enumerate(self.menu_buttons):
            if i == idx:
                b.config(bg=CLR_SIDEBAR_ACTIVE, fg=CLR_SIDEBAR_TEXT_ACT)
            else:
                b.config(bg=CLR_SIDEBAR_BG, fg=CLR_SIDEBAR_TEXT)

        self.lbl_page_title.config(text=self.tab_titles[idx])

        for i, v in enumerate(self.views):
            if i == idx:
                v.pack(fill="both", expand=True)
            else:
                v.pack_forget()

        self.set_status(f"Đang xem: {self.tab_titles[idx]}")

    def _cap_nhat_badge_khoa(self, tt):
        if tt.khoa_lon:
            s_bit = tt.khoa_lon["n"].bit_length()
            self.badge_top_key.set_status(f"✓ Khoá {s_bit} bit (Sẵn sàng)", "success")
        else:
            self.badge_top_key.set_status("🔑 Khoá lớn: Chưa tạo", "info")

    def set_status(self, text):
        self.lbl_status.config(text=text)

    def mo_gioi_thieu(self):
        CuaSoGioiThieu(self)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        if not self.is_fullscreen:
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            init_w = max(1050, min(1200, int(screen_w * 0.9)))
            init_h = max(640, min(int(screen_h * 0.9), 780))
            self.geometry(f"{init_w}x{init_h}")

    def _dang_ky_phim_tat(self):
        self.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False) if self.is_fullscreen else None)

        for i in range(1, 6):
            self.bind(f"<Control-Key-{i}>", lambda e, idx=i-1: self.chuyen_tab(idx))
            self.bind(f"<Alt-Key-{i}>", lambda e, idx=i-1: self.chuyen_tab(idx))
            self.bind(f"{i}", lambda e, idx=i-1: self._phim_so(e, idx))

        self.bind("<Control-Tab>", lambda e: self.chuyen_tab((self.current_tab + 1) % 5))

    def _phim_so(self, event, idx):
        if isinstance(event.widget, (tk.Entry, ttk.Entry, tk.Text, ttk.Spinbox, ttk.Combobox)):
            return
        self.chuyen_tab(idx)


# ==============================================================================
# ĐIỂM VÀO CHÍNH
# ==============================================================================
def main():
    app = UngDungRSA()
    app.mainloop()


if __name__ == "__main__":
    main()
