import random
import matplotlib.pyplot as plt
import tkinter as tk


def set_win_len(board_sz: int) -> int:
    if 6 < board_sz:
        return round(board_sz / 2)
    else:
        return board_sz


def set_check_winner_area(board_sz: int, win_len: int) -> list:
    check_winner_area = []
    for slot in range(board_sz**2):
        # if (the slot row is l dist away from the bottom row) and (the slot column is l dist away from the rightmost column)
        if (slot < board_sz**2 - board_sz*(win_len-1)) and (slot % board_sz <= board_sz-win_len):
            check_winner_area.append(slot)

    return check_winner_area


def setup_board(board_sz: int) -> list:
    # setup board layout
    # eg 3x3 board = ['[ ]','[ ]','[ ]'
    #                 '[ ]','[ ]','[ ]'
    #                 '[ ]','[ ]','[ ]', 'initial_move']
    # OPTIMIZATION STRATEGIES:
    # the whole board is made up of 1 list, instead of 1 list per row
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
        for j in range(i*board_sz, (i*board_sz)+board_sz):
            if board[j] == ' ':
                print('[ ]', end=' ')
            else:
                print(' ' + board[j], end='  ')
    print(end='\n')


def opponent(original: str) -> str:
    # changes player X to O, O to X
    if original == 'O':
        return 'X'
    else:
        return 'O'


def coord_to_slot(coord: str, main_board: list, board_sz: int) -> int | bool:
    # converts the x,y coordinates inputted by player to slot number
    # eg slot num of 3x3 board
    # [0] [1] [2]
    # [3] [4] [5]
    # [6] [7] [8]

    # if player inputs gibberish, return False
    if (coord[:coord.find(',')].isdigit() is False) or (coord[coord.find(',') + 1:].isdigit() is False):
        return False

    # if the player inputted valid coordinates...
    # take the first number as the column num, the second number as the row num
    # I observed that the slot num = (row num*board len) + column num
    slot_num = int(coord[:coord.find(',')]) + ((int((coord[coord.find(',') + 1:])) - 1) * board_sz) - 1

    # if the slot number exceeds the board, return False
    if slot_num + 1 > (board_sz**2):
        return False
    # if the slot number is negative, return False
    elif slot_num < 0:
        return False
    # if the that slot alr has an X or O, return False
    elif main_board[slot_num] != ' ':
        return False
    else:
        return slot_num


def check_winner_anywhere(board: list, board_sz: int, win_len: int, check_winner_area: list) -> tuple:
    # Different from check_winner(), check_winner_anywhere() is used when the rows, columns, and diagonals could be anywhere and not just fixed to the edge of the board.
    # Because the checked_area's origin is its top left corner, the distance from the origin to the bottom right corner of board must be larger than the checked area.
    # For a 5x5 and 4x4 checked area, the origin cannot be at:
    #     0,  1,  NO, NO, NO,
    #     5,  6,  NO, NO, NO,
    #     NO, NO, NO, NO, NO,
    #     NO, NO, NO, NO, NO,
    #     NO, NO, NO, NO, NO

    # OPTIMIZATION STRATEGY:
    # Instead of checking every slot to find those that r outside the checked area, I give the AI indexes of slots that r outside.
    for origin in check_winner_area:
        # OPTIMIZATION STRATEGIES (numbered):
        # 1. Use 'not in' as it is faster than .count()
        # 2. Returns the result as a tuple instead of list.
        # 3. Check the diagonals before the orthogonals. This does not need for loops.
        # if the top left corner has an X and the diagonal top left to down right is filled with X, then X wins.
        if board[origin] == 'X' and board[origin: origin + board_sz * win_len: board_sz + 1].count('X') == win_len:
            return 'X', 'from top left to down right',
        # if the top left corner has an O and the diagonal top left to down right is filled with O, then O wins.
        elif board[origin] == 'O' and board[origin: origin + board_sz * win_len: board_sz + 1].count('O') == win_len:
            return 'O', 'from top left to down right',

        # if the top right corner has an X and the diagonal top right to down left is filled with X, then X wins.
        elif board[origin + win_len - 1] == 'X' and board[
                                                    origin + win_len - 1: origin + board_sz * win_len - 1: board_sz - 1].count(
                'X') == win_len:
            return 'X', 'from top right to down left',
        # if the top right corner has an O and the diagonal top right to down left is filled with O, then O wins.
        elif board[origin + win_len - 1] == 'O' and board[
                                                    origin + win_len - 1: origin + board_sz * win_len - 1: board_sz - 1].count(
                'O') == win_len:
            return 'O', 'from top right to down left',

        else:
            # 4. Instead of using 2 loops for column and row, use only 1 loop that moves one column left and one row down together.
            for count in range(0, win_len):
                # for every X/O in the first row, check if its column is filled with either X/O
                if board[origin + count] != ' ':
                    # if board[checker's current pos: l dist to the right]
                    if board[origin + count: origin + board_sz * win_len: board_sz].count('X') == win_len:
                        return 'X', 'vertically',
                    elif board[origin + count: origin + board_sz * win_len: board_sz].count('O') == win_len:
                        return 'O', 'vertically',

                # for every X/O in the first column, check if its row is filled with either X/O
                if board[count * board_sz + origin] != ' ':
                    # if board[checker's current pos: l dist downwards]
                    if board[count * board_sz + origin: count * board_sz + origin + win_len].count('X') == win_len:
                        return 'X', 'horizontally',
                    elif board[count * board_sz + origin: count * board_sz + origin + win_len].count('O') == win_len:
                        return 'O', 'horizontally',

            # If no one wins yet and no empty slot left, the game is a draw.
            if ' ' not in board:
                return ' ', 'tie',
    # If no one wins yet but there are empty slots, game continues.
    return ' ', ' ',


