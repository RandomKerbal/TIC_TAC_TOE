import collections
import random
import math
import matplotlib.pyplot as plt
import networkx as nx

# initialize universal variables
three_pow = ()
"""
A pre-calculated universal tuple containing 'board_sz**2' integer. Each integer = the place value of a digit with the same index in a base3 number.
E.g.: in a base 3 3x3 board:
    - the element at index 0 = 3^8 (8th place value)
    - the element at index 8 = 3^0 (0th place value)
"""
board_len = 0
"""A universal integer containing the length of the board."""
win_len = 0
"""A universal integer containing the number of X/O in a row/column/diagonal to win."""
bln_sub1 = 0
"""A pre-calculated universal integer calculated as: board_len - 1."""
bln_add1 = 0
"""A pre-calculated universal integer calculated as: board_len + 1."""
max_y_ind = 0
"""A pre-calculated universal integer calculated as: board_len * (board_len - 1)."""
half_win_len = 0
"""A pre-calculated universal integer calculated as: win_len // 2."""
bln_sub_hwl = 0
"""A pre-calculated universal integer calculated as: board_len - (win_len // 2)."""
bln_mul_hwl = 0
"""A pre-calculated universal integer calculated as: board_len * (win_len // 2)."""
bln_add1_mul_hwl = 0
"""A pre-calculated universal integer calculated as: (board_len + 1) * (win_len // 2)."""
bln_sub1_mul_hwl = 0
"""A pre-calculated universal integer calculated as: (board_len - 1) * (win_len // 2)."""
relative_adj = (
    (-1, -1), (0, -1), (1, -1),  # top-left, top-center, top-right
    (-1, 0), (1, 0),  # left, right
    (-1, 1), (0, 1), (1, 1)  # bottom-left, bottom-center, bottom-right
)
"""A pre-calculated universal tuple containing the relative coordinates (x, y) of 8 adjacent cells around a center cell."""
black_table = set()
"""
A universal set that stores nodes that were pre-calculated as black for optimization.
"""

# def set_win_len(board_len: int) -> int:
#     return board_len//4 + 3


def set_universals(tk_board_len: int | None = None, tk_win_len: int | None = None):
    """
    Assign values to all the universal variables.
    """
    global three_pow, board_len, win_len, bln_sub1, bln_add1, max_y_ind, half_win_len, bln_sub_hwl, bln_mul_hwl, bln_add1_mul_hwl, bln_sub1_mul_hwl

    if tk_board_len:
        three_pow = tuple(3 ** place_val for place_val in range(tk_board_len ** 2 - 1, -1, -1))  # counter is reversed as the order of place values is the reverse of index order

        board_len = tk_board_len
        bln_sub1 = board_len - 1
        bln_add1 = board_len + 1
        max_y_ind = board_len * bln_sub1

        cell_to_line = [[]] * board_len

    if tk_win_len:
        win_len = tk_win_len
        half_win_len = win_len // 2

    bln_sub_hwl = board_len - half_win_len
    bln_mul_hwl = board_len * half_win_len
    bln_add1_mul_hwl = bln_add1 * half_win_len
    bln_sub1_mul_hwl = bln_sub1 * half_win_len

    black_table.clear()


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


