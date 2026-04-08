"""
File Cleanup Utility
====================
Finds files unused for more than 5 months (corrupted, empty, or just stale)
and lets the user review them before deleting. Safe, interactive, and easy to use.
"""

import os
import sys
import time
import stat
import struct
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta
from pathlib import Path
import send2trash

# ── Constants ──────────────────────────────────────────────────────────────────
MONTHS_THRESHOLD = 5
DAYS_THRESHOLD   = MONTHS_THRESHOLD * 30

# Known "always useless" extensions
JUNK_EXTENSIONS = {
    ".tmp", ".temp", ".log", ".bak", ".old", ".chk", ".dmp", ".dump",
    ".~", ".swp", ".swo", ".DS_Store", ".Thumbs.db", ".thumbdata",
    ".crdownload", ".part", ".partial", ".cache",
}

# Signatures for basic corruption detection (magic bytes)
KNOWN_SIGNATURES: dict[str, bytes] = {
    ".jpg":  b"\xff\xd8\xff",
    ".jpeg": b"\xff\xd8\xff",
    ".png":  b"\x89PNG",
    ".pdf":  b"%PDF",
    ".zip":  b"PK\x03\x04",
    ".gif":  b"GIF8",
    ".bmp":  b"BM",
    ".mp3":  b"ID3",
    ".mp4":  b"\x00\x00\x00",
    ".docx": b"PK\x03\x04",
    ".xlsx": b"PK\x03\x04",
    ".pptx": b"PK\x03\x04",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def file_age_days(path: Path) -> float:
    """Return the number of days since the file was last accessed or modified."""
    try:
        st = path.stat()
        last_used = max(st.st_atime, st.st_mtime)
        return (time.time() - last_used) / 86400
    except Exception:
        return 0.0


def is_empty(path: Path) -> bool:
    try:
        return path.stat().st_size == 0
    except Exception:
        return False


def is_corrupted(path: Path) -> bool:
    """Heuristic corruption check: verifies magic bytes for known types.

    Reads up to 1024 bytes and searches for the signature anywhere within
    that region, because some formats (e.g. PDF) allow the magic header to
    appear after a BOM or other prefix rather than strictly at byte 0.
    """
    ext = path.suffix.lower()
    if ext not in KNOWN_SIGNATURES:
        return False
    expected = KNOWN_SIGNATURES[ext]
    try:
        with open(path, "rb") as f:
            header = f.read(1024)
        return expected not in header
    except (PermissionError, OSError):
        return False


def is_junk(path: Path) -> bool:
    return path.suffix.lower() in JUNK_EXTENSIONS


def human_size(size_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def human_age(days: float) -> str:
    if days < 1:
        return "< 1 day"
    months = int(days // 30)
    rem_days = int(days % 30)
    if months:
        return f"{months}mo {rem_days}d"
    return f"{int(days)}d"


# ── Main App ──────────────────────────────────────────────────────────────────

class FileCleanerApp(tk.Tk):
    # colour palette (dark-mode)
    BG        = "#1e1e2e"
    PANEL     = "#2a2a3e"
    ACCENT    = "#7c3aed"
    ACCENT2   = "#06b6d4"
    DANGER    = "#ef4444"
    WARNING   = "#f59e0b"
    SUCCESS   = "#22c55e"
    TXT       = "#e2e8f0"
    TXT_DIM   = "#94a3b8"
    BORDER    = "#374151"

    def __init__(self):
        super().__init__()
        self.title("🧹 File Cleanup Utility")
        self.geometry("1080x720")
        self.minsize(800, 560)
        self.configure(bg=self.BG)
        self.resizable(True, True)

        self.scan_dir     = tk.StringVar()
        self.status_text  = tk.StringVar(value="Choose a folder and click Scan.")
        self.results: list[dict] = []
        self._scan_thread = None
        self._stop_scan   = False
        self._selected_items: set[str] = set()

        self._build_styles()
        self._build_ui()

    # ── Styles ─────────────────────────────────────────────────────────────

    def _build_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("Treeview",
                     background=self.PANEL, fieldbackground=self.PANEL,
                     foreground=self.TXT, rowheight=28, borderwidth=0,
                     font=("Segoe UI", 10))
        s.configure("Treeview.Heading",
                     background=self.ACCENT, foreground="white",
                     font=("Segoe UI Semibold", 10), relief="flat")
        s.map("Treeview",
              background=[("selected", self.ACCENT)],
              foreground=[("selected", "white")])
        s.configure("Vertical.TScrollbar",
                     troughcolor=self.PANEL, background=self.ACCENT,
                     borderwidth=0, arrowsize=14)
        s.configure("Accent.TButton",
                     background=self.ACCENT, foreground="white",
                     font=("Segoe UI Semibold", 10), padding=8, relief="flat")
        s.map("Accent.TButton",
              background=[("active", "#6d28d9"), ("disabled", "#4b5563")])
        s.configure("Danger.TButton",
                     background=self.DANGER, foreground="white",
                     font=("Segoe UI Semibold", 10), padding=8, relief="flat")
        s.map("Danger.TButton",
              background=[("active", "#b91c1c"), ("disabled", "#4b5563")])
        s.configure("TProgressbar",
                     troughcolor=self.PANEL, background=self.ACCENT2,
                     thickness=6)

    # ── UI ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Top bar ────────────────────────────────────────────────────────
        top = tk.Frame(self, bg=self.BG, pady=12, padx=16)
        top.pack(fill="x")
        tk.Label(top, text="🧹 File Cleanup Utility", bg=self.BG,
                 fg=self.TXT, font=("Segoe UI Semibold", 18)).pack(side="left")
        tk.Label(top, text=f"Flags files unused >{MONTHS_THRESHOLD} months",
                 bg=self.BG, fg=self.TXT_DIM,
                 font=("Segoe UI", 10)).pack(side="left", padx=12)

        # ── Folder bar ─────────────────────────────────────────────────────
        bar = tk.Frame(self, bg=self.PANEL, padx=12, pady=10)
        bar.pack(fill="x", padx=16, pady=(0, 8))
        tk.Label(bar, text="Scan folder:", bg=self.PANEL, fg=self.TXT,
                 font=("Segoe UI", 10)).pack(side="left")
        entry = tk.Entry(bar, textvariable=self.scan_dir,
                         bg=self.BG, fg=self.TXT, insertbackground=self.TXT,
                         relief="flat", font=("Segoe UI", 10), width=60)
        entry.pack(side="left", padx=8, ipady=4)
        ttk.Button(bar, text="Browse…", style="Accent.TButton",
                   command=self._browse).pack(side="left")
        self.btn_scan = ttk.Button(bar, text="⚡ Scan", style="Accent.TButton",
                                   command=self._start_scan)
        self.btn_scan.pack(side="left", padx=6)

        # ── Filter row ─────────────────────────────────────────────────────
        frow = tk.Frame(self, bg=self.BG, padx=16)
        frow.pack(fill="x", pady=(0, 4))
        self.chk_all_old   = self._chkvar()
        self.chk_empty     = self._chkvar(True)
        self.chk_corrupted = self._chkvar(True)
        self.chk_junk      = self._chkvar(True)
        for text, var in [
            (f"Old (>{MONTHS_THRESHOLD} mo)", self.chk_all_old),
            ("Empty files",                    self.chk_empty),
            ("Corrupted files",                self.chk_corrupted),
            ("Junk extensions",                self.chk_junk),
        ]:
            tk.Checkbutton(frow, text=text, variable=var,
                           bg=self.BG, fg=self.TXT, activebackground=self.BG,
                           activeforeground=self.TXT, selectcolor=self.ACCENT,
                           font=("Segoe UI", 10)).pack(side="left", padx=8)

        # ── Progress bar ───────────────────────────────────────────────────
        self.progress = ttk.Progressbar(self, style="TProgressbar",
                                        mode="indeterminate")
        self.progress.pack(fill="x", padx=16, pady=(0, 4))

        # ── Treeview ───────────────────────────────────────────────────────
        frame = tk.Frame(self, bg=self.BG, padx=16)
        frame.pack(fill="both", expand=True)
        cols = ("select", "name", "path", "type", "size", "last_used", "age")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings",
                                  selectmode="extended")
        headings = {
            "select":    ("☑",         45,  "center"),
            "name":      ("File Name", 200, "w"),
            "path":      ("Path",      260, "w"),
            "type":      ("Issue",      95, "center"),
            "size":      ("Size",       75, "center"),
            "last_used": ("Last Used", 130, "center"),
            "age":       ("Age",        85, "center"),
        }
        for col, (title, width, anchor) in headings.items():
            self.tree.heading(col, text=title,
                              command=lambda c=col: self._sort_by(c))
            self.tree.column(col, width=width, anchor=anchor, stretch=(col == "path"))
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview,
                             style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.tree.tag_configure("empty",     foreground="#60a5fa")
        self.tree.tag_configure("corrupted", foreground=self.DANGER)
        self.tree.tag_configure("junk",      foreground=self.WARNING)
        self.tree.tag_configure("old",       foreground=self.TXT_DIM)
        self.tree.tag_configure("checked",   background="#2d2d44")
        self.tree.bind("<Button-1>", self._on_click)

        # ── Bottom bar ─────────────────────────────────────────────────────
        bot = tk.Frame(self, bg=self.PANEL, padx=16, pady=10)
        bot.pack(fill="x")
        self.lbl_status = tk.Label(bot, textvariable=self.status_text,
                                   bg=self.PANEL, fg=self.TXT_DIM,
                                   font=("Segoe UI", 10))
        self.lbl_status.pack(side="left")
        self.btn_delete = ttk.Button(bot, text="🗑  Move to Recycle Bin",
                                      style="Danger.TButton",
                                      command=self._confirm_delete,
                                      state="disabled")
        self.btn_delete.pack(side="right", padx=4)
        ttk.Button(bot, text="Select All",   style="Accent.TButton",
                   command=self._select_all).pack(side="right", padx=4)
        ttk.Button(bot, text="Deselect All", style="Accent.TButton",
                   command=self._deselect_all).pack(side="right", padx=4)
        self.lbl_selected = tk.Label(bot, text="0 selected",
                                     bg=self.PANEL, fg=self.ACCENT2,
                                     font=("Segoe UI Semibold", 10))
        self.lbl_selected.pack(side="right", padx=12)

    # ── Helpers ────────────────────────────────────────────────────────────

    def _chkvar(self, default=False):
        return tk.BooleanVar(value=default)

    def _browse(self):
        d = filedialog.askdirectory(title="Select folder to scan")
        if d:
            self.scan_dir.set(d)

    # ── Scan ───────────────────────────────────────────────────────────────

    def _start_scan(self):
        folder = self.scan_dir.get().strip()
        if not folder:
            messagebox.showwarning("No Folder", "Please choose a folder to scan.")
            return
        if not os.path.isdir(folder):
            messagebox.showerror("Invalid Folder", f"'{folder}' is not a valid directory.")
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.results.clear()
        self._selected_items.clear()
        self._update_selected_label()
        self.btn_delete.configure(state="disabled")
        self._stop_scan = False
        self.btn_scan.configure(state="disabled")
        self.progress.start(12)
        self.status_text.set("Scanning… please wait")
        self._scan_thread = threading.Thread(target=self._scan_worker,
                                              args=(folder,), daemon=True)
        self._scan_thread.start()

    def _scan_worker(self, folder: str):
        found = []
        cutoff_days = DAYS_THRESHOLD
        want_old        = self.chk_all_old.get()
        want_empty      = self.chk_empty.get()
        want_corrupted  = self.chk_corrupted.get()
        want_junk       = self.chk_junk.get()

        for root, dirs, files in os.walk(folder):
            if self._stop_scan:
                break
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for fname in files:
                if self._stop_scan:
                    break
                path = Path(root) / fname
                try:
                    age  = file_age_days(path)
                    size = path.stat().st_size
                except Exception:
                    continue
                reasons = []
                if want_empty and     is_empty(path):     reasons.append("empty")
                if want_corrupted and is_corrupted(path): reasons.append("corrupted")
                if want_junk and      is_junk(path):      reasons.append("junk")
                if want_old and       age >= cutoff_days: reasons.append("old")
                if not reasons:
                    continue
                last_used = datetime.fromtimestamp(
                    max(path.stat().st_atime, path.stat().st_mtime)
                ).strftime("%Y-%m-%d")
                found.append({
                    "name":      fname,
                    "path":      str(path.parent),
                    "full_path": str(path),
                    "type":      ", ".join(reasons),
                    "size":      size,
                    "last_used": last_used,
                    "age":       age,
                })
        self.results = found
        self.after(0, self._scan_done)

    def _scan_done(self):
        self.progress.stop()
        self.btn_scan.configure(state="normal")
        if not self.results:
            self.status_text.set("✅ No flagged files found. Your folder looks clean!")
            return
        for i, rec in enumerate(self.results):
            tag = rec["type"].split(",")[0].strip()
            self.tree.insert("", "end", iid=str(i), tags=(tag,), values=(
                "☐",
                rec["name"],
                rec["path"],
                rec["type"],
                human_size(rec["size"]),
                rec["last_used"],
                human_age(rec["age"]),
            ))
        total_size = sum(r["size"] for r in self.results)
        self.status_text.set(
            f"Found {len(self.results)} file(s) | {human_size(total_size)} total "
            f"| Review below, then delete selected"
        )

    # ── Selection ──────────────────────────────────────────────────────────

    def _on_click(self, event):
        iid = self.tree.identify_row(event.y)
        if not iid:
            return
        if iid in self._selected_items:
            self._selected_items.discard(iid)
            self.tree.set(iid, "select", "☐")
            tags = [t for t in self.tree.item(iid, "tags") if t != "checked"]
        else:
            self._selected_items.add(iid)
            self.tree.set(iid, "select", "☑")
            tags = list(self.tree.item(iid, "tags")) + ["checked"]
        self.tree.item(iid, tags=tags)
        self._update_selected_label()

    def _select_all(self):
        for iid in self.tree.get_children():
            self._selected_items.add(iid)
            self.tree.set(iid, "select", "☑")
            tags = list(self.tree.item(iid, "tags"))
            if "checked" not in tags:
                tags.append("checked")
            self.tree.item(iid, tags=tags)
        self._update_selected_label()

    def _deselect_all(self):
        for iid in self.tree.get_children():
            self._selected_items.discard(iid)
            self.tree.set(iid, "select", "☐")
            tags = [t for t in self.tree.item(iid, "tags") if t != "checked"]
            self.tree.item(iid, tags=tags)
        self._update_selected_label()

    def _update_selected_label(self):
        n = len(self._selected_items)
        self.lbl_selected.config(text=f"{n} selected")
        self.btn_delete.configure(state="normal" if n > 0 else "disabled")

    # ── Sort ───────────────────────────────────────────────────────────────

    def _sort_by(self, col):
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children()]
        try:
            items.sort(key=lambda t: float(t[0].split()[0])
                       if t[0].replace(".", "").split()[0].isdigit() else t[0])
        except Exception:
            items.sort()
        for index, (_, k) in enumerate(items):
            self.tree.move(k, "", index)

    # ── Delete ─────────────────────────────────────────────────────────────

    def _confirm_delete(self):
        selected_iids = list(self._selected_items)
        if not selected_iids:
            return
        selected_files = [self.results[int(i)] for i in selected_iids]
        total_size = sum(f["size"] for f in selected_files)
        preview_lines = [f"  • {f['name']}  ({f['type']}, {human_size(f['size'])})"
                         for f in selected_files[:15]]
        if len(selected_files) > 15:
            preview_lines.append(f"  … and {len(selected_files) - 15} more file(s)")
        msg = (
            f"🗑  Move {len(selected_files)} file(s) "
            f"({human_size(total_size)}) to the Recycle Bin?\n\n"
            f"{chr(10).join(preview_lines)}\n\n"
            f"You can restore them from the Recycle Bin if needed."
        )
        confirmed = messagebox.askyesno(
            "Move to Recycle Bin", msg, icon="warning", default="no"
        )
        if not confirmed:
            self.status_text.set("Deletion cancelled — no files were removed.")
            return
        self._delete_files(selected_files, selected_iids)

    def _delete_files(self, files: list[dict], iids: list[str]):
        moved, failed = 0, []
        for rec, iid in zip(files, iids):
            try:
                p = Path(rec["full_path"])
                if p.exists():
                    send2trash.send2trash(str(p))
                    self.tree.delete(iid)
                    self._selected_items.discard(iid)
                    moved += 1
            except Exception as e:
                failed.append(f"{rec['name']}: {e}")
        self._update_selected_label()
        remaining = len(self.tree.get_children())
        self.status_text.set(
            f"♻️  Moved {moved} file(s) to Recycle Bin. "
            + (f"❌ {len(failed)} failed." if failed else "")
            + f"  {remaining} item(s) remaining."
        )
        if failed:
            messagebox.showerror(
                "Some Files Could Not Be Moved",
                "Could not move to Recycle Bin:\n\n" + "\n".join(failed[:20])
            )


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = FileCleanerApp()
    app.mainloop()
