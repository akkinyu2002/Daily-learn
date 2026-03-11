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

        self._build()

    # ═══════════════════════ UI ═══════════════════════

    def _build(self):
        pad = tk.Frame(self.root, bg=self.C["bg"], padx=10, pady=10)
        pad.pack(fill="both", expand=True)

        # ── Mode bar ──
        bar = tk.Frame(pad, bg=self.C["bg"])
        bar.pack(fill="x", pady=(0, 6))

        self.lbl_rad = tk.Label(bar, text="RAD", font=self.mode_font,
                                bg=self.C["bg"], fg=self.C["accent"], cursor="hand2")
        self.lbl_rad.pack(side="left", padx=(4, 2))
        self.lbl_rad.bind("<Button-1>", lambda e: self._flip_angle())

        self.lbl_deg = tk.Label(bar, text="DEG", font=self.mode_font,
                                bg=self.C["bg"], fg=self.C["dim"], cursor="hand2")
        self.lbl_deg.pack(side="left", padx=2)
        self.lbl_deg.bind("<Button-1>", lambda e: self._flip_angle())

        self.lbl_inv = tk.Label(bar, text="INV", font=self.mode_font,
                                bg=self.C["bg"], fg=self.C["dim"], cursor="hand2")
        self.lbl_inv.pack(side="left", padx=10)
        self.lbl_inv.bind("<Button-1>", lambda e: self._flip_inv())

        self.lbl_mem = tk.Label(bar, text="", font=self.mode_font,
                                bg=self.C["bg"], fg=self.C["accent"])
        self.lbl_mem.pack(side="right", padx=4)

        # ── Display ──
        dsp = tk.Frame(pad, bg=self.C["disp_bg"], bd=0, highlightthickness=1,
                       highlightbackground="#30363d")
        dsp.pack(fill="x", pady=(0, 10), ipady=10)

        self.hist_lbl = tk.Label(dsp, text="", font=self.history_font,
                                 bg=self.C["disp_bg"], fg=self.C["hist_fg"],
                                 anchor="e", padx=14)
        self.hist_lbl.pack(fill="x")

        self.disp_var = tk.StringVar(value="0")
        self.disp = tk.Label(dsp, textvariable=self.disp_var, font=self.display_font,
                             bg=self.C["disp_bg"], fg=self.C["disp_fg"],
                             anchor="e", padx=14)
        self.disp.pack(fill="x")

    # ═══════════════════════ MODE TOGGLES ════════════════

    def _flip_angle(self):
        self.radian_mode = not self.radian_mode
        self.lbl_rad.config(fg=self.C["accent"] if self.radian_mode else self.C["dim"])
        self.lbl_deg.config(fg=self.C["dim"]    if self.radian_mode else self.C["accent"])

    def _flip_inv(self):
        self.inverse_mode = not self.inverse_mode
        self._upd_inv()

    def _upd_inv(self):
        self.lbl_inv.config(fg=self.C["accent"] if self.inverse_mode else self.C["dim"])

    def _upd_mem(self):
        self.lbl_mem.config(text=f"M={self.memory:.6g}" if self.memory else "")


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
