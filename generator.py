import numpy as np
import random

def generate_full_board():
    """
    Generate a full 9x9 Sudoku board with a valid solution.
    """
    board = np.zeros((9, 9), dtype=int)

    def valid(board, row, col, num):
        """
        Check if a number can be placed in a specific position.
        """
        for i in range(9):
            if board[row, i] == num or board[i, col] == num:
                return False
            if board[row - row % 3 + i // 3, col - col % 3 + i % 3] == num:
                return False
        return True

    def solve_board(board):
        """
        Solve the Sudoku board using backtracking.
        """
        for i in range(9):
            for j in range(9):
                if board[i, j] == 0:
                    for num in range(1, 10):
                        if valid(board, i, j, num):
                            board[i, j] = num
                            if solve_board(board):
                                return True
                            board[i, j] = 0
                    return False
        return True

    solve_board(board)
    return board

def remove_numbers(board, level):
    """
    Remove numbers from the board to create a puzzle of a specific difficulty level.
    """
    levels = {
        "easy": 36,
        "medium": 32,
        "hard": 28,
        "expert": 24
    }

    squares = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(squares)
    for square in squares[:81 - levels[level]]:
        board[square[0], square[1]] = 0

    return board

# Example of generating a puzzle
board = generate_full_board()
puzzle = remove_numbers(board.copy(), "medium")  # Generate a medium difficulty puzzle
