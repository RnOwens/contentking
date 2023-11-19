import numpy as np
from generator import generate_full_board, remove_numbers
from solver import solve_sudoku  # Import your solving and scoring function

def main():
    # User selects difficulty
    difficulty = input("Choose difficulty (easy, medium, hard, expert): ").lower()
    if difficulty not in ["easy", "medium", "hard", "expert"]:
        print("Invalid difficulty. Defaulting to medium.")
        difficulty = "medium"

    # Generate Sudoku puzzle
    board = generate_full_board()
    puzzle = remove_numbers(board.copy(), difficulty)

    # Display the generated puzzle
    print("Generated Sudoku Puzzle:")
    print(puzzle)

    # Solve the puzzle and calculate difficulty score
    solved_board = np.array(puzzle)  # Make sure the board is in the correct format
    difficulty_score = solve_sudoku(solved_board)
    print(f"Difficulty Score: {difficulty_score}")

    # Optionally, display the solved puzzle
    print("Solved Sudoku Puzzle:")
    print(solved_board)

if __name__ == "__main__":
    main()
