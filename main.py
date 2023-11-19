import numpy as np
from generator import generate_full_board, remove_numbers

def main():
    # Example user interaction for selecting difficulty
    difficulty = input("Choose difficulty (easy, medium, hard, expert): ").lower()
    
    # Validate difficulty input
    if difficulty not in ["easy", "medium", "hard", "expert"]:
        print("Invalid difficulty. Defaulting to medium.")
        difficulty = "medium"

    # Generate Sudoku puzzle
    board = generate_full_board()
    puzzle = remove_numbers(board.copy(), difficulty)

    # Display or process the puzzle
    print("Generated Sudoku Puzzle:")
    print(puzzle)

    # Here, you can add your solving and scoring logic
    # ...

if __name__ == "__main__":
    main()
