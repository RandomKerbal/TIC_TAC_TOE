import collections
import operator
import random
from collections.abc import Callable

import networkx as nx
from matplotlib.transforms import Bbox

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

t_table: dict[int, int] = dict()
"""Cross-file; transposition table that stores score of seen boards."""

WIN_SCORE: int = 1

EMPTY_BOARD: int
"""Empty board where the first player will be 1."""


# === AI_NAMES Functions ===
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

    t_table.clear()


def sq_of(y: int, x: int) -> int:
    return y * BOARD_LEN + x


def opp_of(plyr: int) -> 1 | 2:
    """
    :return:
        Opponent of given player.
    """
    return 3 - plyr


def plyr_at(board: int, sq: int) -> 0 | 1 | 2:
    """
    :return:
        Number representating player at given square.
    """
    return board // THREE_POW[sq] % 3


def char_of(plyr: int, show_empty: bool = False) -> str:
    """
    :return:
        Letter representationg given player.
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


def place(board: int, move: int, tree: nx.DiGraph | None = None) -> int:
    """
    :return: board after placing given move.
    By reference: updated tree (optional).
    """
    plyr: int = plyr_of(board)
    child_board = (board
                   + opp_of(plyr) * THREE_POW[move]
                   + (opp_of(plyr) - plyr) * THREE_POW[BOARD_AREA])  # update current player
    if tree is not None:
        tree.add_edge(board, child_board, move=move)

    return child_board


def unplace(board: int, sq: int) -> int:
    return board - plyr_of(board) * THREE_POW[sq]  # don't update current player since for vanish mode


def gen_moves(board: int, move: int) -> list[int]:
    """
    Optimization: Moves are sorted to prune low-priority moves that are unlikely to change the result.

    A move GENERALLY has higher priority if:
        Square is connected to, or at the back of another square connected to, either end of a line formed by current player.
        However, priority varies with dist to move and the number of connected lines.

    A move GENERALLY has low priority if:
        Square has adjacent player. However, priority varies with dist to move and the number of adjacent players.
    """
    plyr: int = plyr_of(board)
    move_y, move_x = divmod(move, BOARD_LEN)

    moves = dict()  # key = square, value = priority

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

    plyr: int = plyr_of(board)
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


def recur_search(BOARD: int, moves: list[int], tree: nx.DiGraph, highlight: Callable[[int, int], None]) -> int:
    """
    At root, player is human.
    Uses special case of Alpha-Beta-Negamax Algorithm:
        Current loses if any child wins.
        Current wins if all childs lose.
        Current ties if any child ties and all other childs lose.

    :return:
        WIN_SCORE: current wins
        0: current ties
        -WIN_SCORE: current loses
    """

    def child_is_leaf() -> bool:
        return len(moves) == 1  # not 0 since move not popped yet

    child_board: int
    child_score: int
    tie_child_move: int | None = None

    for i, child_move in enumerate(moves):
        highlight(child_move, BOARD)

        child_board = place(BOARD, child_move, tree)

        if child_board in t_table:
            child_score = t_table[child_board]

        # base case: if any child wins, current loses
        elif is_win(child_board, child_move):
            t_table[child_board] = WIN_SCORE
            child_score = WIN_SCORE

        # base case: if child tie
        elif child_is_leaf():
            t_table[child_board] = 0
            child_score = 0

        else:
            del moves[i]  # optimization: don't modify moves[] for win & leaf nodes
            child_score = recur_search(child_board, moves, tree, highlight)
            moves.insert(i, child_move)

        # if any child wins, current loses
        # no need to check later childs (alpha-beta prunning with alpha = child_score, beta = WIN_SCORE)
        if child_score == WIN_SCORE:
            t_table[BOARD] = -WIN_SCORE
            return -WIN_SCORE

        # if child tie, save move in case no child win
        if child_score == 0 and tie_child_move is None:
            tie_child_move = child_move

    # no child tie means all childs lose
    # if all childs lose, current wins
    if tie_child_move is None:
        t_table[BOARD] = WIN_SCORE
        return WIN_SCORE

    # tie_child_move exists means some child tie
    # if any child is tie,
    highlight(tie_child_move, BOARD)
    t_table[BOARD] = 0
    return 0


def iter_search(ROOT_BOARD: int, moves: set[int], tree: nx.DiGraph, highlight: Callable[[int, int], None]) -> int:
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
        :param MOVE: Move that created this child, already placed on board.
        :param PARENT_PTR: Only root node's move = None and parent_ptr = None.
        """
        MOVE: int | None
        BOARD: int
        PARENT_PTR: int | None
        is_visited: bool

        def __init__(self, MOVE: int | None, BOARD: int, PARENT_PTR: int | None):
            self.MOVE = MOVE
            self.BOARD = BOARD
            self.PARENT_PTR = PARENT_PTR
            self.is_visited = False

        def visit(self):
            self.is_visited = True

            # discard() won't raise error if MOVE is not in moves[]
            # use discard() since MOVE is None at root
            # optimization: don't modify moves[] until visit
            moves.discard(self.MOVE)

            CURR_PTR: int = s.size - 1
            child_board: int

            for child_move in moves:
                highlight(child_move, self.BOARD)

                child_board = place(self.BOARD, child_move, tree)

                if child_board in t_table:

                    # if any child wins
                    if t_table[child_board] == WIN_SCORE:
                        s.pop_all(CURR_PTR)
                        break

                    # if child loses
                    # no tie child in iter search
                    else:
                        continue

                # if any child wins, current loses
                # discard current node & all childs including those already pushed
                if is_win(child_board, child_move):
                    t_table[child_board] = WIN_SCORE
                    s.pop_all(CURR_PTR)
                    break

                # if child tie
                if child_is_leaf():

                    # treat human tie as lose
                    # do not append it to avoid revisit
                    if plyr_of(child_board) == HUMAN:
                        t_table[child_board] = -WIN_SCORE
                        continue

                    # treat bot tie as win
                    else:
                        t_table[child_board] = WIN_SCORE
                        s.pop_all(CURR_PTR)
                        break

                s.push(Node(child_move, child_board, CURR_PTR))

        def revisit(self) -> int:
            s.pop()
            # node must have won to stay
            t_table[self.BOARD] = WIN_SCORE

            # pop siblings & parent, since parent loses
            # if root is popped, outer loop (while s.size) will stop
            s.pop_all(self.PARENT_PTR)
            return self.MOVE

        def is_root(self) -> bool:
            return self.PARENT_PTR is None

        def parent_is_root(self) -> bool:
            return self.PARENT_PTR == 0

        def __repr__(self) -> str:
            return f"(Move: {self.MOVE}, Player: {char_of(plyr_of(self.BOARD))}, Board: {"Root" if self.is_root() else self.BOARD}{", Visited" if self.is_visited else ""})"

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
            moves.add(self.stack[self.size].MOVE)

        def pop_all(self, new_size: int) -> None:
            """
            Pop multiple elements at once, from the top to new_size (inclusive).
            Additional Tasks:
                1. Add the last popped node's move back into moves.
                2. Add the last popped node to transposition table as lose.
            """
            self.size = new_size
            moves.add(self.stack[self.size].MOVE)
            t_table[self.stack[self.size].BOARD] = -WIN_SCORE

        def push(self, node: Node) -> None:
            self.stack[self.size] = node
            self.size += 1

        def __repr__(self) -> str:
            return f"{tuple(node for i, node in enumerate(self.stack) if i < self.size)}"

    HUMAN: int = plyr_of(ROOT_BOARD)
    s: Stack = Stack()
    s.push(Node(None, ROOT_BOARD, None))

    while s.size != 0:
        curr: Node = s.peek()
        if curr.is_visited:
            if curr.parent_is_root():
                MOVE: int = curr.revisit()  # final move
                highlight(MOVE, ROOT_BOARD)
                return MOVE
            else:
                curr.revisit()
        else:
            curr.visit()


