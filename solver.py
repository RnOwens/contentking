import numpy as np

# Constants for technique costs
COSTS = {
    "sct": (100, 100),  # Single Candidate Technique
    "spt": (100, 100),  # Single Position Technique
    "clt": (350, 200),  # Candidate Lines Technique
    "dpt": (500, 250),  # Double Pairs Technique
    "dj2": (750, 500),  # Naked Pairs Technique
    "us2": (1500, 1200), # Hidden Pairs Technique
    "dj3": (2000, 1400), # Naked Triple Technique
    "us3": (2400, 1600), # Hidden Triple Technique
    "xwg": (2800, 1600)  # X-Wing Technique
    # Add other techniques if needed
}


def find_candidate_lines(board):
    n = 9
    found = False

    # Check each block
    for block_row in range(0, n, 3):
        for block_col in range(0, n, 3):
            # Check each number
            for num in range(1, n + 1):
                possible_cells = [(row, col) for row in range(block_row, block_row + 3)
                                  for col in range(block_col, block_col + 3) 
                                  if board[row][col] == 0 and is_possible(board, row, col, num)]

                rows = [row for row, col in possible_cells]
                cols = [col for row, col in possible_cells]

                # Check if all possible cells for a number are in the same row or column
                if len(set(rows)) == 1:  # All cells in the same row
                    row = rows[0]
                    for col in range(n):  # Eliminate this number from other blocks in the same row
                        if col < block_col or col >= block_col + 3:
                            if board[row][col] == 0 and is_possible(board, row, col, num):
                                board[row][col] = -num  # Indicate elimination
                                found = True

                if len(set(cols)) == 1:  # All cells in the same column
                    col = cols[0]
                    for row in range(n):  # Eliminate this number from other blocks in the same column
                        if row < block_row or row >= block_row + 3:
                            if board[row][col] == 0 and is_possible(board, row, col, num):
                                board[row][col] = -num  # Indicate elimination
                                found = True

    return found


def find_double_pairs(board):
    n = 9
    found = False

    # Check each 3x3 block
    for block_row in range(0, n, 3):
        for block_col in range(0, n, 3):
            # Identify pairs of cells in the block that have only two candidates
            pairs = {}
            for row in range(block_row, block_row + 3):
                for col in range(block_col, block_col + 3):
                    if board[row][col] == 0:
                        candidates = {num for num in range(1, n + 1) if is_possible(board, row, col, num)}
                        if len(candidates) == 2:
                            pair_key = tuple(candidates)
                            if pair_key not in pairs:
                                pairs[pair_key] = []
                            pairs[pair_key].append((row, col))

            # Check for double pairs
            for pair, cells in pairs.items():
                if len(cells) == 2:
                    # Check if the cells are in the same row or column
                    same_row = all(row == cells[0][0] for row, col in cells)
                    same_col = all(col == cells[0][1] for row, col in cells)

                    if same_row or same_col:
                        # Eliminate these numbers from other cells in the row or column
                        for num in pair:
                            if same_row:
                                row = cells[0][0]
                                for col in range(n):
                                    if col < block_col or col >= block_col + 3:
                                        if board[row][col] == 0 and is_possible(board, row, col, num):
                                            board[row][col] = -num  # Indicate elimination
                                            found = True
                            if same_col:
                                col = cells[0][1]
                                for row in range(n):
                                    if row < block_row or row >= block_row + 3:
                                        if board[row][col] == 0 and is_possible(board, row, col, num):
                                            board[row][col] = -num  # Indicate elimination
                                            found = True

    return found



def find_naked_pairs(board):
    # Implementation of Naked Pairs Technique
    # ...
    return False  # Update to True when a change is made


