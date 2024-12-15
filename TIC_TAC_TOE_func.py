import random
import math
import matplotlib.pyplot as plt
import networkx as nx


def set_win_len(board_sz: int) -> int:
    return board_sz//4 + 3


def setup_board(board_sz: int) -> list:
    # setup board layout
    # eg 3x3 board = [0, 0, 0
    #                 0, 0, 0
    #                 0, 0, 0]
    main_board = [0] * (board_sz**2)

    return main_board


def print_board(board: list, board_sz: int):
    # print the board
    # eg 3x3 board:
    #     1   2   3
    # 1  [ ] [ ] [ ]
    # 2  [ ] [ ] [ ]
    # 3  [ ] [ ] [ ]
    print(end='\n')
    print('\t', end='')
    for i in range(board_sz):
        print(str(i + 1) + ' ' * (4 - len(str(i+2))), end='')
    for i in range(board_sz):
        print('\n' + str(i + 1) + ' ' * (3 - len(str(i+1))), end='')
        for ii in range(i*board_sz, (i*board_sz)+board_sz):
            if board[ii] == 0:
                print('[ ]', end=' ')
            else:
                print(' ' + board[ii], end='  ')
    print(end='\n')


def opp(original: int) -> int:
    """
    (opponent)

    Returns 1 when input 2; 2 when input 1.
    """
    return 3-original


def get_symbol(base3: int) -> str:
    """
    Converts a symbol from base3 to readable character.
    """
    if base3 == 1:
        return 'X'
    elif base3 == 2:
        return 'O'
    elif base3 == 0:
        return ' '


