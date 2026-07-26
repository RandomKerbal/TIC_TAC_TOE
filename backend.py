import collections
import random
import math
import matplotlib.pyplot as plt
import networkx as nx

BOARD_LEN: int = 0
"""Cross-file; length of board."""

BOARD_AREA: int = 0
"""Cross-file; length**2 of board."""

WIN_LEN: int = 0
"""Cross-file; number of X/O in a row/column/diagonal to win."""

BOTTOM_ROW: int = 0
"""BOARD_LEN * (BOARD_LEN - 1)"""

HALF_W_LEN: int = 0
"""WIN_LEN // 2"""

HALF_W_LEN_INV: int = 0
"""BOARD_LEN - (WIN_LEN // 2)"""

SE_VEC: int = 0
"""BOARD_LEN + 1"""

SW_VEC: int = 0
"""BOARD_LEN - 1"""

S_VEC_HALF_W_LEN: int = 0
"""BOARD_LEN * (WIN_LEN // 2)"""

SE_VEC_HALF_W_LEN: int = 0
"""SE_VEC * (WIN_LEN // 2)"""

SW_VEC_HALF_W_LEN: int = 0
"""SW_VEC * (WIN_LEN // 2)"""

ADJ: tuple[tuple[int, int], ...] = (
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1)
)
"""Cross-file; contains adjacent coordinates (x, y) relative to a cell."""

THREE_POW: tuple[int]
"""
Contains BOARD_LEN**2 + 1 elements. The ith element is the place value of digit i in a base3 number.
For BOARD_LEN = 3,
    - 0th element is 3**8 (place value of 1st digit)
    - 8th element is 3**0 (place value of 8th digit)
"""

win_table: set[int] = set()
"""Cross-file; transposition table that stores board seen as won."""

WIN_SCORE: int = 1

EMPTY_BOARD: int
"""Empty board where the first player will be 1."""


# ==============
#  AI Functions
# ==============

def set_consts(tk_board_len: int | None = None, tk_win_len: int | None = None) -> None:
    global THREE_POW, BOARD_LEN, BOARD_AREA, WIN_LEN, SW_VEC, SE_VEC, BOTTOM_ROW, HALF_W_LEN, HALF_W_LEN_INV, S_VEC_HALF_W_LEN, SE_VEC_HALF_W_LEN, SW_VEC_HALF_W_LEN, EMPTY_BOARD

    if tk_board_len:
        THREE_POW = tuple(3 ** place_val for place_val in range(tk_board_len ** 2, -1, -1))  # counter is reversed since place values increase from left to right
        BOARD_LEN = tk_board_len
        BOARD_AREA = BOARD_LEN ** 2
        SW_VEC = BOARD_LEN - 1
        SE_VEC = BOARD_LEN + 1
        BOTTOM_ROW = BOARD_LEN * SW_VEC
        EMPTY_BOARD = THREE_POW[BOARD_AREA] * 2  # set player before first player as 2

    if tk_win_len:
        WIN_LEN = tk_win_len
        HALF_W_LEN = WIN_LEN // 2

    HALF_W_LEN_INV = BOARD_LEN - HALF_W_LEN
    S_VEC_HALF_W_LEN = BOARD_LEN * HALF_W_LEN
    SE_VEC_HALF_W_LEN = SE_VEC * HALF_W_LEN
    SW_VEC_HALF_W_LEN = SW_VEC * HALF_W_LEN

    win_table.clear()


def sq_of(y: int, x: int) -> int:
    return y * BOARD_LEN + x


def opp_of(plyr: 1 | 2) -> 1 | 2:
    """
    :return:
        Opponent of given player.
    """
    return 3 - plyr


def plyr_at(board: int, sq: int) -> 0 | 1 | 2:
    """
    :return:
        Number representation of player at given square.
    """
    return board // THREE_POW[sq] % 3


def char_of(plyr: 1 | 2, show_empty: bool = False) -> str:
    """
    :return:
        Letter representation of given player.
    """
    if plyr == 1:
        return 'X'
    elif plyr == 2:
        return 'O'
    elif plyr == 0 and show_empty:
        return '∟'


def plyr_of(board: int) -> 1 | 2:
    """
    :return: Player who made the last move.
    """
    return plyr_at(board, BOARD_AREA)  # board has hidden digit at the end to store last player


