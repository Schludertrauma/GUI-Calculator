'''GUI Calculator'''
'''This module provides a simple GUI calculator using Tkinter.'''
'''The calculator supports basic arithmetic operations: addition, subtraction, multiplication, and division.'''
'''It features a user-friendly interface with buttons for digits and operations.'''
'''The code is structured to handle button clicks and keyboard input to perform calculations.'''
'''Error handling is included to manage invalid inputs and unexpected errors such as division by zero.'''
'''The result is displayed in real-time as the user interacts with the calculator and is logged to a text file.'''
'''This script is designed only for exercising basic Python and Tkinter skills.'''


# Import modules and libraries


import time
from tkinter import messagebox
import tkinter as tk

# Class definition


class gui_calculator:
    def __init__(self, master):
        # Initialize the GUI calculator with a master window.
        self.master = master
        self.master.title("GUI Calculator")
        self.master.geometry("295x250")
        self.master.resizable(False, False)
        self.result_var = tk.StringVar()
        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        # Create the main entry field for input and result display.
        self.entry = tk.Entry(self.master, width=16, font=(
            'Arial', 24), borderwidth=2, relief='ridge')
        self.entry.grid(row=0, column=0, columnspan=4)

        # Define button layout
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '.', '0', '=', '+',
            'C'
        ]

        # Create buttons dynamically
        for i, button in enumerate(buttons):
            def action(x=button): return self.on_button_click(x)
            # Place 'C' button in column 0, row 1, result label is in column 1-3, row 1
            tk.Button(self.master, text=button, width=5, height=2,
                      command=action).grid(row=(i // 4) + 1, column=i % 4)

    def on_button_click(self, char):
        # Handle button clicks and perform calculations.
        self.result_var = tk.StringVar()
        if char == 'C':
            self.entry.delete(0, tk.END)
            self.result_var.set('result: ')
        elif char == '=':
            try:
                input_expr = self.entry.get()
                result = eval(input_expr)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
                self.result_var.set(f'{result}')
                self.log_result(result, input_expr)
            except ZeroDivisionError:
                messagebox.showerror(
                    "Error", "Division by zero is not allowed.")
                self.entry.delete(0, tk.END)
                self.result_var.set('error')
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
                self.entry.delete(0, tk.END)
                self.result_var.set('error')
        elif char in ['+', '-', '*', '/', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.entry.insert(tk.END, char)

    def on_key_press(self, event):
        # Handle key presses for calculator input.
        char = event.char
        if char in '0123456789+-*/.':
            self.entry.insert(tk.END, char)
        elif char == '\r':
            try:
                result = eval(self.entry.get())
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
                self.result_var.set(f'result: {result}')
            except ZeroDivisionError:
                messagebox.showerror(
                    "Error", "Division by zero is not allowed.")
                self.entry.delete(0, tk.END)
                self.result_var.set('result: error')
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
                self.entry.delete(0, tk.END)
                self.result_var.set('result: error')
        elif char == 'c' or char == 'C':
            self.entry.delete(0, tk.END)
            self.result_var.set('result: ')

    def bind_keys(self):
        # Bind keyboard events to the calculator.
        self.master.bind('<KeyPress>', self.on_key_press)

    def log_result(self, result, input_expr):
        # Log input and result to a text file with a timestamp
        calculator_log = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Rechnung: {input_expr} = {result}\n"
        log_path = "calculator_log.txt"
        try:
            with open(log_path, "a") as log_file:
                log_file.write(calculator_log)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to log result: {e}")


# Main execution block to run the calculator application


if __name__ == "__main__":
    root = tk.Tk()
    calculator = gui_calculator(root)
    root.mainloop()