def find_single_candidate(board):
    n = 9
    found = False
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                possible = set(range(1, n + 1))
                for k in range(n):
                    if board[i][k] in possible:
                        possible.remove(board[i][k])
                    if board[k][j] in possible:
                        possible.remove(board[k][j])
                    if board[i - i % 3 + k // 3][j - j % 3 + k % 3] in possible:
                        possible.remove(board[i - i % 3 + k // 3][j - j % 3 + k % 3])
                if len(possible) == 1:
                    board[i][j] = possible.pop()
                    found = True
    return found

def find_single_position(board):
    n = 9
    found = False
    for number in range(1, n + 1):
        for i in range(n):
            possible_positions = []
            for j in range(n):
                if board[i][j] == 0 and is_possible(board, i, j, number):
                    possible_positions.append(j)
            if len(possible_positions) == 1:
                board[i][possible_positions[0]] = number
                found = True
    return found

def find_x_wing(board):
    n = 9
    found = False

    # Check for X-Wing in rows
    for num in range(1, n + 1):
        for row1 in range(n):
            for row2 in range(row1 + 1, n):
                possible_cols = [col for col in range(n) if board[row1][col] == 0 and is_possible(board, row1, col, num) and
                                 board[row2][col] == 0 and is_possible(board, row2, col, num)]
                
                if len(possible_cols) == 2:
                    col1, col2 = possible_cols
                    if all(board[r][col1] != num for r in range(n) if r not in [row1, row2]) and \
                       all(board[r][col2] != num for r in range(n) if r not in [row1, row2]):
                        # Eliminate 'num' from these columns in other rows
                        for r in range(n):
                            if r not in [row1, row2] and board[r][col1] == 0 and is_possible(board, r, col1, num):
                                board[r][col1] = -num  # Indicate elimination
                                found = True
                            if r not in [row1, row2] and board[r][col2] == 0 and is_possible(board, r, col2, num):
                                board[r][col2] = -num  # Indicate elimination
                                found = True

    # Repeat the same logic for X-Wing in columns

    return found


def find_hidden_pairs(board):
    n = 9
    found = False

    # Check for hidden pairs in rows
    for row in range(n):
        for num1 in range(1, n + 1):
            positions = [col for col in range(n) if board[row][col] == 0 and is_possible(board, row, col, num1)]
            if len(positions) == 2:
                for num2 in range(num1 + 1, n + 1):
                    positions2 = [col for col in range(n) if board[row][col] == 0 and is_possible(board, row, col, num2)]
                    if positions == positions2:
                        # Hidden pair found, remove other numbers
                        for col in positions:
                            for num in range(1, n + 1):
                                if num != num1 and num != num2:
                                    board[row][col] = -num  # Indicate elimination
                                    found = True

    # Check for hidden pairs in columns
    for col in range(n):
        for num1 in range(1, n + 1):
            positions = [row for row in range(n) if board[row][col] == 0 and is_possible(board, row, col, num1)]
            if len(positions) == 2:
                for num2 in range(num1 + 1, n + 1):
                    positions2 = [row for row in range(n) if board[row][col] == 0 and is_possible(board, row, col, num2)]
                    if positions == positions2:
                        # Hidden pair found, remove other numbers
                        for row in positions:
                            for num in range(1, n + 1):
                                if num != num1 and num != num2:
                                    board[row][col] = -num  # Indicate elimination
                                    found = True

    # Check for hidden pairs in blocks
    for block_row in range(3):
        for block_col in range(3):
            for num1 in range(1, n + 1):
                positions = []
                for row in range(3 * block_row, 3 * block_row + 3):
                    for col in range(3 * block_col, 3 * block_col + 3):
                        if board[row][col] == 0 and is_possible(board, row, col, num1):
                            positions.append((row, col))
                if len(positions) == 2:
                    for num2 in range(num1 + 1, n + 1):
                        positions2 = []
                        for row in range(3 * block_row, 3 * block_row + 3):
                            for col in range(3 * block_col, 3 * block_col + 3):
                                if board[row][col] == 0 and is_possible(board, row, col, num2):
                                    positions2.append((row, col))
                        if positions == positions2:
                            # Hidden pair found, remove other numbers
                            for (row, col) in positions:
                                for num in range(1, n + 1):
                                    if num != num1 and num != num2:
                                        board[row][col] = -num  # Indicate elimination
                                        found = True

    return found

def find_hidden_triples_in_group(group):
    n = 9
    possibilities = [set() for _ in range(n)]
    for i, cell in enumerate(group):
        if cell == 0:
            possibilities[i] = {num for num in range(1, n + 1) if is_possible_in_group(group, num, i)}

    triples = []
    for num in range(1, n + 1):
        cells = [i for i in range(n) if num in possibilities[i]]
        if len(cells) == 3:
            nums = set.intersection(*[possibilities[cell] for cell in cells])
            if len(nums) <= 3:
                triples.append((nums, cells))

    return triples

def find_naked_triple(board):
    n = 9
    found = False

    for unit in range(n):
        # Check each row and column
        for is_row in [True, False]:
            if is_row:
                group = [board[unit, j] for j in range(n)]  # Row
            else:
                group = [board[j, unit] for j in range(n)]  # Column

            triples = find_naked_triples_in_group(group)
            for triple in triples:
                cells, nums = triple
                for i in range(n):
                    if i not in cells and group[i] == 0:
                        for num in nums:
                            if is_possible(board, unit if is_row else i, i if is_row else unit, num):
                                board[unit if is_row else i, i if is_row else unit] = -num  # Indicate elimination
                                found = True

        # Check each block
        block_row = (unit // 3) * 3
        block_col = (unit % 3) * 3
        block = [board[block_row + r][block_col + c] for r in range(3) for c in range(3)]

        triples = find_naked_triples_in_group(block)
        for triple in triples:
            cells, nums = triple
            for idx in range(9):
                if idx not in cells and block[idx] == 0:
                    row, col = (block_row + idx // 3, block_col + idx % 3)
                    for num in nums:
                        if is_possible(board, row, col, num):
                            board[row, col] = -num  # Indicate elimination
                            found = True

    return found

def find_naked_triples_in_group(group):
    n = 9
    candidates = [set() for _ in range(n)]
    for i, cell in enumerate(group):
        if cell == 0:
            candidates[i] = {num for num in range(1, n + 1) if is_possible_in_group(group, num, i)}

    triples = []
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                union = candidates[i] | candidates[j] | candidates[k]
                if len(union) == 3:
                    triples.append(([i, j, k], union))

    return triples

def is_possible_in_group(group, num, index):
    """
    Checks if a number is a possible candidate in a given cell of a group (row, column, or block)
    """
    n = 9
    for i, cell in enumerate(group):
        if cell == num and i != index:
            return False
    return True



def find_hidden_triple(board):
    n = 9
    found = False

    for unit in range(n):
        # Check each row and column
        for is_row in [True, False]:
            if is_row:
                group = [board[unit, j] for j in range(n)]  # Row
            else:
                group = [board[j, unit] for j in range(n)]  # Column

            triples = find_hidden_triples_in_group(group)
            for triple in triples:
                nums, cells = triple
                for num in nums:
                    for i in range(n):
                        if i in cells and group[i] == 0:
                            if is_possible(board, unit if is_row else i, i if is_row else unit, num):
                                board[unit if is_row else i, i if is_row else unit] = -num  # Indicate elimination
                                found = True

        # Check each block
        block_row = (unit // 3) * 3
        block_col = (unit % 3) * 3
        block = [board[block_row + r][block_col + c] for r in range(3) for c in range(3)]

        triples = find_hidden_triples_in_group(block)
        for triple in triples:
            nums, cells = triple
            for num in nums:
                for idx in range(9):
                    row, col = (block_row + idx // 3, block_col + idx % 3)
                    if idx in cells and block[idx] == 0:
                        if is_possible(board, row, col, num):
                            board[row, col] = -num  # Indicate elimination
                            found = True

    return found

def find_hidden_triples_in_group(group):
    n = 9
    possibilities = [set() for _ in range(n)]
    for i in range(n):
        if group[i] == 0:
            possibilities[i] = {num for num in range(1, n + 1) if is_possible(board, row, col, num)}

    triples = []
    for num in range(1, n + 1):
        cells = [i for i in range(n) if num in possibilities[i]]
        if len(cells) == 3:
            nums = set.intersection(*[possibilities[cell] for cell in cells])
            if len(nums) == 3:
                triples.append((nums, cells))

    return triples

def is_possible(board, row, col, number):
    n = 9
    for i in range(n):
        if board[row][i] == number or board[i][col] == number:
            return False
        if board[row - row % 3 + i // 3][col - col % 3 + i % 3] == number:
            return False
    return True

def solve_sudoku(board):
    total_cost = 0
    techniques_used = {"sct": 0, "spt": 0, "clt": 0, "dpt": 0, "dj2": 0, "us2": 0, "dj3": 0, "us3": 0, "xwg": 0}
    
    while True:
        made_progress = False

        # Check each technique and update progress and costs
        if find_single_candidate(board):
            made_progress = True
            techniques_used["sct"] += 1

        if find_single_position(board):
            made_progress = True
            techniques_used["spt"] += 1

        if find_candidate_lines(board):
            made_progress = True
            techniques_used["clt"] += 1

        if find_double_pairs(board):
            made_progress = True
            techniques_used["dpt"] += 1

        if find_naked_pairs(board):
            made_progress = True
            techniques_used["dj2"] += 1

        if find_hidden_pairs(board):
            made_progress = True
            techniques_used["us2"] += 1

        if find_naked_triple(board):
            made_progress = True
            techniques_used["dj3"] += 1

        if find_hidden_triple(board):
            made_progress = True
            techniques_used["us3"] += 1

        if find_x_wing(board):
            made_progress = True
            techniques_used["xwg"] += 1

        if not made_progress:
            break

    # Calculate the total cost
    for technique, count in techniques_used.items():
        if count > 0:
            first_use_cost, subsequent_use_cost = COSTS[technique]
            total_cost += first_use_cost + subsequent_use_cost * (count - 1)

    return total_cost



# Sample unsolved Sudoku puzzle (transcribed from your provided puzzle)
board = [
    [5, 0, 0, 0, 6, 2, 3, 0, 0],
    [0, 6, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 9, 0, 0, 0, 5, 0, 0],
    [0, 0, 1, 4, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 8, 0, 4, 0],
    [0, 0, 0, 7, 0, 0, 0, 0, 6],
    [0, 7, 0, 0, 0, 1, 0, 8, 4],
    [1, 3, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 0, 8, 2, 0, 0, 0, 0]
]


board = np.array(board)  # Convert to numpy array

difficulty_score = solve_sudoku(board)
print(f"Difficulty Score: {difficulty_score}")
