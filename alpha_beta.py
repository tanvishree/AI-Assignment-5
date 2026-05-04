import math

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

pruned_count = 0   # global counter to show how many branches were skipped


def alpha_beta(node, depth, alpha, beta, is_maximizing):
    global pruned_count
    value, children = node

    if not children or depth == 0:
        return value

    if is_maximizing:
        best = -math.inf
        for child in children:
            score = alpha_beta(child, depth - 1, alpha, beta, False)
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:          # Beta cutoff – MIN won't allow this
                pruned_count += 1
                break
        return best
    else:
        best = math.inf
        for child in children:
            score = alpha_beta(child, depth - 1, alpha, beta, True)
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:          # Alpha cutoff – MAX won't allow this
                pruned_count += 1
                break
        return best

def check_winner(board):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in wins:
        vals = [board[i] for i in combo]
        if vals == ['X','X','X']: return 'X'
        if vals == ['O','O','O']: return 'O'
    return None

def is_full(board):
    return '.' not in board

def print_board(board):
    print()
    for i in range(3):
        print(" | ".join(board[i*3 : i*3+3]))
        if i < 2:
            print("---------")
    print()

def ttt_alpha_beta(board, alpha, beta, is_maximizing):
    winner = check_winner(board)
    if winner == 'X': return 1
    if winner == 'O': return -1
    if is_full(board): return 0

    if is_maximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == '.':
                board[i] = 'X'
                score = ttt_alpha_beta(board, alpha, beta, False)
                board[i] = '.'
                best = max(best, score)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == '.':
                board[i] = 'O'
                score = ttt_alpha_beta(board, alpha, beta, True)
                board[i] = '.'
                best = min(best, score)
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best

def best_move_ab(board):
    best_val = -math.inf
    move = -1
    for i in range(9):
        if board[i] == '.':
            board[i] = 'X'
            val = ttt_alpha_beta(board, -math.inf, math.inf, False)
            board[i] = '.'
            if val > best_val:
                best_val = val
                move = i
    return move

def test_alpha_beta():
    global pruned_count

    print("=" * 40)
    print("TEST 1 – Generic game tree")
    print("=" * 40)
    pruned_count = 0
    result = alpha_beta(SAMPLE_TREE, depth=3, alpha=-math.inf, beta=math.inf,
                        is_maximizing=True)
    print(f"Alpha-Beta value of root: {result}")
    print(f"Branches pruned: {pruned_count}")
    assert result == 6, f"Expected 6, got {result}"
    print("PASS\n")

    print("=" * 40)
    print("TEST 2 – X blocks O's winning move")
    print("=" * 40)
    board = list("XXO" "OO." "X..")
    print("Board:")
    print_board(board)
    move = best_move_ab(board)
    board[move] = 'X'
    print(f"X chose position {move}")
    print_board(board)
    assert move == 5, f"Expected 5, got {move}"
    print("PASS\n")

    print("=" * 40)
    print("TEST 3 – X takes winning move")
    print("=" * 40)
    board = list("XX." "OO." "...")
    print("Board:")
    print_board(board)
    move = best_move_ab(board)
    board[move] = 'X'
    print(f"X chose position {move} and wins!")
    assert check_winner(board) == 'X'
    print("PASS\n")


if __name__ == "__main__":
    test_alpha_beta()
    print("All Alpha-Beta tests passed!")
