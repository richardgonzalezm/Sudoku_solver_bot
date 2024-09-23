import tkinter as tk
from tkinter import messagebox


class SudokuGUI:
    def __init__(self, root, sudoku):
        self.root = root
        self.sudoku = sudoku
        self.entries = []
        self.create_widgets()

    def create_widgets(self):
        self.root.title("Sudoku Generator & Solver")

        # Crea una cuadrícula 9x9 de entradas
        for row in range(9):
            row_entries = []
            for col in range(9):
                entry = tk.Entry(self.root, width=5,
                                 justify='center', font=("Arial", 18))
                entry.grid(row=row, column=col, padx=5,
                           pady=5, ipadx=10, ipady=10)
                row_entries.append(entry)
            self.entries.append(row_entries)

        # Botón para generar Sudoku
        generate_button = tk.Button(
            self.root, text="Generar Sudoku", command=self.generate_sudoku)
        generate_button.grid(row=10, column=0, columnspan=4, pady=10)

        # Espacio vacío entre los botones
        spacer = tk.Label(self.root, text="")
        spacer.grid(row=11, column=0, columnspan=9, pady=10)

        # Botón para resolver Sudoku
        solve_button = tk.Button(
            self.root, text="Resolver Sudoku", command=self.solve_sudoku)
        solve_button.grid(row=12, column=0, columnspan=4, pady=10)

    def generate_sudoku(self):
        """Genera un nuevo tablero de Sudoku y lo muestra en la interfaz."""
        self.sudoku.generate_sudoku(clues=30)
        self.update_grid()

    def solve_sudoku(self):
        """Resuelve el Sudoku y actualiza la interfaz."""
        if self.sudoku.solve():
            self.update_grid()
        else:
            messagebox.showerror("Error", "No se pudo resolver el Sudoku")

    def update_grid(self):
        """Actualiza la cuadrícula de la interfaz con los valores del tablero."""
        for row in range(9):
            for col in range(9):
                value = self.sudoku.grid[row][col]
                self.entries[row][col].delete(0, tk.END)  # Limpia la entrada
                if value != 0:
                    # Inserta el valor del tablero
                    self.entries[row][col].insert(0, str(value))
                    self.entries[row][col].config(
                        state="readonly")  # Lo hace de solo lectura
                else:
                    # Permite editar las celdas vacías
                    self.entries[row][col].config(state="normal")
