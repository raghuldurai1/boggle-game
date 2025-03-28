import tkinter as tk
from tkinter import messagebox

DICTIONARY = {"RAGUL","HAMZA","UMAID","ANMOL","STARK"}

BOARD = [
    ['R', 'A', 'G', 'U', 'L'],
    ['S', 'T', 'A', 'R', 'K'],
    ['A', 'M', 'O', 'L', 'A'],
    ['H', 'A', 'M', 'Z', 'D'],
    ['U', 'M', 'A', 'I', 'D']
]

ROWS = 5
COLS = 5

class BoggleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Predefined Boggle Game")

        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()

        self.current_word_label = tk.Label(root, text="Current Word: ", font=("Arial", 16))
        self.current_word_label.pack(pady=10)

        self.undo_button = tk.Button(root, text="Undo", command=self.undo_last_letter)
        self.undo_button.pack(pady=10)

        self.check_word_button = tk.Button(root, text="Check Word", command=self.check_word)
        self.check_word_button.pack(pady=10)

        self.words_listbox = tk.Listbox(root, width=40, height=10)
        self.words_listbox.pack(pady=10)

        self.grid_labels = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.visited = []
        self.current_word = ""
        self.draw_grid()

    def draw_grid(self):
        for i in range(ROWS):
            for j in range(COLS):
                x1 = j * 100
                y1 = i * 100
                x2 = x1 + 100
                y2 = y1 + 100
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                label = tk.Label(self.canvas, text=BOARD[i][j], font=("Arial", 24), bg="white")
                label.place(x=x1 + 35, y=y1 + 35)
                label.bind("<Button-1>", lambda e, row=i, col=j: self.on_letter_click(row, col))
                self.grid_labels[i][j] = label

    def on_letter_click(self, row, col):
        if (row, col) not in self.visited:
            if self.visited:
                last_row, last_col = self.visited[-1]
                if abs(last_row - row) <= 1 and abs(last_col - col) <= 1:
                    self.add_letter(row, col)
                else:
                    messagebox.showwarning("Invalid Move", "You must click an adjacent letter.")
            else:
                self.add_letter(row, col)

    def add_letter(self, row, col):
        self.visited.append((row, col))
        self.current_word += BOARD[row][col]
        self.grid_labels[row][col].config(bg="lightblue")
        self.update_current_word_label()

    def undo_last_letter(self):
        if self.visited:
            last_row, last_col = self.visited.pop()
            self.current_word = self.current_word[:-1]
            self.grid_labels[last_row][last_col].config(bg="white")
            self.update_current_word_label()

    def update_current_word_label(self):
        self.current_word_label.config(text=f"Current Word: {self.current_word}")

    def check_word(self):
        if self.current_word in DICTIONARY:
            messagebox.showinfo("Valid Word", f"'{self.current_word}' is a valid word!")
            self.words_listbox.insert(tk.END, self.current_word)
        else:
            messagebox.showerror("Invalid Word", f"'{self.current_word}' is not a valid word.")

        self.reset_selection()

    def reset_selection(self):
        for row, col in self.visited:
            self.grid_labels[row][col].config(bg="white")
        self.visited.clear()
        self.current_word = ""
        self.update_current_word_label()


if __name__ == "__main__":
    root = tk.Tk()
    app = BoggleApp(root)
    root.mainloop()