def place(board: int, sq: int, graph: nx.DiGraph | None = None) -> int:
    """
    :return: Board and graph (optional) after placing given player.
    """
    plyr: 1 | 2 = plyr_of(board)
    child_board = (board
                   + opp_of(plyr) * THREE_POW[sq]
                   + (opp_of(plyr) - plyr) * THREE_POW[BOARD_AREA])  # update current player
    if graph is not None:
        graph.add_edge(board, child_board, label=sq)
    return child_board


def unplace(board: int, sq: int) -> int:
    return board - plyr_of(board) * THREE_POW[sq]  # don't update current player since for vanish mode


def sort_moves(board: int, move: int) -> list[int]:
    """
    A move GENERALLY has higher priority if:
        Square is connected to, or at the back of another square connected to, either end of a line formed by current player.
        However, priority varies with dist to move and the number of connected lines.

    A move GENERALLY has low priority if:
        Square has adjacent player. However, priority varies with dist to move and the number of adjacent players.

    Optimization: Sorting allows prunning low-priority moves that are unlikely to change the result.
    """
    plyr: 1 | 2 = plyr_of(board)
    move_y, move_x = divmod(move, BOARD_LEN)

    moves = {}  # key = square, value = priority

    for sq in range(BOARD_AREA):
        if not plyr_at(board, sq):
            y, x = divmod(sq, BOARD_LEN)
            move_d = max(abs(y - move_y), abs(x - move_x))  # calculate Chebyshev distance

            moves[sq] = moves.get(sq, 0) - move_d  # set distance-dependent base priority

            for dir_x, dir_y in ADJ:
                fwd1_x, fwd1_y = x + dir_x, y + dir_y

                if 0 <= fwd1_x < BOARD_LEN and 0 <= fwd1_y < BOARD_LEN and plyr_at(board, sq_of(fwd1_y, fwd1_x)) == plyr:  # if square has an adjacent player
                    moves[sq] += BOARD_LEN  # +BOARD_LEN ensures the furthest square with 1 adjacent player has higher priority than the closest isolated square

                    fwd2_x, fwd2_y = fwd1_x + dir_x, fwd1_y + dir_y

                    if 0 <= fwd2_x < BOARD_LEN and 0 <= fwd2_y < BOARD_LEN and plyr_at(board, sq_of(fwd2_y, fwd2_x)) == plyr:  # if square is connected to either end of a line
                        moves[sq] += BOARD_LEN * 8  # +BOARD_LEN * 8 ensures the furthest square connected to 1 line has higher priority than a square surrounded by 8 players

                        back1_x, back1_y = x - dir_x, y - dir_y

                        if 0 <= back1_x < BOARD_LEN and 0 <= back1_y < BOARD_LEN:  # if square is at the back of another square connected to either end of a line
                            back1_sq = sq_of(back1_y, back1_x)

                            if not plyr_at(board, back1_sq):
                                moves[back1_sq] = moves.get(back1_sq, 0) + BOARD_LEN * 8

    return sorted(moves, key=moves.get, reverse=True)


def win_dir(board: int, move: int) -> str | None:
    return [
        None,
        "vertically",
        "horizontally",
        "from top left to down right",
        "from top right to down left"
    ][is_win(board, move)]


