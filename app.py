import random
import os
import sys

# Size of the 2048 board
SIZE = 4


def clear_screen():
    """Clear console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def new_board():
    """Create a new game board."""
    board = [[0] * SIZE for _ in range(SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    return board


def add_new_tile(board):
    """Add a new 2 or 4 tile in a random empty spot."""
    empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if not empty:
        return
    r, c = random.choice(empty)
    board[r][c] = 4 if random.random() < 0.1 else 2


def print_board(board):
    """Display the board."""
    clear_screen()
    print("\n2048 GAME\n")
    for row in board:
        print("+------" * SIZE + "+")
        print("".join(f"|{num:^6}" if num != 0 else "|      " for num in row) + "|")
    print("+------" * SIZE + "+\n")


def compress(row):
    """Compress non-zero tiles to the left."""
    new_row = [num for num in row if num != 0]
    new_row += [0] * (SIZE - len(new_row))
    return new_row


def merge(row):
    """Merge adjacent equal numbers."""
    for i in range(SIZE - 1):
        if row[i] == row[i + 1] and row[i] != 0:
            row[i] *= 2
            row[i + 1] = 0
    return row


def move_left(board):
    new_board = []
    for row in board:
        compressed = compress(row)
        merged = merge(compressed)
        final = compress(merged)
        new_board.append(final)
    return new_board


def move_right(board):
    new_board = [list(reversed(row)) for row in board]
    new_board = move_left(new_board)
    return [list(reversed(row)) for row in new_board]


def transpose(board):
    return [list(row) for row in zip(*board)]


def move_up(board):
    new_board = transpose(board)
    new_board = move_left(new_board)
    return transpose(new_board)


def move_down(board):
    new_board = transpose(board)
    new_board = move_right(new_board)
    return transpose(new_board)


def can_move(board):
    """Check if there are possible moves."""
    for row in board:
        if 0 in row:
            return True
    for r in range(SIZE):
        for c in range(SIZE - 1):
            if board[r][c] == board[r][c + 1]:
                return True
    for c in range(SIZE):
        for r in range(SIZE - 1):
            if board[r][c] == board[r + 1][c]:
                return True
    return False


def check_win(board):
    """Check if player reached 2048."""
    for row in board:
        if 2048 in row:
            return True
    return False


def play_game():
    board = new_board()

    while True:
        print_board(board)

        if check_win(board):
            print("🎉 You reached 2048! You win!")
            break

        if not can_move(board):
            print("💀 No more moves! Game over.")
            break

        move = input("Move (W/A/S/D): ").strip().lower()
        if move not in ('w', 'a', 's', 'd', 'q'):
            continue

        if move == 'q':
            print("👋 Thanks for playing!")
            sys.exit()

        old_board = [row[:] for row in board]

        if move == 'a':
            board = move_left(board)
        elif move == 'd':
            board = move_right(board)
        elif move == 'w':
            board = move_up(board)
        elif move == 's':
            board = move_down(board)

        # Only add a new tile if the board changed
        if board != old_board:
            add_new_tile(board)


if __name__ == "__main__":
    play_game()
