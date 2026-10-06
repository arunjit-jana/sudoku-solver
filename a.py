import tkinter as tk
from tkinter import messagebox
import threading
import time

# -------------------- Sudoku Logic --------------------

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False
    for x in range(9):
        if board[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True


def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# -------------------- GUI Logic --------------------

def get_board():
    board = []
    for r in range(9):
        row_vals = []
        for c in range(9):
            val = entries[r][c].get()
            if val == "":
                row_vals.append(0)
            else:
                try:
                    n = int(val)
                    if n < 1 or n > 9:
                        raise ValueError
                    row_vals.append(n)
                except ValueError:
                    messagebox.showerror("Error", "Use only numbers 1–9")
                    return None
        board.append(row_vals)
    return board


def set_board(board, animated=False):
    for r in range(9):
        for c in range(9):
            entries[r][c].delete(0, tk.END)
            if board[r][c] != 0:
                if animated:
                    root.after((r * 9 + c) * 20, lambda r=r, c=c: animate_fill(r, c, board[r][c]))
                else:
                    entries[r][c].insert(0, str(board[r][c]))


def animate_fill(r, c, value):
    entries[r][c].insert(0, str(value))
    entries[r][c].config(bg="#b2f2bb")
    root.after(300, lambda: entries[r][c].config(bg="#ffffff"))


def solve_with_animation():
    board = get_board()
    if board is None:
        return

    status_label.config(text="Solving...", fg="#ffa94d")

    def task():
        if solve_sudoku(board):
            root.after(0, lambda: set_board(board, animated=True))
            root.after(2000, lambda: status_label.config(text="Solved! 🎉", fg="#40c057"))
        else:
            root.after(0, lambda: messagebox.showerror("Error", "No solution exists"))
            root.after(0, lambda: status_label.config(text="Error ❌", fg="#fa5252"))

    threading.Thread(target=task).start()


def clear_grid():
    for r in range(9):
        for c in range(9):
            entries[r][c].delete(0, tk.END)
            entries[r][c].config(bg="#ffffff")
    status_label.config(text="Grid Cleared", fg="#339af0")


# -------------------- UI Setup --------------------

root = tk.Tk()
root.title("Sudoku Solver Deluxe")
root.geometry("460x560")
root.configure(bg="#f1f3f5")

# Title
title_label = tk.Label(
    root, text="🧩 Sudoku Solver Deluxe",
    font=("Segoe UI", 20, "bold"),
    bg="#f1f3f5", fg="#212529"
)
title_label.pack(pady=10)

status_label = tk.Label(
    root, text="Enter numbers and click Solve",
    font=("Segoe UI", 11),
    bg="#f1f3f5", fg="#339af0"
)
status_label.pack(pady=5)

# Grid Frame
grid_frame = tk.Frame(root, bg="#dee2e6", padx=8, pady=8)
grid_frame.pack(pady=10)

entries = []

for r in range(9):
    row_entries = []
    for c in range(9):
        entry = tk.Entry(
            grid_frame,
            width=3,
            font=("Segoe UI", 18, "bold"),
            justify="center",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#adb5bd",
            highlightcolor="#228be6"
        )

        # Box separators
        padx = (6 if c % 3 == 0 else 2)
        pady = (6 if r % 3 == 0 else 2)

        entry.grid(row=r, column=c, padx=padx, pady=pady)
        row_entries.append(entry)
    entries.append(row_entries)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#f1f3f5")
btn_frame.pack(pady=15)

solve_btn = tk.Button(
    btn_frame, text="✨ Solve Sudoku",
    font=("Segoe UI", 12, "bold"),
    bg="#40c057", fg="white",
    relief="flat", width=15,
    command=solve_with_animation
)
solve_btn.grid(row=0, column=0, padx=10)

clear_btn = tk.Button(
    btn_frame, text="🧹 Clear Grid",
    font=("Segoe UI", 12, "bold"),
    bg="#fa5252", fg="white",
    relief="flat", width=15,
    command=clear_grid
)
clear_btn.grid(row=0, column=1, padx=10)

# Footer
footer = tk.Label(
    root, text="Made with Python + Tkinter",
    font=("Segoe UI", 9),
    bg="#f1f3f5", fg="#868e96"
)
footer.pack(side="bottom", pady=10)

root.mainloop()