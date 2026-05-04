"""
Minimax Search Algorithm
========================
Minimax is used in two-player games (like Tic-Tac-Toe).
- MAX player tries to get the highest score.
- MIN player tries to get the lowest score.
"""

import math

# ─────────────────────────────────────────────
# Simple game tree for demonstration
# Each node: (value, [children])
# Leaf nodes have no children (empty list)
# ─────────────────────────────────────────────

SAMPLE_TREE = (
    None, [
        (None, [
            (None, [(3, []), (5, [])]),
            (None, [(2, []), (9, [])])
        ]),
        (None, [
            (None, [(1, []), (7, [])]),
            (None, [(4, []), (6, [])])
        ])
    ]
)


def minimax(node, depth, is_maximizing):
    """
    node          : (value, [children])
    depth         : how deep we still want to search
    is_maximizing : True if current player is MAX, False if MIN
    Returns       : best score reachable from this node
    """
    value, children = node

    # Base case – leaf node or depth limit reached
    if not children or depth == 0:
        return value

    if is_maximizing:
        best = -math.inf
        for child in children:
            score = minimax(child, depth - 1, False)   # next level is MIN
            best = max(best, score)
        return best
    else:
        best = math.inf
        for child in children:
            score = minimax(child, depth - 1, True)    # next level is MAX
            best = min(best, score)
        return best


# ─────────────────────────────────────────────
# Tic-Tac-Toe demo
# ─────────────────────────────────────────────

def print_board(board):
    print()
    for i in range(3):
        print(" | ".join(board[i*3 : i*3+3]))
        if i < 2:
            print("---------")
    print()


def check_winner(board):
    """Return 'X', 'O', or None."""
    wins = [
        [0,1,2],[3,4,5],[6,7,8],   # rows
        [0,3,6],[1,4,7],[2,5,8],   # cols
        [0,4,8],[2,4,6]            # diagonals
    ]
    for combo in wins:
        vals = [board[i] for i in combo]
        if vals == ['X','X','X']:
            return 'X'
        if vals == ['O','O','O']:
            return 'O'
    return None


def is_full(board):
    return '.' not in board


def ttt_minimax(board, is_maximizing):
    """Minimax for Tic-Tac-Toe. X=MAX(+1), O=MIN(-1)."""
    winner = check_winner(board)
    if winner == 'X':
        return 1
    if winner == 'O':
        return -1
    if is_full(board):
        return 0

    if is_maximizing:          # X's turn
        best = -math.inf
        for i in range(9):
            if board[i] == '.':
                board[i] = 'X'
                score = ttt_minimax(board, False)
                board[i] = '.'
                best = max(best, score)
        return best
    else:                      # O's turn
        best = math.inf
        for i in range(9):
            if board[i] == '.':
                board[i] = 'O'
                score = ttt_minimax(board, True)
                board[i] = '.'
                best = min(best, score)
        return best


def best_move(board):
    """Find the best move for X using Minimax."""
    best_val = -math.inf
    move = -1
    for i in range(9):
        if board[i] == '.':
            board[i] = 'X'
            val = ttt_minimax(board, False)
            board[i] = '.'
            if val > best_val:
                best_val = val
                move = i
    return move


# ─────────────────────────────────────────────
# Test cases
# ─────────────────────────────────────────────

def test_minimax():
    print("=" * 40)
    print("TEST 1 – Generic game tree")
    print("=" * 40)
    result = minimax(SAMPLE_TREE, depth=3, is_maximizing=True)
    print(f"Minimax value of root: {result}")
    assert result == 6, f"Expected 6, got {result}"
    print("PASS\n")

    print("=" * 40)
    print("TEST 2 – Tic-Tac-Toe: X should block O's win")
    print("=" * 40)
    # O is about to win at position 8
    board = list("XXO" "OO." "X..")
    print("Board before X moves:")
    print_board(board)
    move = best_move(board)
    board[move] = 'X'
    print(f"X chose position {move}")
    print("Board after X moves:")
    print_board(board)
    assert move == 5, f"X should block at position 5, got {move}"
    print("PASS\n")

    print("=" * 40)
    print("TEST 3 – Tic-Tac-Toe: X should win immediately")
    print("=" * 40)
    board = list("XX." "OO." "...")
    print("Board before X moves:")
    print_board(board)
    move = best_move(board)
    board[move] = 'X'
    print(f"X chose position {move} (winning move)")
    print("Board after X moves:")
    print_board(board)
    assert check_winner(board) == 'X', "X should have won"
    print("PASS\n")


if __name__ == "__main__":
    test_minimax()
    print("All Minimax tests passed!")
