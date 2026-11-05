"""Play tic-tac-toe against a computer in the terminal."""

from __future__ import annotations

import argparse
import random

Board = list[str]
WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def print_board(board: Board) -> None:
    """Print the board, showing numbered positions for empty cells."""
    cells = [mark if mark != " " else str(index + 1) for index, mark in enumerate(board)]
    print(f"\n {cells[0]} | {cells[1]} | {cells[2]}")
    print("---+---+---")
    print(f" {cells[3]} | {cells[4]} | {cells[5]}")
    print("---+---+---")
    print(f" {cells[6]} | {cells[7]} | {cells[8]}\n")


def check_winner(board: Board) -> str | None:
    """Return the winning mark, or None if neither player has won."""
    for first, second, third in WINNING_LINES:
        if board[first] != " " and board[first] == board[second] == board[third]:
            return board[first]
    return None


def available_moves(board: Board) -> list[int]:
    """Return the indexes of all empty cells."""
    return [index for index, mark in enumerate(board) if mark == " "]


def random_move(board: Board) -> int:
    """Choose a random empty cell."""
    moves = available_moves(board)
    if not moves:
        raise ValueError("No moves are available.")
    return random.choice(moves)


def minimax(board: Board, computer_turn: bool) -> int:
    """Score a position recursively: computer wins are 1, human wins -1."""
    winner = check_winner(board)
    if winner == "O":
        return 1
    if winner == "X":
        return -1

    moves = available_moves(board)
    if not moves:
        return 0

    scores = []
    mark = "O" if computer_turn else "X"
    for move in moves:
        board[move] = mark
        scores.append(minimax(board, not computer_turn))
        board[move] = " "

    return max(scores) if computer_turn else min(scores)


def optimal_move(board: Board) -> int:
    """Choose a move with the best minimax score for the computer."""
    moves = available_moves(board)
    if not moves:
        raise ValueError("No moves are available.")

    best_move = moves[0]
    best_score = -2
    for move in moves:
        board[move] = "O"
        score = minimax(board, computer_turn=False)
        board[move] = " "
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def get_human_move(board: Board) -> int:
    """Prompt until the human enters the number of an empty cell."""
    while True:
        choice = input("Choose an empty space (1-9): ").strip()
        if not choice.isdigit() or not 1 <= int(choice) <= 9:
            print("Please enter a number from 1 to 9.")
            continue

        move = int(choice) - 1
        if board[move] != " ":
            print("That space is already taken. Choose an empty one.")
            continue
        return move


def play(strategy: str) -> None:
    """Run a human-versus-computer game."""
    board: Board = [" "] * 9
    print("Tic-tac-toe: you are X, and the computer is O.")

    while True:
        print_board(board)
        board[get_human_move(board)] = "X"

        if check_winner(board) == "X":
            print_board(board)
            print("You win!")
            return
        if not available_moves(board):
            print_board(board)
            print("It's a draw!")
            return

        move = random_move(board) if strategy == "random" else optimal_move(board)
        board[move] = "O"
        print(f"The computer places O in space {move + 1}.")

        if check_winner(board) == "O":
            print_board(board)
            print("The computer wins!")
            return
        if not available_moves(board):
            print_board(board)
            print("It's a draw!")
            return


def main() -> None:
    parser = argparse.ArgumentParser(description="Play tic-tac-toe against the computer.")
    parser.add_argument(
        "--strategy",
        choices=("random", "optimal"),
        default="random",
        help="computer move strategy (default: random)",
    )
    args = parser.parse_args()
    play(args.strategy)


if __name__ == "__main__":
    main()
