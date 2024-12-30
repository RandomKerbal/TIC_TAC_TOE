import random
import math
import matplotlib.pyplot as plt
import networkx as nx

three_pow = ()
"""
A universal tuple containing 'board_sz**2' integer. Each integer = the place value of a digit with the same index in a base3 number.
E.g.: in a base 3 3x3 board:
    - the element at index 0 = 3^8 (8th place value)
    - the element at index 8 = 3^0 (0th place value)

Initialized as empty tuple(). Value is afterwards assigned by the function set_three_pow().
"""
# TODO: universalize main_board, board_len, win_len, pc, simmable_inds


def set_win_len(board_len: int) -> int:
    return board_len//4 + 3


def set_three_pow(board_len: int):
    """
    Initialize the universal var three_pow.
    """
    global three_pow
    three_pow = tuple(3**place_val for place_val in range(board_len**2 - 1, -1, -1))  # counter is reversed as the order of place values is the reverse of index order


def opp(original: int) -> int:
    """
    (opponent)

    Returns 1 when input 2; 2 when input 1.
    """
    return 3 - original


def convert_symbol(base3: int, show_empty: bool = False) -> str:
    """
    Converts a symbol from base3 to readable character.
    """
    if base3 == 1:
        return 'X'
    elif base3 == 2:
        return 'O'
    elif base3 == 0 and show_empty:
        return '∟'


def get_symbol(board: int, ind: int) -> int:
    """
    Extracts the base3 symbol of the cell of given index.
    """
    return board // three_pow[ind] % 3


def print_board(board: int, board_len: int):
    """
    Print the board in the following format:\n
         1  2  3  ...\n
    1  ∟ ∟ ∟\n
    2  ∟ ∟ ∟\n
    3  ∟ ∟ ∟\n
    ...
    """
    print('\t', end='')
    for i in range(board_len):
        print(str(i + 1) + ' ' * (4 - len(str(i+2))), end='')  # print the col number
    for i in range(board_len):
        print('\n' + str(i + 1) + ' ' * (3 - len(str(i+1))), end='')  # print the row number
        for ii in range(i*board_len, (i+1)*board_len):
            print(' ' + convert_symbol(get_symbol(board, ii), show_empty=True), end='  ')  # print the symbols in the row
    print(end='\n')


def fac_tree_layout(tree, root=None) -> dict:
    """
    Creates a hierarchical layout for a directed factorial tree graph. Property of a factorial tree graph:
        |
        - the total number of children from 1 parent equals the total number of parents minus 1.

    :param tree: networkx graph object (must be directed).
    :param root: root node of the tree (if None: chooses an arbitrary node).
    :return: dictionary whose key = node, val = coord of the node saved as a tuple (x, y).
    """
    if root is None:
        root = next(iter(tree))  # select an arbitrary root if not provided

    def assign_pos(parent, parent_x: float = 0.0, parent_y: float = 0.0):
        """
        Recursively updating coord of parent nodes and calculating coord of child nodes.
        """
        pos[parent] = (parent_x, parent_y)
        children = list(tree.successors(parent))
        if children:
            total_child_sep = math.factorial(len(children)) - math.factorial(len(children)-1)
            child_sep = total_child_sep / max(1, (len(children)-1))

            for i, child in enumerate(children):
                assign_pos(child, parent_x - total_child_sep/2 + i*child_sep, parent_y - 1)

    pos = {}
    assign_pos(root)
    return pos


