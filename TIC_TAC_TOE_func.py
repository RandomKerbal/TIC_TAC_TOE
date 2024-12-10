import random
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import pygraphviz_layout


def set_win_len(board_sz: int) -> int:
    return board_sz//4 + 3


# def set_check_winner_area(board_sz: int, win_len: int) -> set:
#     """
#     :return: check_winner_area (set containing a win_len**2 area of indexes in the top left corner of board)
#     """
#     check_winner_area = set()
#     for row in range(board_sz - win_len + 1):
#         for col in range(board_sz - win_len + 1):
#             check_winner_area.add(row * board_sz + col)
#
#     return check_winner_area


def setup_board(board_sz: int) -> list:
    # setup board layout
    # eg 3x3 board = [' ',' ',' '
    #                 ' ',' ',' '
    #                 ' ',' ',' ', 'initial_move']
    main_board = [' '] * (board_sz**2)
    # main_board.append('_')  # TODO

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
            if board[ii] == ' ':
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
    Limits indexes that PC can simulate to the 12 empty indexes with the highest priority.
    Assigns priority to indexes accordingly:
        1. index is adjacent to the origin -> highest priority.
        2. index is 1 of the 2 at each ends of each line formed by player -> within the middle priorities; varies with dist to origin and the number of connected lines.
        3. index has adjacent player cell -> within the lowest priorities; varies with dist to origin and the number of adjacent player cells.
    :return: simmable_inds
    """
    # convert origin to coords and clamp between 1 to board_sz-2 -> ensure all adjacents are inside board.
    origin_row = max(1, min(origin // board_sz, board_sz-2))
    origin_col = max(1, min(origin % board_sz, board_sz-2))

    # setup coords (x_coord, y_coord) of 8 indexes around a center
    adjacents = (
        (-1, -1), (0, -1), (1, -1),  # Top-left, Top-right
        (-1, 0),           (1, 0),   # Left, Right
        (-1, 1),  (0, 1),  (1, 1)    # Bottom-left, Bottom-right
    )

    # stores the 12 indexes
    simmable_inds = []

    # key = index, value = priority
    ind_priority = {}

    for ind, symbol in enumerate(board):
        if symbol == ' ':
            row = ind // board_sz
            col = ind % board_sz

            origin_d = max(abs(row - origin_row), abs(col - origin_col))  # Chebyshev distance

            if origin_d <= 1:  # if the index is adjacent the origin
                simmable_inds.append(ind)
                continue

            else:
                ind_priority[ind] = ind_priority.get(ind, 0) - origin_d  # set distance-dependent base priority

                for dir_x, dir_y in adjacents:
                    fwd1_row = row + dir_y
                    fwd1_col = col + dir_x

                    if 0 <= fwd1_row < board_sz and 0 <= fwd1_col < board_sz and board[fwd1_row * board_sz + fwd1_col] == opp:  # if ind has an adjacent player cell

                        ind_priority[ind] += board_sz  # +board_sz ensures the furthest index with 1 adjacent player cell has higher priority than the closest lone index

                        fwd2_row = fwd1_row + dir_y
                        fwd2_col = fwd1_col + dir_x

                        if 0 <= fwd2_row < board_sz and 0 <= fwd2_col < board_sz and board[fwd2_row * board_sz + fwd2_col] == opp:  # if ind is at the end of a line formed by player

                            back1_row = row - dir_y
                            back1_col = col - dir_x
                            back1_ind = back1_row * board_sz + back1_col

                            if 0 <= back1_row < board_sz and 0 <= back1_col < board_sz and board[back1_ind] == ' ':  # if the 2nd index at the end of the line formed by player is valid

                                ind_priority[ind] += 8
                                # +8 ensures any index connected to 1 line formed by player has higher priority than an index fully surrounded by player cells.
                                # Why not +board_sz+8 -> +board_sz was done 2 if statements outside.

                                ind_priority[back1_ind] = ind_priority.get(back1_ind, 0) + board_sz + 8

    print(f'\nIndex priority: {ind_priority}')

    simmable_inds.extend(
        sorted(ind_priority, key=ind_priority.get, reverse=True)
    )

    simmable_inds = simmable_inds[:12]

    print(f'Simulatable indexes: {simmable_inds}')

    return simmable_inds


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
        :param parent: the board at the parent node
        :param parent_origin: latest move made on board 'parent'
        :param parent_plyr: the plyr who made the move 'parent_origin' on the board 'parent'
        | Finds the path where:
            i) the PC has at least 1 winning path whenever it's human's turn
            ii) the human has 0 winning paths whenever it's PC's turn

        Returns True if all children are 'black' -> their parent's player will win -> their parent is 'white'. Returns False if any children are 'white' -> their parent's player will lose -> their parent is 'black'.
            'Black': this node lost for whoever is playing at that layer.

            'White': this node won for whoever is playing at that layer.
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

                child[sim_ind] = ' '
                simmable_inds.insert(i, sim_ind)
                return False

            child[sim_ind] = ' '
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

            child[sim_ind] = ' '
            simmable_inds.insert(i, sim_ind)


def pc_input_v1(pc: int, main_board: list, board_sz: int, win_len: int, origin: int, simmable_inds: list, is_debugging: bool) -> int:
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

    def analyze_child(parent: list, parent_plyr: int, parent_origin: int) -> bool:

        is_win = is_plyr_win(parent, parent_plyr, parent_origin)

        if is_win is True:
            if parent_plyr is pc:
                win_probs[parent[-1]] += len(simmable_inds)+1   # +1 since len(simmable_inds) can be 0
                return True

            else:  # if parent_plyr is not pc
                win_probs[parent[-1]] -= (len(simmable_inds)+1)
                return False

        elif is_win is False and len(simmable_inds) != 0:     # if this node has no winner and not tie yet, continue branching down.
            child_plyr = opp(parent_plyr)
            win_child_count = len(simmable_inds)//2

            for i, sim_ind in enumerate(simmable_inds):
                del simmable_inds[i]

                child = parent
                child[sim_ind] = child_plyr

                # if child[-1] == '_':
                #     child[-1] = sim_ind
                #     analyze_child(child, child_plyr, sim_ind)

                # elif analyze_child(child, child_plyr, sim_ind) is False:
                #     if child_win_count > 1:    # if less than 1/2 of the childs lost, continue countdown
                #         child_win_count -= 1
                #     elif child_win_count == 1:   # OPTIMIZATION: if more than 1/2 of the childs lost, this parent kills itself and assume all children loss.
                #         win_probs[parent[-1]] -= math.factorial(len(simmable_inds)//2)
                #         simmable_inds.insert(i, sim_ind)
                #         return False

                child[sim_ind] = ' '
                simmable_inds.insert(i, sim_ind)

    def pick_init_move(plyr: str, outcomes: dict) -> int:
        # find which first-gen move results in the most winning child nodes
        max_win_prob = max(outcomes.values())

        # moves_pool creates a list of initial moves containing the same highest win_prob to be picked randomly
        moves_pool = [key for key, value in outcomes.items() if value == max_win_prob]
        move = moves_pool[random.randint(0, len(moves_pool) - 1)]

        # try putting the final move decision onto the current board to check for any statistical deathtraps
        # statistical deathtraps are only confirmed to exist on 3x3 board
        main_board_copy = main_board.copy()
        main_board_copy[move] = plyr
        # if (the board l is 3) and (deathtrap is present) and (there are still other moves to play other than this move):
        # if board_sz == 3 and check_deathtrap(plyr, main_board_copy) and len(list(outcomes.keys())) > 1:
        #     print('Deathtrap found! Choosing a new move...')
        #     if is_debugging:
        #         debugger.insert(tk.END, 'PC\'s comment:\nDeathtrap found! Choosing a new move...\n')
        #     outcomes.pop(move)
        #     move = pick_init_move(plyr, outcomes)
        return move

    # def check_deathtrap(plyr: str, board: list) -> bool:
    #     # a statistical deathtrap is a first-gen move that appeared to be statistically superior to all other first-gen moves, but it will lead to an outcome like this (computer is X):
    #     # [O] [ ] [X]
    #     # [ ] [X] [ ]
    #     # [O] [ ] [O]
    #     # simulates the current board with the final move decision 3 times into the future
    #     # a statistical deathtrap can be identified by checking 3 moves later, whether all the child nodes of a parent node will loose
    #     for next_move in next_moves[1:]:
    #         if check_winner_anywhere(next_move, board_sz, win_len, check_winner_area) == (' ', ' ',):
    #             next_next_moves = give_birth(plyr, next_move)
    #             death_count = 0
    #             for next_next_move in next_next_moves[1:]:
    #                 if check_winner_anywhere(next_next_move, board_sz, board_sz, [0]) == (' ', ' ',):
    #                     next_next_next_moves = give_birth(opp(plyr), next_next_move)
    #                     for next_next_next_move in next_next_next_moves[1:]:
    #                         if check_winner_anywhere(next_next_next_move, board_sz, board_sz, [0])[0] == 'X':
    #                             # counts how many child nodes loose
    #                             death_count += 1
    #
    #             # if all the child nodes loose, the first-gen move is a deathtrap
    #             if death_count > len(next_next_moves):
    #                 return True
    #     return False

    win_probs = {ind: 0 for ind in simmable_inds}   # dict saved as {'initial_move_n': win_probability_of_n}
    analyze_child(main_board, opp(pc), prev_input)
    fin_move = pick_init_move(pc, win_probs)
    if is_debugging:
        plt.clf()
        p = plt.bar(list(win_probs.keys()), list(win_probs.values()), color='c')
        plt.bar_label(p, label_type='center')
        plt.locator_params(axis='x', nbins=board_sz * win_len + 1)  # sets the tick interval of graph
        plt.title('Computer\'s Risk Analysis of each 1st-Gen Move')
        plt.xlabel('1st-Generation Move')
        plt.ylabel('Winning Probability')
        plt.show()
    return int(fin_move)