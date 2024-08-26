# Sudoku solver bot

## Description
This is a project to automatically solve an specific puzzle (a sudoku) and then upload it automatically to the web it came from. This would allow us to become absolute champions in the sudoku world without actually being so.

To integrate object-oriented programming, we designed the following class diagram.

## Class diagram

```mermaid
---
title: Sudoku solver bot
---
classDiagram
  class Sudoku {
    - List of Lists: sudoku
    + __init__(self, )
    + solve_sudoku(self)
    + is_possible(self, x, y): Bool

    + print_sudoku(self)
  }
  class SubGrid{
    - List: subgrid
    + find_sub_grid_coordinates(value)
    + is_possible_subgrid(self)    
  }
  Sudoku --* SubGrid
  class ScrapperBot {
    - webdriver: driver
    - str: link
    + __init__(self, driver)
    + read_sudoku(self) sudoku
    + upload_sudoku(self, sudoku)
  }

  class ScrapperNYTimes {
    - str: nyTimes_link
    + __init__(self)
    + read_sudoku(self, difficulty)
  }
  ScrapperBot --> Sudoku
  ScrapperBot<|--ScrapperNYTimes
```