def snake_gen_moves(BOARD: int, Y0: int, X0: int) -> "collections.Iterator[tuple[int, int]]":
    y1: int
    x1: int

    for DIR_X, DIR_Y in ADJ:
        y1 = Y0 + DIR_Y
        x1 = X0 + DIR_X

        if 0 <= y1 < BOARD_LEN and 0 <= x1 < BOARD_LEN and not plyr_at(BOARD, sq_of(y1, x1)):
            yield y1, x1


def snake_search_first_move(BOARD: int, MOVES: list[int], Y_CHILD: int, X_CHILD: int, tree: nx.DiGraph, highlight: Callable[[int, int], None]) -> None:
    child_board: int

    for child_move in MOVES:
        highlight(child_move, BOARD)

        child_board = place(BOARD, child_move, tree)

        # noinspection PyTypeChecker
        if snake_search(child_board, Y_CHILD, X_CHILD, *divmod(child_move, BOARD_LEN), tree, highlight) == WIN_SCORE:
            t_table[BOARD] = -WIN_SCORE
            return

    t_table[BOARD] = WIN_SCORE


def snake_search(BOARD: int, Y0: int, X0: int, Y_CHILD: int, X_CHILD: int, tree: nx.DiGraph, highlight: Callable[[int, int], None]) -> int:
    """
    :param Y0:
    :param X0: square that the current player last placed
    :param Y_CHILD:
    :param X_CHILD: square that the child player last placed

    See also :func:`recur_search()`
    """

    def child_is_stuck() -> bool:
        # no child and any square is empty
        return child_move is None and any(not plyr_at(BOARD, sq) for sq in range(BOARD_AREA))

    child_board: int
    child_score: int
    child_move: int | None = None
    tie_child_move: int | None = None

    for y1, x1 in snake_gen_moves(BOARD, Y0, X0):
        child_move = sq_of(y1, x1)

        highlight(child_move, BOARD)

        child_board = place(BOARD, child_move, tree)

        if child_board in t_table:
            child_score = t_table[child_board]

        # base case: win
        elif is_win(child_board, child_move):
            t_table[child_board] = WIN_SCORE
            child_score = WIN_SCORE

        else:
            child_score = snake_search(child_board, Y_CHILD, X_CHILD, y1, x1, tree, highlight)

        # lose
        if child_score == WIN_SCORE:
            t_table[BOARD] = -WIN_SCORE
            return -WIN_SCORE

    # if child stuck or if all childs lose, current win
    if child_is_stuck() or tie_child_move is None:
        t_table[BOARD] = WIN_SCORE
        return WIN_SCORE

    # tie
    highlight(tie_child_move, BOARD)
    t_table[BOARD] = 0
    return 0


