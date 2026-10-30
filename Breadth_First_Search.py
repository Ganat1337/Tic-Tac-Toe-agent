from collections import deque

# 1. Create the game board and define coordinates
def generate_game_board():
    return [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9']
    ]

# Mapping board positions to matrix coordinates (row, column)
position_mapper = {
    '1': (0, 0), '2': (0, 1), '3': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '7': (2, 0), '8': (2, 1), '9': (2, 2)
}

# 2. Display the board grid
def display_board(current_grid):
    for line in current_grid:
        print(' | '.join(line))
        print('-' * 9)

# 3. Find all available empty cells
def find_free_cells(grid_state):
    available_cells = []
    for row_idx in range(3):
        for col_idx in range(3):
            if grid_state[row_idx][col_idx] not in ('X', 'O'):
                available_cells.append((row_idx, col_idx))
    return available_cells

# 4. Define winning combinations and check for a winner
VICTORY_LINES = [
    # Horizontal lines
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    # Vertical lines
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    # Diagonal lines
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)]
]

def check_game_winner(grid_state):
    for (r1, c1), (r2, c2), (r3, c3) in VICTORY_LINES:
        first_cell = grid_state[r1][c1]
        second_cell = grid_state[r2][c2]
        third_cell = grid_state[r3][c3]

        if first_cell in ('X', 'O') and first_cell == second_cell == third_cell:
            return first_cell
    return None

# 5. Determine AI agent move using BFS exploration
def compute_ai_move(grid_state):
    open_positions = find_free_cells(grid_state)

    if not open_positions:
        return None

    # Step 1: Immediate win for AI if possible
    for r_pos, c_pos in open_positions:
        temp_grid = [list(r) for r in grid_state]
        temp_grid[r_pos][c_pos] = 'O'

        if check_game_winner(temp_grid) == 'O':
            return (r_pos, c_pos)

    # Step 2: Block opponent's winning move
    for r_pos, c_pos in open_positions:
        temp_grid = [list(r) for r in grid_state]
        temp_grid[r_pos][c_pos] = 'X'

        if check_game_winner(temp_grid) == 'X':
            return (r_pos, c_pos)

    # Step 3: Explore game states using Breadth-First Search (BFS)
    search_queue = deque()

    # Enqueue all initial possible moves for 'O'
    for r_pos, c_pos in open_positions:
        next_board = [list(r) for r in grid_state]
        next_board[r_pos][c_pos] = 'O'
        search_queue.append((next_board, 'X', (r_pos, c_pos)))

    while search_queue:
        active_board, active_turn, initial_step = search_queue.popleft()

        if check_game_winner(active_board) == 'O':
            return initial_step

        if check_game_winner(active_board) == 'X':
            continue

        unoccupied_spots = find_free_cells(active_board)

        if not unoccupied_spots:
            continue

        for r_pos, c_pos in unoccupied_spots:
            simulated_board = [list(r) for r in active_board]
            simulated_board[r_pos][c_pos] = active_turn
            following_turn = 'O' if active_turn == 'X' else 'X'

            search_queue.append((simulated_board, following_turn, initial_step))

    return open_positions[0]

# 6. Main game execution loop
def start_match():
    main_board = generate_game_board()
    human_turn = False  # False: Computer O, True: Human Player X

    while True:
        display_board(main_board)
        free_cells = find_free_cells(main_board)
        if not free_cells:
            break

        if human_turn:
            user_choice = input('Choose a position from 1 to 9: ').strip()
            if user_choice not in position_mapper:
                print('Invalid input. Please choose a number from 1 to 9.')
                continue
            r_coord, c_coord = position_mapper[user_choice]
            if (r_coord, c_coord) not in free_cells:
                print('This position is already taken. Please choose another one.')
                continue
            main_board[r_coord][c_coord] = 'X'
        else:
            r_coord, c_coord = compute_ai_move(main_board)
            main_board[r_coord][c_coord] = 'O'
            print(f'Computer chose position {r_coord * 3 + c_coord + 1}.')

        match_winner = check_game_winner(main_board)
        if match_winner is not None:
            display_board(main_board)
            print('The winner is:', match_winner)
            return match_winner

        human_turn = not human_turn

    display_board(main_board)
    print('It is a draw!')
    return 'Draw'

# Run the game
start_match()