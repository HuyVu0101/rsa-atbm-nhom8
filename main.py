"""
main.py -- Giao diện đồ hoạ (GUI Tkinter) Demo Hệ mã RSA.
Học phần: An toàn và bảo mật thông tin mạng
Nhóm thực hiện: Nhóm 8 - Ngành Thương mại điện tử (5 thành viên)

Yêu cầu môi trường:
- Python 3.8+ (khuyến nghị Python 3.10+)
- Chỉ sử dụng thư viện chuẩn của Python:
  tkinter, ttk, threading, queue, time, os, csv, hashlib, sys
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
# HẰNG SỐ VÀ CẤU HÌNH GIAO DIỆN
# ==============================================================================
VAN_BAN_MAU = "Thương mại điện tử an toàn nhờ mật mã khoá công khai RSA"
GIOI_HAN_TEP = 200 * 1024  # Cảnh báo nếu tệp lớn hơn 200 KB

# Bảng màu giao diện hiện đại (Modern Academic Palette)
MAU_CHINH = "#1B365D"       # Xanh Navy đậm chủ đạo
MAU_CHINH_HOVER = "#2A4D7E" # Hover nút chính
MAU_NEN_CHINH = "#F4F6F9"   # Nền ứng dụng xám sáng
MAU_CARD = "#FFFFFF"        # Nền các khung chứa
MAU_VIEN = "#CBD5E1"        # Viền khung
MAU_CHU = "#0F172A"         # Chữ chính đậm rõ
MAU_CHU_PHU = "#475569"     # Chữ phụ / chú thích
MAU_DUNG = "#16A34A"        # Xanh lá khi kiểm tra ĐÚNG
MAU_DUNG_NEN = "#DCFCE7"    # Nền xanh nhạt
MAU_SAI = "#DC2626"         # Đỏ khi kiểm tra SAI / lỗi
MAU_SAI_NEN = "#FEE2E2"     # Nền đỏ nhạt
MAU_DIEM_NHAN = "#0284C7"   # Xanh dương sáng (Accent)

FONT_TIEU_DE = ("Segoe UI", 16, "bold")
FONT_SUB_HEADER = ("Segoe UI", 11)
FONT_SECTION = ("Segoe UI", 12, "bold")
FONT_NOI_DUNG = ("Segoe UI", 11)
FONT_CHU_DAM = ("Segoe UI", 11, "bold")
FONT_CODE = ("Consolas", 11)
FONT_CODE_BOLD = ("Consolas", 11, "bold")


# ==============================================================================
# TIỆN ÍCH CHUNG
# ==============================================================================
def rut_gon(so, dau=20, cuoi=8):
    """
    Rút gọn số nguyên rất dài để hiển thị trên giao diện:
    1234...5678 (còn N chữ số).
    """
    s = str(so)
    if len(s) <= dau + cuoi + 8:
        return s
    return f"{s[:dau]}...{s[-cuoi:]}  ({len(s)} chữ số)"


def tinh_euclid_cac_buoc(phi, e):
    """
    Sinh danh sách các bước của thuật toán Euclid mở rộng giải: phi*x + e*y = 1
    Mỗi bước trả về tuple: (buoc_so, q, r, x, y, he_thuc)
    Đối chiếu nghiêm ngặt với kết quả của so_hoc.euclid_mo_rong.
    """
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

    # Đối chiếu với kết quả hàm euclid_mo_rong trong module so_hoc
    g, _, y_tv2 = euclid_mo_rong(phi, e)
    assert g == gcd and y_tv2 % phi == d, "Kết quả không khớp với so_hoc.euclid_mo_rong!"

    return cac_buoc, gcd, d


def tinh_luy_thua_cac_buoc(co_so, so_mu, modulo):
    """
    Sinh danh sách các bước của thuật toán Bình phương và nhân (Square-and-Multiply)
    khi tính: (co_so ** so_mu) % modulo.
    Duyệt bit từ trái sang phải (MSB -> LSB) để trực quan cho người học.
    Đối chiếu kết quả với so_hoc.luy_thua_modulo.
    """
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

    # Đối chiếu kết quả với hàm luy_thua_modulo
    assert kq == luy_thua_modulo(co_so, so_mu, modulo), "Không khớp so_hoc.luy_thua_modulo!"

    return cac_buoc, kq


# ==============================================================================
# ĐỐI TƯỢNG QUẢN LÝ TRẠNG THÁI TOÀN CỤC (STATE MANAGEMENT)
# ==============================================================================
class TrangThai:
    """
    Lưu giữ trạng thái dùng chung giữa các tab:
    - khoa_nho: cặp khoá ví dụ nhỏ (p, q, e, n, d)
    - khoa_lon: cặp khoá lớn (512 - 2048 bit)
    """
    def __init__(self):
        self.khoa_nho = None
        self.khoa_lon = None
        self.thoi_gian_sinh_lon = 0.0
        self._listeners = []

    def dang_ky_lang_nghe(self, callback):
        self._listeners.append(callback)

    def phat_tin_hieu_thay_doi(self):
        for cb in self._listeners:
            try:
                cb(self)
            except Exception:
                pass


# ==============================================================================
# HỘP THOẠI XEM ĐẦY ĐỦ SỐ NGUYÊN LỚN
# ==============================================================================
class HopThoaiXemChiTiet(tk.Toplevel):
    """Cửa sổ popup hiển thị toàn bộ giá trị số lớn với tính năng Sao chép."""
    def __init__(self, parent, tieu_de, ten_bien, gia_tri, so_bit=None):
        super().__init__(parent)
        self.title(f"Chi tiết giá trị: {ten_bien}")
        self.geometry("720x460")
        self.minsize(550, 350)
        self.configure(bg=MAU_NEN_CHINH)
        self.transient(parent)
        self.grab_set()

        # Header
        frame_head = tk.Frame(self, bg=MAU_CHINH, padx=16, pady=12)
        frame_head.pack(fill="x")
        tk.Label(frame_head, text=f"Tham số: {ten_bien}", font=FONT_SECTION,
                 fg="white", bg=MAU_CHINH).pack(anchor="w")
        info = f"Độ dài: {len(str(gia_tri))} chữ số thập phân"
        if so_bit:
            info += f" | {so_bit} bit nhị phân"
        tk.Label(frame_head, text=info, font=FONT_SUB_HEADER,
                 fg="#CBD5E1", bg=MAU_CHINH).pack(anchor="w")

        # Nội dung
        frame_body = tk.Frame(self, bg=MAU_NEN_CHINH, padx=16, pady=12)
        frame_body.pack(fill="both", expand=True)

        txt = tk.Text(frame_body, font=FONT_CODE, wrap="char", bd=1, relief="solid")
        txt.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(frame_body, orient="vertical", command=txt.yview)
        sb.pack(side="right", fill="y")
        txt.configure(yscrollcommand=sb.set)

        txt.insert("1.0", str(gia_tri))
        txt.configure(state="disabled")

        # Nút bấm dưới
        frame_btn = tk.Frame(self, bg=MAU_NEN_CHINH, padx=16, pady=10)
        frame_btn.pack(fill="x")

        self.lbl_thong_bao = tk.Label(frame_btn, text="", font=FONT_NOI_DUNG,
                                      fg=MAU_DUNG, bg=MAU_NEN_CHINH)
        self.lbl_thong_bao.pack(side="left")

        btn_dong = ttk.Button(frame_btn, text="Đóng", command=self.destroy)
        btn_dong.pack(side="right", padx=4)

        btn_copy = ttk.Button(frame_btn, text="📋 Sao chép vào bộ nhớ",
                              command=lambda: self.sao_chep(str(gia_tri)))
        btn_copy.pack(side="right", padx=4)

    def sao_chep(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.lbl_thong_bao.config(text="✓ Đã sao chép thành công!")
        self.after(2000, lambda: self.lbl_thong_bao.config(text=""))


# ==============================================================================
# TAB 1: KHOÁ NHỎ VÀ CÁC BƯỚC TÍNH TOÁN CHI TIẾT
# ==============================================================================
class TabKhoaNho(ttk.Frame):
    """
    Tab 1: Minh hoạ nguyên lý toán học RSA với khoá nhỏ (tính tay được).
    - Tạo khoá từng bước với thuật toán Euclid mở rộng.
    - Mã hoá / giải mã số hoặc chữ cái với thuật toán Bình phương và nhân.
    - Hỗ trợ chế độ trình chiếu từng bước (Bước tiếp theo / Hiện tất cả / Làm lại).
    """
    def __init__(self, parent, trang_thai, status_callback):
        super().__init__(parent, padding=12)
        self.trang_thai = trang_thai
        self.set_status = status_callback

        # Dữ liệu phục vụ trình chiếu từng bước Euclid
        self.euclid_steps = []
        self.euclid_idx = 0
        self.euclid_gcd = None
        self.euclid_d = None

        # Dữ liệu phục vụ trình chiếu từng bước Bình phương và nhân
        self.sq_steps = []
        self.sq_idx = 0
        self.sq_kq = None

        self._tao_giao_dien()

    def _tao_giao_dien(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        paned = ttk.PanedWindow(self, orient="vertical")
        paned.grid(row=0, column=0, sticky="nsew")

        # KHUNG 1: TẠO KHOÁ NHỎ & BẢNG EUCLID
        frame_tao_khoa = ttk.LabelFrame(paned, text=" 1. Tạo khoá ví dụ nhỏ (p, q, e) & Bảng Euclid mở rộng ", padding=10)
        paned.add(frame_tao_khoa, weight=3)

        # Thanh nhập p, q, e
        frame_input = ttk.Frame(frame_tao_khoa)
        frame_input.pack(fill="x", pady=(0, 6))

        ttk.Label(frame_input, text="Số p:", font=FONT_CHU_DAM).pack(side="left", padx=(0, 4))
        self.ent_p = ttk.Entry(frame_input, width=8, font=FONT_CODE)
        self.ent_p.insert(0, "11")
        self.ent_p.pack(side="left", padx=(0, 10))

        ttk.Label(frame_input, text="Số q:", font=FONT_CHU_DAM).pack(side="left", padx=(0, 4))
        self.ent_q = ttk.Entry(frame_input, width=8, font=FONT_CODE)
        self.ent_q.insert(0, "13")
        self.ent_q.pack(side="left", padx=(0, 10))

        ttk.Label(frame_input, text="Số e:", font=FONT_CHU_DAM).pack(side="left", padx=(0, 4))
        self.ent_e = ttk.Entry(frame_input, width=8, font=FONT_CODE)
        self.ent_e.insert(0, "7")
        self.ent_e.pack(side="left", padx=(0, 14))

        btn_tao = ttk.Button(frame_input, text="⚡ Bắt đầu tạo khoá", command=self.thuc_hien_tao_khoa)
        btn_tao.pack(side="left", padx=4)

        btn_mau1 = ttk.Button(frame_input, text="Mẫu (11, 13, 7)",
                              command=lambda: self._dat_mau(11, 13, 7))
        btn_mau1.pack(side="left", padx=4)

        btn_mau2 = ttk.Button(frame_input, text="Mẫu (17, 11, 7)",
                              command=lambda: self._dat_mau(17, 11, 7))
        btn_mau2.pack(side="left", padx=4)

        # Vùng tóm tắt các bước lý thuyết
        self.lbl_buoc_ly_thuyet = ttk.Label(
            frame_tao_khoa,
            text="Nhấn 'Bắt đầu tạo khoá' để kiểm tra số nguyên tố và giải phương trình đồng dư tìm d.",
            font=FONT_NOI_DUNG, foreground=MAU_CHU_PHU
        )
        self.lbl_buoc_ly_thuyet.pack(fill="x", pady=2)

        # Bảng Euclid mở rộng và các nút trình chiếu
        frame_euclid_control = ttk.Frame(frame_tao_khoa)
        frame_euclid_control.pack(fill="x", pady=4)

        ttk.Label(frame_euclid_control, text="Bảng thuật toán Euclid mở rộng tìm d:", font=FONT_CHU_DAM).pack(side="left")

        self.btn_euclid_next = ttk.Button(frame_euclid_control, text="⏭ Bước tiếp theo",
                                          command=self.euclid_buoc_tiep, state="disabled")
        self.btn_euclid_next.pack(side="left", padx=(16, 4))

        self.btn_euclid_all = ttk.Button(frame_euclid_control, text="⏩ Hiện tất cả",
                                         command=self.euclid_hien_tat_ca, state="disabled")
        self.btn_euclid_all.pack(side="left", padx=4)

        self.btn_euclid_reset = ttk.Button(frame_euclid_control, text="🔄 Làm lại",
                                           command=self.euclid_lam_lai, state="disabled")
        self.btn_euclid_reset.pack(side="left", padx=4)

        # Treeview Euclid
        cols_e = ("buoc", "q", "r", "x", "y", "he_thuc")
        self.tree_euclid = ttk.Treeview(frame_tao_khoa, columns=cols_e, show="headings", height=5)
        self.tree_euclid.heading("buoc", text="Bước")
        self.tree_euclid.heading("q", text="q (Thương)")
        self.tree_euclid.heading("r", text="r (Số dư)")
        self.tree_euclid.heading("x", text="x")
        self.tree_euclid.heading("y", text="y")
        self.tree_euclid.heading("he_thuc", text="Hệ thức đồng dư (r = phi*x + e*y)")

        self.tree_euclid.column("buoc", width=50, anchor="center")
        self.tree_euclid.column("q", width=90, anchor="center")
        self.tree_euclid.column("r", width=90, anchor="center")
        self.tree_euclid.column("x", width=90, anchor="center")
        self.tree_euclid.column("y", width=90, anchor="center")
        self.tree_euclid.column("he_thuc", width=340, anchor="w")

        self.tree_euclid.pack(fill="both", expand=True, pady=4)

        # Khung hiển thị Cặp khoá kết quả
        self.frame_ket_qua_khoa = ttk.Frame(frame_tao_khoa)
        self.frame_ket_qua_khoa.pack(fill="x", pady=4)

        self.lbl_khoa_ku = tk.Label(self.frame_ket_qua_khoa, text="Khoá công khai KU = { e, n } (Dùng Mã hoá)",
                                    font=FONT_CHU_DAM, bg="#E0F2FE", fg="#0369A1",
                                    padx=12, pady=6, relief="groove")
        self.lbl_khoa_ku.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.lbl_khoa_kr = tk.Label(self.frame_ket_qua_khoa, text="Khoá bí mật KR = { d, p, q } (Dùng Giải mã)",
                                    font=FONT_CHU_DAM, bg="#FEF3C7", fg="#B45309",
                                    padx=12, pady=6, relief="groove")
        self.lbl_khoa_kr.pack(side="left", fill="x", expand=True, padx=(6, 0))

        # KHUNG 2: MÃ HOÁ / GIẢI MÃ VỚI KHOÁ NHỎ (BÌNH PHƯƠNG VÀ NHÂN)
        frame_ma_hoa = ttk.LabelFrame(paned, text=" 2. Thử nghiệm Mã hoá & Giải mã với khoá nhỏ (Bình phương và nhân) ", padding=10)
        paned.add(frame_ma_hoa, weight=3)

        frame_input_mh = ttk.Frame(frame_ma_hoa)
        frame_input_mh.pack(fill="x", pady=(0, 6))

        ttk.Label(frame_input_mh, text="Nhập số M (0 ≤ M < n) hoặc chữ cái (A-Z):", font=FONT_CHU_DAM).pack(side="left", padx=(0, 8))
        self.ent_m = ttk.Entry(frame_input_mh, width=14, font=FONT_CODE)
        self.ent_m.insert(0, "9")
        self.ent_m.pack(side="left", padx=(0, 10))

        btn_tinh_mh = ttk.Button(frame_input_mh, text="🔒 Mã hoá & Giải mã", command=self.thuc_hien_ma_hoa_nho)
        btn_tinh_mh.pack(side="left", padx=4)

        btn_chumo = ttk.Button(frame_input_mh, text="Thử chữ 'HELLO'", command=lambda: self._dat_m_chu("HELLO"))
        btn_chumo.pack(side="left", padx=4)

        self.lbl_ket_qua_mh = tk.Label(frame_ma_hoa, text="Chưa có dữ liệu tính toán.",
                                       font=FONT_CHU_DAM, bg=MAU_NEN_CHINH, fg=MAU_CHU_PHU,
                                       anchor="w", padx=8, pady=4)
        self.lbl_ket_qua_mh.pack(fill="x", pady=2)

        # Điều khiển trình chiếu Bình phương và nhân
        frame_sq_control = ttk.Frame(frame_ma_hoa)
        frame_sq_control.pack(fill="x", pady=4)

        self.lbl_sq_title = ttk.Label(frame_sq_control, text="Bảng Bình phương và nhân từng bước:", font=FONT_CHU_DAM)
        self.lbl_sq_title.pack(side="left")

        self.btn_sq_next = ttk.Button(frame_sq_control, text="⏭ Bước tiếp theo",
                                      command=self.sq_buoc_tiep, state="disabled")
        self.btn_sq_next.pack(side="left", padx=(16, 4))

        self.btn_sq_all = ttk.Button(frame_sq_control, text="⏩ Hiện tất cả",
                                     command=self.sq_hien_tat_ca, state="disabled")
        self.btn_sq_all.pack(side="left", padx=4)

        self.btn_sq_reset = ttk.Button(frame_sq_control, text="🔄 Làm lại",
                                       command=self.sq_lam_lai, state="disabled")
        self.btn_sq_reset.pack(side="left", padx=4)

        # Treeview Bình phương và nhân
        cols_sq = ("buoc", "bit", "bp", "nhan", "kq")
        self.tree_sq = ttk.Treeview(frame_ma_hoa, columns=cols_sq, show="headings", height=5)
        self.tree_sq.heading("buoc", text="Bước i")
        self.tree_sq.heading("bit", text="Bit số mũ")
        self.tree_sq.heading("bp", text="Bình phương (x² mod n)")
        self.tree_sq.heading("nhan", text="Nhân cơ số (nếu bit=1)")
        self.tree_sq.heading("kq", text="Kết quả sau bước")

        self.tree_sq.column("buoc", width=60, anchor="center")
        self.tree_sq.column("bit", width=80, anchor="center")
        self.tree_sq.column("bp", width=240, anchor="w")
        self.tree_sq.column("nhan", width=240, anchor="w")
        self.tree_sq.column("kq", width=120, anchor="center")

        self.tree_sq.pack(fill="both", expand=True, pady=4)

    def _dat_mau(self, p, q, e):
        self.ent_p.delete(0, "end")
        self.ent_p.insert(0, str(p))
        self.ent_q.delete(0, "end")
        self.ent_q.insert(0, str(q))
        self.ent_e.delete(0, "end")
        self.ent_e.insert(0, str(e))
        self.thuc_hien_tao_khoa()

    def _dat_m_chu(self, s):
        self.ent_m.delete(0, "end")
        self.ent_m.insert(0, s)
        self.thuc_hien_ma_hoa_nho()

    def thuc_hien_tao_khoa(self):
        """Kiểm tra p, q, e và thiết lập bảng Euclid mở rộng."""
        try:
            p_str = self.ent_p.get().strip()
            q_str = self.ent_q.get().strip()
            e_str = self.ent_e.get().strip()

            if not p_str or not q_str or not e_str:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ 3 số p, q, e!")
                return

            p = int(p_str)
            q = int(q_str)
            e = int(e_str)

            if p <= 1 or q <= 1:
                messagebox.showerror("Lỗi giá trị", "p và q phải là các số nguyên lớn hơn 1!")
                return

            if p == q:
                messagebox.showerror("Lỗi p = q", "p và q phải là hai số nguyên tố KHÁC NHAU!")
                return

            # Kiểm tra số nguyên tố bằng Miller-Rabin từ sinh_khoa.py
            if not miller_rabin(p):
                messagebox.showerror("Số không nguyên tố", f"p = {p} không phải là số nguyên tố!")
                return
            if not miller_rabin(q):
                messagebox.showerror("Số không nguyên tố", f"q = {q} không phải là số nguyên tố!")
                return

            n = p * q
            phi = (p - 1) * (q - 1)

            if uoc_chung_lon_nhat(e, phi) != 1:
                messagebox.showerror(
                    "gcd(e, phi) ≠ 1",
                    f"e = {e} không nguyên tố cùng nhau với phi(n) = {phi} (gcd = {uoc_chung_lon_nhat(e, phi)})!\n"
                    "Vui lòng chọn e khác."
                )
                return

            # Sinh các bước Euclid mở rộng
            steps, gcd, d = tinh_euclid_cac_buoc(phi, e)
            khoa = khoa_tu_p_q(p, q, e)
            self.trang_thai.khoa_nho = khoa

            # Cập nhật thông báo các bước
            text_ly_thuyet = (
                f"✓ Bước 1: p = {p}, q = {q} (nguyên tố)\n"
                f"✓ Bước 2: Modulo n = p * q = {p} * {q} = {n}\n"
                f"✓ Bước 3: Phi(n) = (p-1)*(q-1) = {p-1} * {q-1} = {phi}\n"
                f"✓ Bước 4: Chọn e = {e} (gcd({e}, {phi}) = 1 hợp lệ)\n"
                f"✓ Bước 5: Tìm d = e⁻¹ mod phi(n) = {d}. Kiểm tra: e*d mod phi = {e*d % phi} (ĐÚNG)"
            )
            self.lbl_buoc_ly_thuyet.config(text=text_ly_thuyet, foreground=MAU_CHU)

            self.euclid_steps = steps
            self.euclid_idx = 0
            self.euclid_gcd = gcd
            self.euclid_d = d

            # Reset bảng Treeview
            for item in self.tree_euclid.get_children():
                self.tree_euclid.delete(item)

            self.btn_euclid_next.config(state="normal")
            self.btn_euclid_all.config(state="normal")
            self.btn_euclid_reset.config(state="normal")

            # Cập nhật khung kết quả
            self.lbl_khoa_ku.config(text=f"Khoá công khai KU = {{ e = {e}, n = {n} }} (Dùng Mã hoá)")
            self.lbl_khoa_kr.config(text=f"Khoá bí mật KR = {{ d = {d}, p = {p}, q = {q} }} (Dùng Giải mã)")

            self.set_status(f"Đã tạo khoá nhỏ: n={n}, e={e}, d={d}")

        except ValueError:
            messagebox.showerror("Sai định dạng", "p, q, e phải là các số nguyên hợp lệ!")
        except Exception as e:
            messagebox.showerror("Lỗi không mong muốn", f"Đã xảy ra lỗi: {e}")

    def euclid_buoc_tiep(self):
        if self.euclid_idx < len(self.euclid_steps):
            item = self.euclid_steps[self.euclid_idx]
            self.tree_euclid.insert("", "end", values=item)
            self.euclid_idx += 1
            if self.euclid_idx == len(self.euclid_steps):
                self.btn_euclid_next.config(state="disabled")
                self.set_status(f"Euclid hoàn tất: gcd = {self.euclid_gcd}, d = {self.euclid_d}")

    def euclid_hien_tat_ca(self):
        while self.euclid_idx < len(self.euclid_steps):
            self.euclid_buoc_tiep()

    def euclid_lam_lai(self):
        for item in self.tree_euclid.get_children():
            self.tree_euclid.delete(item)
        self.euclid_idx = 0
        self.btn_euclid_next.config(state="normal")
        self.set_status("Đã làm lại bảng Euclid.")

    def thuc_hien_ma_hoa_nho(self):
        """Mã hoá và giải mã với khoá nhỏ (số hoặc chữ)."""
        if self.trang_thai.khoa_nho is None:
            # Tự động tạo khoá chuẩn nếu người dùng chưa bấm tạo khoá
            self.thuc_hien_tao_khoa()

        if self.trang_thai.khoa_nho is None:
            return

        n = self.trang_thai.khoa_nho["n"]
        e = self.trang_thai.khoa_nho["e"]
        d = self.trang_thai.khoa_nho["d"]

        raw = self.ent_m.get().strip()
        if not raw:
            messagebox.showwarning("Chưa nhập dữ liệu", "Vui lòng nhập một số hoặc chữ cái A-Z!")
            return

        # Trường hợp 1: Nhập số nguyên
        if raw.isdigit():
            m = int(raw)
            if m < 0 or m >= n:
                messagebox.showerror("Lỗi giá trị M", f"Bản rõ số M phải thoả mãn 0 ≤ M < n (tức 0 ≤ M < {n})!")
                return

            c = ma_hoa_so(m, n, e)
            m_giai = giai_ma_so(c, n, d)
            dung = (m == m_giai)

            self.lbl_ket_qua_mh.config(
                text=f"Bản rõ M = {m}  ==>  Bản mã C = M^{e} mod {n} = {c}  ==>  Giải mã M' = C^{d} mod {n} = {m_giai}  "
                     f"({'✓ ĐÚNG' if dung else '✗ SAI'})",
                bg=MAU_DUNG_NEN if dung else MAU_SAI_NEN,
                fg=MAU_DUNG if dung else MAU_SAI
            )

            # Thiết lập bảng Bình phương và nhân cho phép mã hoá C = M^e mod n
            self.sq_steps, self.sq_kq = tinh_luy_thua_cac_buoc(m, e, n)
            self.lbl_sq_title.config(text=f"Bình phương và nhân tính C = {m}^{e} mod {n}:")
            self.sq_lam_lai()

        # Trường hợp 2: Nhập chuỗi chữ cái A-Z
        elif raw.isalpha() and raw.isascii():
            raw_upper = raw.upper()
            gia_tri = [ord(ch) - 64 for ch in raw_upper]

            if max(gia_tri) >= n:
                messagebox.showerror("Khoá quá nhỏ", f"Khoá n = {n} không đủ lớn để mã hoá chữ cái này (cần n > 26)!")
                return

            ban_ma = []
            ban_giai = []
            chi_tiet = []

            for ch, m_val in zip(raw_upper, gia_tri):
                c_val = ma_hoa_so(m_val, n, e)
                m2_val = giai_ma_so(c_val, n, d)
                ban_ma.append(c_val)
                ban_giai.append(chr(m2_val + 64))
                chi_tiet.append(f"{ch}(M={m_val})→C={c_val}→{chr(m2_val+64)}")

            chuoi_giai = "".join(ban_giai)
            dung = (raw_upper == chuoi_giai)

            self.lbl_ket_qua_mh.config(
                text=f"Từ gốc: '{raw_upper}'  ==>  Bản mã: {ban_ma}  ==>  Giải mã: '{chuoi_giai}'  "
                     f"({'✓ ĐÚNG' if dung else '✗ SAI'})",
                bg=MAU_DUNG_NEN if dung else MAU_SAI_NEN,
                fg=MAU_DUNG if dung else MAU_SAI
            )

            # Chọn chữ cái đầu tiên để minh hoạ bình phương và nhân
            ch_dau = raw_upper[0]
            m_dau = gia_tri[0]
            self.sq_steps, self.sq_kq = tinh_luy_thua_cac_buoc(m_dau, e, n)
            self.lbl_sq_title.config(text=f"Bình phương và nhân cho ký tự đầu '{ch_dau}' (M={m_dau}^{e} mod {n}):")
            self.sq_lam_lai()

        else:
            messagebox.showerror("Dữ liệu không hợp lệ", "Vui lòng nhập số nguyên không âm hoặc các chữ cái A-Z (không dấu)!")

    def sq_buoc_tiep(self):
        if self.sq_idx < len(self.sq_steps):
            item = self.sq_steps[self.sq_idx]
            self.tree_sq.insert("", "end", values=item)
            self.sq_idx += 1
            if self.sq_idx == len(self.sq_steps):
                self.btn_sq_next.config(state="disabled")
                self.set_status(f"Bình phương và nhân hoàn tất: Kết quả = {self.sq_kq}")

    def sq_hien_tat_ca(self):
        while self.sq_idx < len(self.sq_steps):
            self.sq_buoc_tiep()

    def sq_lam_lai(self):
        for item in self.tree_sq.get_children():
            self.tree_sq.delete(item)
        self.sq_idx = 0
        self.btn_sq_next.config(state="normal")
        self.btn_sq_all.config(state="normal")
        self.btn_sq_reset.config(state="normal")


# ==============================================================================
# TAB 2: KHOÁ LỚN (512, 1024, 2048 BIT)
# ==============================================================================
class TabKhoaLon(ttk.Frame):
    """
    Tab 2: Sinh cặp khoá RSA kích thước lớn trong luồng nền (background thread).
    - Lựa chọn 512, 1024, 2048 bit hoặc tự nhập.
    - Hiển thị p, q, n, d dạng rút gọn kèm số chữ số.
    - Cho phép xem đầy đủ và sao chép.
    - Kiểm tra đẳng thức e*d mod phi(n) = 1.
    """
    def __init__(self, parent, trang_thai, status_callback):
        super().__init__(parent, padding=16)
        self.trang_thai = trang_thai
        self.set_status = status_callback
        self.dang_sinh = False
        self.msg_queue = queue.Queue()

        self._tao_giao_dien()
        self._kiem_tra_queue()

    def _tao_giao_dien(self):
        # Bảng điều khiển chọn độ dài bit và nút sinh khoá
        frame_top = ttk.LabelFrame(self, text=" Thiết lập độ dài khoá RSA ", padding=12)
        frame_top.pack(fill="x", pady=(0, 12))

        ttk.Label(frame_top, text="Chọn độ dài Modulo N (bit):", font=FONT_CHU_DAM).pack(side="left", padx=(0, 8))

        self.cbo_bit = ttk.Combobox(frame_top, values=["512", "1024", "2048"], width=10, font=FONT_CODE)
        self.cbo_bit.set("1024")
        self.cbo_bit.pack(side="left", padx=(0, 16))

        self.btn_sinh = ttk.Button(frame_top, text="🚀 Sinh cặp khoá RSA", command=self.bat_dau_sinh_khoa)
        self.btn_sinh.pack(side="left", padx=4)

        self.progress = ttk.Progressbar(frame_top, mode="indeterminate", length=220)
        self.progress.pack(side="left", padx=(16, 8))

        self.lbl_time = ttk.Label(frame_top, text="", font=FONT_CHU_DAM, foreground=MAU_CHINH)
        self.lbl_time.pack(side="left", padx=8)

        # Bảng hiển thị các thành phần của khoá
        frame_params = ttk.LabelFrame(self, text=" Các thành phần của cặp khoá RSA ", padding=12)
        frame_params.pack(fill="both", expand=True)

        self.danh_sach_widget = {}
        cac_thanh_phan = [
            ("p", "Số nguyên tố bí mật p (~k/2 bit):"),
            ("q", "Số nguyên tố bí mật q (~k/2 bit):"),
            ("n", "Modulo công khai N = p * q (k bit):"),
            ("e", "Số mũ công khai e (thường chọn 65537):"),
            ("d", "Số mũ bí mật d = e⁻¹ mod phi(n):"),
        ]

        for idx, (key, label_text) in enumerate(cac_thanh_phan):
            f_row = ttk.Frame(frame_params)
            f_row.pack(fill="x", pady=6)

            lbl_title = ttk.Label(f_row, text=label_text, width=32, font=FONT_CHU_DAM, anchor="w")
            lbl_title.pack(side="left")

            ent_val = ttk.Entry(f_row, font=FONT_CODE)
            ent_val.pack(side="left", fill="x", expand=True, padx=(4, 8))
            ent_val.configure(state="readonly")

            btn_view = ttk.Button(f_row, text="🔍 Xem đầy đủ", width=12,
                                  command=lambda k=key, name=label_text: self.xem_day_du(k, name))
            btn_view.pack(side="left", padx=2)

            btn_copy = ttk.Button(f_row, text="📋 Sao chép", width=10,
                                  command=lambda k=key: self.sao_chep_thanh_phan(k))
            btn_copy.pack(side="left", padx=2)

            self.danh_sach_widget[key] = ent_val

        # Khung kiểm định toán học & nút copy toàn bộ
        frame_bot = ttk.Frame(frame_params)
        frame_bot.pack(fill="x", pady=(12, 0))

        self.lbl_kiem_tra = tk.Label(
            frame_bot,
            text="Trạng thái: Chưa sinh khoá lớn.",
            font=FONT_CHU_DAM, bg=MAU_NEN_CHINH, fg=MAU_CHU_PHU,
            padx=12, pady=8, relief="groove", anchor="w"
        )
        self.lbl_kiem_tra.pack(side="left", fill="x", expand=True)

        btn_copy_all = ttk.Button(frame_bot, text="📋 Sao chép toàn bộ khoá (KU & KR)",
                                  command=self.sao_chep_tat_ca)
        btn_copy_all.pack(side="right", padx=(12, 0))

    def bat_dau_sinh_khoa(self):
        """Khởi động luồng sinh khoá để không đơ giao diện."""
        if self.dang_sinh:
            return

        try:
            so_bit_str = self.cbo_bit.get().strip()
            so_bit = int(so_bit_str)
            if so_bit < 64:
                messagebox.showerror("Độ dài quá nhỏ", "Độ dài khoá phải ≥ 64 bit!")
                return
            if so_bit > 4096:
                messagebox.showwarning("Cảnh báo", "Độ dài > 4096 bit sẽ mất rất nhiều thời gian!")
        except ValueError:
            messagebox.showerror("Sai định dạng", "Độ dài bit phải là một số nguyên dương!")
            return

        self.dang_sinh = True
        self.btn_sinh.config(state="disabled")
        self.progress.start(10)
        self.lbl_time.config(text="Đang sinh hai số nguyên tố p, q...")
        self.set_status(f"Đang sinh khoá RSA {so_bit} bit (chạy nền)...")

        # Khởi chạy luồng nền
        thread = threading.Thread(target=self._worker_sinh_khoa, args=(so_bit,), daemon=True)
        thread.start()

    def _worker_sinh_khoa(self, so_bit):
        try:
            t0 = time.perf_counter()
            khoa = sinh_khoa(so_bit)
            thoi_gian = time.perf_counter() - t0
            self.msg_queue.put(("DONE", khoa, thoi_gian, so_bit))
        except Exception as e:
            self.msg_queue.put(("ERROR", str(e)))

    def _kiem_tra_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                loai = msg[0]
                if loai == "DONE":
                    _, khoa, thoi_gian, so_bit = msg
                    self._cap_nhat_giao_dien_khoa(khoa, thoi_gian, so_bit)
                elif loai == "ERROR":
                    _, err = msg
                    self.progress.stop()
                    self.btn_sinh.config(state="normal")
                    self.dang_sinh = False
                    messagebox.showerror("Lỗi sinh khoá", f"Không thể sinh khoá: {err}")
                    self.set_status("Lỗi trong quá trình sinh khoá.")
        except queue.Empty:
            pass

        self.after(50, self._kiem_tra_queue)

    def _cap_nhat_giao_dien_khoa(self, khoa, thoi_gian, so_bit):
        self.progress.stop()
        self.btn_sinh.config(state="normal")
        self.dang_sinh = False

        self.trang_thai.khoa_lon = khoa
        self.trang_thai.thoi_gian_sinh_lon = thoi_gian
        self.trang_thai.phat_tin_hieu_thay_doi()

        # Hiển thị rút gọn lên các Entry
        for k in ("p", "q", "n", "e", "d"):
            val = khoa[k]
            ent = self.danh_sach_widget[k]
            ent.configure(state="normal")
            ent.delete(0, "end")
            if k == "e":
                ent.insert(0, str(val))
            else:
                ent.insert(0, rut_gon(val, dau=28, cuoi=12))
            ent.configure(state="readonly")

        self.lbl_time.config(text=f"Thời gian: {thoi_gian:.3f} giây ({so_bit} bit)")

        # Kiểm tra tính đúng đắn toán học: e*d mod phi(n) = 1
        phi = (khoa["p"] - 1) * (khoa["q"] - 1)
        kiem_tra = (khoa["e"] * khoa["d"]) % phi
        if kiem_tra == 1:
            self.lbl_kiem_tra.config(
                text=f"✓ Đã xác minh: e * d mod phi(n) = 1  |  Khoá công khai KU={{e, n}}, Khoá riêng KR={{d, p, q}}",
                bg=MAU_DUNG_NEN, fg=MAU_DUNG
            )
        else:
            self.lbl_kiem_tra.config(
                text="✗ CẢNH BÁO: e * d mod phi(n) ≠ 1 (Khoá bị lỗi!)",
                bg=MAU_SAI_NEN, fg=MAU_SAI
            )

        self.set_status(f"Sinh khoá {so_bit} bit thành công trong {thoi_gian:.3f}s.")

    def xem_day_du(self, key, ten_bien):
        if self.trang_thai.khoa_lon is None:
            messagebox.showinfo("Chưa có khoá", "Vui lòng sinh khoá trước khi xem chi tiết!")
            return
        val = self.trang_thai.khoa_lon[key]
        so_bit = val.bit_length() if isinstance(val, int) else None
        HopThoaiXemChiTiet(self, "Chi tiết tham số", ten_bien, val, so_bit)

    def sao_chep_thanh_phan(self, key):
        if self.trang_thai.khoa_lon is None:
            return
        val = str(self.trang_thai.khoa_lon[key])
        self.clipboard_clear()
        self.clipboard_append(val)
        self.set_status(f"Đã sao chép tham số '{key}' vào bộ nhớ tạm.")

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
        messagebox.showinfo("Đã sao chép", "Đã sao chép toàn bộ thông tin cặp khoá vào Clipboard!")


# ==============================================================================
# TAB 3: MÃ HOÁ VÀ GIẢI MÃ VĂN BẢN
# ==============================================================================
class TabMaHoaVanBan(ttk.Frame):
    """
    Tab 3: Mã hoá và giải mã chuỗi văn bản (UTF-8, hỗ trợ tiếng Việt có dấu).
    - Tự động chia khối dựa theo _kich_thuoc_khoi(n).
    - Đo thời gian mã hoá và giải mã.
    - So sánh tính toàn vẹn (ĐÚNG/SAI).
    - Tự động sinh khoá 1024 bit nếu chưa có khoá lớn.
    """
    def __init__(self, parent, trang_thai, status_callback):
        super().__init__(parent, padding=14)
        self.trang_thai = trang_thai
        self.set_status = status_callback

        self.ban_ma_hien_tai = None
        self.do_dai_goc = 0
        self.van_ban_goc = ""

        self._tao_giao_dien()

    def _tao_giao_dien(self):
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.columnconfigure(0, weight=1)

        # 1. Khung nhập văn bản nguồn
        frame_in = ttk.LabelFrame(self, text=" 1. Văn bản bản rõ (Plaintext) - Hỗ trợ Tiếng Việt UTF-8 ", padding=8)
        frame_in.grid(row=0, column=0, sticky="nsew", pady=(0, 6))

        self.txt_ro = tk.Text(frame_in, height=4, font=FONT_NOI_DUNG, wrap="word", bd=1, relief="solid")
        self.txt_ro.pack(side="left", fill="both", expand=True)
        sb_ro = ttk.Scrollbar(frame_in, orient="vertical", command=self.txt_ro.yview)
        sb_ro.pack(side="right", fill="y")
        self.txt_ro.configure(yscrollcommand=sb_ro.set)
        self.txt_ro.insert("1.0", VAN_BAN_MAU)

        # Thanh nút thao tác nguồn
        frame_btn_in = ttk.Frame(self)
        frame_btn_in.grid(row=0, column=0, sticky="se", padx=16, pady=12)

        btn_mau = ttk.Button(frame_btn_in, text="Mẫu", width=6, command=self._dat_cau_mau)
        btn_mau.pack(side="right", padx=2)

        btn_xoa = ttk.Button(frame_btn_in, text="Xoá", width=6, command=lambda: self.txt_ro.delete("1.0", "end"))
        btn_xoa.pack(side="right", padx=2)

        # 2. Khung bản mã (Ciphertext)
        frame_ma = ttk.LabelFrame(self, text=" 2. Bản mã (Ciphertext) & Thông tin phân khối ", padding=8)
        frame_ma.grid(row=1, column=0, sticky="nsew", pady=6)

        frame_info_mh = ttk.Frame(frame_ma)
        frame_info_mh.pack(fill="x", pady=(0, 4))

        self.btn_ma_hoa = ttk.Button(frame_info_mh, text="🔒 Thực hiện Mã hoá", command=self.thuc_hien_ma_hoa)
        self.btn_ma_hoa.pack(side="left", padx=(0, 12))

        self.lbl_info_khoi = ttk.Label(
            frame_info_mh,
            text="Kích thước văn bản: 0 byte | Khối: 0 byte | Số khối: 0",
            font=FONT_CHU_DAM, foreground=MAU_CHINH
        )
        self.lbl_info_khoi.pack(side="left")

        btn_copy_bm = ttk.Button(frame_info_mh, text="📋 Sao chép bản mã", width=16, command=self._sao_chep_ban_ma)
        btn_copy_bm.pack(side="right", padx=(8, 0))

        self.lbl_time_mh = ttk.Label(frame_info_mh, text="", font=FONT_CHU_DAM, foreground=MAU_DIEM_NHAN)
        self.lbl_time_mh.pack(side="right")

        self.txt_ma = tk.Text(frame_ma, height=4, font=FONT_CODE, wrap="char", bd=1, relief="solid", bg="#F8FAFC")
        self.txt_ma.pack(side="left", fill="both", expand=True)
        sb_ma = ttk.Scrollbar(frame_ma, orient="vertical", command=self.txt_ma.yview)
        sb_ma.pack(side="right", fill="y")
        self.txt_ma.configure(yscrollcommand=sb_ma.set)

        # 3. Khung giải mã (Decrypted Text)
        frame_out = ttk.LabelFrame(self, text=" 3. Kết quả Giải mã & Kiểm tra tính toàn vẹn ", padding=8)
        frame_out.grid(row=2, column=0, sticky="nsew", pady=(6, 0))

        frame_info_gm = ttk.Frame(frame_out)
        frame_info_gm.pack(fill="x", pady=(0, 4))

        self.btn_giai_ma = ttk.Button(frame_info_gm, text="🔓 Thực hiện Giải mã", command=self.thuc_hien_giai_ma)
        self.btn_giai_ma.pack(side="left", padx=(0, 12))

        self.lbl_time_gm = ttk.Label(frame_info_gm, text="", font=FONT_CHU_DAM, foreground=MAU_DIEM_NHAN)
        self.lbl_time_gm.pack(side="left")

        self.lbl_ket_luan = tk.Label(frame_info_gm, text="", font=FONT_CHU_DAM, padx=8, pady=2)
        self.lbl_ket_luan.pack(side="right")

        self.txt_giai = tk.Text(frame_out, height=4, font=FONT_NOI_DUNG, wrap="word", bd=1, relief="solid")
        self.txt_giai.pack(side="left", fill="both", expand=True)
        sb_giai = ttk.Scrollbar(frame_out, orient="vertical", command=self.txt_giai.yview)
        sb_giai.pack(side="right", fill="y")
        self.txt_giai.configure(yscrollcommand=sb_giai.set)

    def _dat_cau_mau(self):
        self.txt_ro.delete("1.0", "end")
        self.txt_ro.insert("1.0", VAN_BAN_MAU)

    def _sao_chep_ban_ma(self):
        noi_dung = self.txt_ma.get("1.0", "end-1c")
        if not noi_dung:
            return
        self.clipboard_clear()
        self.clipboard_append(noi_dung)
        self.set_status("Đã sao chép các khối bản mã vào Clipboard.")

    def _kiem_tra_khoa_lon(self):
        """Đảm bảo đã có khoá lớn, nếu chưa thì tự động sinh 1024 bit."""
        if self.trang_thai.khoa_lon is None:
            messagebox.showinfo(
                "Tự động sinh khoá",
                "Chưa có cặp khoá lớn. Hệ thống sẽ tự động tạo cặp khoá RSA 1024 bit để thực hiện."
            )
            self.set_status("Đang tự động sinh khoá 1024 bit...")
            khoa = sinh_khoa(1024)
            self.trang_thai.khoa_lon = khoa
            self.trang_thai.phat_tin_hieu_thay_doi()
            self.set_status("Đã tự động tạo khoá 1024 bit.")
        return self.trang_thai.khoa_lon

    def thuc_hien_ma_hoa(self):
        try:
            van_ban = self.txt_ro.get("1.0", "end-1c")
            if not van_ban:
                messagebox.showwarning("Văn bản rỗng", "Vui lòng nhập văn bản cần mã hoá!")
                return

            khoa = self._kiem_tra_khoa_lon()
            n, e = khoa["n"], khoa["e"]

            du_lieu = van_ban.encode("utf-8")
            k_khoi = _kich_thuoc_khoi(n)

            # Thực hiện mã hoá và đo thời gian
            t0 = time.perf_counter()
            ban_ma, do_dai = ma_hoa_van_ban(van_ban, n, e)
            t_mh = time.perf_counter() - t0

            self.ban_ma_hien_tai = ban_ma
            self.do_dai_goc = do_dai
            self.van_ban_goc = van_ban

            # Cập nhật thông tin khối
            self.lbl_info_khoi.config(
                text=f"Văn bản: {len(du_lieu)} byte UTF-8 | Kích thước khối k: {k_khoi} byte | Số khối bản mã: {len(ban_ma)}"
            )
            self.lbl_time_mh.config(text=f"Thời gian mã hoá: {t_mh * 1000:.2f} ms")

            # Hiển thị các khối bản mã dạng hex
            self.txt_ma.delete("1.0", "end")
            dong_ma = []
            for idx, c in enumerate(ban_ma, 1):
                c_hex = format(c, "x")
                dong_ma.append(f"[Khối {idx:02d}]: {c_hex}")
            self.txt_ma.insert("1.0", "\n".join(dong_ma))

            # Reset vùng giải mã
            self.txt_giai.delete("1.0", "end")
            self.lbl_ket_luan.config(text="", bg=MAU_NEN_CHINH)
            self.lbl_time_gm.config(text="")

            self.set_status(f"Mã hoá văn bản thành công: {len(ban_ma)} khối ({t_mh*1000:.2f} ms).")

        except Exception as ex:
            messagebox.showerror("Lỗi mã hoá", f"Không thể mã hoá văn bản: {ex}")

    def thuc_hien_giai_ma(self):
        try:
            if not self.ban_ma_hien_tai:
                messagebox.showwarning("Chưa có bản mã", "Vui lòng thực hiện mã hoá trước khi giải mã!")
                return

            khoa = self._kiem_tra_khoa_lon()
            n, d = khoa["n"], khoa["d"]

            # Thực hiện giải mã và đo thời gian
            t0 = time.perf_counter()
            van_ban_giai = giai_ma_van_ban(self.ban_ma_hien_tai, self.do_dai_goc, n, d)
            t_gm = time.perf_counter() - t0

            self.txt_giai.delete("1.0", "end")
            self.txt_giai.insert("1.0", van_ban_giai)

            self.lbl_time_gm.config(text=f"Thời gian giải mã: {t_gm * 1000:.2f} ms")

            # So sánh tính toàn vẹn
            if van_ban_giai == self.van_ban_goc:
                self.lbl_ket_luan.config(
                    text="✓ ĐÚNG: Khớp 100% với văn bản gốc!",
                    bg=MAU_DUNG_NEN, fg=MAU_DUNG
                )
            else:
                self.lbl_ket_luan.config(
                    text="✗ SAI: Văn bản giải mã không khớp!",
                    bg=MAU_SAI_NEN, fg=MAU_SAI
                )

            self.set_status(f"Giải mã hoàn tất trong {t_gm*1000:.2f} ms.")

        except Exception as ex:
            messagebox.showerror("Lỗi giải mã", f"Không thể giải mã: {ex}")


# ==============================================================================
# TAB 4: MÃ HOÁ VÀ GIẢI MÃ TỆP (FILE ENCRYPTION & IMAGE PREVIEW)
# ==============================================================================
class TabMaHoaTep(ttk.Frame):
    """
    Tab 4: Mã hoá và giải mã tệp nhị phân (văn bản, PDF, ảnh nhỏ...).
    - Lưu tệp mã hoá dạng .rsa: dòng 1 là độ dài gốc, các dòng sau là hex của khối.
    - So sánh hash SHA-256 giữa tệp gốc và tệp giải mã.
    - Hỗ trợ xem trước ảnh (PNG/GIF) bằng tkinter.PhotoImage cạnh nhau.
    - Cảnh báo nếu tệp > 200 KB và chạy trong thread nền với progressbar.
    """
    def __init__(self, parent, trang_thai, status_callback):
        super().__init__(parent, padding=14)
        self.trang_thai = trang_thai
        self.set_status = status_callback

        self.duong_dan_tep = None
        self.duong_dan_rsa = None
        self.duong_dan_giaima = None

        self.img_goc_tk = None
        self.img_giai_tk = None
        self.msg_queue = queue.Queue()

        self._tao_giao_dien()
        self._kiem_tra_queue()

    def _tao_giao_dien(self):
        self.columnconfigure(0, weight=1)

        # 1. Khung chọn tệp
        frame_file = ttk.LabelFrame(self, text=" 1. Chọn tệp nguồn cần mã hoá ", padding=10)
        frame_file.pack(fill="x", pady=(0, 8))

        btn_browse = ttk.Button(frame_file, text="📁 Chọn tệp...", command=self.chon_tep)
        btn_browse.pack(side="left", padx=(0, 8))

        self.lbl_file_path = ttk.Label(frame_file, text="Chưa chọn tệp nào.", font=FONT_CODE)
        self.lbl_file_path.pack(side="left", fill="x", expand=True)

        self.lbl_file_size = ttk.Label(frame_file, text="", font=FONT_CHU_DAM, foreground=MAU_CHINH)
        self.lbl_file_size.pack(side="right")

        # 2. Khung thao tác mã hoá và giải mã
        frame_action = ttk.LabelFrame(self, text=" 2. Thao tác Mã hoá (.rsa) & Giải mã (_giaima) ", padding=10)
        frame_action.pack(fill="x", pady=6)

        self.btn_mh_tep = ttk.Button(frame_action, text="🔒 Mã hoá tệp", command=self.bat_dau_ma_hoa_tep)
        self.btn_mh_tep.pack(side="left", padx=(0, 8))

        self.btn_gm_tep = ttk.Button(frame_action, text="🔓 Giải mã tệp", command=self.bat_dau_giai_ma_tep)
        self.btn_gm_tep.pack(side="left", padx=(0, 16))

        self.progress_tep = ttk.Progressbar(frame_action, orient="horizontal", mode="determinate", length=220)
        self.progress_tep.pack(side="left", padx=(0, 12))

        self.lbl_tien_do = ttk.Label(frame_action, text="Sẵn sàng", font=FONT_NOI_DUNG)
        self.lbl_tien_do.pack(side="left")

        # 3. Khung kiểm tra SHA-256
        frame_hash = ttk.LabelFrame(self, text=" 3. Kiểm định toàn vẹn dữ liệu (Băm SHA-256) ", padding=10)
        frame_hash.pack(fill="x", pady=6)

        f_h1 = ttk.Frame(frame_hash)
        f_h1.pack(fill="x", pady=2)
        ttk.Label(f_h1, text="SHA-256 tệp gốc:      ", font=FONT_CHU_DAM).pack(side="left")
        self.lbl_hash_goc = ttk.Label(f_h1, text="-", font=FONT_CODE)
        self.lbl_hash_goc.pack(side="left")

        f_h2 = ttk.Frame(frame_hash)
        f_h2.pack(fill="x", pady=2)
        ttk.Label(f_h2, text="SHA-256 tệp giải mã:", font=FONT_CHU_DAM).pack(side="left")
        self.lbl_hash_giai = ttk.Label(f_h2, text="-", font=FONT_CODE)
        self.lbl_hash_giai.pack(side="left")

        self.lbl_kq_hash = tk.Label(frame_hash, text="Trạng thái so sánh: Chưa thực hiện.",
                                    font=FONT_CHU_DAM, bg=MAU_NEN_CHINH, fg=MAU_CHU_PHU,
                                    anchor="w", padx=8, pady=4)
        self.lbl_kq_hash.pack(fill="x", pady=(6, 0))

        # 4. Khung xem trước ảnh cạnh nhau
        frame_img = ttk.LabelFrame(self, text=" 4. So sánh trực quan hình ảnh (Xem trước PNG / GIF) ", padding=10)
        frame_img.pack(fill="both", expand=True, pady=(6, 0))

        frame_img.columnconfigure(0, weight=1)
        frame_img.columnconfigure(1, weight=1)
        frame_img.rowconfigure(0, weight=1)

        # Box ảnh gốc
        box_img_goc = ttk.LabelFrame(frame_img, text=" [ Ảnh gốc ban đầu ] ", padding=6)
        box_img_goc.grid(row=0, column=0, sticky="nsew", padx=6)
        self.lbl_preview_goc = ttk.Label(box_img_goc, text="(Chưa có ảnh gốc)", anchor="center")
        self.lbl_preview_goc.pack(fill="both", expand=True)

        # Box ảnh giải mã
        box_img_giai = ttk.LabelFrame(frame_img, text=" [ Ảnh sau khi giải mã ] ", padding=6)
        box_img_giai.grid(row=0, column=1, sticky="nsew", padx=6)
        self.lbl_preview_giai = ttk.Label(box_img_giai, text="(Chưa có ảnh giải mã)", anchor="center")
        self.lbl_preview_giai.pack(fill="both", expand=True)

    def chon_tep(self):
        duong_dan = filedialog.askopenfilename(
            title="Chọn tệp để mã hoá hoặc giải mã",
            filetypes=[
                ("Tất cả tệp", "*.*"),
                ("Tệp văn bản", "*.txt"),
                ("Tệp hình ảnh", "*.png;*.gif"),
                ("Tệp mã hoá RSA", "*.rsa"),
            ]
        )
        if not duong_dan:
            return

        self.duong_dan_tep = duong_dan
        kich_thuoc = os.path.getsize(duong_dan)
        ten_tep = os.path.basename(duong_dan)

        self.lbl_file_path.config(text=f"{ten_tep} ({duong_dan})")
        if kich_thuoc < 1024:
            size_str = f"{kich_thuoc} Bytes"
        else:
            size_str = f"{kich_thuoc / 1024:.1f} KB ({kich_thuoc} Bytes)"
        self.lbl_file_size.config(text=f"Dung lượng: {size_str}")

        # Reset các nhãn kết quả
        self.lbl_hash_goc.config(text="-")
        self.lbl_hash_giai.config(text="-")
        self.lbl_kq_hash.config(text="Trạng thái: Đã chọn tệp mới, sẵn sàng thao tác.", bg=MAU_NEN_CHINH, fg=MAU_CHU_PHU)
        self._hien_thi_anh_goc(duong_dan)

        # Cảnh báo nếu tệp vượt giới hạn
        if kich_thuoc > GIOI_HAN_TEP and not duong_dan.endswith(".rsa"):
            tra_loi = messagebox.askyesno(
                "Cảnh báo tệp lớn",
                f"Tệp có dung lượng {kich_thuoc // 1024} KB (> 200 KB).\n"
                "RSA cơ bản tính toán thuần số học Python nên quá trình giải mã sẽ tốn thời gian.\n"
                "Bạn có muốn tiếp tục không?"
            )
            if not tra_loi:
                self.duong_dan_tep = None
                self.lbl_file_path.config(text="Đã huỷ chọn tệp do dung lượng lớn.")
                self.lbl_file_size.config(text="")
                return

        self.set_status(f"Đã chọn tệp: {ten_tep} ({size_str})")

    def _hien_thi_anh_goc(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext in (".png", ".gif"):
            try:
                img = tk.PhotoImage(file=path)
                w, h = img.width(), img.height()
                if w > 240 or h > 200:
                    ti_le = max((w + 239) // 240, (h + 199) // 200)
                    img = img.subsample(ti_le, ti_le)
                self.img_goc_tk = img
                self.lbl_preview_goc.config(image=self.img_goc_tk, text="")
            except Exception:
                self.lbl_preview_goc.config(image="", text="(Không thể đọc định dạng ảnh)")
        else:
            self.lbl_preview_goc.config(image="", text="(Định dạng không hỗ trợ xem trước)")

    def _hien_thi_anh_giai(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext in (".png", ".gif"):
            try:
                img = tk.PhotoImage(file=path)
                w, h = img.width(), img.height()
                if w > 240 or h > 200:
                    ti_le = max((w + 239) // 240, (h + 199) // 200)
                    img = img.subsample(ti_le, ti_le)
                self.img_giai_tk = img
                self.lbl_preview_giai.config(image=self.img_giai_tk, text="")
            except Exception:
                self.lbl_preview_giai.config(image="", text="(Không thể đọc định dạng ảnh)")
        else:
            self.lbl_preview_giai.config(image="", text="(Định dạng không hỗ trợ xem trước)")

    def _kiem_tra_khoa_lon(self):
        if self.trang_thai.khoa_lon is None:
            messagebox.showinfo("Tự động sinh khoá", "Chưa có khoá lớn, hệ thống sẽ tự sinh khoá 1024 bit.")
            khoa = sinh_khoa(1024)
            self.trang_thai.khoa_lon = khoa
            self.trang_thai.phat_tin_hieu_thay_doi()
        return self.trang_thai.khoa_lon

    def bat_dau_ma_hoa_tep(self):
        if not self.duong_dan_tep or not os.path.isfile(self.duong_dan_tep):
            messagebox.showwarning("Chưa chọn tệp", "Vui lòng chọn tệp hợp lệ trước!")
            return

        khoa = self._kiem_tra_khoa_lon()
        self.btn_mh_tep.config(state="disabled")
        self.btn_gm_tep.config(state="disabled")
        self.lbl_tien_do.config(text="Đang mã hoá từng khối...")

        thread = threading.Thread(target=self._worker_ma_hoa_tep, args=(self.duong_dan_tep, khoa), daemon=True)
        thread.start()

    def _worker_ma_hoa_tep(self, duong_dan, khoa):
        try:
            with open(duong_dan, "rb") as f:
                du_lieu = f.read()

            hash_goc = hashlib.sha256(du_lieu).hexdigest()
            n, e = khoa["n"], khoa["e"]
            k = _kich_thuoc_khoi(n)
            tong_khoi = (len(du_lieu) + k - 1) // k

            ban_ma = []
            t0 = time.perf_counter()

            for i in range(0, len(du_lieu), k):
                khoi = du_lieu[i:i + k]
                m = int.from_bytes(khoi, "big")
                c = ma_hoa_so(m, n, e)
                ban_ma.append(c)
                phan_tram = int((len(ban_ma) / max(tong_khoi, 1)) * 100)
                self.msg_queue.put(("PROGRESS_MH", phan_tram, len(ban_ma), tong_khoi))

            t_mh = time.perf_counter() - t0

            # Ghi ra tệp .rsa theo đúng định dạng main_cli.py
            tep_ma = duong_dan + ".rsa"
            with open(tep_ma, "w", encoding="ascii") as f:
                f.write(f"{len(du_lieu)}\n")
                f.write("\n".join(format(c, "x") for c in ban_ma))

            self.msg_queue.put(("DONE_MH", tep_ma, hash_goc, t_mh, len(ban_ma)))

        except Exception as ex:
            self.msg_queue.put(("ERROR_MH", str(ex)))

    def bat_dau_giai_ma_tep(self):
        if not self.duong_dan_tep:
            messagebox.showwarning("Chưa chọn tệp", "Vui lòng chọn tệp để giải mã!")
            return

        if self.duong_dan_tep.endswith(".rsa"):
            tep_rsa = self.duong_dan_tep
        else:
            tep_rsa = self.duong_dan_rsa or (self.duong_dan_tep + ".rsa")

        if not os.path.isfile(tep_rsa):
            messagebox.showwarning("Không tìm thấy tệp", f"Chưa tìm thấy tệp mã hoá .rsa để giải mã:\n{tep_rsa}")
            return

        khoa = self._kiem_tra_khoa_lon()
        self.btn_mh_tep.config(state="disabled")
        self.btn_gm_tep.config(state="disabled")
        self.lbl_tien_do.config(text="Đang giải mã từng khối...")

        thread = threading.Thread(target=self._worker_giai_ma_tep, args=(tep_rsa, khoa), daemon=True)
        thread.start()

    def _worker_giai_ma_tep(self, tep_rsa, khoa):
        try:
            with open(tep_rsa, "r", encoding="ascii") as f:
                noi_dung = f.read().split("\n")

            do_dai_goc = int(noi_dung[0])
            ban_ma = [int(x, 16) for x in noi_dung[1:] if x.strip()]

            n, d = khoa["n"], khoa["d"]
            k = _kich_thuoc_khoi(n)
            tong_khoi = len(ban_ma)

            ket_qua = bytearray()
            con_lai = do_dai_goc
            t0 = time.perf_counter()

            for idx, c in enumerate(ban_ma, 1):
                m = giai_ma_so(c, n, d)
                do_dai_khoi = min(k, con_lai)
                ket_qua += m.to_bytes(do_dai_khoi, "big")
                con_lai -= do_dai_khoi
                phan_tram = int((idx / max(tong_khoi, 1)) * 100)
                self.msg_queue.put(("PROGRESS_GM", phan_tram, idx, tong_khoi))

            t_gm = time.perf_counter() - t0
            du_lieu_giai = bytes(ket_qua)
            hash_giai = hashlib.sha256(du_lieu_giai).hexdigest()

            # Xác định tên tệp giải mã
            if tep_rsa.endswith(".rsa"):
                tien_to = tep_rsa[:-4]
                goc, ext = os.path.splitext(tien_to)
                tep_giai = f"{goc}_giaima{ext}"
                tep_goc_can_check = tien_to
            else:
                goc, ext = os.path.splitext(tep_rsa)
                tep_giai = f"{goc}_giaima{ext}"
                tep_goc_can_check = None

            with open(tep_giai, "wb") as f:
                f.write(du_lieu_giai)

            # Tính hash của tệp gốc nếu tệp gốc tồn tại
            hash_goc_doc = None
            if tep_goc_can_check and os.path.isfile(tep_goc_can_check):
                with open(tep_goc_can_check, "rb") as fg:
                    hash_goc_doc = hashlib.sha256(fg.read()).hexdigest()

            self.msg_queue.put(("DONE_GM", tep_giai, hash_giai, t_gm, hash_goc_doc))

        except Exception as ex:
            self.msg_queue.put(("ERROR_GM", str(ex)))

    def _kiem_tra_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                loai = msg[0]

                if loai == "PROGRESS_MH":
                    _, pct, cur, total = msg
                    self.progress_tep["value"] = pct
                    self.lbl_tien_do.config(text=f"Mã hoá: khối {cur}/{total} ({pct}%)")

                elif loai == "DONE_MH":
                    _, tep_ma, hash_goc, t_mh, so_khoi = msg
                    self.duong_dan_rsa = tep_ma
                    self.lbl_hash_goc.config(text=hash_goc)
                    self.progress_tep["value"] = 100
                    self.lbl_tien_do.config(text=f"Đã mã hoá {so_khoi} khối ({t_mh:.2f}s) -> .rsa")
                    self.btn_mh_tep.config(state="normal")
                    self.btn_gm_tep.config(state="normal")
                    messagebox.showinfo("Thành công", f"Đã mã hoá thành công vào tệp:\n{tep_ma}")
                    self.set_status(f"Mã hoá tệp hoàn tất trong {t_mh:.2f}s.")

                elif loai == "PROGRESS_GM":
                    _, pct, cur, total = msg
                    self.progress_tep["value"] = pct
                    self.lbl_tien_do.config(text=f"Giải mã: khối {cur}/{total} ({pct}%)")

                elif loai == "DONE_GM":
                    _, tep_giai, hash_giai, t_gm, hash_goc_doc = msg
                    self.duong_dan_giaima = tep_giai
                    self.lbl_hash_giai.config(text=hash_giai)
                    if hash_goc_doc:
                        self.lbl_hash_goc.config(text=hash_goc_doc)

                    self.progress_tep["value"] = 100
                    self.lbl_tien_do.config(text=f"Đã giải mã xong ({t_gm:.2f}s)")
                    self.btn_mh_tep.config(state="normal")
                    self.btn_gm_tep.config(state="normal")

                    # So sánh hash SHA-256
                    hash_goc = self.lbl_hash_goc.cget("text")
                    if hash_goc != "-" and hash_goc == hash_giai:
                        self.lbl_kq_hash.config(
                            text="✓ ĐÚNG: Tệp giải mã TRÙNG KHỚP 100% tệp gốc (Khớp mã băm SHA-256)!",
                            bg=MAU_DUNG_NEN, fg=MAU_DUNG
                        )
                    elif hash_goc != "-" and hash_goc != hash_giai:
                        self.lbl_kq_hash.config(
                            text="✗ SAI: Mã băm SHA-256 không trùng khớp (Tệp bị lỗi)!",
                            bg=MAU_SAI_NEN, fg=MAU_SAI
                        )
                    else:
                        self.lbl_kq_hash.config(
                            text="✓ Đã giải mã thành công (Không có tệp gốc để đối chiếu SHA-256).",
                            bg=MAU_NEN_CHINH, fg=MAU_CHU
                        )

                    self._hien_thi_anh_giai(tep_giai)
                    messagebox.showinfo("Thành công", f"Đã giải mã thành công vào tệp:\n{tep_giai}")
                    self.set_status(f"Giải mã tệp hoàn tất trong {t_gm:.2f}s.")

                elif loai in ("ERROR_MH", "ERROR_GM"):
                    _, err = msg
                    self.progress_tep["value"] = 0
                    self.lbl_tien_do.config(text="Đã xảy ra lỗi.")
                    self.btn_mh_tep.config(state="normal")
                    self.btn_gm_tep.config(state="normal")
                    messagebox.showerror("Lỗi", f"Thao tác thất bại: {err}")
                    self.set_status(f"Lỗi tệp: {err}")

        except queue.Empty:
            pass

        self.after(50, self._kiem_tra_queue)


# ==============================================================================
# TAB 5: ĐO THỜI GIAN VÀ BIỂU ĐỒ CỘT (BENCHMARK & CANVAS CHART)
# ==============================================================================
class TabDoThoiGian(ttk.Frame):
    """
    Tab 5: Đo hiệu năng RSA theo độ dài khoá (512, 1024, 2048 bit).
    - Đo thời gian: Sinh khoá, Mã hoá, Giải mã văn bản ~1000 byte.
    - Hiển thị bảng Treeview và xuất CSV (utf-8-sig).
    - Vẽ biểu đồ cột trên Canvas (thuần Python, không dùng matplotlib).
    """
    def __init__(self, parent, trang_thai, status_callback):
        super().__init__(parent, padding=14)
        self.trang_thai = trang_thai
        self.set_status = status_callback

        self.ket_qua_do = []
        self.dang_do = False
        self.msg_queue = queue.Queue()

        self._tao_giao_dien()
        self._kiem_tra_queue()

    def _tao_giao_dien(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # 1. Khung điều khiển đo nghiệm
        frame_top = ttk.LabelFrame(self, text=" 1. Thiết lập tham số đo nghiệm ", padding=10)
        frame_top.pack(fill="x", pady=(0, 8))

        ttk.Label(frame_top, text="Số lần lặp mỗi độ dài khoá:", font=FONT_CHU_DAM).pack(side="left", padx=(0, 6))

        self.spn_so_lan = ttk.Spinbox(frame_top, from_=1, to=10, width=5, font=FONT_CODE)
        self.spn_so_lan.set("3")
        self.spn_so_lan.pack(side="left", padx=(0, 16))

        self.btn_bat_dau_do = ttk.Button(frame_top, text="⏱ Bắt đầu đo nghiệm", command=self.bat_dau_do)
        self.btn_bat_dau_do.pack(side="left", padx=4)

        self.btn_xuat_csv = ttk.Button(frame_top, text="📥 Xuất file CSV", command=self.xuat_csv, state="disabled")
        self.btn_xuat_csv.pack(side="left", padx=4)

        self.progress_do = ttk.Progressbar(frame_top, orient="horizontal", mode="determinate", length=200)
        self.progress_do.pack(side="left", padx=(16, 8))

        self.lbl_trang_thai_do = ttk.Label(frame_top, text="Sẵn sàng đo (512 / 1024 / 2048 bit)", font=FONT_NOI_DUNG)
        self.lbl_trang_thai_do.pack(side="left")

        # 2. Bảng dữ liệu đo nghiệm (Treeview)
        frame_bang = ttk.LabelFrame(self, text=" 2. Bảng kết quả đo lường trung bình ", padding=8)
        frame_bang.pack(fill="x", pady=6)

        cols_bm = ("bit", "sinh_khoa", "ma_hoa", "giai_ma", "so_lan")
        self.tree_bm = ttk.Treeview(frame_bang, columns=cols_bm, show="headings", height=4)
        self.tree_bm.heading("bit", text="Độ dài khoá (bit)")
        self.tree_bm.heading("sinh_khoa", text="Sinh khoá TB (giây)")
        self.tree_bm.heading("ma_hoa", text="Mã hoá TB (ms)")
        self.tree_bm.heading("giai_ma", text="Giải mã TB (ms)")
        self.tree_bm.heading("so_lan", text="Số lần đo")

        self.tree_bm.column("bit", width=140, anchor="center")
        self.tree_bm.column("sinh_khoa", width=180, anchor="center")
        self.tree_bm.column("ma_hoa", width=180, anchor="center")
        self.tree_bm.column("giai_ma", width=180, anchor="center")
        self.tree_bm.column("so_lan", width=100, anchor="center")

        self.tree_bm.pack(fill="x", pady=2)

        # 3. Biểu đồ cột Canvas
        frame_chart = ttk.LabelFrame(self, text=" 3. Biểu đồ trực quan hoá thời gian (Canvas) ", padding=8)
        frame_chart.pack(fill="both", expand=True, pady=(6, 0))

        # Thanh chọn chỉ số hiển thị
        frame_opt = ttk.Frame(frame_chart)
        frame_opt.pack(fill="x", pady=(0, 4))

        ttk.Label(frame_opt, text="Xem biểu đồ:", font=FONT_CHU_DAM).pack(side="left", padx=(0, 12))

        self.var_loai_bieu_do = tk.StringVar(value="tat_ca")
        r1 = ttk.Radiobutton(frame_opt, text="Tất cả chỉ số", variable=self.var_loai_bieu_do,
                             value="tat_ca", command=self.ve_bieu_do)
        r1.pack(side="left", padx=8)

        r2 = ttk.Radiobutton(frame_opt, text="Chỉ Sinh khoá (giây)", variable=self.var_loai_bieu_do,
                             value="sinh_khoa", command=self.ve_bieu_do)
        r2.pack(side="left", padx=8)

        r3 = ttk.Radiobutton(frame_opt, text="Chỉ Mã hoá & Giải mã (ms)", variable=self.var_loai_bieu_do,
                             value="ma_giai", command=self.ve_bieu_do)
        r3.pack(side="left", padx=8)

        self.canvas = tk.Canvas(frame_chart, bg="#FFFFFF", bd=1, relief="solid")
        self.canvas.pack(fill="both", expand=True, pady=4)
        self.canvas.bind("<Configure>", lambda e: self.ve_bieu_do())

    def bat_dau_do(self):
        if self.dang_do:
            return

        try:
            so_lan = int(self.spn_so_lan.get().strip())
            if so_lan < 1:
                so_lan = 1
        except ValueError:
            so_lan = 3

        self.dang_do = True
        self.btn_bat_dau_do.config(state="disabled")
        self.btn_xuat_csv.config(state="disabled")
        self.progress_do["value"] = 0

        for item in self.tree_bm.get_children():
            self.tree_bm.delete(item)
        self.canvas.delete("all")

        thread = threading.Thread(target=self._worker_do_thoi_gian, args=(so_lan,), daemon=True)
        thread.start()

    def _worker_do_thoi_gian(self, so_lan):
        try:
            # Tạo dữ liệu đo: văn bản mẫu ~1000 byte tương tự main_cli.py
            mau = (VAN_BAN_MAU * 20).encode("utf-8")[:1000].decode("utf-8", errors="ignore")
            bits_list = [512, 1024, 2048]
            tong_buoc = len(bits_list) * so_lan
            buoc_hien_tai = 0
            ket_qua = []

            for so_bit in bits_list:
                t_khoa_tong = 0.0
                t_mh_tong = 0.0
                t_gm_tong = 0.0

                for lan in range(1, so_lan + 1):
                    buoc_hien_tai += 1
                    pct = int((buoc_hien_tai / tong_buoc) * 100)
                    self.msg_queue.put(("STEP", pct, f"Đang đo {so_bit} bit (lần {lan}/{so_lan})..."))

                    # Đo sinh khoá
                    t0 = time.perf_counter()
                    k = sinh_khoa(so_bit)
                    t_khoa_tong += (time.perf_counter() - t0)

                    # Đo mã hoá
                    t0 = time.perf_counter()
                    bm, dd = ma_hoa_van_ban(mau, k["n"], k["e"])
                    t_mh_tong += (time.perf_counter() - t0)

                    # Đo giải mã
                    t0 = time.perf_counter()
                    giai_ma_van_ban(bm, dd, k["n"], k["d"])
                    t_gm_tong += (time.perf_counter() - t0)

                tb_khoa = t_khoa_tong / so_lan
                tb_mh = (t_mh_tong / so_lan) * 1000  # mili-giây
                tb_gm = (t_gm_tong / so_lan) * 1000  # mili-giây

                ket_qua.append((so_bit, tb_khoa, tb_mh, tb_gm, so_lan))
                self.msg_queue.put(("ROW_DONE", (so_bit, tb_khoa, tb_mh, tb_gm, so_lan)))

            self.msg_queue.put(("ALL_DONE", ket_qua))

        except Exception as ex:
            self.msg_queue.put(("ERROR_DO", str(ex)))

    def _kiem_tra_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                loai = msg[0]

                if loai == "STEP":
                    _, pct, text = msg
                    self.progress_do["value"] = pct
                    self.lbl_trang_thai_do.config(text=text)

                elif loai == "ROW_DONE":
                    _, row = msg
                    so_bit, a, b, c, so_lan = row
                    self.tree_bm.insert("", "end", values=(
                        f"{so_bit} bit",
                        f"{a:.3f} s",
                        f"{b:.2f} ms",
                        f"{c:.2f} ms",
                        f"{so_lan}"
                    ))

                elif loai == "ALL_DONE":
                    _, res = msg
                    self.ket_qua_do = res
                    self.dang_do = False
                    self.btn_bat_dau_do.config(state="normal")
                    self.btn_xuat_csv.config(state="normal")
                    self.progress_do["value"] = 100
                    self.lbl_trang_thai_do.config(text="✓ Đã hoàn tất đo nghiệm toàn bộ các khoá!")
                    self.ve_bieu_do()
                    self.set_status("Đã hoàn tất đo thời gian 512, 1024, 2048 bit.")

                elif loai == "ERROR_DO":
                    _, err = msg
                    self.dang_do = False
                    self.btn_bat_dau_do.config(state="normal")
                    messagebox.showerror("Lỗi đo nghiệm", f"Quá trình đo gặp lỗi: {err}")
                    self.set_status(f"Lỗi đo nghiệm: {err}")

        except queue.Empty:
            pass

        self.after(50, self._kiem_tra_queue)

    def ve_bieu_do(self):
        """Vẽ biểu đồ cột trực quan trên Canvas với tỉ lệ và chú giải rõ ràng."""
        self.canvas.delete("all")
        if not self.ket_qua_do:
            self.canvas.create_text(
                self.canvas.winfo_width() // 2 or 300,
                self.canvas.winfo_height() // 2 or 100,
                text="Chưa có dữ liệu đo nghiệm. Nhấn 'Bắt đầu đo nghiệm' ở trên.",
                font=FONT_NOI_DUNG, fill=MAU_CHU_PHU
            )
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 100 or h < 100:
            return

        loai = self.var_loai_bieu_do.get()

        # Toạ độ trục toạ độ
        pad_l, pad_r, pad_t, pad_b = 60, 40, 30, 40
        plot_w = w - pad_l - pad_r
        plot_h = h - pad_t - pad_b

        # Trục toạ độ
        self.canvas.create_line(pad_l, pad_t + plot_h, pad_l + plot_w, pad_t + plot_h, fill="#94A3B8", width=2)
        self.canvas.create_line(pad_l, pad_t, pad_l, pad_t + plot_h, fill="#94A3B8", width=2)

        # Chú thích màu sắc (Legend)
        colors = {
            "sinh_khoa": ("#F59E0B", "Sinh khoá (s)"),
            "ma_hoa": ("#10B981", "Mã hoá (ms)"),
            "giai_ma": ("#3B82F6", "Giải mã (ms)")
        }

        # Vẽ Legend ở góc trên bên phải
        leg_x = pad_l + plot_w - 240
        leg_y = pad_t - 15
        if loai in ("tat_ca", "sinh_khoa"):
            self.canvas.create_rectangle(leg_x, leg_y, leg_x + 12, leg_y + 12, fill=colors["sinh_khoa"][0], outline="")
            self.canvas.create_text(leg_x + 16, leg_y + 6, text="Sinh khoá (s)", font=("Segoe UI", 9), anchor="w")
            leg_x += 80
        if loai in ("tat_ca", "ma_giai"):
            self.canvas.create_rectangle(leg_x, leg_y, leg_x + 12, leg_y + 12, fill=colors["ma_hoa"][0], outline="")
            self.canvas.create_text(leg_x + 16, leg_y + 6, text="Mã hoá (ms)", font=("Segoe UI", 9), anchor="w")
            leg_x += 80
            self.canvas.create_rectangle(leg_x, leg_y, leg_x + 12, leg_y + 12, fill=colors["giai_ma"][0], outline="")
            self.canvas.create_text(leg_x + 16, leg_y + 6, text="Giải mã (ms)", font=("Segoe UI", 9), anchor="w")

        # Tìm giá trị lớn nhất để chuẩn hoá trục Y
        max_val = 0.001
        for row in self.ket_qua_do:
            _, a, b, c, _ = row
            if loai == "sinh_khoa":
                max_val = max(max_val, a)
            elif loai == "ma_giai":
                max_val = max(max_val, b, c)
            else:
                max_val = max(max_val, a, b, c)

        # Làm tròn max_val
        y_max = max_val * 1.25

        # Vẽ đường lưới ngang (Grid lines)
        for i in range(5):
            val_grid = y_max * (i / 4)
            y_pos = pad_t + plot_h - (val_grid / y_max) * plot_h
            self.canvas.create_line(pad_l, y_pos, pad_l + plot_w, y_pos, fill="#F1F5F9", width=1)
            self.canvas.create_text(pad_l - 6, y_pos, text=f"{val_grid:.1f}", font=("Segoe UI", 9), anchor="e", fill=MAU_CHU_PHU)

        # Vẽ các nhóm cột
        num_groups = len(self.ket_qua_do)
        group_width = plot_w / num_groups

        for g_idx, row in enumerate(self.ket_qua_do):
            so_bit, a, b, c, _ = row
            center_x = pad_l + g_idx * group_width + group_width / 2

            # Nhãn trục X
            self.canvas.create_text(center_x, pad_t + plot_h + 16, text=f"{so_bit} bit", font=FONT_CHU_DAM, fill=MAU_CHU)

            if loai == "sinh_khoa":
                bar_items = [(a, colors["sinh_khoa"][0], f"{a:.3f}s")]
            elif loai == "ma_giai":
                bar_items = [(b, colors["ma_hoa"][0], f"{b:.1f}ms"), (c, colors["giai_ma"][0], f"{c:.1f}ms")]
            else:
                bar_items = [
                    (a, colors["sinh_khoa"][0], f"{a:.2f}s"),
                    (b, colors["ma_hoa"][0], f"{b:.1f}ms"),
                    (c, colors["giai_ma"][0], f"{c:.1f}ms"),
                ]

            bar_w = min(28, (group_width * 0.7) / len(bar_items))
            start_x = center_x - (len(bar_items) * bar_w) / 2

            for b_idx, (val, color, lbl_text) in enumerate(bar_items):
                bx = start_x + b_idx * bar_w
                bh = (val / y_max) * plot_h
                by = pad_t + plot_h - bh

                # Vẽ cột
                self.canvas.create_rectangle(bx, by, bx + bar_w - 2, pad_t + plot_h, fill=color, outline="")
                # Nhãn giá trị trên cột
                self.canvas.create_text(bx + bar_w / 2, by - 8, text=lbl_text, font=("Segoe UI", 8, "bold"), fill=MAU_CHU)

    def xuat_csv(self):
        """Xuất bảng kết quả ra file CSV chuẩn utf-8-sig."""
        if not self.ket_qua_do:
            messagebox.showwarning("Chưa có kết quả", "Chưa có dữ liệu để xuất file CSV!")
            return

        duong_dan = filedialog.asksaveasfilename(
            title="Lưu kết quả đo thời gian",
            initialfile="thoi_gian_rsa.csv",
            defaultextension=".csv",
            filetypes=[("Tệp CSV", "*.csv")]
        )
        if not duong_dan:
            return

        try:
            with open(duong_dan, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["Khoá (bit)", "Sinh khoá (s)", "Mã hoá (ms)", "Giải mã (ms)", "Số lần đo"])
                for row in self.ket_qua_do:
                    so_bit, a, b, c, so_lan = row
                    writer.writerow([so_bit, round(a, 3), round(b, 2), round(c, 2), so_lan])

            messagebox.showinfo("Xuất CSV thành công", f"Đã lưu bảng kết quả đo thời gian vào:\n{duong_dan}")
            self.set_status(f"Đã xuất file CSV: {os.path.basename(duong_dan)}")
        except Exception as ex:
            messagebox.showerror("Lỗi lưu file", f"Không thể xuất file CSV: {ex}")


# ==============================================================================
# CỬA SỔ GIỚI THIỆU (ABOUT DIALOG)
# ==============================================================================
class CuaSoGioiThieu(tk.Toplevel):
    """Hộp thoại giới thiệu đề tài, nhóm thực hiện và cảnh báo học tập."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Giới thiệu Đề tài Hệ mã RSA - Nhóm 8")
        self.geometry("640x520")
        self.resizable(False, False)
        self.configure(bg=MAU_NEN_CHINH)
        self.transient(parent)
        self.grab_set()

        # Banner Header
        frame_head = tk.Frame(self, bg=MAU_CHINH, padx=20, pady=16)
        frame_head.pack(fill="x")

        tk.Label(
            frame_head, text="HỆ MÃ HOÁ KHOÁ CÔNG KHAI RSA",
            font=FONT_TIEU_DE, fg="white", bg=MAU_CHINH
        ).pack(anchor="w")

        tk.Label(
            frame_head,
            text="Học phần: An toàn và bảo mật thông tin mạng\nĐề tài môn học - Nhóm 8 (Ngành Thương mại điện tử)",
            font=FONT_SUB_HEADER, fg="#CBD5E1", bg=MAU_CHINH, justify="left"
        ).pack(anchor="w", pady=(4, 0))

        # Nội dung
        frame_body = tk.Frame(self, bg=MAU_NEN_CHINH, padx=20, pady=14)
        frame_body.pack(fill="both", expand=True)

        txt_info = (
            "📌 TỔNG QUAN NGUYÊN LÝ HOẠT ĐỘNG:\n"
            "1. Sinh khoá: Chọn hai số nguyên tố ngẫu nhiên p và q (kiểm tra bằng Miller-Rabin).\n"
            "2. Tính modulo n = p * q và hàm Euler phi(n) = (p - 1) * (q - 1).\n"
            "3. Chọn số mũ công khai e nguyên tố cùng nhau với phi(n) (thường chọn e = 65537).\n"
            "4. Tìm số mũ bí mật d = e⁻¹ mod phi(n) nhờ thuật toán Euclid mở rộng.\n"
            "5. Khoá công khai KU = {e, n} dùng để Mã hoá: C = M^e mod n.\n"
            "6. Khoá riêng KR = {d, p, q} dùng để Giải mã: M = C^d mod n.\n"
            "   (Cả hai phép tính luỹ thừa lớn đều tối ưu bằng Bình phương và nhân).\n\n"
            "👥 THÀNH VIÊN THỰC HIỆN (NHÓM 8):\n"
            "• Nhóm 5 sinh viên chuyên ngành Thương mại điện tử\n"
            "• Đề tài: Cài đặt và trực quan hoá giải thuật RSA thuần Python\n\n"
            "⚠️ LƯU Ý MẬT MÃ QUAN TRỌNG:\n"
            "Chương trình cài đặt hệ mã RSA ở dạng toán học cơ bản (Textbook RSA), chưa tích hợp "
            "chuẩn đệm chống tấn công (OAEP - Optimal Asymmetric Encryption Padding) mà các hệ "
            "thống thực tế sử dụng. Vì vậy, ứng dụng chỉ phục vụ mục đích nghiên cứu và học tập."
        )

        lbl_text = tk.Label(frame_body, text=txt_info, font=FONT_NOI_DUNG,
                            justify="left", bg=MAU_NEN_CHINH, fg=MAU_CHU)
        lbl_text.pack(anchor="w", fill="both", expand=True)

        btn_dong = ttk.Button(self, text="Đóng", command=self.destroy, width=12)
        btn_dong.pack(pady=(0, 16))


