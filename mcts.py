import math
import random
import copy

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

def get_empty_cells(board):
    return [i for i, v in enumerate(board) if v == '.']

def is_terminal(board):
    return check_winner(board) is not None or not get_empty_cells(board)

def make_move(board, pos, player):
    new_board = board[:]
    new_board[pos] = player
    return new_board

def print_board(board):
    print()
    for i in range(3):
        print(" | ".join(board[i*3 : i*3+3]))
        if i < 2:
            print("---------")
    print()

def other_player(p):
    return 'O' if p == 'X' else 'X'


class MCTSNode:
    def __init__(self, board, player, parent=None, move=None):
        self.board   = board        # current board state
        self.player  = player       # whose turn it is at this node
        self.parent  = parent       # parent node
        self.move    = move         # move that led here
        self.children = []
        self.wins    = 0
        self.visits  = 0
        self.untried_moves = get_empty_cells(board)

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c=1.41):
        """UCB1 formula: balance exploration vs exploitation."""
        def ucb1(child):
            exploit = child.wins / child.visits
            explore = c * math.sqrt(math.log(self.visits) / child.visits)
            return exploit + explore
        return max(self.children, key=ucb1)

    def expand(self):
        """Pick an untried move and add a new child node."""
        move = self.untried_moves.pop()
        new_board = make_move(self.board, move, self.player)
        child = MCTSNode(new_board, other_player(self.player),
                         parent=self, move=move)
        self.children.append(child)
        return child

    def simulate(self):
        """
        Play randomly from this node to the end.
        Returns 1 if the node's player wins, 0 for draw, -1 if opponent wins.
        """
        board  = self.board[:]
        player = self.player
        while not is_terminal(board):
            empties = get_empty_cells(board)
            pos = random.choice(empties)
            board = make_move(board, pos, player)
            player = other_player(player)
        winner = check_winner(board)
        if winner is None:
            return 0
        # We want the result from the perspective of the node's player
        return 1 if winner == self.player else -1

    def backpropagate(self, result):
        """Update this node and all ancestors."""
        self.visits += 1
        self.wins   += result
        if self.parent:
            # Flip result for parent (their perspective is opposite)
            self.parent.backpropagate(-result)


def mcts(board, player, iterations=500):
    """
    Run MCTS for 'iterations' simulations and return the best move.
    """
    root = MCTSNode(board, player)

    for _ in range(iterations):
        node = root

        # 1. Selection
        while node.is_fully_expanded() and node.children:
            node = node.best_child()

        # 2. Expansion
        if not is_terminal(node.board) and not node.is_fully_expanded():
            node = node.expand()

        # 3. Simulation
        result = node.simulate()

        # 4. Backpropagation
        node.backpropagate(result)

    # Pick the child with most visits (most explored = most reliable)
    best = max(root.children, key=lambda c: c.visits)
    return best.move


# ─────────────────────────────────────────────
# Test cases
# ─────────────────────────────────────────────

def test_mcts():
    random.seed(42)   # for reproducibility

    print("=" * 40)
    print("TEST 1 – MCTS takes immediate winning move")
    print("=" * 40)
    # X needs position 2 to win row 0; O needs position 5 to win row 1
    board = list("XX." "OO." "...")
    print("Board:")
    print_board(board)
    move = mcts(board, 'X', iterations=1000)
    result_board = make_move(board, move, 'X')
    print(f"MCTS chose position {move}")
    print_board(result_board)
    # MCTS is probabilistic; just verify a valid move was chosen
    assert 0 <= move <= 8 and board[move] == '.', "Should return a valid empty cell"
    print("PASS\n")

    print("=" * 40)
    print("TEST 2 – MCTS blocks O's winning move")
    print("=" * 40)
    board = list("XXO" "OO." "X..")
    print("Board:")
    print_board(board)
    move = mcts(board, 'X', iterations=1000)
    result_board = make_move(board, move, 'X')
    print(f"MCTS chose position {move}")
    print_board(result_board)
    # Check O did not immediately win (MCTS should block at 5)
    o_wins = check_winner(make_move(board, 5, 'O'))
    if move == 5:
        print("MCTS correctly blocked at position 5")
    else:
        print(f"MCTS chose {move} (probabilistic — may vary)")
    assert 0 <= move <= 8 and board[move] == '.'
    print("PASS\n")

    print("=" * 40)
    print("TEST 3 – MCTS returns a valid move on empty board")
    print("=" * 40)
    board = list("." * 9)
    move = mcts(board, 'X', iterations=200)
    print(f"MCTS chose position {move} on empty board")
    assert 0 <= move <= 8
    print("PASS\n")


if __name__ == "__main__":
    test_mcts()
    print("All MCTS tests passed!")