def print_board(board: int):
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
        - each node has at least one less children than its parent

    Use case:
        - when you don't know the maximum number of children, but you know the maximum number of layers

    :param tree: networkx graph object (must be directed).
    :param root: root node of the tree (if None, chooses an arbitrary node).
    :return: dictionary whose key = node, val = coord of the node saved as a tuple (x, y).
    """
    def assign_pos(layer: int, children, parent_x: float):
        """
        Recursively updating coord of parent nodes and calculating coord of child nodes.
        """
        if children:
            layer_neg1 = layer - 1
            sep_count = len(children) - 1  # total number of separations between children
            sep_dist = factorials[layer + 1] / max(1, sep_count)  # separation distance between each child

            # assign positions for each child
            start_x = parent_x - (sep_count/2) * sep_dist
            for i, child in enumerate(children):
                child_x = start_x + i*sep_dist
                pos[child] = (child_x, layer_neg1)
                assign_pos(layer_neg1, list(tree.successors(child)), child_x)

    if root is None:
        root = next(iter(tree))  # select an arbitrary root if not provided

    root_children = list(tree.successors(root))
    max_layer = len(root_children)  # the maximum number of layers, assuming the bottommost layer is 1
    factorials = tuple(math.factorial(layer) for layer in range(max_layer+2))

    pos = {root: (0, max_layer)}
    assign_pos(max_layer, root_children, 0.0)
    return pos


def recip_tree_layout(tree, root=None) -> dict:
    """
    Creates a hierarchical layout for a directed reciprocal tree graph. Property of a reciprocal tree graph:
        - each node from any layer has a maximum of *n* children

    Use case:
        - when you don't know the maximum number of layers, but you know the maximum number of children

    :param tree: networkx graph object (must be directed).
    :param root: root node of the tree (if None, chooses an arbitrary node).
    :return: dictionary whose key = node, val = coord of the node saved as a tuple (x, y).
    """
    def assign_pos(layer: int, children, parent_x: float):
        """
        Recursively updating coord of parent nodes and calculating coord of child nodes.
        """
        if children:
            layer_neg1 = layer - 1
            sep_dist = max_sep_count**layer  # separation distance between each child. DO NOT use 1/(max_sep_count**layer) as layer is negative.

            # assign positions for each child
            start_x = parent_x - (len(children)-1)/2 * sep_dist
            for i, child in enumerate(children):
                child_x = start_x + i*sep_dist
                pos[child] = (child_x, layer_neg1)
                assign_pos(layer_neg1, list(tree.successors(child)), child_x)

    if root is None:
        root = next(iter(tree))  # select an arbitrary root if not provided

    max_sep_count = max(degree for _, degree in tree.degree()) - 1  # the maximum number of separations between children of any node (maximum number of children - 1)
    root_children = list(tree.successors(root))

    pos = {root: (0, 0)}
    assign_pos(0, root_children, 0.0)
    return pos


# ALL FUNCTIONS BELOW ARE FOR THE AI
def prune(plyr: int, board: int, origin: int) -> list:
    """
    Limits indexes that PC can simulate to the 15 empty indexes with the highest priority.
    Assigns priority to indexes accordingly:
        1. if index is connected to, or at the back of another index connected to, either end of a line formed by player: within the high priorities; varies with dist to origin and the number of connected lines.
        2. index has adjacent player cell -> within the low priorities; varies with dist to origin and the number of adjacent player cells.
    :return: simmable_inds (simulatable indexes): a list containing the indexes that AI can simulate
    """
    # convert origin to coords
    origin_x, origin_y = origin % board_len, origin // board_len

    ind_priority = {}  # key = index of cell, value = priority

    for ind in range(board_len**2):
        if get_symbol(board, ind) == 0:
            x, y = ind % board_len, ind // board_len
            origin_d = max(abs(y - origin_y), abs(x - origin_x))  # calculate Chebyshev distance

            ind_priority[ind] = ind_priority.get(ind, 0) - origin_d  # set distance-dependent base priority

            for dir_x, dir_y in relative_adj:
                fwd1_x, fwd1_y = x + dir_x, y + dir_y

                if 0 <= fwd1_x < board_len and 0 <= fwd1_y < board_len and get_symbol(board, fwd1_y * board_len + fwd1_x) == plyr:  # if ind has an adjacent player cell
                    ind_priority[ind] += board_len  # +board_len ensures the furthest index with 1 adjacent player cell has higher priority than the closest lone index

                    fwd2_x, fwd2_y = fwd1_x + dir_x, fwd1_y + dir_y

                    if 0 <= fwd2_x < board_len and 0 <= fwd2_y < board_len and get_symbol(board, fwd2_y * board_len + fwd2_x) == plyr:  # if ind is connected to either end of a line formed by player
                        ind_priority[ind] += board_len * 8  # +board_len*8 ensures the furthest index connected to 1 line formed by player has higher priority than an index surrounded by 8 player cells

                        back1_x, back1_y = x - dir_x, y - dir_y

                        if 0 <= back1_x < board_len and 0 <= back1_y < board_len:  # if ind is at the back of another ind connected to either end of a line formed by player
                            back1_ind = back1_y * board_len + back1_x

                            if get_symbol(board, back1_ind) == 0:
                                ind_priority[back1_ind] = ind_priority.get(back1_ind, 0) + board_len*8

    # print(f'\nIndex Priority: {ind_priority}')

    simmable_inds = sorted(ind_priority, key=ind_priority.get, reverse=True)

    return simmable_inds


def plyr_win_formation(plyr: int, board: int, origin: int) -> str | None:

    origin_x = origin % board_len
    origin_y = origin // board_len

    # check column
    # I put check column as the first block as it is the fastest to complete
    if (origin_y >= half_win_len and get_symbol(board, origin - bln_mul_hwl) == plyr) or (origin_y < bln_sub_hwl and get_symbol(board, origin + bln_mul_hwl) == plyr):

        start = origin
        while (start >= board_len) and get_symbol(board, start - board_len) == plyr:
            start -= board_len
        end = origin
        while (end < max_y_ind) and get_symbol(board, end + board_len) == plyr:
            end += board_len

        if end // board_len - start // board_len + 1 >= win_len:
            return 'vertically'

    # check row
    if (origin_x >= half_win_len and get_symbol(board, origin - half_win_len) == plyr) or (origin_x < bln_sub_hwl and get_symbol(board, origin + half_win_len) == plyr):

        start = origin
        while (start % board_len > 0) and get_symbol(board, start - 1) == plyr:
            start -= 1
        end = origin
        while (end % board_len < bln_sub1) and get_symbol(board, end + 1) == plyr:
            end += 1

        if end - start + 1 >= win_len:
            return 'horizontally'

    # check top left to down right
    if (origin_y >= half_win_len <= origin_x and get_symbol(board, origin - bln_add1_mul_hwl) == plyr) or (
            origin_y < bln_sub_hwl > origin_x and get_symbol(board, origin + bln_add1_mul_hwl) == plyr):

        start = origin
        while (start >= board_len) and (start % board_len > 0) and get_symbol(board, start - bln_add1) == plyr:
            start -= bln_add1
        end = origin
        while (end < max_y_ind) and (end % board_len < bln_sub1) and get_symbol(board, end + bln_add1) == plyr:
            end += bln_add1

        if (end // board_len - start // board_len) + 1 >= win_len:
            return 'from top left to down right'

    # check top right to down left
    if (origin_y >= half_win_len and origin_x < bln_sub_hwl and get_symbol(board, origin - bln_sub1_mul_hwl) == plyr) or (
            origin_y < bln_sub_hwl and origin_x >= half_win_len and get_symbol(board, origin + bln_sub1_mul_hwl) == plyr):

        start = origin
        while (start >= board_len) and (start % board_len < bln_sub1) and get_symbol(board, start - bln_sub1) == plyr:
            start -= bln_sub1
        end = origin
        while (end < max_y_ind) and (end % board_len > 0) and get_symbol(board, end + bln_sub1) == plyr:
            end += bln_sub1

        if (end // board_len - start // board_len + 1) >= win_len:
            return 'from top right to down left'

    return None


def is_win(plyr: int, board: int, origin: int) -> bool:
    """
    Note: This function works even if the origin cell on the board is empty.
    :param plyr: player who made the move at 'origin'
    :param board: same as board in pc_input_recur
    :param origin: latest move made on the board
    """
    # OPTIMIZATION:
    # 1. only check for the row/col/diagonals connected to the origin
    # 2. only check for whether the current plyr of this node wins, because only the current plyr is allowed to move (and may win)
    # 3. pre-calculate only once: half_win_len, bln_sub1, bln_add1, bln_sub_hwl, max_row_ind, origin_col, origin_row

    origin_x = origin % board_len
    origin_y = origin // board_len

    # check column
    # I put check column as the first block as it is the fastest to complete
    if (origin_y >= half_win_len and get_symbol(board, origin - bln_mul_hwl) == plyr) or (origin_y < bln_sub_hwl and get_symbol(board, origin + bln_mul_hwl) == plyr):

        start = origin
        while (start >= board_len) and get_symbol(board, start - board_len) == plyr:
            start -= board_len
        end = origin
        while (end < max_y_ind) and get_symbol(board, end + board_len) == plyr:
            end += board_len

        if end // board_len - start // board_len + 1 >= win_len:
            return True

    # check row
    if (origin_x >= half_win_len and get_symbol(board, origin - half_win_len) == plyr) or (origin_x < bln_sub_hwl and get_symbol(board, origin + half_win_len) == plyr):

        start = origin
        while (start % board_len > 0) and get_symbol(board, start - 1) == plyr:
            start -= 1
        end = origin
        while (end % board_len < bln_sub1) and get_symbol(board, end + 1) == plyr:
            end += 1

        if end - start + 1 >= win_len:
            return True

    # check top left to down right
    if (origin_y >= half_win_len <= origin_x and get_symbol(board, origin - bln_add1_mul_hwl) == plyr) or (
            origin_y < bln_sub_hwl > origin_x and get_symbol(board, origin + bln_add1_mul_hwl) == plyr):

        start = origin
        while (start >= board_len) and (start % board_len > 0) and get_symbol(board, start - bln_add1) == plyr:
            start -= bln_add1
        end = origin
        while (end < max_y_ind) and (end % board_len < bln_sub1) and get_symbol(board, end + bln_add1) == plyr:
            end += bln_add1

        if (end // board_len - start // board_len) + 1 >= win_len:
            return True

    # check top right to down left
    if (origin_y >= half_win_len and origin_x < bln_sub_hwl and get_symbol(board, origin - bln_sub1_mul_hwl) == plyr) or (
            origin_y < bln_sub_hwl and origin_x >= half_win_len and get_symbol(board, origin + bln_sub1_mul_hwl) == plyr):

        start = origin
        while (start >= board_len) and (start % board_len < bln_sub1) and get_symbol(board, start - bln_sub1) == plyr:
            start -= bln_sub1
        end = origin
        while (end < max_y_ind) and (end % board_len > 0) and get_symbol(board, end + bln_sub1) == plyr:
            end += bln_sub1

        if (end // board_len - start // board_len) + 1 >= win_len:
            return True

    return False


def pc_input_recur(pc: int, main_board: int, simmable_inds: list, is_debugging: bool):
    """
    Note: This function exploits Python generator function's 'lazy' evaluation (pauses until next element is called), together with iterating over this function using a 'for' loop, to achieve multithreading.

    :rtype: collections.Iterable[int]
    :return: a generator object containing the index of root nodes that are already simulated. The last element of the generator is the chosen move.
    """

    def is_white(u_board: int, u_plyr: int) -> bool:
        """
        'u' = current node, prefix 'u_' = belong to parent node

        'v' = child node, prefix 'v_' = belong to child node

        'w' = parent node, prefix 'w_' = belong to grandparent node

        Finds the path where:

            - The PC has at least 1 winning move whenever it's the human's turn.
            - The human has 0 winning move whenever it's the PC's turn.

        Returns:
            True:
                When all children are 'black', meaning their parent's player will win, so their parent is 'white'.

                - **Black**: This node lost for whoever is playing at that layer.
                - **White**: This node won for whoever is playing at that layer.

            False:
                When any children are 'white', meaning their parent's player will lose, so their parent is 'black'.

        :param u_board: the board at the parent node
        :param u_plyr: the plyr who made the move u_origin on the u_board

        """
        v_plyr = opp(u_plyr)

        if len(simmable_inds) == 1:  # if v is at the bottommost layer
            if v_plyr == pc:  # if pc is next turn -> pc can only win/tie -> v must be white -> u must be black
                black_table.add(u_board)
                return False

            else:  # if human is next turn -> human can win/tie/loose -> check
                for sim_ind in simmable_inds:
                    if is_win(v_plyr, u_board, sim_ind):  # OPTIMIZATION: v_board is not generated at the bottommost layer
                        black_table.add(u_board)
                        return False

        else:
            for i, sim_ind in enumerate(simmable_inds):
                del simmable_inds[i]
                v_board = u_board + v_plyr*three_pow[sim_ind]

                if is_debugging: tree.add_edge(u_board, v_board, ); edge_labels[(u_board, v_board,)] = sim_ind

                if v_board not in black_table and (is_win(v_plyr, u_board, sim_ind) or is_white(v_board, v_plyr)):
                    simmable_inds.insert(i, sim_ind)
                    black_table.add(u_board)
                    return False

                simmable_inds.insert(i, sim_ind)

        return True

    for i, root_sim_ind in enumerate(simmable_inds):
        yield root_sim_ind

        if len(simmable_inds) == 1 or is_win(pc, main_board, root_sim_ind):
            return  # root_sim_ind is already returned by 'yield'

        else:
            if is_debugging: tree = nx.DiGraph(); edge_labels = {}

            del simmable_inds[i]
            root_board = main_board + pc*three_pow[root_sim_ind]

            if root_board not in black_table and is_white(root_board, pc):
                simmable_inds.insert(i, root_sim_ind)

                if is_debugging:  # noinspection PyUnboundLocalVariable
                    tree.add_edge(main_board, root_board,)

                    # get positions for each node of the tree
                    pos = recip_tree_layout(tree, main_board)
                    plt.figure()
                    plt.title('Simulated Nodes under the Chosen Initial Node')
                    nx.draw(
                        tree, pos, with_labels=True, arrows=False,
                        node_size=0,
                        bbox=dict(facecolor=(44/255, 255/255, 140/255, 1.0), boxstyle='round,pad=0.4', linewidth=0.5),
                        font_family='Arial', font_weight='bold', font_size=10
                    ),
                    nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_labels,
                                                 bbox=dict(facecolor='white', alpha=0.75, edgecolor='none', boxstyle='circle', pad=0),
                                                 font_color='crimson', font_family='Arial', font_size=10, rotate=False)
                    plt.text(
                        0.0, 0.0,  # coordinates (x, y) in axes fraction
                        f'Total # of Nodes: {tree.number_of_nodes()}  |  Max # of Children: {max(dict(tree.out_degree()).values())}',
                        fontsize=10, color='gray',
                        transform=plt.gca().transAxes  # use axes fraction for positioning
                    )
                    plt.tight_layout()
                    plt.show(block=False)

                return  # root_sim_ind is already returned by 'yield'

            simmable_inds.insert(i, root_sim_ind)


def pc_input_iter(pc: int, main_board: int, simmable_inds: set, is_debugging: bool):
    """
    Note: This function exploits Python generator function's 'lazy' evaluation (pauses until next element is called), together with iterating over this function using a 'for' loop, to achieve multithreading.

    :rtype: collections.Iterable[int]
    :return: a generator object containing the index of root nodes that are already simulated. The last element of the generator is the chosen move.
    """
    stack: list[None | tuple] = [None] * sum(range(1, len(simmable_inds) + 1))  # Preallocate list size. The largest possible size is (n) + (n-1) + (n-2) + ... + 1, where n is len(simmable_inds).

    def pop() -> tuple:
        nonlocal top
        top -= 1
        return stack[top]

    def append(node: tuple):
        nonlocal top
        stack[top] = node
        top += 1

    def truncate(new_top: int):
        """
        Slice off a section of stack, starting from new_top (inclusive) to the end.
        """
        nonlocal top
        top = new_top

    for root_sim_ind in simmable_inds.copy():
        yield root_sim_ind

        if is_debugging: tree = nx.DiGraph(); edge_labels = {}

        top = 0  # reset stack
        append((root_sim_ind, None,))

        while top:
            u = pop()
            """            
            'u' = current node, prefix 'u_' = belong to parent node

            'v' = child node, prefix 'v_' = belong to child node

            'w' = parent node, prefix 'w_' = belong to grandparent node

            A node can be either of 2 types:
                1. Typical Node:
                    - A typical node is a tuple containing 2 elements:

                        - index 0 = simulated index
                        - index 1 (aka pointer) = index of previous marker

                    - The information on the player at this node and, the board at parent node, is stored in the previous marker.

                2. Marker:
                    - A 'marker' is a tuple containing 4 elements:

                        - index 0 = opponent of the former popped node
                        - index 1 = board of the former popped node
                        - index 2 = simulated index of the former popped node
                        - index 3 (aka pointer) = index of previous marker

                    - A marker replaces a node that can have children and has been popped. It has 2 uses:

                        1. Record the player, board, and simulated index of the popped node.
                        2. Indicate whether the former popped node was white.

                            - if the index of the node has a marker -> the node is white.
                            - if the index of the node does not have a marker -> the node is black.
            """

            if len(u) == 4:  # if node is marker
                simmable_inds.add(u[2])
                if top:
                    # skip siblings
                    truncate(u[3] + 1)

                    # skip w
                    w = pop()
                    black_table.add(w[1])  # since u is white, its w must be black
                    simmable_inds.add(w[2])
                    if not top:
                        break
                continue

            u_sim_ind, u_pointer = u
            w = stack[u_pointer] if top else (pc, main_board,)  # get info from w to construct u_plyr, u_board, ...
            u_plyr = w[0]
            u_board = w[1] + u_plyr * three_pow[u_sim_ind]
            v_plyr = opp(u_plyr)
            v_pointer = top

            if is_debugging: tree.add_edge(w[1], u_board,); edge_labels[(w[1], u_board,)] = u_sim_ind

            if u_board in black_table:
                if not top:
                    break
                continue

            elif len(simmable_inds) == 2:  # if v is at the bottommost layer
                if v_plyr == pc:  # if pc is next turn -> pc can only win/tie -> v must be white -> u must be black
                    continue

                # if human is next turn -> human can win/tie/loose -> check
                simmable_inds.remove(u_sim_ind)

                for v_sim_ind in simmable_inds:
                    if is_win(v_plyr, u_board, v_sim_ind):  # OPTIMIZATION: v_board is not generated
                        break
                else:  # if inner loop did NOT break -> all v is black; if inner loop DID break -> GOTO end of loop
                    append((v_plyr, u_board, u_sim_ind, u_pointer,))  # append marker
                    continue

            else:
                simmable_inds.remove(u_sim_ind)

                append((v_plyr, u_board, u_sim_ind, u_pointer,))  # append marker

                for v_sim_ind in simmable_inds:
                    if is_win(v_plyr, u_board, v_sim_ind):  # OPTIMIZATION: v_board is not generated
                        truncate(v_pointer)  # pop all v and u
                        break  # GOTO end of outer loop
                    else:
                        append((v_sim_ind, v_pointer,))  # append v

                else:  # if inner loop did NOT break -> no v is white; if inner loop DID break -> GOTO end of loop
                    continue

            black_table.add(u_board)
            simmable_inds.add(u_sim_ind)
            if not top:
                break

        else:
            if is_debugging:
                # get positions for each node of the tree
                pos = recip_tree_layout(tree, main_board)
                plt.figure()
                plt.title('Simulated Nodes under the Chosen Initial Node')
                nx.draw(
                    tree, pos, with_labels=True, arrows=False,
                    node_size=0,
                    bbox=dict(facecolor=(44 / 255, 255 / 255, 140 / 255, 1.0), boxstyle='round', pad=0.4, linewidth=0.5),
                    font_family='Arial', font_weight='bold', font_size=10
                )
                nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_labels,
                                             bbox=dict(facecolor='white', alpha=0.75, edgecolor='none', boxstyle='circle', pad=0),
                                             font_color='crimson', font_family='Arial', font_size=10, rotate=False)
                plt.text(
                    0.0, 0.0,  # coordinates (x, y) in axes fraction
                    f'Total # of Nodes: {tree.number_of_nodes()}  |  Max # of Children: {max(dict(tree.out_degree()).values())}',
                    fontsize=10, color='gray',
                    transform=plt.gca().transAxes  # use axes fraction for positioning
                )
                plt.tight_layout()
                plt.show(block=True)

            return  # root_sim_ind is already returned by 'yield'


def snake_pc_input(pc: int, main_board: int, pc_y: int, pc_x: int, plyr_y: int, plyr_x: int, is_debugging: bool):

    def is_white(u_board: int, u_plyr: int, grand_u_y: int, grand_u_x: int, u_y: int, u_x: int) -> bool:
        v_plyr = opp(u_plyr)
        has_valid = False

        for dir_x, dir_y in relative_adj:
            v_x = grand_u_x + dir_x
            v_y = grand_u_y + dir_y

            if 0 <= v_x < board_len and 0 <= v_y < board_len:
                v_sim_ind = v_y * board_len + v_x

                if get_symbol(u_board, v_sim_ind) == 0:
                    has_valid = True

                    if is_win(v_plyr, u_board, v_sim_ind):  # TODO: make is_win accept origin row, col
                        return False

                    else:
                        v_board = u_board + v_plyr * three_pow[v_sim_ind]  # place v_plyr on the board

                        if is_debugging: tree.add_edge(u_board, v_board, ); edge_labels[(u_board, v_board,)] = v_sim_ind

                        # or if any v is white and is not at the bottommost layer yet
                        if is_white(v_board, v_plyr, u_y, u_x, v_y, v_x):
                            return False

        return has_valid

    for dir_x, dir_y in relative_adj:
        v_x = pc_x + dir_x
        v_y = pc_y + dir_y

        if 0 <= v_x < board_len and 0 <= v_y < board_len:
            root_sim_ind = v_y * board_len + v_x

            if get_symbol(main_board, root_sim_ind) == 0:

                if is_win(pc, main_board, root_sim_ind):
                    return root_sim_ind

                else:
                    if is_debugging: tree = nx.DiGraph(); edge_labels = {}

                    root_board = main_board + pc*three_pow[root_sim_ind]

                    if is_white(root_board, pc, plyr_y, plyr_x, v_y, v_x):
                        if is_debugging:  # noinspection PyUnboundLocalVariable
                            tree.add_edge(main_board, root_board, )

                            # get positions for each node of the tree
                            pos = recip_tree_layout(tree, main_board)
                            plt.title('Simulated Nodes under the Chosen Initial Node')
                            nx.draw(
                                tree, pos, with_labels=True, arrows=False,
                                node_size=0,
                                bbox=dict(facecolor=(44 / 255, 255 / 255, 140 / 255, 1.0), boxstyle='round,pad=0.4', linewidth=0.5),
                                font_family='Arial', font_weight='bold', font_size=10
                            ),
                            nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_labels,
                                                         bbox=dict(facecolor='white', alpha=0.75, edgecolor='none', boxstyle='circle', pad=0),
                                                         font_color='crimson', font_family='Arial', font_size=10, rotate=False)
                            plt.text(
                                0.0, 0.0,  # coordinates (x, y) in axes fraction
                                f'Total # of Nodes: {tree.number_of_nodes()}  |  Max # of Children: {max(dict(tree.out_degree()).values())}',
                                fontsize=10, color='gray',
                                transform=plt.gca().transAxes  # use axes fraction for positioning
                            )
                            plt.tight_layout()
                            plt.show(block=False)

                        return root_sim_ind


def czy_pc_input(pc: int, main_board: int, simmable_inds: list, is_debugging: bool):
    """
    Note: This function exploits Python generator function's 'lazy' evaluation (pauses until next element is called), together with iterating over this function using a 'for' loop, to achieve multithreading.

    :rtype: collections.Iterable[int]
    :return: a generator object containing the index of root nodes that are already simulated. The last element of the generator is the chosen move.
    """

    def recur(u_board: int, pc: int, u_origin: int) -> bool:

        _is_win = is_win(pc, u_board, u_origin)

        if _is_win:  # this layer is always pc
            win_probs[root_sim_ind] += len(simmable_inds) + 1  # +1 because len(simmable_inds) can be 0

        elif _is_win is False and simmable_inds:  # if this node has no winner and not tie yet: continue branching down
            plyr = opp(pc)

            for i, sim_ind in enumerate(simmable_inds):
                del simmable_inds[i]

                v_board = u_board + plyr*three_pow[sim_ind]
                _is_win = is_win(plyr, v_board, sim_ind)

                if _is_win:  # this layer is always player
                    win_probs[root_sim_ind] -= len(simmable_inds) - 2

                    simmable_inds.insert(i, sim_ind)
                    return False

                elif _is_win is False and simmable_inds:

                    if u_origin == root_sim_ind:  # if this is the highest simulated layer
                        all_v_lost = True

                    for ii, sim_ind_ii in enumerate(simmable_inds):
                        del simmable_inds[ii]

                        v_ii_board = v_board + pc*three_pow[sim_ind]

                        if recur(v_ii_board, pc, sim_ind_ii) is None and u_origin == root_sim_ind:
                            all_v_lost = False

                            simmable_inds.insert(ii, sim_ind_ii)
                            break

                        simmable_inds.insert(ii, sim_ind_ii)

                    if u_origin == root_sim_ind and all_v_lost:
                        del win_probs[root_sim_ind]
                        # print(f'Deathtrap Found: Index {root_sim_ind}')

                        simmable_inds.insert(i, sim_ind)
                        return False

                simmable_inds.insert(i, sim_ind)

    def pick_init_move(plyr: int, outcomes: dict) -> int:
        # find which root_sim_ind results in the most winning leaves
        max_win_prob = max(outcomes.values())

        # moves_pool creates a list of root_sim_ind containing the same highest win_prob to be picked randomly
        moves_pool = [key for key, value in outcomes.items() if value == max_win_prob]
        move = moves_pool[random.randint(0, len(moves_pool) - 1)]

        return move

    win_probs = {ind: 0 for ind in simmable_inds}   # key = init_move, val = win_probability of the init_move

    for i, root_sim_ind in enumerate(simmable_inds):
        yield root_sim_ind

        del simmable_inds[i]

        root_board = main_board + pc*three_pow[root_sim_ind]
        recur(root_board, pc, root_sim_ind)

        simmable_inds.insert(i, root_sim_ind)

    fin_move = pick_init_move(pc, win_probs)

    if is_debugging:
        plt.figure()
        bar = plt.bar(list(win_probs.keys()), list(win_probs.values()), color=(34/255, 245/255, 130/255, 1.0))
        plt.bar_label(bar, label_type='center')
        plt.locator_params(axis='x')  # sets the tick interval of graph
        plt.title('Computer\'s Risk Analysis of each Initial Node')
        plt.xlabel('Initial Move')
        plt.ylabel('Winning Probability')
        plt.show(block=False)

    yield fin_move
    return