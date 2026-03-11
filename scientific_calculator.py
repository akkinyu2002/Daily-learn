"""
Scientific Calculator — Modern Dark-Theme GUI
Built with tkinter • Supports trig, inverse-trig, hyperbolic, log, power,
factorial, constants, memory, RAD/DEG toggle, keyboard input & more.
"""

import tkinter as tk
from tkinter import font as tkfont
import math


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("🔬 Scientific Calculator")
        self.root.configure(bg="#0d1117")
        self.root.resizable(False, False)

        # ── State ────────────────────────────────────
        self.expression = ""
        self.history = ""
        self.memory = 0
        self.ans = 0
        self.inverse_mode = False
        self.radian_mode = True

        # ── Fonts ────────────────────────────────────
        self.display_font = tkfont.Font(family="Segoe UI", size=30, weight="bold")
        self.history_font = tkfont.Font(family="Segoe UI", size=11)
        self.btn_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.btn_font_sm = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.mode_font = tkfont.Font(family="Segoe UI", size=9, weight="bold")

        # ── Colour palette ───────────────────────────
        self.C = {
            "bg":         "#0d1117",
            "disp_bg":    "#161b22",
            "disp_fg":    "#e6edf3",
            "hist_fg":    "#8b949e",
            "num_bg":     "#21262d",
            "num_fg":     "#e6edf3",
            "num_hv":     "#30363d",
            "op_bg":      "#da3633",
            "op_fg":      "#ffffff",
            "op_hv":      "#f85149",
            "fn_bg":      "#0d419d",
            "fn_fg":      "#79c0ff",
            "fn_hv":      "#1158c7",
            "sp_bg":      "#6e40c9",
            "sp_fg":      "#d2a8ff",
            "sp_hv":      "#8957e5",
            "eq_bg":      "#238636",
            "eq_fg":      "#ffffff",
            "eq_hv":      "#2ea043",
            "cl_bg":      "#b62324",
            "cl_fg":      "#ffffff",
            "cl_hv":      "#da3633",
            "accent":     "#58a6ff",
            "dim":        "#484f58",
        }


# ═══════════════════════ MAIN ═══════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    w, h = 440, 680
    root.geometry(f"{w}x{h}")
    root.update_idletasks()
    x = (root.winfo_screenwidth()  - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"+{x}+{y}")

    ScientificCalculator(root)
    root.mainloop()
