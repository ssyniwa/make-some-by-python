import sys
from tkinter import *
import tkinter as tk


class Calculator:
    def __init__(self, root):
        self.root = root
        root.title("Overlapped Window")  # ウィンドウのタイトルを設定
        root.geometry("400x300")  # ウィンドウのサイズを設定
        # ウィジェットの配置などをここに追加
        label = tk.Label(root, text="これはオーバーラップウィンドウです", font=("Arial", 14))
        label.pack(pady=20)
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


root = tk.Tk()
root.title("Overlapped Window")  # ウィンドウのタイトルを設定
root.geometry("400x300")  # ウィンドウのサイズを設定
# calculator = Calculator(root)
label = tk.Label(root, text="Hello, Tkinter!")
label.pack()
button = tk.Button(root, text="Click me!")
button.pack()
root.mainloop()
