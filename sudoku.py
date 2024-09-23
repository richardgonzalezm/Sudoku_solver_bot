import tkinter as tk
from tkinter import messagebox
import random


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


class Grid:
    def __init__(self, values):
        self._values = values

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, new_values):
        if len(new_values) != len(self._values):
            raise ValueError(
                "New values must have the same length as the original values.")
        self._values = new_values


class Row(Grid):
    def __init__(self, values):
        super().__init__(values)


class Col(Grid):
    def __init__(self, values):
        super().__init__(values)


class Subgrid:
    def __init__(self, grid):
        self._grid = grid
        self.rows = [Row(row) for row in grid]
        self.cols = [Col([grid[r][c] for r in range(3)]) for c in range(3)]

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, new_grid):
        if len(new_grid) != 3 or any(len(row) != 3 for row in new_grid):
            raise ValueError("Subgrid must be a 3x3 grid.")
        self._grid = new_grid


class Sudoku(Subgrid):
    def __init__(self, grid=None):
        if grid:
            if len(grid) != 9 or any(len(row) != 9 for row in grid):
                raise ValueError("Sudoku grid must be a 9x9 grid.")
            super().__init__(grid)
        else:
            # Crea una cuadrícula vacía
            self._grid = [[0 for _ in range(9)] for _ in range(9)]
        self.size = 9

    def is_valid(self, num, pos):
        # Check row
        for i in range(self.size):
            if self.grid[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(self.size):
            if self.grid[i][pos[1]] == num and pos[0] != i:
                return False

        # Check subgrid
        subgrid_x = pos[1] // 3
        subgrid_y = pos[0] // 3

        for i in range(subgrid_y * 3, subgrid_y * 3 + 3):
            for j in range(subgrid_x * 3, subgrid_x * 3 + 3):
                if self.grid[i][j] == num and (i, j) != pos:
                    return False

        return True

    def find_empty(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)  # row, col
        return None

    def solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.is_valid(i, (row, col)):
                self.grid[row][col] = i

                if self.solve():
                    return True

                self.grid[row][col] = 0

        return False

    def generate_sudoku(self, clues=30):
        # Rellena la cuadrícula completamente
        self._fill_grid()

        # Elimina valores de la cuadrícula para crear un puzzle
        self._remove_numbers(clues)

    def _fill_grid(self):
        """Rellena la cuadrícula de Sudoku usando backtracking"""
        find = self.find_empty()
        if not find:
            return True  # La cuadrícula está completamente llena
        else:
            row, col = find

        # Intenta insertar números del 1 al 9 de forma aleatoria
        nums = list(range(1, 10))
        random.shuffle(nums)
        for num in nums:
            if self.is_valid(num, (row, col)):
                self.grid[row][col] = num

                if self._fill_grid():
                    return True

                # Resetea la celda si no es válida más adelante
                self.grid[row][col] = 0

        return False  # Triggera backtracking

    def _remove_numbers(self, clues):
        """Remueve números de la cuadrícula para dejar solo las pistas dadas"""
        total_cells = 81
        cells_to_remove = total_cells - clues

        while cells_to_remove > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.grid[row][col] != 0:
                # Verifica que eliminar este número no haga el Sudoku irresoluble
                backup = self.grid[row][col]
                self.grid[row][col] = 0

                # Si no es solucionable, vuelve a colocar el número
                grid_copy = [row.copy() for row in self.grid]
                if not Sudoku(grid_copy).solve():
                    self.grid[row][col] = backup
                else:
                    cells_to_remove -= 1


if __name__ == "__main__":
    root = tk.Tk()
    sudoku = Sudoku()
    app = SudokuGUI(root, sudoku)
    root.mainloop()
