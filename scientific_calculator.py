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
        self._bind_keys()

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

        # ── Button grid ──
        grid = tk.Frame(pad, bg=self.C["bg"])
        grid.pack(fill="both", expand=True)

        # Layout: (label, colspan, category)
        layout = [
            # Row 0 — trig / log
            [("sin",1,"fn"),("cos",1,"fn"),("tan",1,"fn"),("log",1,"fn"),("ln",1,"fn"),("π",1,"sp")],
            # Row 1 — power / roots
            [("x²",1,"fn"),("xʸ",1,"fn"),("√",1,"fn"),("n!",1,"fn"),("e",1,"sp"),("(",1,"sp")],
            # Row 2 — hyper / memory
            [("sinh",1,"fn"),("cosh",1,"fn"),("tanh",1,"fn"),("M+",1,"fn"),("MR",1,"fn"),(")",1,"sp")],
            # Row 3 — clear row
            [("C",1,"cl"),("CE",1,"cl"),("⌫",1,"fn"),("%",1,"op"),("±",1,"fn"),("÷",1,"op")],
            # Row 4
            [("7",1,"num"),("8",1,"num"),("9",1,"num"),("×",1,"op"),("EXP",1,"fn"),("mod",1,"op")],
            # Row 5
            [("4",1,"num"),("5",1,"num"),("6",1,"num"),("−",1,"op"),("⌊x⌋",1,"fn"),("⌈x⌉",1,"fn")],
            # Row 6
            [("1",1,"num"),("2",1,"num"),("3",1,"num"),("+",1,"op"),("|x|",1,"fn"),("1/x",1,"fn")],
            # Row 7
            [("0",2,"num"),(".",1,"num"),("=",2,"eq"),("Ans",1,"sp")],
        ]

        cat_style = {
            "num": (self.C["num_bg"], self.C["num_fg"], self.C["num_hv"], self.btn_font),
            "op":  (self.C["op_bg"],  self.C["op_fg"],  self.C["op_hv"],  self.btn_font),
            "fn":  (self.C["fn_bg"],  self.C["fn_fg"],  self.C["fn_hv"],  self.btn_font_sm),
            "sp":  (self.C["sp_bg"],  self.C["sp_fg"],  self.C["sp_hv"],  self.btn_font_sm),
            "eq":  (self.C["eq_bg"],  self.C["eq_fg"],  self.C["eq_hv"],  self.btn_font),
            "cl":  (self.C["cl_bg"],  self.C["cl_fg"],  self.C["cl_hv"],  self.btn_font_sm),
        }

        for r, row in enumerate(layout):
            c = 0
            for (txt, span, cat) in row:
                bg, fg, hv, fnt = cat_style[cat]
                lbl = tk.Label(grid, text=txt, font=fnt, bg=bg, fg=fg,
                               cursor="hand2", relief="flat", bd=0,
                               padx=2, pady=12)
                lbl.grid(row=r, column=c, columnspan=span,
                         sticky="nsew", padx=2, pady=2, ipadx=2, ipady=2)
                lbl.bind("<Enter>", lambda e, b=lbl, h=hv: b.config(bg=h))
                lbl.bind("<Leave>", lambda e, b=lbl, o=bg: b.config(bg=o))
                lbl.bind("<Button-1>", lambda e, t=txt: self._click(t))
                c += span

        for c in range(6):
            grid.columnconfigure(c, weight=1, uniform="b")
        for r in range(len(layout)):
            grid.rowconfigure(r, weight=1)

    # ═══════════════════════ KEYBOARD ════════════════════

    def _bind_keys(self):
        self.root.bind("<Key>", self._key)
        self.root.bind("<Return>", lambda e: self._click("="))
        self.root.bind("<KP_Enter>", lambda e: self._click("="))
        self.root.bind("<BackSpace>", lambda e: self._click("⌫"))
        self.root.bind("<Escape>", lambda e: self._click("C"))
        self.root.bind("<Delete>", lambda e: self._click("CE"))

    def _key(self, ev):
        k = ev.char
        if k in "0123456789.()":
            self._click(k)
        elif k == "+": self._click("+")
        elif k == "-": self._click("−")
        elif k == "*": self._click("×")
        elif k == "/": self._click("÷")
        elif k == "%": self._click("%")
        elif k == "^": self._click("xʸ")

    # ═══════════════════════ CLICK DISPATCH ══════════════

    def _click(self, t):
        # ── Digits / dot ──
        if t in "0123456789.":
            self.expression = t if (self.expression == "0" and t != ".") else self.expression + t
            return self._refresh()

        # ── Parens ──
        if t in ("(", ")"):
            self.expression += t
            return self._refresh()

        # ── Operators ──
        ops = {"+":"+", "−":"-", "×":"*", "÷":"/", "%":"%", "mod":"%"}
        if t in ops:
            self.expression += ops[t]
            return self._refresh()

        # ── Power ──
        if t == "xʸ":
            self.expression += "**"
            return self._refresh()
        if t == "x²":
            self.expression += "**2"
            return self._refresh()

        # ── Constants ──
        if t == "π":
            self.expression += str(math.pi)
            return self._refresh()
        if t == "e":
            self.expression += str(math.e)
            return self._refresh()
        if t == "Ans":
            self.expression += str(self.ans)
            return self._refresh()

        # ── Functions ──
        fmap = {
            "sin":"sin","cos":"cos","tan":"tan",
            "sinh":"sinh","cosh":"cosh","tanh":"tanh",
            "log":"log10","ln":"log","√":"sqrt",
            "n!":"factorial","|x|":"fabs","EXP":"exp",
        }
        inv_map = {"sin":"asin","cos":"acos","tan":"atan",
                   "sinh":"asinh","cosh":"acosh","tanh":"atanh"}

        if t in fmap:
            fn = inv_map[t] if (self.inverse_mode and t in inv_map) else fmap[t]
            self.expression += f"__{fn}__("
            self.inverse_mode = False
            self._upd_inv()
            return self._refresh()

        if t == "⌊x⌋":
            self.expression += "__floor__("
            return self._refresh()
        if t == "⌈x⌉":
            self.expression += "__ceil__("
            return self._refresh()
        if t == "1/x":
            self.expression += "1/("
            return self._refresh()

        # ── Negate ──
        if t == "±":
            e = self.expression
            if e.startswith("-") and e[1:].replace(".","").isdigit():
                self.expression = e[1:]
            elif e:
                self.expression = f"-({e})"
            else:
                self.expression = "-"
            return self._refresh()

        # ── Clear ──
        if t == "C":
            self.expression = self.history = ""
            self.hist_lbl.config(text="")
            return self._refresh()
        if t == "CE":
            self.expression = ""
            return self._refresh()

        # ── Backspace ──
        if t == "⌫":
            tokens = [
                "__asin__(","__acos__(","__atan__(",
                "__asinh__(","__acosh__(","__atanh__(",
                "__sin__(","__cos__(","__tan__(",
                "__sinh__(","__cosh__(","__tanh__(",
                "__log10__(","__log__(","__sqrt__(",
                "__factorial__(","__fabs__(","__exp__(",
                "__floor__(","__ceil__(",
            ]
            for tok in tokens:
                if self.expression.endswith(tok):
                    self.expression = self.expression[:-len(tok)]
                    return self._refresh()
            self.expression = self.expression[:-1]
            return self._refresh()

        # ── Memory ──
        if t == "M+":
            try:
                self.memory += self._eval(self.expression)
                self._upd_mem()
            except Exception:
                pass
            return
        if t == "MR":
            self.expression += str(self.memory)
            return self._refresh()
        if t == "MC":
            self.memory = 0
            self._upd_mem()
            return

        # ── Equals ──
        if t == "=":
            return self._calc()

    # ═══════════════════════ EVALUATION ══════════════════

    def _calc(self):
        if not self.expression:
            return
        try:
            result = self._eval(self.expression)
            self.history = self._pretty(self.expression) + " ="
            self.hist_lbl.config(text=self.history)
            self.ans = result

            if isinstance(result, float):
                if result == int(result) and abs(result) < 1e15:
                    rs = str(int(result))
                elif abs(result) > 1e15 or (abs(result) < 1e-6 and result != 0):
                    rs = f"{result:.8e}"
                else:
                    rs = f"{result:.10g}"
            else:
                rs = str(result)

            self.expression = rs
            self._refresh()
        except ZeroDivisionError:
            self._error("Cannot divide by zero")
        except ValueError as ve:
            self._error(f"Math error")
        except OverflowError:
            self._error("Overflow")
        except Exception:
            self._error("Syntax error")

    def _eval(self, expr):
        # Auto-close parens
        diff = expr.count("(") - expr.count(")")
        if diff > 0:
            expr += ")" * diff

        deg = not self.radian_mode
        ns = {"__builtins__": {}}

        if deg:
            ns["_sin"]  = lambda x: math.sin(math.radians(x))
            ns["_cos"]  = lambda x: math.cos(math.radians(x))
            ns["_tan"]  = lambda x: math.tan(math.radians(x))
            ns["_asin"] = lambda x: math.degrees(math.asin(x))
            ns["_acos"] = lambda x: math.degrees(math.acos(x))
            ns["_atan"] = lambda x: math.degrees(math.atan(x))
        else:
            ns["_sin"]  = math.sin
            ns["_cos"]  = math.cos
            ns["_tan"]  = math.tan
            ns["_asin"] = math.asin
            ns["_acos"] = math.acos
            ns["_atan"] = math.atan

        ns["_sinh"]      = math.sinh
        ns["_cosh"]      = math.cosh
        ns["_tanh"]      = math.tanh
        ns["_asinh"]     = math.asinh
        ns["_acosh"]     = math.acosh
        ns["_atanh"]     = math.atanh
        ns["_log10"]     = math.log10
        ns["_log"]       = math.log
        ns["_sqrt"]      = math.sqrt
        ns["_factorial"] = math.factorial
        ns["_fabs"]      = math.fabs
        ns["_exp"]       = math.exp
        ns["_floor"]     = math.floor
        ns["_ceil"]      = math.ceil

        proc = expr
        for tok in ["sin","cos","tan","asin","acos","atan",
                     "sinh","cosh","tanh","asinh","acosh","atanh",
                     "log10","log","sqrt","factorial","fabs",
                     "exp","floor","ceil"]:
            proc = proc.replace(f"__{tok}__", f"_{tok}")
        return eval(proc, ns)

    # ═══════════════════════ DISPLAY HELPERS ═════════════

    def _pretty(self, e):
        swaps = [
            ("__sin__(","sin("),("__cos__(","cos("),("__tan__(","tan("),
            ("__asin__(","sin⁻¹("),("__acos__(","cos⁻¹("),("__atan__(","tan⁻¹("),
            ("__sinh__(","sinh("),("__cosh__(","cosh("),("__tanh__(","tanh("),
            ("__asinh__(","sinh⁻¹("),("__acosh__(","cosh⁻¹("),("__atanh__(","tanh⁻¹("),
            ("__log10__(","log("),("__log__(","ln("),
            ("__sqrt__(","√("),("__factorial__(","fact("),
            ("__fabs__(","|"),("__exp__(","exp("),
            ("__floor__(","⌊"),("__ceil__(","⌈"),
            ("**","^"),("*","×"),("/","÷"),
        ]
        for old, new in swaps:
            e = e.replace(old, new)
        return e

    def _refresh(self):
        txt = self._pretty(self.expression) if self.expression else "0"
        self.disp_var.set(txt)
        # Auto-scale font
        n = len(txt)
        if n > 24:
            self.disp.config(font=tkfont.Font(family="Segoe UI", size=16, weight="bold"))
        elif n > 16:
            self.disp.config(font=tkfont.Font(family="Segoe UI", size=22, weight="bold"))
        else:
            self.disp.config(font=self.display_font)

    def _error(self, msg):
        self.disp_var.set(msg)
        self.disp.config(fg="#f85149")
        self.expression = ""
        self.root.after(1800, lambda: self.disp.config(fg=self.C["disp_fg"]))
        self.root.after(1800, self._refresh)

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
