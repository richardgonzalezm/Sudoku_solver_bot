from sudoku_module import sudoku
from sudoku_module import gui
import tkinter as tk


def main():
    root = tk.Tk()
    sudoku_game = sudoku.Sudoku()
    app = gui.SudokuGUI(root, sudoku_game)
    root.mainloop()


if __name__ == '__main__':
    main()