def is_win(board: int, move: int) -> int:
    # Optimizations:
    # 1. only check for the row/col/diagonals connected to the last move
    # 2. only check for whether the current plyr of this node wins, because only the current plyr is allowed to move (and may win)
    # 3. precalculate constants

    plyr: 1 | 2 = plyr_of(board)
    move_y, move_x = divmod(move, BOARD_LEN)
    start: int
    end: int

    # check column
    # is the first block as it is the fastest to complete
    if ((move_y >= HALF_W_LEN and plyr_at(board, move - S_VEC_HALF_W_LEN) == plyr) or
            (move_y < HALF_W_LEN_INV and plyr_at(board, move + S_VEC_HALF_W_LEN) == plyr)):

        start = move
        while (start >= BOARD_LEN) and plyr_at(board, start - BOARD_LEN) == plyr:
            start -= BOARD_LEN
        end = move
        while (end < BOTTOM_ROW) and plyr_at(board, end + BOARD_LEN) == plyr:
            end += BOARD_LEN

        if end // BOARD_LEN - start // BOARD_LEN + 1 >= WIN_LEN:
            return 1

    # check row
    if ((move_x >= HALF_W_LEN and plyr_at(board, move - HALF_W_LEN) == plyr) or
            (move_x < HALF_W_LEN_INV and plyr_at(board, move + HALF_W_LEN) == plyr)):

        start = move
        while (start % BOARD_LEN > 0) and plyr_at(board, start - 1) == plyr:
            start -= 1
        end = move
        while (end % BOARD_LEN < SW_VEC) and plyr_at(board, end + 1) == plyr:
            end += 1

        if end - start + 1 >= WIN_LEN:
            return 2

    # check top left to down right
    if ((move_y >= HALF_W_LEN <= move_x and plyr_at(board, move - SE_VEC_HALF_W_LEN) == plyr) or
            (move_y < HALF_W_LEN_INV > move_x and plyr_at(board, move + SE_VEC_HALF_W_LEN) == plyr)):

        start = move
        while (start >= BOARD_LEN) and (start % BOARD_LEN > 0) and plyr_at(board, start - SE_VEC) == plyr:
            start -= SE_VEC
        end = move
        while (end < BOTTOM_ROW) and (end % BOARD_LEN < SW_VEC) and plyr_at(board, end + SE_VEC) == plyr:
            end += SE_VEC

        if (end // BOARD_LEN - start // BOARD_LEN) + 1 >= WIN_LEN:
            return 3

    # check top right to down left
    if ((move_y >= HALF_W_LEN and move_x < HALF_W_LEN_INV and plyr_at(board, move - SW_VEC_HALF_W_LEN) == plyr) or
            (move_y < HALF_W_LEN_INV and move_x >= HALF_W_LEN and plyr_at(board, move + SW_VEC_HALF_W_LEN) == plyr)):

        start = move
        while (start >= BOARD_LEN) and (start % BOARD_LEN < SW_VEC) and plyr_at(board, start - SW_VEC) == plyr:
            start -= SW_VEC
        end = move
        while (end < BOTTOM_ROW) and (end % BOARD_LEN > 0) and plyr_at(board, end + SW_VEC) == plyr:
            end += SW_VEC

        if (end // BOARD_LEN - start // BOARD_LEN) + 1 >= WIN_LEN:
            return 4

    return 0


def exhaust(gen: "collections.Iterator[int]") -> int:
    """
    Exhaust all yield values in a generator function and get the return value.
    """
    try:
        while True:
            next(gen)
    except StopIteration as e:
        return e.value


def recur_search(board: int, moves: list[int], is_root: bool, graph: nx.DiGraph | None) -> "collections.Iterator[int] | int":
    """
    At root, player is human.
    Uses Alpha-Beta-Negamax-ish Algorithm:
        Current loses if any child wins.
        Current wins if all child loses.

    Uses generator function's lazy evaluation when iterated to fake multithreading.
    :yield:
        Move in moves in order, until after finding the best move.

    :return:
        WIN_SCORE: current wins
        0: current ties
        -WIN_SCORE: current loses
    """

    def child_is_leaf() -> bool:
        return len(moves) == 1  # not 0 since move not popped yet

    child_board: int
    best_child_score: int = -WIN_SCORE

    for i, move in enumerate(moves):
        yield move
        child_board = place(board, move)

        # since any child wins, curr loses
        if child_board in win_table:
            return -WIN_SCORE

        if is_win(child_board, move):
            win_table.add(child_board)
            return -WIN_SCORE

        # must come after is_win()
        if child_is_leaf():
            continue

        del moves[i]  # optimization: don't modify for win & leaf nodes

        best_child_score = max(
            best_child_score,
            exhaust(recur_search(
                place(board, move, graph),
                moves, False, graph)
            )
        )
        moves.insert(i, move)

        # since any child wins, current loses (alpha-beta prunning with alpha = best_child_score, beta = WIN_SCORE)
        if best_child_score == WIN_SCORE:
            win_table.add(child_board)

            if is_root and graph is not None:
                print_tree(graph, recip_tree_pos(graph, board))

            return -WIN_SCORE

    # since all child lose, current wins
    if best_child_score == -WIN_SCORE:
        return WIN_SCORE

    # base case: tie
    return 0


def iter_search(root_board: int, moves: set[int], graph: nx.DiGraph | None) -> "collections.Iterator[int]":
    """
    See also :func:`recur_search()` for player at root.

    Algorithm:
        When traversing down (visit):
            Current loses if any child wins -> pops current -> no revisit.
            Current wins if all childs lose -> current stays -> will revisit.

        When traversing up (revisit):
            All revisited nodes must have won -> parent loses -> pops siblings & parent.

    Inspired by codons in RNA.
    """

    def child_is_leaf() -> bool:
        return len(moves) == 1  # not 0 since move not popped yet

    class Node:
        """
        :param move: Move that created this child, already placed on board.
        :param parent_ptr: Only root node's move = None and parent_ptr = None.
        """
        move: int | None
        board: int
        parent_ptr: int | None
        is_visited: bool

        def __init__(self, move: int | None, board: int, parent_ptr: int | None):
            self.move = move
            self.board = board
            self.parent_ptr = parent_ptr
            self.is_visited = False

        def visit(self) -> "collections.Iterator[int]":
            self.is_visited = True

            if not self.is_root():
                moves.remove(self.move)  # optimization: don't modify until visit

            curr_ptr: int = s.size - 1
            child_board: int

            for move in moves:
                yield move
                child_board = place(self.board, move, graph)

                # since any child wins, current loses
                # discard current node & all childs including those already pushed
                if child_board in win_table:
                    s.pop_all(curr_ptr)
                    break

                if is_win(self.board, move):
                    win_table.add(child_board)
                    s.pop_all(curr_ptr)
                    break

                # must come after is_win()
                if child_is_leaf():

                    # treat human tie leaf as lose
                    # do not append it to avoid revisit
                    if plyr_of(child_board) == HUMAN:
                        continue

                    # treat bot tie leaf as win
                    else:
                        s.pop_all(curr_ptr)
                        break

                s.push(Node(move, child_board, curr_ptr))

        def revisit(self) -> int:
            s.pop()
            # node must have won to stay
            win_table.add(self.board)

            # since parent loses, pop siblings & parent
            # if root is popped, outer loop (while s.size) will stop
            s.pop_all(self.parent_ptr)
            return self.move

        def is_root(self) -> bool:
            return self.parent_ptr is None

        def parent_is_root(self) -> bool:
            return self.parent_ptr == 0

        def __repr__(self) -> str:
            return f"(Move: {self.move}, Player: {char_of(plyr_of(self.board))}, Board: {"Root" if self.is_root() else self.board}{", Visited" if self.is_visited else ""})"

    class Stack:
        stack: list[Node | None] = [None] * sum(range(1, len(moves) + 1))  # preallocate size. Max size is (n) + (n-1) + (n-2) + ... + 1, where n = len(moves).
        size: int = 0

        def peek(self) -> Node:
            return self.stack[self.size - 1]

        def pop(self) -> None:
            """
            Pop and add the popped node's move back into moves.
            """
            self.size -= 1
            moves.add(self.stack[self.size].move)

        def pop_all(self, new_size: int) -> None:
            """
            Pop multiple elements at once, from the top to new_size (inclusive).
            Add the last popped node's move back into moves.
            """
            self.size = new_size
            moves.add(self.stack[self.size].move)

        def push(self, node: Node) -> None:
            self.stack[self.size] = node
            self.size += 1

        def __repr__(self) -> str:
            return f"{list(node for i, node in enumerate(self.stack) if i < self.size)}"

    HUMAN: int = plyr_of(root_board)
    s: Stack = Stack()
    s.push(Node(None, root_board, None))

    while s.size != 0:
        curr: Node = s.peek()
        if curr.is_visited:
            if curr.parent_is_root():
                yield curr.revisit()  # final move
            else:
                curr.revisit()
        else:
            if curr.is_root():
                yield from curr.visit()  # move in moves
            else:
                exhaust(curr.visit())

    if graph:
        print_tree(graph, recip_tree_pos(graph, root_board))


def bot_iter_v2(root_board: int, bot: int, moves: set):
    for root_move in moves:
        yield root_move

        stack = [(root_board, root_move, moves.difference({root_move}), bot, eldest_ptr := 0,)]

        def truncate(new_size: int):
            del stack[new_size:]

        def is_eldest():
            return eldest_ptr == len(stack)  # if eldest pointer is pointing to its own square

        while stack:
            parent_board, move, moves, plyr, eldest_ptr = stack.pop()

            board = place(parent_board, plyr, move)

            if is_win(parent_board, plyr, move) or (len(moves) == 0 and plyr == bot):
                win_table.add(parent_board)
                if stack:
                    ww_board, _, _, parent_plyr, parent_eldest_ptr = stack[eldest_ptr - 1]

                    if parent_plyr == plyr:
                        win_table.add(ww_board)
                        truncate(parent_eldest_ptr)  # pop parent and all its siblings and children
                        if not stack and bot == parent_plyr:
                            return
                        continue

                    else:
                        truncate(eldest_ptr)  # pop curr and all its siblings
                        if not stack and bot == plyr:
                            return
                        continue

                elif bot == plyr:
                    return

            elif len(moves) == 0 and is_eldest() and plyr == opp_of(bot):
                win_table.add(board)
                if stack:
                    ww_board, _, _, parent_plyr, parent_eldest_ptr = stack[-1]

                    if parent_plyr == plyr:
                        continue

                    elif parent_plyr != plyr:
                        truncate(parent_eldest_ptr)  # pop parent and all its siblings
                        if not stack and bot == parent_plyr:
                            return
                        continue

                elif bot != plyr:
                    return

            else:
                board = place(parent_board, plyr, move)

                child_plyr = opp_of(plyr)
                child_eldest_ptr = len(stack)
                for child_move in moves:
                    stack.push((board, child_move, moves.difference({child_move}), child_plyr, child_eldest_ptr,))


def snake_gen_moves(board: int, y0: int, x0: int) -> "collections.Iterator[tuple[int, int]]":
    for dir_x, dir_y in ADJ:
        y1 = y0 + dir_y
        x1 = x0 + dir_x

        if 0 <= y1 < BOARD_LEN and 0 <= x1 < BOARD_LEN and not plyr_at(board, sq_of(y1, x1)):
            yield y1, x1


def snake_search(board: int, y0: int, x0: int, y_child: int, x_child: int, is_root: bool, graph: nx.DiGraph | None) -> "collections.Iterator[int] | int":
    """
    :param y0:
    :param x0: square that the given player last placed
    :param y_child:
    :param x_child: square that the other player last placed

    See also :func:`recur_search()`
    """

    best_child_score: int
    child_board: int

    for y1, x1 in snake_gen_moves(board, y0, x0):
        move = sq_of(y1, x1)
        yield move
        child_board = place(board, move, graph)

        # base case: win
        if child_board in win_table:
            return WIN_SCORE

        if is_win(child_board, move):
            win_table.add(child_board)
            return WIN_SCORE

        best_child_score = max(best_child_score, exhaust(snake_search(child_board, y_child, x_child, y1, x1, False, graph)))

        # lose (technically alpha-beta prunning)
        if best_child_score == WIN_SCORE:
            win_table.add(child_board)
            return -WIN_SCORE

    # win
    if best_child_score == -WIN_SCORE:

        if is_root and graph is not None:
            print_tree(graph, recip_tree_pos(graph, board))

        return WIN_SCORE

    # base case: tie
    return 0


def prob_ai(root_board: int, moves: list[int], has_graph: bool) -> "collections.Iterator[int]":
    """
    Traverse the entire tree to get each root node's weighted win probability ((# win leaf childs - # lose leaf childs) / (# win leaf childs + # lose leaf childs)).
    Closest to actual machine learning, but least effecient.
    Has Statraps (Statistical Traps): a node with the least lose childs but always lose if best play.

    See also :func:`recur_search()` for player at root.
    """

    def traverse(board: int) -> tuple[int, int]:
        """
        :return:
            child_score (# win leaf childs - # lose leaf childs)
            child_num (# win leaf childs + # lose leaf childs)
        """

        def is_root() -> bool:
            return board == root_board

        def score_by_depth() -> int:
            if plyr_of(child_board) == HUMAN:
                # reward
                # len(moves) for depth bonus
                # //2 to only count the layers with the player's turn
                # +1 because len(moves) can be 0
                return len(moves) // 2 + 1
            else:
                # penalize
                return len(moves) // 2 - 1

        child_score: int
        child_num: int

        for i, move in enumerate(moves):
            child_board: int = place(board, move)

            # base case: win
            if is_win(child_board, move):
                child_score += score_by_depth()
                child_num += 1

            else:
                del moves[i]
                child_score, child_num = (
                    x + y for x, y in zip(
                    (child_score, child_num),
                    traverse(child_board))
                )
                moves.insert(i, move)

            if is_root() and child_num > 0:
                wscores[move] = child_score / child_num
                child_score = 0
                child_num = 0

        return child_score, child_num

    wscores = {move: 0.0 for move in moves}  # key = root move, val = its score
    HUMAN: int = plyr_of(root_board)
    traverse(root_board)

    if has_graph:
        plt.Figure()
        bar = plt.bar(list(wscores.keys()), list(wscores.values()), color="MediumSpringGreen")
        plt.bar_label(bar, label_type="center")
        plt.locator_params(axis="x")  # set x tick interval
        plt.xlabel("Root Move")
        plt.ylabel("Weighted Win Probability")
        plt.title(f"{plt.gca().get_ylabel()} of each {plt.gca().get_xlabel()}")
        plt.show(block=False)

    # list root_move(s) with the max wscore to pick randomly
    yield random.choice(  # DO NOT use return
        [move for move, score in
         wscores.items()
         if score == max(wscores.values())]
    )
    return None


# ==================
# Graphing Functions
# ==================
def print_board(board: int, show_axis: bool = True) -> str:
    """Does not print to console, only return as string."""
    output = ""
    if show_axis:
        # x axis
        output += " " * 3
        for i in range(BOARD_LEN):
            str_i = str(i)
            output += str_i + " " * (3 - len(str_i))
        output += "\n"

    for y in range(BOARD_LEN):
        if show_axis:
            # y axis
            str_i = str(i)
            output += str_i + " " * (3 - len(str_i))

        for x in range(BOARD_LEN):
            output += char_of(plyr_at(board, sq_of(y, x)), show_empty=True) + " " * 2  # print rows
        output += "\n"

    return output


def print_tree(tree: nx.DiGraph, pos: dict):
    def recapture_bg(_=None):
        """Retake screenshot after zoom or pan."""
        nonlocal bg
        fig.canvas.draw()  # redraw canvas to get correct bbox
        bg = fig.canvas.copy_from_bbox(fig.bbox)

    def on_click(event):
        """If mouse clicked on a node, update fig_text to show its detailed information and animate scaling of clicked node."""
        is_node, info = fig_nodes.contains(event)

        if is_node:  # if clicked on a node
            # get the node under cursor and its label
            node = tree_2d[info['ind'][0]]
            label = fig_labels[node]

            # UPDATE FIG_TEXT
            parents = list(tree.predecessors(node))
            children = list(tree.successors(node))

            fig_text.set_text(
                f"Node: {node}\n"
                f"Decoded:\n{print_board(node, show_axis=False)}"
                f"{len(parents)} Parent: {parents}\n"
                f"{len(parents)} Eldest Sibling: {[next(tree.successors(parent)) for parent in parents]}\n"
                f"{max(dict(tree.out_degree()).values()) + (pos[node][1] + 1) - len(children)} Skipped Children*\n"  # total # of children of root (assume root has max # of children) - # of layers away from root (root = -1) + # of visited children
                f"{len(children)} Visited Children: {children}"
            )

            # DRAW
            def on_timer():
                nonlocal frame
                k: int = 8  # must be integer
                scale = 1 + 0.5 * math.sin(math.pi * frame / k)
                label.set_fontsize(10 * scale)  # 10 is moveal size of node

                fig.canvas.restore_region(bg)  # revert background to erase previous frame
                fig.draw_artist(fig_text)  # show temporary fig_text while waiting for label animation
                fig.draw_artist(label)
                fig.canvas.blit(fig.bbox)

                frame += 1
                if frame > 8:
                    timer.stop()
                    fig.canvas.draw_idle()
                    return

            frame = 0
            timer = fig.canvas.new_timer(interval=30, callbacks=[(on_timer, (), {})])
            timer.start()

        else:
            fig_text.set_text(
                f"Total # of Nodes: {tree.number_of_nodes()}"
            )
            fig.canvas.draw_idle()

    def on_move(event):
        """If mouse hover over a node, change cursor to hand2."""
        is_node, info = fig_nodes.contains(event)
        fig.canvas.get_tk_widget().config(cursor="hand2" if is_node else "")

    tree_2d: list = list(tree.nodes)

    fig = plt.figure()
    plt.axis("off")
    plt.tight_layout()

    # draw nodes and edges separately to set picker on nodes
    fig_nodes = nx.draw_networkx_nodes(
        tree, pos, node_shape="s", alpha=0.0
    )
    # noinspection PyTypeChecker
    fig_nodes.set_picker(True)

    fig_labels: dict = {}
    for node, (x, y) in pos.items():  # replaced nx.draw_networkx_labels to color each label separately
        fig_labels[node] = plt.text(
            x, y, node,
            ha="center", va="center",
            bbox=dict(facecolor="SeaGreen" if node in win_table else "MediumSpringGreen", boxstyle="round", pad=0.4, linewidth=0.5),
            color="white" if node in win_table else "black",
            family="Arial", weight="bold", size=10
        )

    nx.draw_networkx_edges(
        tree, pos, arrows=False, alpha=0.75
    )
    nx.draw_networkx_edge_labels(
        tree, pos, nx.get_edge_attributes(tree, "label"),
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.5, boxstyle="circle", pad=0),
        font_color="crimson", font_family="Arial", font_size=10, rotate=False
    )

    bg = None
    recapture_bg()  # screenshot background WITHOUT fig_text

    fig_text = plt.text(
        0.0, 0.0, f"Total # of Nodes: {tree.number_of_nodes()}\nClick a node to show details",
        transform=plt.gca().transAxes,  # use axes fraction for positioning
        bbox=dict(facecolor="white", edgecolor="gray", alpha=0.8, boxstyle="square", pad=0.75),
        family="Consolas", linespacing=1.5
    )

    fig.gca().callbacks.connect("xlim_changed", recapture_bg)
    fig.gca().callbacks.connect("ylim_changed", recapture_bg)
    fig.canvas.mpl_connect("resize_event", recapture_bg)
    fig.canvas.mpl_connect("button_press_event", on_click)
    fig.canvas.mpl_connect("motion_notify_event", on_move)
    plt.show(block=True)


def fac_tree_pos(tree, root=None) -> dict:
    """
    Creates a hierarchical layout for a directed factorial tree.
    In a factorial tree, each node has at least one less children than its parent
    Use this when you don't know the maximum number of children, but you know the maximum number of layers

    :param tree: networkx graph object (must be directed).
    :param root: root node of the tree (if None, chooses an arbitrary node).
    :return:
        Dictionary with key = node, val = coord of the node saved as a tuple (x, y).
    """

    def assign_pos(layer: int, children, parent_x: float):
        """
        Recursively update coord of parent nodes and calculate coord of child nodes.
        """
        if children:
            layer_neg1 = layer - 1
            sep_count = len(children) - 1  # total number of separations between children
            sep_dist = factorials[layer + 1] / max(1, sep_count)  # separation distance between each child

            # assign positions for each child
            start_x = parent_x - (sep_count / 2) * sep_dist
            for i, child in enumerate(children):
                child_x = start_x + i * sep_dist
                pos[child] = (child_x, layer_neg1)
                assign_pos(layer_neg1, list(tree.successors(child)), child_x)

    if root is None:
        root = next(iter(tree))  # select an arbitrary root if not provided

    root_children = list(tree.successors(root))
    max_layer = len(root_children)  # the maximum number of layers, assuming the bottommost layer is 1
    factorials = tuple(math.factorial(layer) for layer in range(max_layer + 2))

    pos = {root: (0, max_layer)}
    assign_pos(max_layer, root_children, 0.0)
    return pos


def recip_tree_pos(tree, root=None) -> dict:
    """
    Creates a hierarchical layout for a directed reciprocal tree.
    In a reciprocal tree, every node has n or fewer children.
    Use this when you don't know the maximum number of layers, but you know the maximum number of children.

    See :func:`fac_tree_pos()` for params and return.
    """

    def assign_pos(layer: int, children, parent_x: float):
        """See :func:`assign_pos()` in :func:`fac_tree_pos()`"""
        if children:
            layer_neg1 = layer - 1
            sep_dist = max_sep_count ** layer  # separation distance between each child. DO NOT use 1/(max_sep_count**layer) as layer is negative.

            # assign positions for each child
            start_x = parent_x - (len(children) - 1) / 2 * sep_dist
            for i, child in enumerate(children):
                child_x = start_x + i * sep_dist
                pos[child] = (child_x, layer_neg1)
                assign_pos(layer_neg1, list(tree.successors(child)), child_x)

    if root is None:
        root = next(iter(tree))  # select an arbitrary root if not provided

    max_sep_count = max(degree for _, degree in tree.degree()) - 1  # the maximum number of separations between children of any node (maximum number of children - 1)
    root_children = list(tree.successors(root))

    pos = {root: (0, 0)}
    assign_pos(0, root_children, 0.0)
    return pos