def plyr_win_formation(board: list, board_sz: int, win_len: int, plyr: int, origin: int) -> str | None:
    half_win_len = win_len // 2
    board_sz_sub1 = board_sz-1
    board_sz_add1 = board_sz+1
    bsz_sub_hwl = board_sz - half_win_len
    max_row_ind = board_sz * board_sz_sub1

    origin_col = origin % board_sz
    origin_row = origin // board_sz

    # check column
    # I put check column as the first function as it is the fastest to complete
    start = origin
    end = origin

    if (origin_row >= half_win_len and board[origin - board_sz * half_win_len] == plyr) or (origin_row < bsz_sub_hwl and board[origin + board_sz * half_win_len] == plyr):

        while (start >= board_sz) and board[start - board_sz] == plyr:
            start -= board_sz
        while (end < max_row_ind) and board[end + board_sz] == plyr:
            end += board_sz

        if end // board_sz - start // board_sz + 1 >= win_len:
            return 'vertically'

    # check row
    start = origin
    end = origin

    if (origin_col >= half_win_len and board[origin - half_win_len] == plyr) or (origin_col < bsz_sub_hwl and board[origin + half_win_len] == plyr):

        while (start % board_sz > 0) and board[start - 1] == plyr:
            start -= 1
        while (end % board_sz < board_sz_sub1) and board[end + 1] == plyr:
            end += 1

        if end - start + 1 >= win_len:
            return 'horizontally'

    # check top left to down right
    start = origin
    end = origin

    if (origin_row >= half_win_len <= origin_col and board[origin - board_sz_add1 * half_win_len] == plyr) or (
            origin_row < bsz_sub_hwl > origin_col and board[origin + board_sz_add1 * half_win_len] == plyr):

        while (start >= board_sz) and (start % board_sz > 0) and board[start - board_sz_add1] == plyr:
            start -= board_sz_add1
        while (end < max_row_ind) and (end % board_sz < board_sz_sub1) and board[end + board_sz_add1] == plyr:
            end += board_sz_add1

        if (end // board_sz - start // board_sz) + 1 >= win_len:
            return 'from top left to down right'

    # check top right to down left
    start = origin
    end = origin

    if (origin_row >= half_win_len and origin_col < bsz_sub_hwl and board[origin - board_sz_sub1 * half_win_len] == plyr) or (
            origin_row < bsz_sub_hwl and origin_col >= half_win_len and board[origin + board_sz_sub1 * half_win_len] == plyr):

        while (start >= board_sz) and (start % board_sz < board_sz_sub1) and board[start - board_sz_sub1] == plyr:
            start -= board_sz_sub1
        while (end < max_row_ind) and (end % board_sz > 0) and board[end + board_sz_sub1] == plyr:
            end += board_sz_sub1

        if (end // board_sz - start // board_sz + 1) >= win_len:
            return 'from top right to down left'

    return None


# ALL FUNCTIONS BELOW ARE FOR THE AI
def prune(board: list, board_sz: int, opp: int, origin: int) -> list:
    """
    Limits indexes that PC can simulate to the 13 empty indexes with the highest priority.
    Assigns priority to indexes accordingly:
        1. if index is connected to, or at the back of another index connected to, either end of a line formed by player -> within the high priorities; varies with dist to origin and the number of connected lines.
        2. index has adjacent player cell -> within the low priorities; varies with dist to origin and the number of adjacent player cells.
    :return: simmable_inds
    """
    # convert origin to coords
    origin_row = origin // board_sz
    origin_col = origin % board_sz

    # setup coords (x_coord, y_coord) of 8 indexes around a center
    adjacents = (
        (-1, -1), (0, -1), (1, -1),  # Top-left, Top-right
        (-1, 0),           (1, 0),   # Left, Right
        (-1, 1),  (0, 1),  (1, 1)    # Bottom-left, Bottom-right
    )

    # key = index, value = priority
    ind_priority = {}

    for ind, symbol in enumerate(board):
        if symbol == 0:
            row = ind // board_sz
            col = ind % board_sz
            origin_d = max(abs(row - origin_row), abs(col - origin_col))  # calculate Chebyshev distance

            ind_priority[ind] = ind_priority.get(ind, 0) - origin_d  # set distance-dependent base priority

            for dir_x, dir_y in adjacents:
                fwd1_row = row + dir_y
                fwd1_col = col + dir_x

                if 0 <= fwd1_row < board_sz and 0 <= fwd1_col < board_sz and board[fwd1_row * board_sz + fwd1_col] == opp:  # if ind has an adjacent player cell

                    ind_priority[ind] += board_sz  # +board_sz ensures the furthest index with 1 adjacent player cell has higher priority than the closest lone index

                    fwd2_row = fwd1_row + dir_y
                    fwd2_col = fwd1_col + dir_x

                    if 0 <= fwd2_row < board_sz and 0 <= fwd2_col < board_sz and board[fwd2_row * board_sz + fwd2_col] == opp:  # if ind is connected to either end of a line formed by player

                        ind_priority[ind] += board_sz * 8  # +board_sz*8 ensures the furthest index connected to 1 line formed by player has higher priority than an index surrounded by 8 player cells

                        back1_row = row - dir_y
                        back1_col = col - dir_x

                        if 0 <= back1_row < board_sz and 0 <= back1_col < board_sz:  # if ind is at the back of another ind connected to either end of a line formed by player
                            back1_ind = back1_row * board_sz + back1_col

                            if board[back1_ind] == 0:
                                ind_priority[back1_ind] = ind_priority.get(back1_ind, 0) + board_sz*8

    print(f'\nIndex Priority: {ind_priority}')

    # get top 12 priorities
    simmable_inds = sorted(ind_priority, key=ind_priority.get, reverse=True)[:13]

    print(f'Simulatable Indexes: {simmable_inds}')

    return simmable_inds


def fac_tree_layout(graph, root=None) -> dict:
    """
    Creates a hierarchical layout for a directed factorial tree graph. Property of a factorial tree graph:
        |
        - the total number of children from 1 parent equals the total number of parents minus 1.

    :param graph: networkx graph object (must be directed).
    :param root: root node of the tree (if None, chooses an arbitrary node).
    :return: dictionary whose key = node, val = coord of the node saved as a tuple (x, y).
    """
    if root is None:
        root = next(iter(graph))  # Select an arbitrary root if not provided

    def assign_pos(parent, parent_x: float = 0.0, parent_y: float = 0.0):
        """
        Recursively updating coord of parent nodes and calculating coord of child nodes.
        """
        pos[parent] = (parent_x, parent_y)
        children = list(graph.successors(parent))
        if children:
            total_child_sep = math.factorial(len(children)) - math.factorial(len(children)-1)
            child_sep = total_child_sep / (len(children)-1)

            for i, child in enumerate(children):
                assign_pos(child, parent_x - total_child_sep/2 + i*child_sep, parent_y - 1)

    pos = {}
    assign_pos(root)
    return pos


def pc_input(pc: int, main_board: list, board_sz: int, win_len: int, origin: int, simmable_inds: list, is_debugging: bool) -> int:
    board_sz_sub1 = board_sz-1
    board_sz_add1 = board_sz+1
    half_win_len = win_len // 2
    bsz_sub_hwl = board_sz - half_win_len
    max_row_ind = board_sz * board_sz_sub1

    def is_plyr_win(board: list, plyr: int, origin: int) -> bool:
        """
        :param board: same as board in pc_input
        :param origin: latest move made on the board
        :param plyr: player who made the move at 'origin'
        """
        # OPTIMIZATION:
        # 1. only check for the row/col/diagonals connected to the origin
        # 2. only check for whether the current plyr of this node wins, because only the current plyr is allowed to move (and may win)
        # 3. pre-calculate only once: half_win_len, board_sz_sub1, board_sz_add1, bsz_sub_hwl, max_row_ind, origin_col, origin_row

        origin_col = origin % board_sz
        origin_row = origin // board_sz

        # check column
        # I put check column as the first function as it is the fastest to complete
        start = origin
        end = origin

        if (origin_row >= half_win_len and board[origin - board_sz * half_win_len] == plyr) or (origin_row < bsz_sub_hwl and board[origin + board_sz * half_win_len] == plyr):

            while (start >= board_sz) and board[start - board_sz] == plyr:
                start -= board_sz
            while (end < max_row_ind) and board[end + board_sz] == plyr:
                end += board_sz

            if end // board_sz - start // board_sz + 1 >= win_len:
                return True

        # check row
        start = origin
        end = origin

        if (origin_col >= half_win_len and board[origin - half_win_len] == plyr) or (origin_col < bsz_sub_hwl and board[origin + half_win_len] == plyr):

            while (start % board_sz > 0) and board[start - 1] == plyr:
                start -= 1
            while (end % board_sz < board_sz_sub1) and board[end + 1] == plyr:
                end += 1

            if end - start + 1 >= win_len:
                return True

        # check top left to down right
        start = origin
        end = origin

        if (origin_row >= half_win_len <= origin_col and board[origin - board_sz_add1 * half_win_len] == plyr) or (
                origin_row < bsz_sub_hwl > origin_col and board[origin + board_sz_add1 * half_win_len] == plyr):

            while (start >= board_sz) and (start % board_sz > 0) and board[start - board_sz_add1] == plyr:
                start -= board_sz_add1
            while (end < max_row_ind) and (end % board_sz < board_sz_sub1) and board[end + board_sz_add1] == plyr:
                end += board_sz_add1

            if (end // board_sz - start // board_sz) + 1 >= win_len:
                return True

        # check top right to down left
        start = origin
        end = origin

        if (origin_row >= half_win_len and origin_col < bsz_sub_hwl and board[origin - board_sz_sub1 * half_win_len] == plyr) or (
                origin_row < bsz_sub_hwl and origin_col >= half_win_len and board[origin + board_sz_sub1 * half_win_len] == plyr):

            while (start >= board_sz) and (start % board_sz < board_sz_sub1) and board[start - board_sz_sub1] == plyr:
                start -= board_sz_sub1
            while (end < max_row_ind) and (end % board_sz > 0) and board[end + board_sz_sub1] == plyr:
                end += board_sz_sub1

            if (end // board_sz - start // board_sz) + 1 >= win_len:
                return True

        return False

    def is_white(parent: list, parent_plyr: int, parent_origin: int) -> bool:
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
        child_plyr = opp(parent_plyr)

        for i, sim_ind in enumerate(simmable_inds):
            del simmable_inds[i]

            child = parent
            child[sim_ind] = child_plyr

            if is_plyr_win(child, child_plyr, sim_ind) is True or (len(simmable_inds) == 0 and child_plyr == pc) or (len(simmable_inds) != 0 and is_white(child, child_plyr, sim_ind) is True):
                # if a child is white
                # or if a child is tie (not white) and is at the bottommost layer and the bottommost layer is pc's turn
                # or if a child is white and is not at the bottommost layer yet
                white_num['Lyr ' + str(len(simmable_inds))] += 1

                child[sim_ind] = 0
                simmable_inds.insert(i, sim_ind)
                return False

            child[sim_ind] = 0
            simmable_inds.insert(i, sim_ind)

        return True

    for i, sim_ind in enumerate(simmable_inds):
        global white_num
        white_num = {f"Lyr {i}": 0 for i in range(len(simmable_inds)-1, -1, -1)}

        del simmable_inds[i]

        child = main_board
        child[sim_ind] = pc

        if is_plyr_win(child, pc, sim_ind) is True or is_white(child, pc, sim_ind) is True:
            white_num['Lyr ' + str(len(simmable_inds))] += 1
            print('Number of white nodes at', sim_ind, ':', white_num)

            simmable_inds.insert(i, sim_ind)

            return sim_ind
        else:
            print('Number of white nodes at', sim_ind, ':', white_num)

            child[sim_ind] = 0
            simmable_inds.insert(i, sim_ind)


def pc_input_v1(pc: int, main_board: list, board_sz: int, win_len: int, origin: int, simmable_inds: list, is_debugging: bool) -> int:
    board_sz_sub1 = board_sz-1
    board_sz_add1 = board_sz+1
    half_win_len = win_len // 2
    bsz_sub_hwl = board_sz - half_win_len
    max_row_ind = board_sz * board_sz_sub1

    simmable_inds = simmable_inds[:9]  # CZY AI is only capable of simulating 9 indexes

    def is_plyr_win(board: list, plyr: int, origin: int) -> bool:
        """
        :param board: same as board in pc_input
        :param origin: latest move made on the board
        :param plyr: player who made the move at 'origin'
        """
        # OPTIMIZATION:
        # 1. only check for the row/col/diagonals connected to the origin
        # 2. only check for whether the current plyr of this node wins, because only the current plyr is allowed to move (and may win)
        # 3. pre-calculate only once: half_win_len, board_sz_sub1, board_sz_add1, bsz_sub_hwl, max_row_ind, origin_col, origin_row

        origin_col = origin % board_sz
        origin_row = origin // board_sz

        # check column
        # I put check column as the first function as it is the fastest to complete
        start = origin
        end = origin

        if (origin_row >= half_win_len and board[origin - board_sz * half_win_len] == plyr) or (origin_row < bsz_sub_hwl and board[origin + board_sz * half_win_len] == plyr):

            while (start >= board_sz) and board[start - board_sz] == plyr:
                start -= board_sz
            while (end < max_row_ind) and board[end + board_sz] == plyr:
                end += board_sz

            if end // board_sz - start // board_sz + 1 >= win_len:
                return True

        # check row
        start = origin
        end = origin

        if (origin_col >= half_win_len and board[origin - half_win_len] == plyr) or (origin_col < bsz_sub_hwl and board[origin + half_win_len] == plyr):

            while (start % board_sz > 0) and board[start - 1] == plyr:
                start -= 1
            while (end % board_sz < board_sz_sub1) and board[end + 1] == plyr:
                end += 1

            if end - start + 1 >= win_len:
                return True

        # check top left to down right
        start = origin
        end = origin

        if (origin_row >= half_win_len <= origin_col and board[origin - board_sz_add1 * half_win_len] == plyr) or (
                origin_row < bsz_sub_hwl > origin_col and board[origin + board_sz_add1 * half_win_len] == plyr):

            while (start >= board_sz) and (start % board_sz > 0) and board[start - board_sz_add1] == plyr:
                start -= board_sz_add1
            while (end < max_row_ind) and (end % board_sz < board_sz_sub1) and board[end + board_sz_add1] == plyr:
                end += board_sz_add1

            if (end // board_sz - start // board_sz) + 1 >= win_len:
                return True

        # check top right to down left
        start = origin
        end = origin

        if (origin_row >= half_win_len and origin_col < bsz_sub_hwl and board[origin - board_sz_sub1 * half_win_len] == plyr) or (
                origin_row < bsz_sub_hwl and origin_col >= half_win_len and board[origin + board_sz_sub1 * half_win_len] == plyr):

            while (start >= board_sz) and (start % board_sz < board_sz_sub1) and board[start - board_sz_sub1] == plyr:
                start -= board_sz_sub1
            while (end < max_row_ind) and (end % board_sz > 0) and board[end + board_sz_sub1] == plyr:
                end += board_sz_sub1

            if (end // board_sz - start // board_sz) + 1 >= win_len:
                return True

        return False

    def recur(parent: list, pc: int, parent_origin: int) -> bool:

        is_win = is_plyr_win(parent, pc, parent_origin)

        if is_win is True:  # this layer is always pc
            win_probs[init_ind] += len(simmable_inds) + 1   # +1 because len(simmable_inds) can be 0

        elif is_win is False and len(simmable_inds) != 0:     # if this node has no winner and not tie yet, continue branching down.
            plyr = opp(pc)

            for i, sim_ind in enumerate(simmable_inds):
                del simmable_inds[i]

                child = parent
                child[sim_ind] = plyr

                is_win = is_plyr_win(child, plyr, sim_ind)

                if is_win is True:  # this layer is always player
                    win_probs[init_ind] -= (len(simmable_inds) + 1)

                    child[sim_ind] = 0
                    simmable_inds.insert(i, sim_ind)
                    return False

                elif is_win is False and len(simmable_inds) != 0:

                    if parent_origin == init_ind:  # if this is the first recursion
                        all_child_lost = True

                    for ii, sim_ind_ii in enumerate(simmable_inds):
                        del simmable_inds[ii]

                        child_ii = child
                        child_ii[sim_ind_ii] = pc

                        if recur(child_ii, pc, sim_ind_ii) is None and parent_origin == init_ind:
                            all_child_lost = False

                            child[sim_ind_ii] = 0
                            simmable_inds.insert(ii, sim_ind_ii)
                            break  # OPTIMIZATION ?

                        child[sim_ind_ii] = 0
                        simmable_inds.insert(ii, sim_ind_ii)

                    if parent_origin == init_ind is True and all_child_lost is True:
                        del win_probs[init_ind]
                        print(f'Deathtrap Found: Index {init_ind}')

                        child[sim_ind] = 0
                        simmable_inds.insert(i, sim_ind)
                        return False

                child[sim_ind] = 0
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
        global init_ind
        init_ind = sim_ind

        del simmable_inds[i]

        child = main_board
        child[sim_ind] = pc

        recur(child, pc, sim_ind)

        child[sim_ind] = 0
        simmable_inds.insert(i, sim_ind)

    fin_move = pick_init_move(pc, win_probs)

    if is_debugging:
        plt.clf()
        p = plt.bar(list(win_probs.keys()), list(win_probs.values()), color='c')
        plt.bar_label(p, label_type='center')
        plt.locator_params(axis='x', nbins=board_sz * win_len + 1)  # sets the tick interval of graph
        plt.title('Computer\'s Risk Analysis of each Initial Move')
        plt.xlabel('Initial Move')
        plt.ylabel('Winning Probability')
        plt.show()

    return fin_move