# ==============================================================================
# CỬA SỔ CHÍNH ỨNG DỤNG (MAIN APPLICATION)
# ==============================================================================
class UngDungRSA(tk.Tk):
    """Lớp điều khiển chính của chương trình demo RSA."""
    def __init__(self):
        super().__init__()

        self.title("Chương trình Demo Hệ mã RSA - An toàn và bảo mật thông tin mạng (Nhóm 8)")
        self.geometry("1180x760")
        self.minsize(1050, 680)
        self.configure(bg=MAU_NEN_CHINH)

        # Quản lý trạng thái và toàn màn hình
        self.trang_thai = TrangThai()
        self.is_fullscreen = False

        # Cấu hình Theme và Style
        self._cau_hinh_styles()

        # Tạo giao diện chính
        self._tao_header()
        self._tao_notebook()
        self._tao_status_bar()

        # Đăng ký phím tắt
        self._dang_ky_phim_tat()

        # Xử lý đóng cửa sổ an toàn
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _cau_hinh_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Cấu hình màu nền chung
        style.configure(".", background=MAU_NEN_CHINH, font=FONT_NOI_DUNG, foreground=MAU_CHU)

        # Cấu hình Notebook và Tab
        style.configure("TNotebook", background=MAU_NEN_CHINH, borderwidth=0)
        style.configure("TNotebook.Tab", padding=[16, 8], font=FONT_SECTION, background="#E2E8F0")
        style.map("TNotebook.Tab",
                  background=[("selected", MAU_CHINH), ("active", "#CBD5E1")],
                  foreground=[("selected", "white"), ("active", MAU_CHU)])

        # Cấu hình LabelFrame
        style.configure("TLabelframe", background=MAU_CARD, relief="groove", borderwidth=1)
        style.configure("TLabelframe.Label", font=FONT_SECTION, foreground=MAU_CHINH, background=MAU_CARD)

        # Cấu hình Button
        style.configure("TButton", font=FONT_CHU_DAM, padding=[10, 5], background="#E2E8F0", foreground=MAU_CHU)
        style.map("TButton",
                  background=[("active", MAU_CHINH_HOVER), ("pressed", MAU_CHINH)],
                  foreground=[("active", "white"), ("pressed", "white")])

        # Cấu hình Treeview
        style.configure("Treeview", font=FONT_NOI_DUNG, rowheight=26, background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=FONT_CHU_DAM, background="#E2E8F0", foreground=MAU_CHU)
        style.map("Treeview.Heading", background=[("active", "#CBD5E1")])

    def _tao_header(self):
        frame_header = tk.Frame(self, bg=MAU_CHINH, padx=18, pady=10)
        frame_header.pack(fill="x")

        # Khối bên trái: Tiêu đề và phân nhóm
        f_left = tk.Frame(frame_header, bg=MAU_CHINH)
        f_left.pack(side="left")

        lbl_app = tk.Label(
            f_left, text="HỆ MÃ KHOÁ CÔNG KHAI RSA (RIVEST - SHAMIR - ADLEMAN)",
            font=FONT_TIEU_DE, fg="white", bg=MAU_CHINH
        )
        lbl_app.pack(anchor="w")

        lbl_sub = tk.Label(
            f_left,
            text="Học phần: An toàn và bảo mật thông tin mạng  |  Nhóm 8 - Sinh viên Thương mại điện tử",
            font=FONT_SUB_HEADER, fg="#CBD5E1", bg=MAU_CHINH
        )
        lbl_sub.pack(anchor="w")

        # Khối bên phải: Nút trợ giúp và toàn màn hình
        f_right = tk.Frame(frame_header, bg=MAU_CHINH)
        f_right.pack(side="right")

        btn_about = ttk.Button(f_right, text="ℹ Giới thiệu", command=self.mo_gioi_thieu)
        btn_about.pack(side="left", padx=4)

        btn_fs = ttk.Button(f_right, text="⛶ Toàn màn hình (F11)", command=self.toggle_fullscreen)
        btn_fs.pack(side="left", padx=4)

    def _tao_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(8, 4))

        # Khởi tạo 5 tab theo đúng trình tự demo
        self.tab1 = TabKhoaNho(self.notebook, self.trang_thai, self.set_status)
        self.tab2 = TabKhoaLon(self.notebook, self.trang_thai, self.set_status)
        self.tab3 = TabMaHoaVanBan(self.notebook, self.trang_thai, self.set_status)
        self.tab4 = TabMaHoaTep(self.notebook, self.trang_thai, self.set_status)
        self.tab5 = TabDoThoiGian(self.notebook, self.trang_thai, self.set_status)

        self.notebook.add(self.tab1, text="  1. Khoá nhỏ & Từng bước  ")
        self.notebook.add(self.tab2, text="  2. Khoá lớn (512 - 2048 bit)  ")
        self.notebook.add(self.tab3, text="  3. Mã hoá văn bản  ")
        self.notebook.add(self.tab4, text="  4. Mã hoá tệp & Ảnh  ")
        self.notebook.add(self.tab5, text="  5. Đo thời gian & Biểu đồ  ")

    def _tao_status_bar(self):
        frame_status = tk.Frame(self, bg="#E2E8F0", padx=14, pady=4)
        frame_status.pack(fill="x", side="bottom")

        self.lbl_status = tk.Label(frame_status, text="Sẵn sàng.", font=FONT_NOI_DUNG, bg="#E2E8F0", fg=MAU_CHU)
        self.lbl_status.pack(side="left")

        lbl_keys = tk.Label(
            frame_status,
            text="F11: Toàn màn hình  |  Ctrl+Tab / Phím 1-5: Chuyển tab  |  Enter: Thao tác",
            font=("Segoe UI", 9), bg="#E2E8F0", fg=MAU_CHU_PHU
        )
        lbl_keys.pack(side="right")

    def set_status(self, text):
        self.lbl_status.config(text=text)

    def mo_gioi_thieu(self):
        CuaSoGioiThieu(self)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        if not self.is_fullscreen:
            self.geometry("1180x760")

    def _dang_ky_phim_tat(self):
        self.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.bind("<Escape>", lambda e: self._exit_fullscreen())

        # Chuyển tab bằng Ctrl+Tab hoặc số 1-5 khi không gõ text
        self.bind("<Control-Tab>", self._next_tab)
        for i in range(1, 6):
            self.bind(f"<Control-Key-{i}>", lambda e, idx=i-1: self.notebook.select(idx))
            self.bind(f"<Alt-Key-{i}>", lambda e, idx=i-1: self.notebook.select(idx))

        # Phím Enter thực hiện thao tác chính của tab
        self.bind("<Return>", self._on_enter_pressed)

    def _exit_fullscreen(self):
        if self.is_fullscreen:
            self.toggle_fullscreen()

    def _next_tab(self, event=None):
        cur = self.notebook.index(self.notebook.select())
        next_tab = (cur + 1) % self.notebook.index("end")
        self.notebook.select(next_tab)

    def _on_enter_pressed(self, event):
        # Tránh trigger khi đang gõ văn bản nhiều dòng trong Text widget
        if isinstance(event.widget, tk.Text):
            return

        cur_idx = self.notebook.index(self.notebook.select())
        if cur_idx == 0:
            self.tab1.thuc_hien_tao_khoa()
        elif cur_idx == 1:
            self.tab2.bat_dau_sinh_khoa()
        elif cur_idx == 2:
            self.tab3.thuc_hien_ma_hoa()
        elif cur_idx == 3:
            self.tab4.bat_dau_ma_hoa_tep()
        elif cur_idx == 4:
            self.tab5.bat_dau_do()

    def on_closing(self):
        """Xử lý đóng cửa sổ an toàn."""
        self.destroy()


# ==============================================================================
# ĐIỂM VÀO CHÍNH CỦA CHƯƠNG TRÌNH
# ==============================================================================
def main():
    app = UngDungRSA()
    app.mainloop()


if __name__ == "__main__":
    main()