def prob_search(ROOT_BOARD: int, moves: list[int], wscores: dict[int, float], highlight: Callable[[int, int], None]) -> None:
    """
    :param wscores: key = root move, val = its weighted score.

    Traverse the entire tree to get each root node's weighted win probability ((# win leaf childs - # lose leaf childs) / (# win leaf childs + # lose leaf childs)).
    Closest to actual machine learning, but least effecient among all AIs.
    Has Statistical Traps: a node with the least lose childs but always lose if best play.

    See also :func:`recur_search()` for player at root.
    """

    def traverse(BOARD: int) -> tuple[int, int]:
        """
        :return:
            child_score (# win leaf childs - # lose leaf childs)
            child_num (# win leaf childs + # lose leaf childs)
        """

        def is_root() -> bool:
            return BOARD == ROOT_BOARD

        def score_by_depth() -> int:
            if plyr_of(child_board) == HUMAN:
                # penalize
                # -2 so loss is more impactful than win
                return len(moves) // 2 - 2
            else:
                # reward
                # len(moves) for depth bonus
                # //2 to only count the layers that are the player's turn
                # +1 because len(moves) can be 0
                return len(moves) // 2 + 1

        child_board: int
        child_score: int = 0
        child_num: int = 0

        for i, child_move in enumerate(moves):
            highlight(child_move, BOARD)

            child_board = place(BOARD, child_move)

            # base case: win
            if is_win(child_board, child_move):
                child_score += score_by_depth()
                child_num += 1

            else:
                del moves[i]
                child_score, child_num = map(
                    operator.add,
                    (child_score, child_num),
                    traverse(child_board)
                )
                moves.insert(i, child_move)

            if is_root() and child_num > 0:
                wscores[child_move] = child_score / child_num
                child_score = 0
                child_num = 0

        return child_score, child_num

    HUMAN: int = plyr_of(ROOT_BOARD)
    traverse(ROOT_BOARD)

    # pick random move from root moves with highest wscore
    # use highlight(), NOT return
    highlight(
        random.choice(
            tuple(move for move, score in wscores.items() if score == max(wscores.values()))
        ),
        ROOT_BOARD
    )


# === Graphing Functions ===
def print_board(BOARD: int, SHOW_AXES: bool = True) -> str:
    """Does not print to console, only return as string."""
    output = ""
    if SHOW_AXES:
        # x axis
        output += " " * 3
        for i in range(BOARD_LEN):
            output += str(i) + " " * (3 - len(str(i)))
        output += "\n"

    for y in range(BOARD_LEN):
        if SHOW_AXES:
            # y axis
            output += str(y) + " " * (3 - len(str(y)))

        for x in range(BOARD_LEN):
            output += char_of(plyr_at(BOARD, sq_of(y, x)), show_empty=True) + " " * 2  # print rows
        output += "\n"

    return output


def midpoint(P0: tuple[float, float], P1: tuple[float, float]) -> tuple[float, float]:
    return (
        (P0[0] + P1[0]) / 2,
        (P0[1] + P1[1]) / 2
    )


def trim_line(P0: tuple[float, float], P1: tuple[float, float], BBOX: Bbox) -> tuple[tuple[float, float], ...] | None:
    """
    Return section of a line segment inside a rectangle.
    Point is defined by P0, P1. Rectangle is defined by matplotlib Bbox.
    :rtype: object
    """

    X_MIN: float = BBOX.x0
    X_MAX: float = BBOX.x1
    Y_MIN: float = BBOX.y0
    Y_MAX: float = BBOX.y1
    X0: float = P0[0]
    Y0: float = P0[1]
    t0: float = 0.0
    t1: float = 1.0

    dx, dy = map(
        operator.sub,
        P1,
        P0
    )

    for p, q in (
            (-dx, X0 - X_MIN),
            (dx, X_MAX - X0),
            (-dy, Y0 - Y_MIN),
            (dy, Y_MAX - Y0),
    ):
        if p == 0:
            if q < 0:
                return None
            continue

        r = q / p

        if p < 0:
            if r > t1:
                return None
            if r > t0:
                t0 = r
        else:
            if r < t0:
                return None
            if r < t1:
                t1 = r

    return (
        (X0 + t0 * dx, Y0 + t0 * dy),
        (X0 + t1 * dx, Y0 + t1 * dy)
    )