# ALL FUNCTIONS BELOW ARE FOR THE AI
def ask_input(plyr: str, main_board: list, board_sz: int, filled_slots_ind: list, win_len: int, check_winner_area: list) -> int:
    while check_winner_anywhere(main_board, board_sz, win_len, check_winner_area) == (' ', ' ',):
        print_board(main_board, board_sz)
        player_coord = input(f'Your turn [{plyr}]! Choose your x,y coordinates: ')
        global slot_num
        slot_num = coord_to_slot(player_coord, main_board, board_sz)
        if slot_num is False:
            print('Invalid Position!')
        else:
            filled_slots_ind.append(slot_num)
            return slot_num
    return -1


# noinspection PyUnboundLocalVariable
def pc_input(pc: str, main_board: list, board_sz: int, filled_slots_ind: list, win_len: int, check_winner_area: list, last_input: int, is_debugging: bool, debugger, slot_buttons) -> int:
    def prune(origin: int) -> list:
        # OPTIMIZATION STRATEGY:
        #   only reserve empty slots in the 3x3 area around the origin
        #   If there aren't enough empty slots:
        #   ...also reserve empty slots in the 4 corners of the 5x5 area around the origin (aka diagonal adjacents)
        #   If there still aren't enough empty slots:
        #   ...also reserve 4 empty slots at the top, bottom, left, & right of the 5x5 area
        #   If there still still aren't enough empty slots:
        #   also reserve rest of the empty slots in the 5x5 area

        # slots in the reserved_area are stored as (x_coord, y_coord)
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

        # add coords of the rest of the slots, in clock-wise order
        # central 3x3 must come before diagonal adjs, and...
        # diagonal adjs must come before the orthogonal adjs, and...
        # orthogonal adjs must come before the rest, as items are ignored starting from the back if there alr r enough empty slots
        reserved_area.append((start_col, start_row - 1))
        reserved_area.append((start_col + 2, start_row - 1))
        reserved_area.append((start_col + 3, start_row))
        reserved_area.append((start_col + 3, start_row + 2))
        reserved_area.append((start_col + 2, start_row + 3))
        reserved_area.append((start_col, start_row + 3))
        reserved_area.append((start_col - 1, start_row + 2))
        reserved_area.append((start_col - 1, start_row))

        # Creating the pruned board:
        # first fill all empty slots with 'N'
        pboard = ['N' if _ == ' ' else _ for _ in main_board]

        global empty_slots_ind
        empty_slots_ind = []

        # if the slots in reserved_area are:
        #   1. inside the board (0 <= slot_index < len)
        #   2. 'N' on the board
        #   and there aren't enough empty slots
        # then turn them back to '[ ]'
        count = 0
        for coord in reserved_area:
            if (0 <= coord[0] < board_sz and 0 <= coord[1] < board_sz) and (pboard[coord[1] * board_sz + coord[0]] == 'N') and count <= 8:
                slot = coord[1] * board_sz + coord[0]
                pboard[slot] = ' '
                empty_slots_ind.append(slot)
                if is_debugging:
                    slot_buttons[slot].config(background='lemon chiffon2')
                count += 1

        print(f'Player\'s move: {origin}')
        print_board(pboard, board_sz)
        print(f'Empty slots: {empty_slots_ind}')
        debugger.insert(tk.END, f'Player\'s move:\n{origin}\n')
        debugger.insert(tk.END, f'Pruned board:\n{pboard}\n')
        debugger.insert(tk.END, 'Empty slots on PBoard:\n' + str(empty_slots_ind) + '\n')

        return pboard

    def sim_childs(nxt_plyr: str, prev_move: list) -> list:
        # branches a parent node down by 1 layer
        # given that next player is 'plyr' and the board now looks like 'prev_move'...
        # returns a list of all possible moves that the player could play next
        # OPTIMIZATION STRATEGIES:
        # instead of every time checking all slots in the parent node for empty slots for simulation, I give the AI indexes of all slots that r empty
        prev_moves = [
            nxt_plyr
        ]
        for slot in empty_slots_ind:
            if prev_move[slot] == ' ':
                prev_moves.append(prev_move.copy())
                prev_moves[-1][slot] = nxt_plyr

                # if the child nodes are the first generation and are played by pc, record the first move as a str at the end of each board
                if prev_move[-1] == '_':
                    prev_moves[-1][-1] = slot

        return prev_moves

    def sort_childs(prev_moves: list):
        # For each move in 'prev_moves', branches it down by 1 layer.
        # Sorts the childs by whether the computer wins, looses, or draws. If no results, branches it down again...
        # OPTIMIZATION STRATEGIES:
        # 1. don't go through boards where player already win
        # 2. don't go through boards where player loss
        # 3. don't go through or save tie boards until when there is only a few empty slots left
        # 4. sets are faster and automatically don't repeat items

        for prev_move in prev_moves[1:]:
            # OPTIMIZATION STRATEGY:
            # 1. If the number of O is less than the number needed to win, then no one wins (assuming that a player can't win a 3x3 with just 3 moves, a 4x4 with just 4 moves, etc.), so we skip the check_winner().
            # 2. If there are no X/O in the first row and column, then no one wins so we skip the check_winner().
            if (prev_move.count('O') < win_len) or ('X' not in prev_move[: board_sz] and 'X' not in prev_move[: (board_sz**2): board_sz] and 'O' not in prev_move[: board_sz] and 'O' not in prev_move[0: (board_sz**2): board_sz]):
                sort_childs(sim_childs(opponent(prev_moves[0]), prev_move))

            else:
                winner = check_winner_anywhere(prev_move, board_sz, win_len, check_winner_area)
                if winner[0] == pc:
                    # end_moves saved as ({bad}, {good}, {tie})
                    end_moves[1].add(tuple(prev_move))
                elif winner[0] == opponent(pc):
                    end_moves[0].add(tuple(prev_move))
                elif winner[1] == 'tie' and len(empty_slots_ind) <= board_sz+1:
                    # if this is in tie, it doesn't affect final win_prob evaluation, so don't save them
                    # But, we still need the best tie boards so the computer can still make moves while unable to win...
                    # so, we start saving tie boards when there is only a few empty slots left
                    print('Start including draws in my calculation')
                    debugger.insert(tk.END, 'PC\'s comment:\nStart including draws in my calculation\n')
                    end_moves[2].add(tuple(prev_move))
                else:
                    # if the parent node has no outcome yet, continue branching down
                    sort_childs(sim_childs(opponent(prev_moves[0]), prev_move))

    def weight_init_moves(is_debugging: bool) -> dict:
        # recall that each child node saved its first-gen move
        win_probs = {}  # dict saved as {'initial_move_n': win_probability_of_n}

        # count the frequency of each first-gen move that results in a loosing child node
        # to punish a first-gen move that results in a loosing child node, its frequency is negative
        for end_move in end_moves[0]:
            if end_move[-1] not in win_probs:
                # we also see how long a first-gen move takes to lose, by counting the num of empty slots left when it lose
                # more empty slots = loss earlier = more risky
                # less empty slots = loss later = less risky
                win_probs[end_move[-1]] = -4 * (1+end_move.count(' '))
            else:
                win_probs[end_move[-1]] -= 4 * (1+end_move.count(' '))

        # count the frequency of each first-gen move that results in a winning child node
        # to reward a first-gen move that results in a winning child node, its frequency is positive
        for end_move in end_moves[1]:
            if end_move[-1] not in win_probs:
                # we also see how long a first-gen move takes to win, by counting the num of empty slots left when it win
                win_probs[end_move[-1]] = 2 * end_move.count(' ')
            else:
                win_probs[end_move[-1]] += 2 * end_move.count(' ')

        # count the frequency of each first-gen move that results in a draw child node
        # a first-gen move that results in a draw child node is not punished and not rewarded
        for end_move in end_moves[2]:
            if end_move[-1] not in win_probs:
                win_probs[end_move[-1]] = 0

        print(end_moves)
        print(win_probs)
        if is_debugging:
            plt.clf()
            p = plt.bar(list(win_probs.keys()), list(win_probs.values()), color='c')
            plt.bar_label(p, label_type='center')
            plt.locator_params(axis='x', nbins=board_sz * win_len + 1)  # sets the tick interval of graph
            plt.title('Computer\'s Risk Analysis of each 1st-Gen Move')
            plt.xlabel('1st-Generation Move')
            plt.ylabel('Winning Probability')
            plt.show()

        return win_probs

    def pick_init_move(plyr: str, outcomes: dict) -> int:
        # find which first-gen move results in the most winning child nodes
        max_win_prob = max(outcomes.values())

        # moves_pool creates a list of initial moves containing the same highest win_prob to be picked randomly
        moves_pool = [key for key, value in outcomes.items() if value == max_win_prob]
        move = moves_pool[random.randint(0, len(moves_pool) - 1)]

        # try putting the final move decision onto the current board to check for any statistical deathtraps
        # statistical deathtraps are only confirmed to exist on 3x3 board
        pboard_copy = pboard.copy()
        pboard_copy[move] = plyr
        # if (the board l is 3) and (deathtrap is present) and (there are still other moves to play other than this move):
        if board_sz == 3 and check_deathtrap(plyr, pboard_copy) and len(list(outcomes.keys())) > 1:
            print('Deathtrap found! Choosing a new move...')
            debugger.insert(tk.END, 'PC\'s comment:\nDeathtrap found! Choosing a new move...\n')
            outcomes.pop(move)
            move = pick_init_move(plyr, outcomes)
        return move

    def check_deathtrap(plyr: str, pboard: list) -> bool:
        # a statistical deathtrap is a first-gen move that appeared to be statistically superior to all other first-gen moves...
        # ...but it will lead to an outcome like this (computer is X):
        # [O] [ ] [X]
        # [ ] [X] [ ]
        # [O] [ ] [O]
        next_moves = sim_childs(opponent(plyr), pboard)
        # simulates the current board with the final move decision 3 times into the future
        # a statistical deathtrap can be identified by checking 3 moves later, whether all the child nodes of a parent node will loose
        for next_move in next_moves[1:]:
            if check_winner_anywhere(next_move, board_sz, win_len, check_winner_area) == (' ', ' ',):
                next_next_moves = sim_childs(plyr, next_move)
                death_count = 0
                for next_next_move in next_next_moves[1:]:
                    if check_winner_anywhere(next_next_move, board_sz, board_sz, [0]) == (' ', ' ',):
                        next_next_next_moves = sim_childs(opponent(plyr), next_next_move)
                        for next_next_next_move in next_next_next_moves[1:]:
                            if check_winner_anywhere(next_next_next_move, board_sz, board_sz, [0])[0] == 'X':
                                # counts how many child nodes loose
                                death_count += 1

                # if all the child nodes loose, the first-gen move is a deathtrap
                if death_count > len(next_next_moves):
                    return True
        return False

    print_board(main_board, board_sz)
    print(f'Computer [{pc}]\'s turn! Please wait...')
    if last_input == -1:
        return random.randint(0, board_sz**2 - 1)
    else:
        # if the board_sz <= 4, prune a 3x3 area around the most recent player input
        # if the board_sz >= 5, prune a 5x5 area around the most recent player input
        # we cannot prune a 4x4 area as 4x4 has no center slot
        pboard = prune(last_input)

        if ' ' not in pboard:
            return -1

        # if the 3x3 grid around the opponent's newest move are full, find the closest empty slot
        elif ' ' not in pboard:
            print('No empty slots found! Randomly generating next move...')
            fin_move = random.choice([_ for _ in range(board_sz**2) if main_board[_] == ' '])

        else:
            end_moves = (set(), set(), set())
            sort_childs(sim_childs(pc, pboard))
            fin_move = pick_init_move(pc, weight_init_moves(is_debugging))
        filled_slots_ind.append(fin_move)
    return int(fin_move)


