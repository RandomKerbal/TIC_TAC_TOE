import math
import random
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import pygraphviz_layout
import tkinter as tk


def set_win_len(board_sz: int) -> int:
    return min(board_sz, 4)


def set_check_winner_area(board_sz: int, win_len: int) -> list:
    check_winner_area = []
    for ind in range(board_sz**2):
        # if (the ind row is l dist away from the bottom row) and (the ind column is l dist away from the rightmost column)
        if (ind < board_sz**2 - board_sz*(win_len-1)) and (ind % board_sz <= board_sz-win_len):
            check_winner_area.append(ind)

    return check_winner_area


def setup_board(board_sz: int) -> list:
    # setup board layout
    # eg 3x3 board = ['[ ]','[ ]','[ ]'
    #                 '[ ]','[ ]','[ ]'
    #                 '[ ]','[ ]','[ ]', 'initial_move']
    main_board = [' ' for _ in range(board_sz**2)]
    main_board.append('_')

    return main_board


def print_board(board: list, board_sz: int) -> None:
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


def opp(original: str) -> str:
    # changes player X to O, O to X
    if original == 'O':
        return 'X'
    else:
        return 'O'


def coord_to_ind(coord: str, main_board: list, board_sz: int) -> int | bool:
    # converts the x,y coordinates inputted by player to ind number
    # eg ind num of 3x3 board
    # [0] [1] [2]
    # [3] [4] [5]
    # [6] [7] [8]

    # if player inputs gibberish, return False
    if (coord[:coord.find(',')].isdigit() is False) or (coord[coord.find(',') + 1:].isdigit() is False):
        return False

    # if the player inputted valid coordinates...
    # take the first number as the column num, the second number as the row num
    # I observed that the ind num = (row num*board len) + column num
    ind = int(coord[:coord.find(',')]) + ((int((coord[coord.find(',') + 1:])) - 1) * board_sz) - 1

    # if the ind number exceeds the board, return False
    if ind + 1 > (board_sz**2):
        return False
    # if the ind number is negative, return False
    elif ind < 0:
        return False
    # if the that ind alr has an X or O, return False
    elif main_board[ind] != ' ':
        return False
    else:
        return ind


def check_winner_anywhere(board: list, board_sz: int, win_len: int, check_winner_area: list) -> tuple:
    # Different from check_winner(), check_winner_anywhere() is used when the rows, columns, and diagonals could be anywhere and not just fixed to the edge of the board.
    # Because the checked_area's origin is its top left corner, the distance from the origin to the bottom right corner of board must be larger than the checked area.
    # For a 5x5 and 4x4 checked area, the origin cannot be at:
    #     0,  1,  NO, NO, NO,
    #     5,  6,  NO, NO, NO,
    #     NO, NO, NO, NO, NO,
    #     NO, NO, NO, NO, NO,
    #     NO, NO, NO, NO, NO
    x_win_formation = ['X' for _ in range(win_len)]
    o_win_formation = ['O' for _ in range(win_len)]
    # OPTIMIZATION:
    # Instead of checking every ind to find those that r outside the checked area, I give the AI indexes that r outside.
    for origin in check_winner_area:
        # OPTIMIZATIONS:
        # 1. Use 'not in' as it is faster than .count()
        # 2. Returns the result as a tuple instead of list.
        # 3. Check the diagonals before the orthogonals. This does not need for loops.
        # if the top left corner has an X and the diagonal top left to down right is filled with X, then X wins.
        if board[origin] == 'X' and board[origin: origin + board_sz * win_len: board_sz + 1] == x_win_formation:
            return 'X', 'from top left to down right',
        # if the top left corner has an O and the diagonal top left to down right is filled with O, then O wins.
        elif board[origin] == 'O' and board[origin: origin + board_sz * win_len: board_sz + 1] == o_win_formation:
            return 'O', 'from top left to down right',

        # if the top right corner has an X and the diagonal top right to down left is filled with X, then X wins.
        elif board[origin + win_len - 1] == 'X' and board[
                                                    origin + win_len - 1: origin + board_sz * win_len - 1: board_sz - 1] == x_win_formation:
            return 'X', 'from top right to down left',
        # if the top right corner has an O and the diagonal top right to down left is filled with O, then O wins.
        elif board[origin + win_len - 1] == 'O' and board[
                                                    origin + win_len - 1: origin + board_sz * win_len - 1: board_sz - 1] == o_win_formation:
            return 'O', 'from top right to down left',

        else:
            # 4. Instead of using 2 loops for column and row, use only 1 loop that moves one column left and one row down together.
            for count in range(0, win_len):
                # for every X/O in the first row, check if its column is filled with either X/O
                if board[origin + count] != ' ':
                    # if board[checker's current pos: l dist to the right]
                    if board[origin + count: origin + board_sz * win_len: board_sz] == x_win_formation:
                        return 'X', 'vertically',
                    elif board[origin + count: origin + board_sz * win_len: board_sz] == o_win_formation:
                        return 'O', 'vertically',

                # for every X/O in the first column, check if its row is filled with either X/O
                if board[count * board_sz + origin] != ' ':
                    # if board[checker's current pos: l dist downwards]
                    if board[count * board_sz + origin: count * board_sz + origin + win_len] == x_win_formation:
                        return 'X', 'horizontally',
                    elif board[count * board_sz + origin: count * board_sz + origin + win_len] == o_win_formation:
                        return 'O', 'horizontally',

            # If no one wins yet and no empty ind left, the game is a draw.
            if ' ' not in board:
                return ' ', 'tie',
    # If no one wins yet but there are empty indexes, game continues.
    return ' ', ' ',


