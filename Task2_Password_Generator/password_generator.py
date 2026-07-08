"""
Random Password Generator (GUI Version)
Oasis Infobyte - Python Programming Internship
Task 2: Random Password Generator
"""

import ctypes
import sys
import random
import string
import tkinter as tk
from tkinter import messagebox

# Windows high-DPI screens par blurry/pixelated rendering fix karta hai
if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator | Oasis Infobyte")
        self.root.configure(bg="#eef2f7")
        self.root.minsize(420, 560)

        self.include_upper = tk.BooleanVar(value=True)
        self.include_lower = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)

        self.build_ui()

    def build_ui(self):
        # ---------- Header Banner ----------
        header = tk.Frame(self.root, bg="#2c3e50")
        header.pack(fill="x")

        tk.Label(
            header, text="Password Generator", font=("Segoe UI", 21, "bold"),
            bg="#2c3e50", fg="white"
        ).pack(pady=(20, 0))

        tk.Label(
            header, text="Create strong, random passwords instantly",
            font=("Segoe UI", 10), bg="#2c3e50", fg="#bdc3c7"
        ).pack(pady=(0, 20))

        # ---------- Card (simple bordered frame, no fixed pixel placement) ----------
        outer_pad = tk.Frame(self.root, bg="#eef2f7")
        outer_pad.pack(fill="both", expand=True, padx=25, pady=25)

        card = tk.Frame(
            outer_pad, bg="white", highlightbackground="#d0d7e2",
            highlightthickness=1, bd=0
        )
        card.pack(fill="both", expand=True)

        inner = tk.Frame(card, bg="white")
        inner.pack(fill="both", expand=True, padx=28, pady=26)

        # Password length
        tk.Label(
            inner, text="PASSWORD LENGTH", font=("Segoe UI", 9, "bold"),
            bg="white", fg="#7f8c8d"
        ).pack(anchor="w", pady=(0, 5))

        self.length_var = tk.IntVar(value=12)
        self.length_slider = tk.Scale(
            inner, from_=4, to=32, orient="horizontal",
            variable=self.length_var, bg="white", fg="#2c3e50",
            highlightthickness=0, troughcolor="#dcdde1",
            font=("Segoe UI", 9), showvalue=True
        )
        self.length_slider.pack(fill="x", pady=(0, 18))

        # Character options
        tk.Label(
            inner, text="INCLUDE CHARACTERS", font=("Segoe UI", 9, "bold"),
            bg="white", fg="#7f8c8d"
        ).pack(anchor="w", pady=(0, 8))

        opts_frame = tk.Frame(inner, bg="white")
        opts_frame.pack(fill="x", pady=(0, 18))

        self._make_checkbox(opts_frame, "Uppercase (A-Z)", self.include_upper)
        self._make_checkbox(opts_frame, "Lowercase (a-z)", self.include_lower)
        self._make_checkbox(opts_frame, "Digits (0-9)", self.include_digits)
        self._make_checkbox(opts_frame, "Symbols (!@#$%)", self.include_symbols)

        # Generate button
        gen_btn = tk.Button(
            inner, text="Generate Password", font=("Segoe UI", 11, "bold"),
            bg="#2980b9", fg="white", activebackground="#3498db",
            activeforeground="white", relief="flat", cursor="hand2",
            command=self.generate_password
        )
        gen_btn.pack(fill="x", ipady=10, pady=(4, 16))

        # Result area
        result_frame = tk.Frame(inner, bg="#f4f6f8")
        result_frame.pack(fill="x")

        self.password_label = tk.Label(
            result_frame, text="Your password will appear here",
            font=("Consolas", 13, "bold"), bg="#f4f6f8", fg="#95a5a6",
            wraplength=300, justify="center"
        )
        self.password_label.pack(pady=(18, 8), padx=10)

        copy_btn = tk.Button(
            result_frame, text="Copy to Clipboard", font=("Segoe UI", 9, "bold"),
            bg="#ecf0f1", fg="#2c3e50", relief="flat", cursor="hand2",
            command=self.copy_to_clipboard
        )
        copy_btn.pack(pady=(0, 16))

    def _make_checkbox(self, parent, text, variable):
        cb = tk.Checkbutton(
            parent, text=text, variable=variable, font=("Segoe UI", 10),
            bg="white", fg="#2c3e50", activebackground="white",
            selectcolor="#f4f6f8", anchor="w"
        )
        cb.pack(fill="x", pady=2)

    def generate_password(self):
        pools = ""
        if self.include_upper.get():
            pools += string.ascii_uppercase
        if self.include_lower.get():
            pools += string.ascii_lowercase
        if self.include_digits.get():
            pools += string.digits
        if self.include_symbols.get():
            pools += "!@#$%^&*()-_=+"

        if not pools:
            messagebox.showerror("No Character Type Selected", "Please select at least one character type.")
            return

        length = self.length_var.get()
        password = "".join(random.choice(pools) for _ in range(length))
        self.generated_password = password

        self.password_label.config(text=password, fg="#27ae60")

    def copy_to_clipboard(self):
        if hasattr(self, "generated_password"):
            self.root.clipboard_clear()
            self.root.clipboard_append(self.generated_password)
            self.root.update()
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("No Password", "Generate a password first.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()