def plyr_win_formation(board: int, board_len: int, win_len: int, plyr: int, origin: int) -> str | None:
    half_win_len = win_len // 2
    board_len_sub1 = board_len-1
    board_len_add1 = board_len+1
    bsz_sub_hwl = board_len - half_win_len
    max_row_ind = board_len * board_len_sub1

    origin_col = origin % board_len
    origin_row = origin // board_len

    # check column
    # I put check column as the first function as it is the fastest to complete
    if (origin_row >= half_win_len and get_symbol(board, origin - board_len * half_win_len) == plyr) or (origin_row < bsz_sub_hwl and get_symbol(board, origin + board_len * half_win_len) == plyr):

        start = origin
        while (start >= board_len) and get_symbol(board, start - board_len) == plyr:
            start -= board_len
        end = origin
        while (end < max_row_ind) and get_symbol(board, end + board_len) == plyr:
            end += board_len

        if end // board_len - start // board_len + 1 >= win_len:
            return 'vertically'

    # check row
    if (origin_col >= half_win_len and get_symbol(board, origin - half_win_len) == plyr) or (origin_col < bsz_sub_hwl and get_symbol(board, origin + half_win_len) == plyr):

        start = origin
        while (start % board_len > 0) and get_symbol(board, start - 1) == plyr:
            start -= 1
        end = origin
        while (end % board_len < board_len_sub1) and get_symbol(board, end + 1) == plyr:
            end += 1

        if end - start + 1 >= win_len:
            return 'horizontally'

    # check top left to down right
    if (origin_row >= half_win_len <= origin_col and get_symbol(board, origin - board_len_add1 * half_win_len) == plyr) or (
            origin_row < bsz_sub_hwl > origin_col and get_symbol(board, origin + board_len_add1 * half_win_len) == plyr):

        start = origin
        while (start >= board_len) and (start % board_len > 0) and get_symbol(board, start - board_len_add1) == plyr:
            start -= board_len_add1
        end = origin
        while (end < max_row_ind) and (end % board_len < board_len_sub1) and get_symbol(board, end + board_len_add1) == plyr:
            end += board_len_add1

        if (end // board_len - start // board_len) + 1 >= win_len:
            return 'from top left to down right'

    # check top right to down left
    if (origin_row >= half_win_len and origin_col < bsz_sub_hwl and get_symbol(board, origin - board_len_sub1 * half_win_len) == plyr) or (
            origin_row < bsz_sub_hwl and origin_col >= half_win_len and get_symbol(board, origin + board_len_sub1 * half_win_len) == plyr):

        start = origin
        while (start >= board_len) and (start % board_len < board_len_sub1) and get_symbol(board, start - board_len_sub1) == plyr:
            start -= board_len_sub1
        end = origin
        while (end < max_row_ind) and (end % board_len > 0) and get_symbol(board, end + board_len_sub1) == plyr:
            end += board_len_sub1

        if (end // board_len - start // board_len + 1) >= win_len:
            return 'from top right to down left'

    return None


# ALL FUNCTIONS BELOW ARE FOR THE AI
def prune(board: int, board_len: int, opp: int, origin: int) -> list:
    """
    Limits indexes that PC can simulate to the 13 empty indexes with the highest priority.
    Assigns priority to indexes accordingly:
        1. if index is connected to, or at the back of another index connected to, either end of a line formed by player: within the high priorities; varies with dist to origin and the number of connected lines.
        2. index has adjacent player cell -> within the low priorities; varies with dist to origin and the number of adjacent player cells.
    :return: simmable_inds
    """
    # convert origin to coords
    origin_row = origin // board_len
    origin_col = origin % board_len

    # setup coords (x_coord, y_coord) of 8 indexes around a center
    adjacents = (
        (-1, -1), (0, -1), (1, -1),  # top-left, top-right
        (-1, 0),           (1, 0),   # left, right
        (-1, 1),  (0, 1),  (1, 1)    # bottom-left, bottom-right
    )

    ind_priority = {}  # key = index of cell, value = priority

    for ind in range(board_len**2):
        if get_symbol(board, ind) == 0:
            row = ind // board_len
            col = ind % board_len
            origin_d = max(abs(row - origin_row), abs(col - origin_col))  # calculate Chebyshev distance

            ind_priority[ind] = ind_priority.get(ind, 0) - origin_d  # set distance-dependent base priority

            for dir_x, dir_y in adjacents:
                fwd1_row = row + dir_y
                fwd1_col = col + dir_x

                if 0 <= fwd1_row < board_len and 0 <= fwd1_col < board_len and get_symbol(board, fwd1_row * board_len + fwd1_col) == opp:  # if ind has an adjacent player cell

                    ind_priority[ind] += board_len  # +board_len ensures the furthest index with 1 adjacent player cell has higher priority than the closest lone index

                    fwd2_row = fwd1_row + dir_y
                    fwd2_col = fwd1_col + dir_x

                    if 0 <= fwd2_row < board_len and 0 <= fwd2_col < board_len and get_symbol(board, fwd2_row * board_len + fwd2_col) == opp:  # if ind is connected to either end of a line formed by player

                        ind_priority[ind] += board_len * 8  # +board_len*8 ensures the furthest index connected to 1 line formed by player has higher priority than an index surrounded by 8 player cells

                        back1_row = row - dir_y
                        back1_col = col - dir_x

                        if 0 <= back1_row < board_len and 0 <= back1_col < board_len:  # if ind is at the back of another ind connected to either end of a line formed by player
                            back1_ind = back1_row * board_len + back1_col

                            if get_symbol(board, back1_ind) == 0:
                                ind_priority[back1_ind] = ind_priority.get(back1_ind, 0) + board_len*8

    print(f'\nIndex Priority: {ind_priority}')

    # get the 14 cells with top priority
    simmable_inds = sorted(ind_priority, key=ind_priority.get, reverse=True)[:15]

    print(f'Simulatable Indexes: {simmable_inds}')

    return simmable_inds


def pc_input(pc: int, main_board: int, board_len: int, win_len: int, simmable_inds: list, is_debugging: bool) -> int:
    board_len_sub1 = board_len-1
    board_len_add1 = board_len+1
    half_win_len = win_len // 2
    bsz_sub_hwl = board_len - half_win_len
    max_row_ind = board_len * board_len_sub1

    def is_plyr_win(board: int, plyr: int, origin: int) -> bool:
        """
        :param board: same as board in pc_input
        :param origin: latest move made on the board
        :param plyr: player who made the move at 'origin'
        """
        # OPTIMIZATION:
        # 1. only check for the row/col/diagonals connected to the origin
        # 2. only check for whether the current plyr of this node wins, because only the current plyr is allowed to move (and may win)
        # 3. pre-calculate only once: half_win_len, board_len_sub1, board_len_add1, bsz_sub_hwl, max_row_ind, origin_col, origin_row

        origin_col = origin % board_len
        origin_row = origin // board_len

        # check column
        # I put check column as the first function as it is the fastest to complete
        if (origin_row >= half_win_len and get_symbol(board, origin - board_len * half_win_len) == plyr) or (origin_row < bsz_sub_hwl and get_symbol(board, origin + board_len * half_win_len) == plyr):

            start = origin
            while (start >= board_len) and get_symbol(board, start - board_len) == plyr:
                start -= board_len
            end = origin
            while (end < max_row_ind) and get_symbol(board, end + board_len) == plyr:
                end += board_len

            if end // board_len - start // board_len + 1 >= win_len:
                return True

        # check row
        if (origin_col >= half_win_len and get_symbol(board, origin - half_win_len) == plyr) or (origin_col < bsz_sub_hwl and get_symbol(board, origin + half_win_len) == plyr):

            start = origin
            while (start % board_len > 0) and get_symbol(board, start - 1) == plyr:
                start -= 1
            end = origin
            while (end % board_len < board_len_sub1) and get_symbol(board, end + 1) == plyr:
                end += 1

            if end - start + 1 >= win_len:
                return True

        # check top left to down right
        if (origin_row >= half_win_len <= origin_col and get_symbol(board, origin - board_len_add1 * half_win_len) == plyr) or (
                origin_row < bsz_sub_hwl > origin_col and get_symbol(board, origin + board_len_add1 * half_win_len) == plyr):

            start = origin
            while (start >= board_len) and (start % board_len > 0) and get_symbol(board, start - board_len_add1) == plyr:
                start -= board_len_add1
            end = origin
            while (end < max_row_ind) and (end % board_len < board_len_sub1) and get_symbol(board, end + board_len_add1) == plyr:
                end += board_len_add1

            if (end // board_len - start // board_len) + 1 >= win_len:
                return True

        # check top right to down left
        if (origin_row >= half_win_len and origin_col < bsz_sub_hwl and get_symbol(board, origin - board_len_sub1 * half_win_len) == plyr) or (
                origin_row < bsz_sub_hwl and origin_col >= half_win_len and get_symbol(board, origin + board_len_sub1 * half_win_len) == plyr):

            start = origin
            while (start >= board_len) and (start % board_len < board_len_sub1) and get_symbol(board, start - board_len_sub1) == plyr:
                start -= board_len_sub1
            end = origin
            while (end < max_row_ind) and (end % board_len > 0) and get_symbol(board, end + board_len_sub1) == plyr:
                end += board_len_sub1

            if (end // board_len - start // board_len) + 1 >= win_len:
                return True

        return False

    def is_white(parent: int, parent_plyr: int, parent_origin: int) -> bool:
        """
        Finds the path where:
            |
            - The PC has at least 1 winning path whenever it's the human's turn.
            - The human has 0 winning paths whenever it's the PC's turn.
            |
        Returns:
            True:
                When all children are 'black', meaning their parent's player will win, so their parent is 'white'.

                - **Black**: This node lost for whoever is playing at that layer.
                - **White**: This node won for whoever is playing at that layer.

            False:
                When any children are 'white', meaning their parent's player will lose, so their parent is 'black'.

        :param parent: the board at the parent node
        :param parent_origin: latest move made on board 'parent'
        :param parent_plyr: the plyr who made the move 'parent_origin' on the board 'parent'

        """
        if parent in color_table:
            return color_table[parent]

        else:
            child_plyr = opp(parent_plyr)

            for i, sim_ind in enumerate(simmable_inds):

                # if child is white. OPTIMIZATION: is_plyr_win can function without placing child_plyr on the board beforehand
                # or if child is at the bottommost layer and is pc's turn
                # why not len(simmable_inds) == 0? -> the len is at parent node's
                if is_plyr_win(parent, child_plyr, sim_ind) is True or (len(simmable_inds) == 1 and child_plyr == pc):
                    color_table[parent] = False
                    return False

                elif len(simmable_inds) > 1:  # OPTIMIZATION: child is only generated if it is not at the bottommost layer
                    del simmable_inds[i]

                    child = parent + child_plyr*three_pow[sim_ind]  # place child_plyr on the board

                    # or if a child is white and is not at the bottommost layer yet
                    if is_white(child, child_plyr, sim_ind) is True:
                        tree.add_edge(parent, child,)

                        simmable_inds.insert(i, sim_ind)

                        color_table[parent] = False
                        return False

                    tree.add_edge(parent, child,)

                    simmable_inds.insert(i, sim_ind)

            color_table[parent] = True
            return True

    color_table = {}  # OPTIMIZATION: stores the color of nodes that had been calculated in a dict whose key = board, val = is_white. Dict has lookup time of O(1).

    for i, sim_ind in enumerate(simmable_inds):
        tree = nx.DiGraph()

        if is_plyr_win(main_board, pc, sim_ind) is True or len(simmable_inds) == 1:
            return sim_ind

        elif len(simmable_inds) > 1:
            del simmable_inds[i]

            child = main_board + pc*three_pow[sim_ind]

            if is_white(child, pc, sim_ind) is True:
                tree.add_node(child,)

                simmable_inds.insert(i, sim_ind)

                if is_debugging:
                    # get positions for each node of the tree
                    pos = fac_tree_layout(tree, child)
                    plt.title('Simulated Nodes under the Chosen Initial Node')
                    nx.draw(
                        tree, pos, with_labels=True,
                        node_size=500, node_color='c',
                        font_size=10, font_weight='bold'
                    )
                    plt.show()

                return sim_ind

            simmable_inds.insert(i, sim_ind)


def pc_input_v1(pc: int, main_board: int, board_len: int, win_len: int, simmable_inds: list, is_debugging: bool) -> int:
    board_len_sub1 = board_len-1
    board_len_add1 = board_len+1
    half_win_len = win_len // 2
    bsz_sub_hwl = board_len - half_win_len
    max_row_ind = board_len * board_len_sub1

    simmable_inds = simmable_inds[:9]  # CZY's AI is only capable of simulating 9 indexes

    def is_plyr_win(board: int, plyr: int, origin: int) -> bool:
        """
        :param board: same as board in pc_input
        :param origin: latest move made on the board
        :param plyr: player who made the move at 'origin'
        """
        # OPTIMIZATION:
        # 1. only check for the row/col/diagonals connected to the origin
        # 2. only check for whether the current plyr of this node wins, because only the current plyr is allowed to move (and may win)
        # 3. pre-calculate only once: half_win_len, board_len_sub1, board_len_add1, bsz_sub_hwl, max_row_ind, origin_col, origin_row

        origin_col = origin % board_len
        origin_row = origin // board_len

        # check column
        # I put check column as the first function as it is the fastest to complete
        if (origin_row >= half_win_len and get_symbol(board, origin - board_len * half_win_len) == plyr) or (origin_row < bsz_sub_hwl and get_symbol(board, origin + board_len * half_win_len) == plyr):

            start = origin
            while (start >= board_len) and get_symbol(board, start - board_len) == plyr:
                start -= board_len
            end = origin
            while (end < max_row_ind) and get_symbol(board, end + board_len) == plyr:
                end += board_len

            if end // board_len - start // board_len + 1 >= win_len:
                return True

        # check row
        if (origin_col >= half_win_len and get_symbol(board, origin - half_win_len) == plyr) or (origin_col < bsz_sub_hwl and get_symbol(board, origin + half_win_len) == plyr):

            start = origin
            while (start % board_len > 0) and get_symbol(board, start - 1) == plyr:
                start -= 1
            end = origin
            while (end % board_len < board_len_sub1) and get_symbol(board, end + 1) == plyr:
                end += 1

            if end - start + 1 >= win_len:
                return True

        # check top left to down right
        if (origin_row >= half_win_len <= origin_col and get_symbol(board, origin - board_len_add1 * half_win_len) == plyr) or (
                origin_row < bsz_sub_hwl > origin_col and get_symbol(board, origin + board_len_add1 * half_win_len) == plyr):

            start = origin
            while (start >= board_len) and (start % board_len > 0) and get_symbol(board, start - board_len_add1) == plyr:
                start -= board_len_add1

            end = origin
            while (end < max_row_ind) and (end % board_len < board_len_sub1) and get_symbol(board, end + board_len_add1) == plyr:
                end += board_len_add1

            if (end // board_len - start // board_len) + 1 >= win_len:
                return True

        # check top right to down left
        if (origin_row >= half_win_len and origin_col < bsz_sub_hwl and get_symbol(board, origin - board_len_sub1 * half_win_len) == plyr) or (
                origin_row < bsz_sub_hwl and origin_col >= half_win_len and get_symbol(board, origin + board_len_sub1 * half_win_len) == plyr):

            start = origin
            while (start >= board_len) and (start % board_len < board_len_sub1) and get_symbol(board, start - board_len_sub1) == plyr:
                start -= board_len_sub1
            end = origin
            while (end < max_row_ind) and (end % board_len > 0) and get_symbol(board, end + board_len_sub1) == plyr:
                end += board_len_sub1

            if (end // board_len - start // board_len) + 1 >= win_len:
                return True

        return False

    def recur(parent: int, pc: int, parent_origin: int) -> bool:

        is_win = is_plyr_win(parent, pc, parent_origin)

        if is_win is True:  # this layer is always pc
            win_probs[init_ind] += len(simmable_inds) + 1   # +1 because len(simmable_inds) can be 0

        elif is_win is False and len(simmable_inds) != 0:     # if this node has no winner and not tie yet: continue branching down
            plyr = opp(pc)

            for i, sim_ind in enumerate(simmable_inds):
                del simmable_inds[i]

                child = parent + plyr*three_pow[sim_ind]

                is_win = is_plyr_win(child, plyr, sim_ind)

                if is_win is True:  # this layer is always player
                    win_probs[init_ind] -= (len(simmable_inds) + 1)

                    simmable_inds.insert(i, sim_ind)
                    return False

                elif is_win is False and len(simmable_inds) != 0:

                    if parent_origin == init_ind:  # if this is the highest simulated layer
                        all_child_lost = True

                    for ii, sim_ind_ii in enumerate(simmable_inds):
                        del simmable_inds[ii]

                        child_ii = child + pc*three_pow[sim_ind]

                        if recur(child_ii, pc, sim_ind_ii) is None and parent_origin == init_ind:
                            all_child_lost = False

                            simmable_inds.insert(ii, sim_ind_ii)
                            break  # OPTIMIZATION ?

                        simmable_inds.insert(ii, sim_ind_ii)

                    # noinspection PyUnboundLocalVariable
                    if parent_origin == init_ind is True and all_child_lost is True:
                        del win_probs[init_ind]
                        print(f'Deathtrap Found: Index {init_ind}')

                        simmable_inds.insert(i, sim_ind)
                        return False

                simmable_inds.insert(i, sim_ind)

    def pick_init_move(plyr: int, outcomes: dict) -> int:
        # find which init_ind results in the most winning child nodes
        max_win_prob = max(outcomes.values())

        # moves_pool creates a list of init_inds containing the same highest win_prob to be picked randomly
        moves_pool = [key for key, value in outcomes.items() if value == max_win_prob]
        move = moves_pool[random.randint(0, len(moves_pool) - 1)]

        return move

    win_probs = {ind: 0 for ind in simmable_inds}   # key = init_move, val = win_probability of the init_move

    for i, sim_ind in enumerate(simmable_inds):
        init_ind = sim_ind

        del simmable_inds[i]

        child = main_board + pc*three_pow[sim_ind]
        recur(child, pc, sim_ind)

        simmable_inds.insert(i, sim_ind)

    fin_move = pick_init_move(pc, win_probs)

    if is_debugging:
        plt.clf()
        p = plt.bar(list(win_probs.keys()), list(win_probs.values()), color='c')
        plt.bar_label(p, label_type='center')
        plt.locator_params(axis='x', nbins=board_len * win_len + 1)  # sets the tick interval of graph
        plt.title('Computer\'s Risk Analysis of each Initial Node')
        plt.xlabel('Initial Move')
        plt.ylabel('Winning Probability')
        plt.show()

    return fin_move