# ALL FUNCTIONS BELOW ARE FOR THE AI
def ask_input(plyr: str, main_board: list, board_sz: int, win_len: int, check_winner_area: list) -> int:
    while check_winner_anywhere(main_board, board_sz, win_len, check_winner_area) == (' ', ' ',):
        print_board(main_board, board_sz)
        player_coord = input(f'Your turn [{plyr}]! Choose your x,y coordinates: ')
        global ind
        ind = coord_to_ind(player_coord, main_board, board_sz)
        if ind is False:
            print('Invalid Position!')
        else:
            return ind
    return -1


def pc_input(pc: str, main_board: list, board_sz: int, win_len: int, check_winner_area: list, prev_input: int, is_debugging: bool, debugger=None, ind_buttons=None) -> int:

    def prune(origin: int):
        """
        Limits the indexes that PC can simulate to the 12 empty indexes closest to the origin.
        """
        # OPTIMIZATIONS:
        #   only reserve empty indexes in the 3x3 area around the origin
        #   If there aren't enough empty indexes:
        #   ...also reserve empty indexes in the 4 corners of the 5x5 area around the origin (aka diagonal adjacents)
        #   If there still aren't enough empty indexes:
        #   ...also reserve 4 empty indexes at the top, bottom, left, & right of the 5x5 area
        #   If there still still aren't enough empty indexes:
        #   also reserve rest of the empty indexes in the 5x5 area

        # indexes in the reserved_area are stored as (x_coord, y_coord)
        reserved_area = []

        start_col = max(0, min(origin % board_sz - 1, board_sz - 3))
        start_row = max(0, min(origin // board_sz - 1, board_sz - 3))

        # add coords of 3x3 area around the origin
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                reserved_area.append((col, row))

        # add coords of the 4 diagonal adjacents, in clock-wise order
        reserved_area.append((start_col - 1, start_row - 1))
        reserved_area.append((start_col + 3, start_row - 1))
        reserved_area.append((start_col + 3, start_row + 3))
        reserved_area.append((start_col - 1, start_row + 3))

        # add coords of the 4 orthogonal adjacents, in clock-wise order
        reserved_area.append((start_col + 1, start_row - 1))
        reserved_area.append((start_col + 3, start_row + 1))
        reserved_area.append((start_col + 1, start_row + 3))
        reserved_area.append((start_col - 1, start_row + 1))

        # add coords of the rest of the indexes, in clock-wise order
        # central 3x3 must come before diagonal adjs, and...
        # diagonal adjs must come before the orthogonal adjs, and...
        # orthogonal adjs must come before the rest, as items are ignored starting from the back if there alr r enough empty indexes
        reserved_area.append((start_col, start_row - 1))
        reserved_area.append((start_col + 2, start_row - 1))
        reserved_area.append((start_col + 3, start_row))
        reserved_area.append((start_col + 3, start_row + 2))
        reserved_area.append((start_col + 2, start_row + 3))
        reserved_area.append((start_col, start_row + 3))
        reserved_area.append((start_col - 1, start_row + 2))
        reserved_area.append((start_col - 1, start_row))

        # simmable_inds records the 12 indexes
        global simmable_inds
        simmable_inds = []

        # if the indexes in reserved_area are:
        #   1. within the board (0 <= ind_index < len)
        #   2. ' ' on the board
        #   and there aren't enough empty indexes.
        # then add them back to simmable_inds
        count = 1
        for coord in reserved_area:
            if (0 <= coord[0] < board_sz and 0 <= coord[1] < board_sz) and (main_board[coord[1] * board_sz + coord[0]] == ' ') and count <= 12:
                ind = coord[1] * board_sz + coord[0]
                simmable_inds.append(ind)
                if is_debugging:
                    ind_buttons[ind].config(background='Lemon Chiffon2')
                count += 1

        debugger.insert(tk.END, 'Empty indexes after prunning:\n' + str(simmable_inds) + '\n')
        print(f'\nEmpty indexes: {simmable_inds}')

    def is_plyr_win(board: list, plyr: str, origin: int) -> bool:
        half_win_len = win_len // 2
        origin_col = origin % board_sz
        origin_row = origin // board_sz
        board_sz_neg1 = board_sz - 1

        # check column
        # I put check column as the first function as it is the fastest to complete
        start = origin
        end = origin

        if (origin_row >= half_win_len and board[origin - board_sz * half_win_len] == plyr) or (origin_row < board_sz - half_win_len and board[origin + board_sz * half_win_len] == plyr):

            while (start >= board_sz) and board[start - board_sz] == plyr:
                start -= board_sz
            while (end < board_sz * board_sz_neg1) and board[end + board_sz] == plyr:
                end += board_sz

            if end // board_sz - start // board_sz + 1 >= win_len:
                return True

        # check row
        start = origin
        end = origin

        if (origin_col >= half_win_len and board[origin - half_win_len] == plyr) or (origin_col < board_sz - half_win_len and board[origin + half_win_len] == plyr):

            while (start % board_sz > 0) and board[start - 1] == plyr:
                start -= 1
            while (end % board_sz < board_sz_neg1) and board[end + 1] == plyr:
                end += 1

            if end - start + 1 >= win_len:
                return True

        # check up left to down right
        start = origin
        end = origin

        if (origin_row >= half_win_len <= origin_col and board[origin - (board_sz + 1) * half_win_len] == plyr) or (
                origin_row < board_sz - half_win_len > origin_col and board[origin + (board_sz + 1) * half_win_len] == plyr):

            while (start >= board_sz) and (start % board_sz > 0) and board[start - (board_sz + 1)] == plyr:
                start -= (board_sz + 1)
            while (end < board_sz * board_sz_neg1) and (end % board_sz < board_sz_neg1) and board[end + board_sz + 1] == plyr:
                end += (board_sz + 1)

            if (end // board_sz - start // board_sz) + 1 >= win_len:
                return True

        # check up right to down left
        start = origin
        end = origin

        if (origin_row >= half_win_len and origin_col < board_sz - half_win_len and board[origin - board_sz_neg1 * half_win_len] == plyr) or (
                origin_row < board_sz - half_win_len and origin_col >= half_win_len and board[origin + board_sz_neg1 * half_win_len] == plyr):

            while (start >= board_sz) and (start % board_sz < board_sz_neg1) and board[start - board_sz_neg1] == plyr:
                start -= board_sz_neg1
            while (end < board_sz * board_sz_neg1) and (end % board_sz > 0) and board[end + board_sz_neg1] == plyr:
                end += board_sz_neg1

            if (end // board_sz - start // board_sz) + 1 >= win_len:
                return True

        return False

    def is_white(parent: list, parent_plyr: str, parent_origin: int) -> bool:
        """
        Finds the path where: i) the PC has at least 1 winning path whenever it's human's turn; ii) the human has 0 winning paths whenever it's PC's turn.

        Returns True if all children are 'black' -> their parent's player will win -> their parent is 'white'
            'Black': this node lost for whoever is playing at that layer.

        Returns False if any children are 'white' -> their parent's player will lose -> their parent is 'black'
            'White': this node won for whoever is playing at that layer.
        """
        child_plyr = opp(parent_plyr)

        for i in range(len(simmable_inds)):
            sim_ind = simmable_inds.pop(i)

            child = parent.copy()
            child[sim_ind] = child_plyr

            if is_plyr_win(child, child_plyr, sim_ind) is True or (len(simmable_inds) == 0 and child_plyr == pc) or (len(simmable_inds) != 0 and is_white(child, child_plyr, sim_ind) is True):
                # if a child is white
                # or if a child is tie (not white) and is at the bottommost layer and the bottommost layer is pc's turn
                # or if a child is white and is not at the bottommost layer yet
                white_num[str('Lyr ' + str(len(simmable_inds)))] += 1
                simmable_inds.insert(i, sim_ind)
                return False

            simmable_inds.insert(i, sim_ind)

        return True

    # def analyze_child(parent: list, parent_plyr: str, parent_origin: int) -> bool:
    #     child_plyr = opp(parent_plyr)
    #
    #     # OPTIMIZATION: I only check for whether the active plyr wins in this state because only the active plyr moved so is possible to win.
    #     plyr_win = is_plyr_win(parent, parent_plyr, parent_origin)
    #
    #     if plyr_win is True and parent_plyr is pc:
    #         win_probs[parent[-1]] += len(simmable_inds)+1   # +1 since len(simmable_inds) can be 0
    #
    #     elif plyr_win is True and parent_plyr is not pc:
    #         win_probs[parent[-1]] -= (len(simmable_inds)+1)
    #         return False
    #
    #     elif plyr_win is False and len(simmable_inds) != 0:     # if the parent node has no winner yet, and the tree can still branch, continue branching down.
    #         children_won = len(simmable_inds)//2
    #
    #         for i in range(len(simmable_inds)):
    #             sim_ind = simmable_inds.pop(i)
    #
    #             child = parent.copy()
    #             child[sim_ind] = child_plyr
    #             if child[-1] == '_':
    #                 child[-1] = sim_ind
    #                 analyze_child(child, child_plyr, sim_ind)
    #
    #             elif analyze_child(child, child_plyr, sim_ind) is False:
    #                 if children_won > 1:    # if less than 1/2 of the childs lost, continue countdown
    #                     children_won -= 1
    #                 elif children_won == 1:   # OPTIMIZATION: if more than 1/2 of the childs lost, this parent kills itself and assume all children loss.
    #                     win_probs[parent[-1]] -= math.factorial(len(simmable_inds)//2)
    #                     simmable_inds.insert(i, sim_ind)
    #                     return False
    #
    #             simmable_inds.insert(i, sim_ind)

    # def pick_init_move(plyr: str, outcomes: dict) -> int:
    #     # find which first-gen move results in the most winning child nodes
    #     max_win_prob = max(outcomes.values())
    #
    #     # moves_pool creates a list of initial moves containing the same highest win_prob to be picked randomly
    #     moves_pool = [key for key, value in outcomes.items() if value == max_win_prob]
    #     move = moves_pool[random.randint(0, len(moves_pool) - 1)]
    #
    #     # try putting the final move decision onto the current board to check for any statistical deathtraps
    #     # statistical deathtraps are only confirmed to exist on 3x3 board
    #     main_board_copy = main_board.copy()
    #     main_board_copy[move] = plyr
    #     # if (the board l is 3) and (deathtrap is present) and (there are still other moves to play other than this move):
    #     if board_sz == 3 and check_deathtrap(plyr, main_board_copy) and len(list(outcomes.keys())) > 1:
    #         print('Deathtrap found! Choosing a new move...')
    #         if is_debugging:
    #             debugger.insert(tk.END, 'PC\'s comment:\nDeathtrap found! Choosing a new move...\n')
    #         outcomes.pop(move)
    #         move = pick_init_move(plyr, outcomes)
    #     return move

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

    if prev_input == -1:  # if PC starts first
        return random.randint(0, board_sz**2 - 1)
    else:
        # if the board_sz <= 4, prune a 3x3 area around the most recent player input. I cannot prune a 4x4 area as 4x4 has no center ind.
        # if the board_sz >= 5, prune a 5x5 area around the most recent player input
        prune(prev_input)

        # if the 3x3 grid around the opponent's newest move are full, find the closest empty ind
        if len(simmable_inds) == 0:
            if is_debugging:
                debugger.insert(tk.END, 'PC\'s comment:\nNo empty indexes found! Randomly generating next move...')
            fin_move = random.choice([_ for _ in range(board_sz**2) if main_board[_] == ' '])

        else:
            for i in range(len(simmable_inds)):
                global white_num
                white_num = {f"Lyr {i}": 0 for i in range(len(simmable_inds)-1, -1, -1)}

                sim_ind = simmable_inds.pop(i)

                child = main_board.copy()
                child[sim_ind] = pc

                if is_plyr_win(child, pc, sim_ind) is True or is_white(child, pc, sim_ind) is True:
                    white_num[str('Lyr ' + str(len(simmable_inds)))] += 1
                    print('Number of white nodes at', sim_ind, ':', white_num)
                    return sim_ind
                else:
                    print('Number of white nodes at', sim_ind, ':', white_num)
                    simmable_inds.insert(i, sim_ind)

            # win_probs = {ind: 0 for ind in simmable_inds}   # dict saved as {'initial_move_n': win_probability_of_n}
            # analyze_child(main_board, opp(pc), prev_input)
            # fin_move = pick_init_move(pc, win_probs)
            # if is_debugging:
            #     plt.clf()
            #     p = plt.bar(list(win_probs.keys()), list(win_probs.values()), color='c')
            #     plt.bar_label(p, label_type='center')
            #     plt.locator_params(axis='x', nbins=board_sz * win_len + 1)  # sets the tick interval of graph
            #     plt.title('Computer\'s Risk Analysis of each 1st-Gen Move')
            #     plt.xlabel('1st-Generation Move')
            #     plt.ylabel('Winning Probability')
            #     plt.show()
    # return int(fin_move)
