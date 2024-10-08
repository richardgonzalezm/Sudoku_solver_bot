# Sudoku solver bot

## Description
This is a project that automatically generates and solves an specific puzzle (a sudoku). Creating this bot, we realized what the internal processes to solve a sudoku were, and this helped us come up with our own personal ways to solve sudokus by ourselves.

The code uses recursion and backtraking to solve the sudoku, making it review each possibility for a solution in a matter of seconds, correcting itself over and over again until it finds the answer.

To integrate an object-oriented programming, we designed the following class diagram.

## Class diagram

```mermaid
---
title: Sudoku solver (and generator)
---
classDiagram
    class Line {
        -_values
        +values() @property
        +values(new_values) @getter
        +is_valid(num, pos) bool
        +find_empty()
    }
    class Col {
        -values
    }
    class Row {
        -values
    }
    Line <|-- Col
    Line <|-- Row
    class Sudoku {
        -size: int
        +is_valid(num, pos) bool
        +find_empty() 
        +solve() bool
        +generate_sudoku(clues)
        -_fill_grid() bool
        -_remove_numbers(clues)
    }
    class SudokuGUI {
        -root: Tkinter interface
        -sudoku: Sudoku
        +create_widgets()
        +generate_sudoku()
        +solve_sudoku()
        +update_grid()
    }
    SudokuGUI --> Sudoku
    class Subgrid {
        -_grid: List of List of int
        -rows: List of Row
        -cols: List of Col
        +grid()@property
        +grid(new_grid)@setter
        +is_valid(num, pos) bool
        +find_empty()
    }

    Col --* Subgrid
    Row --* Subgrid
    Sudoku --|> Subgrid
```

## Main classes:

"SudokuGUI" is a graphical user interface for generating and solving Sudoku puzzles.

    -Attributes:
        root (tk.Tk): The root window of the Tkinter application.
        sudoku (Sudoku): An instance of the Sudoku class that handles the puzzle logic.
        entries (list): A 2D list of Tkinter Entry widgets representing the Sudoku grid.
    -Methods:
        __init__(root, sudoku):
            Initializes the SudokuGUI with the given root window and Sudoku instance.
        create_widgets():
            Creates the widgets for the Sudoku GUI, including the grid of entries and buttons.
        generate_sudoku():
            Generates a new Sudoku puzzle with a specified number of clues and updates the grid.
        solve_sudoku():
            Solves the current Sudoku puzzle and updates the grid. Displays an error message if the puzzle cannot be solved.
        update_grid():
            Updates the GUI grid with the values from the Sudoku puzzle. Sets cells to read-only if they contain a value.

"Line" is a class to represent a Sudoku horizontal or vertical line.

    -Attributes:
        values (list): A list representing the values in the Sudoku line.
    -Methods:
      values:
            Getter: Returns the current values of the line.
            Setter: Sets new values for the line, ensuring the length matches the original.
        is_valid(num):
            Checks if a given number is not already present in the line.
        find_empty():
            Finds the first empty position (represented by 0) in the line and returns its index.

"Col" represents a column. Inherits from Line.

"Row" represents a row. Inherits from Line too.

"Subgrid" is a class to represent a 3x3 subgrid in a Sudoku puzzle.
    
    -Attributes:
        _grid (list of list of int): The 3x3 grid representing the subgrid.
        rows (list of Row): List of Row objects representing each row in the subgrid.
        cols (list of Col): List of Col objects representing each column in the subgrid.
    -Methods:
        __init__(grid):
            Initializes the Subgrid with a 3x3 grid.
        grid:
            A getter for the current grid.
        grid(new_grid):
            A setter that updates the grid. Raises ValueError if the new grid is not 3x3.
        is_valid(num, pos):
            Checks if a number can be placed in the subgrid without violating the rules.
        find_empty():
            Finds the first empty cell (represented by 0) in the subgrid.

"Sudoku": A class that represents the Sudoku puzzle.

    -Attributes:
        size (int): The size of the Sudoku grid (default is 9).
    -Methods:
        __init__(grid=None):
            Initializes the Sudoku grid. If a grid is provided, it validates the grid.
            Otherwise, it creates an empty 9x9 grid.
        is_valid(num, pos):
            Checks if a given number can be placed at a given position in the grid
            without violating Sudoku rules.
        find_empty():
            Finds an empty cell in the Sudoku grid.
        solve():
            Solves the Sudoku puzzle using backtracking.
        generate_sudoku(clues=30):
            Generates a Sudoku puzzle with a given number of clues. Fills the grid completely
            and then removes numbers to create the puzzle.
        _fill_grid():
            Fills the Sudoku grid completely using backtracking. This is a helper method
            used by generate_sudoku().
        _remove_numbers(clues):
            Removes numbers from the filled grid to leave only the given number of clues.
            Ensures that the resulting puzzle is still solvable.
          