# tmp = tk.Text()
# mode = ''
# while mode == '':
#     # ask player for mode pvp, pvcx, or pvco
#     mode = input(
#         'Type:\n>PvP  - play against another player\n>PvCX - play against the computer with the computer starting first\n>PvCO - play against the computer with you starting first\n>')
#     mode = mode.lower()
#
#     # if player input rubbish, ask again
#     if mode != 'pvp' and mode != 'pvcx' and mode != 'pvco' and mode != 'pvc':
#         print('Invalid Answer!')
#         mode = ''
#
# board_sz: str | int = ''
# while board_sz == '':
#     # ask player for board len
#     board_sz = input(
#        'Select a board length. Boards that are 7*7 or larger only needs half the board length to win!\n>')
#     # if player input rubbish, ask again
#     if board_sz.isdigit() is False:
#         print('Board length must be an integer!')
#         board_sz = ''
#     elif int(board_sz) < 2:
#         print('Board length must be 2 or larger!')
#         board_sz = ''
#
# # initialize the board len and how many slots in a row/column/diagonal to win
# board_sz = int(board_sz)
# filled_slots_ind = []
# win_len = set_win_len(board_sz)
# check_winner_area = set_check_winner_area(board_sz, win_len)
#
# # initialize the board based on board_sz
# main_board = setup_board(board_sz)
#
# # initialize the sign for player and computer (if not pvp)
# if mode == 'pvp':
#     plyr = 'X'
# elif mode == 'pvcx':
#     plyr = 'O'
#     # computer's turn if computer starts first
#     # last_input = -1 means there is no last_input yet and the computer will randomly generate a number
#     main_board[pc_input(opponent(plyr), main_board, board_sz, filled_slots_ind, min(win_len, 4), set_check_winner_area(board_sz, min(win_len, 4)), last_input=-1, is_debugging=False, debugger=tmp, slot_buttons=tmp)] = opponent(plyr)
# elif mode == 'pvco' or mode == 'pvc':
#     plyr = 'X'
#
# # start of the Player versus Computer mode
# while mode == 'pvcx' or mode == 'pvco' or mode == 'pvc':
#     # human's turn if human starts first
#     # noinspection PyUnboundLocalVariable
#     last_input = ask_input(plyr, main_board, board_sz, filled_slots_ind, win_len, check_winner_area)
#     main_board[last_input] = plyr
#
#     # computer's turn regardless computer or human starts first
#     main_board[pc_input(opponent(plyr), main_board, board_sz, filled_slots_ind, min(win_len, 4), set_check_winner_area(board_sz, min(win_len, 4)), last_input, is_debugging=False, debugger=tmp, slot_buttons=tmp)] = opponent(plyr)
#
#     winner = check_winner_anywhere(main_board, board_sz, win_len, check_winner_area)
#     if winner[1] == 'tie':
#         print_board(main_board, board_sz)
#         print('=' * 50 + '\n' + ' ' * ((51 - len('Game ended in a draw'))//2) + 'Game ended in a draw')
#         print(' ' * ((51 - len('So close...but I will NEVER lose!'))//2) + 'So close...but I will NEVER lose!' + '\n' + '=' * 50)
#         break
#     elif winner[0] == opponent(plyr):
#         print_board(main_board, board_sz)
#         print('=' * 50 + '\n' + ' ' * ((51 - len(f'Computer wins {winner[1]}!')) // 2) + f'Computer wins {winner[1]}!')
#         print(' ' * ((51 - len('Humans should\'ve been smarter...'))//2) + 'Humans should\'ve been smarter...' + '\n' + '=' * 50)
#         break
#     elif winner[0] == plyr:
#         print_board(main_board, board_sz)
#         print('=' * 50 + '\n' + ' ' * ((51 - len(f'You win {winner[1]}!')) // 2) + f'You win {winner[1]}!' + '\n' + '=' * 50)
#         break
#
# # start of the Player versus Player mode
# while mode == 'pvp':
#     # player 'X' turn
#     main_board[ask_input(plyr, main_board, board_sz, filled_slots_ind, win_len, check_winner_area)] = plyr
#
#     # player 'O' turn
#     main_board[ask_input(opponent(plyr), main_board, board_sz, filled_slots_ind, win_len, check_winner_area)] = opponent(plyr)
#
#     winner = check_winner_anywhere(main_board, board_sz, win_len, check_winner_area)
#     if winner[1] == 'tie':
#         print_board(main_board, board_sz)
#         print('=' * 50 + '\n' + ' ' * ((51 - len('Game ended in a draw.'))//2) + 'Game ended in a draw.' + '\n' + '=' * 50)
#         break
#     elif winner != (' ', ' ',):
#         print_board(main_board, board_sz)
#         print('=' * 50 + '\n' + ' ' * ((51 - len(f'Player \'{winner[0]}\' wins {winner[1]}!')) // 2) + f'Player \'{winner[0]}\' wins {winner[1]}!' + '\n' + '=' * 50)
#         break
