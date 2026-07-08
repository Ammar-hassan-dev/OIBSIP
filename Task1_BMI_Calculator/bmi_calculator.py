"""
BMI Calculator (GUI Version)
Oasis Infobyte - Python Programming Internship
Task 1: BMI Calculator
"""

import ctypes
import sys
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


class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator | Oasis Infobyte")
        self.root.configure(bg="#eef2f7")
        self.root.minsize(400, 520)

        self.build_ui()

    def build_ui(self):
        # ---------- Header Banner ----------
        header = tk.Frame(self.root, bg="#2c3e50")
        header.pack(fill="x")

        tk.Label(
            header, text="BMI Calculator", font=("Segoe UI", 22, "bold"),
            bg="#2c3e50", fg="white"
        ).pack(pady=(20, 0))

        tk.Label(
            header, text="Check your Body Mass Index instantly",
            font=("Segoe UI", 10), bg="#2c3e50", fg="#bdc3c7"
        ).pack(pady=(0, 20))

        # ---------- Card (simple bordered frame, flexible layout) ----------
        outer_pad = tk.Frame(self.root, bg="#eef2f7")
        outer_pad.pack(fill="both", expand=True, padx=25, pady=25)

        card = tk.Frame(
            outer_pad, bg="white", highlightbackground="#d0d7e2",
            highlightthickness=1, bd=0
        )
        card.pack(fill="both", expand=True)

        inner = tk.Frame(card, bg="white")
        inner.pack(fill="both", expand=True, padx=30, pady=30)

        # Weight input
        tk.Label(
            inner, text="WEIGHT (kg)", font=("Segoe UI", 9, "bold"),
            bg="white", fg="#7f8c8d"
        ).pack(anchor="w", pady=(0, 5))

        self.weight_entry = tk.Entry(
            inner, font=("Segoe UI", 13), relief="flat",
            bg="#f4f6f8", highlightthickness=1,
            highlightbackground="#dcdde1", highlightcolor="#2980b9"
        )
        self.weight_entry.pack(fill="x", ipady=8, pady=(0, 18))

        # Height input
        tk.Label(
            inner, text="HEIGHT (m)", font=("Segoe UI", 9, "bold"),
            bg="white", fg="#7f8c8d"
        ).pack(anchor="w", pady=(0, 5))

        self.height_entry = tk.Entry(
            inner, font=("Segoe UI", 13), relief="flat",
            bg="#f4f6f8", highlightthickness=1,
            highlightbackground="#dcdde1", highlightcolor="#2980b9"
        )
        self.height_entry.pack(fill="x", ipady=8, pady=(0, 20))

        # Buttons row
        btn_row = tk.Frame(inner, bg="white")
        btn_row.pack(fill="x", pady=(0, 20))

        calc_btn = tk.Button(
            btn_row, text="Calculate BMI", font=("Segoe UI", 11, "bold"),
            bg="#2980b9", fg="white", activebackground="#3498db",
            activeforeground="white", relief="flat", cursor="hand2",
            command=self.calculate_bmi
        )
        calc_btn.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))

        reset_btn = tk.Button(
            btn_row, text="Reset", font=("Segoe UI", 11, "bold"),
            bg="#ecf0f1", fg="#2c3e50", activebackground="#dcdde1",
            relief="flat", cursor="hand2", command=self.reset_fields
        )
        reset_btn.pack(side="left", ipady=10, padx=(8, 0))

        # Result badge area
        result_frame = tk.Frame(inner, bg="#f4f6f8")
        result_frame.pack(fill="x")

        self.bmi_value_label = tk.Label(
            result_frame, text="--", font=("Segoe UI", 26, "bold"),
            bg="#f4f6f8", fg="#2c3e50"
        )
        self.bmi_value_label.pack(pady=(15, 0))

        self.category_label = tk.Label(
            result_frame, text="Enter your details above",
            font=("Segoe UI", 11, "bold"), bg="#f4f6f8", fg="#95a5a6"
        )
        self.category_label.pack(pady=(0, 15))

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

            if weight <= 0 or height <= 0:
                messagebox.showerror("Invalid Input", "Weight and height must be positive numbers.")
                return

            bmi = round(weight / (height ** 2), 1)

            if bmi < 18.5:
                category, color = "Underweight", "#3498db"
            elif bmi < 25:
                category, color = "Normal Weight", "#27ae60"
            elif bmi < 30:
                category, color = "Overweight", "#f39c12"
            else:
                category, color = "Obese", "#e74c3c"

            self.bmi_value_label.config(text=str(bmi), fg=color)
            self.category_label.config(text=category.upper(), fg=color)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for weight and height.")

    def reset_fields(self):
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.bmi_value_label.config(text="--", fg="#2c3e50")
        self.category_label.config(text="Enter your details above", fg="#95a5a6")


if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()