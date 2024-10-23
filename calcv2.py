import sys
from tkinter import *
import tkinter as tk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        root.title("Calculator basic")  # ウィンドウのタイトルを設定
        root.geometry("300x400")  # ウィンドウのサイズを設定
        # ウィジェットの配置などをここに追加
        self.expression = ""

        self.display = tk.Entry(root, font=("Arial", 20), bd=10, insertwidth=2, width=14, borderwidth=4)
        self.display.grid(row=0, column=0, columnspan=4)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', 'C', '=', '+'
        ]

        row_val = 1
        col_val = 0
        for button in buttons:
            def action(x=button): return self.click_event(x)
            tk.Button(root, text=button, padx=20, pady=20, font=("Arial", 18),
                      command=action).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def click_event(self, key):
        if key == "=":
            try:
                result = str(eval(self.expression))
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, result)
                self.expression = result
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "エラー")
                self.expression = ""
        elif key == "C":
            self.display.delete(0, tk.END)
            self.expression = ""
        else:
            self.expression += str(key)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)


def scientific_calculator():
    print("Select operation:")
    print("1. Sine")
    print("2. Cosine")
    print("3. Tangent")
    print("4. Logarithm")
    print("5. Exponential")

    choice = input("Enter choice(1/2/3/4/5): ")

    num = float(input("Enter number: "))

    if choice == '1':
        print("Sin(", num, ") =", math.sin(math.radians(num)))
    elif choice == '2':
        print("Cos(", num, ") =", math.cos(math.radians(num)))
    elif choice == '3':
        print("Tan(", num, ") =", math.tan(math.radians(num)))
    elif choice == '4':
        print("Logarithm(", num, ") =", math.log(num))
    elif choice == '5':
        print("Exponential(", num, ") =", math.exp(num))
    else:
        print("Invalid input")

while True:
    print("Select mode:")
    print("1. Basic Calculator")
    print("2. Scientific Calculator")
    print("3. Exit")
    mode=input("Enter mode(1/2/3):")
    if mode=='1':
        root = tk.Tk()
        calculator = Calculator(root)

        root.mainloop()
    elif mode == '2':
        scientific_calculator()
    elif mode == '3':
        break
    else:
        print("Invalid input")
