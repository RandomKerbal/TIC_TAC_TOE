import random

mode = ''
while mode == '':
    # ask player for mode pvp, pvcx, or pvco
    mode = input('Type:\n>PvP  - play against another player\n>PvCX - play against the computer with the computer starting first\n>PvCO - play against the computer with you starting first\n>')
    mode = mode.lower()

    # if player input rubbish, ask again
    if mode != 'pvp' and mode != 'pvcx' and mode != 'pvco' and mode != 'pvc':
        print('Invalid Answer!')
        mode = ''

board_sz: str | int = ''
while board_sz == '':
    # ask player for board length
    board_sz = input('Select a board length. Boards that are 7*7 or larger only needs half the board length to win!\n>')
    # if player input rubbish, ask again
    if board_sz.isdigit() is False:
        print('Board size must be an integer!')
        board_sz = ''
    elif int(board_sz) < 2:
        print('Board size must be 2 or larger!')
        board_sz = ''
board_sz = int(board_sz)


# setup board layout
# eg 3x3 board = ['[ ]','[ ]','[ ]'
#                 '[ ]','[ ]','[ ]'
#                 '[ ]','[ ]','[ ]', 'initial_move']
main_board = []
for slot in range(board_sz**2):
    main_board.append('[ ]')
main_board.append('_')


def print_board(board: list) -> None:
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
            if board[j] == '[ ]':
                print(board[j], end=' ')
            else:
                print(' ' + board[j], end='  ')
    print(end='\n')


def opponent(origin_plyr: str) -> str:
    # changes player X to O, O to X
    if origin_plyr == 'O':
        return 'X'
    elif origin_plyr == 'X':
        return 'O'


def coord_to_slot(coord: str) -> int | bool:
    # converts the x,y coordinates inputed by player to slot number
    # eg slot num of 3x3 board
    # [0] [1] [2]
    # [3] [4] [5]
    # [6] [7] [8]

    # if player inputs gibberish, return False
    if (coord[:coord.find(',')].isdigit() is False) or (coord[coord.find(',') + 1:].isdigit() is False):
        return False

    # if the player inputed valid coordinates...
    # take the first number as the column num, the second number as the row num
    # I observed that the slot num = (row num*board size) + column num
    slot_num = int(coord[:coord.find(',')]) + ((int((coord[coord.find(',') + 1:])) - 1) * board_sz) - 1

    # if the slot number exceeds the board, return False
    if slot_num + 1 > (board_sz**2):
        return False
    # if the slot number is negative, return False
    elif slot_num < 0:
        return False
    # if the that slot alr has an X or O, return False
    elif main_board[slot_num] != '[ ]':
        return False
    else:
        return slot_num


def sim_next_moves(plyr: str, prev_move: list) -> list:
    # branches a parent node down by 1 layer
    # given that next player is 'plyr' and the board now looks like 'prev_move'...
    # returns a list of all possible moves that the player could play next
    moves = [
        plyr
    ]
    for Slot in range(pboard_sz**2):
        if prev_move[Slot] == '[ ]':
            prev_move[Slot] = plyr
            if prev_move[-1] == '_':
                moves.append(prev_move[:])
                # if the child nodes are the first generation, records the first-gen move as a str at the end of each board
                moves[-1][-1] = Slot
            else:
                # if the child nodes are not the first generation, records the first-gen move as a str at the end of each board
                moves.append(prev_move[:])
            prev_move[Slot] = '[ ]'
    return moves


def filter_next_moves(plyr: str, prev_moves: list) -> list:
    # given that computer is 'plyr' and the board now looks like 'prev_move'...
    # recursively branches a parent node down by 1 layer until the computer wins, looses, or draws in the child move
    # returns a list of boards where the computer wins, looses, or draws
    # STRATEGIES USED TO SAVE PERFORMANCE:
    # 1. don't go through boards where player already win
    # 2. don't go through boards where player loss
    # 3. don't go through or save tie boards until when there is only a few empty slots left
    end_moves = [[], [], []]    # end_moves saved as [[bad], [good], [tie]]

    for prev_move in prev_moves[1:]:
        if check_winner(prev_move)[0] == plyr:
            # if this is won by the player, store it separately in 'good move list'
            end_moves[1].append(prev_move)
        elif check_winner(prev_move)[0] == opponent(plyr):
            # if this is loss by the player, store it separately in 'bad move list'
            end_moves[0].append(prev_move)
        elif check_winner(prev_move)[1] == 'tie' and main_board.count('[ ]') < pboard_sz:
            # if this is in tie, it doesn't affect final win_prob evaluation, so don't save them
            # But, we still need the best tie boards so the computer can still make moves while unable to win...
            # so, we start saving tie boards when there is only a few empty slots left
            print('Computer: No one will win this game... start simulating the best moves for draw\n')
            end_moves[2].append(prev_move)
        else:
            # if the parent node has no outcome yet, continue branching down
            next_moves = sim_next_moves(opponent(prev_moves[0]), prev_move)
            next_moves = filter_next_moves(plyr, next_moves)
            for i in range(3):  # i = [bad], [good], [tie]
                for next_move in next_moves[i]:
                    if next_move not in end_moves[i]:
                        end_moves[i].append(next_move)
    return end_moves


def weight_init_moves(end_moves: list) -> dict:
    # recall that each child node saved its first-gen move
    win_probs = {}     # dict saved as {'initial_move_n': win_probability_of_n}

    # count the freqeuncy of each first-gen move that results in a loosing child node
    # to punish a first-gen move that results in a loosing child node, its freqeuncy is negative
    # to punish them hard, its freqeuncy is x3
    for end_move in end_moves[0]:
        if end_move[-1] not in win_probs:
            win_probs[end_move[-1]] = -3
        else:
            win_probs[end_move[-1]] -= 3

    # count the freqeuncy of each first-gen move that results in a winning child node
    # to reward a first-gen move that results in a winning child node, its freqeuncy is positive
    for end_move in end_moves[1]:
        if end_move[-1] not in win_probs:
            win_probs[end_move[-1]] = 1
        else:
            win_probs[end_move[-1]] += 1

    # count the freqeuncy of each first-gen move that results in a draw child node
    # a first-gen move that results in a draw child node is not punished and not rewarded
    for end_move in end_moves[2]:
        if end_move[-1] not in win_probs:
            win_probs[end_move[-1]] = 0

    return win_probs


def pick_init_move(plyr: str, outcomes: dict) -> int:
    # find which first-gen move results in the most winning child nodes
    max_win_prob = max(outcomes.values())

    # moves_pool creates a list of initial moves containing the same highest win_prob to be picked randomly
    moves_pool = [key for key, value in outcomes.items() if value == max_win_prob]
    move = moves_pool[random.randint(0, len(moves_pool)-1)]

    # try putting the final move decision onto the current board to check for any statistical deathtraps
    pboard_copy = pboard[:]
    pboard_copy[move] = plyr
    if check_deathtrap(plyr, pboard_copy):
        print('Deathtrap found! Choosing a new move...')
        outcomes.pop(move)
        move = pick_init_move(plyr, outcomes)
    return move


def check_deathtrap(plyr: str, cur_move: list) -> bool:
    # a statistical deathtrap is a first-gen move that appeared to be statistically superior to all other first-gen moves...
    # but it will lead to an outcome like this (computer is X):
    # [O] [ ] [X]
    # [ ] [X] [ ]
    # [O] [ ] [O]
    next_moves = sim_next_moves(opponent(plyr), cur_move)
    # simulates the current board with the final move decision 3 times into the future
    # a statistical deathtrap can be identified by checking 3 moves later, whether all the child nodes of a parent node will loose
    for next_move in next_moves[1:]:
        if check_winner(next_move) == [' ', ' ']:
            next_next_moves = sim_next_moves(plyr, next_move)
            death_count = 0
            for next_next_move in next_next_moves[1:]:
                if check_winner(next_next_move) == [' ', ' ']:
                    next_next_next_moves = sim_next_moves(opponent(plyr), next_next_move)
                    for next_next_next_move in next_next_next_moves[1:]:
                        if check_winner(next_next_next_move)[0] == 'X':
                            # counts how many child nodes loose
                            death_count += 1

            # if all the child nodes loose, the first-gen move is a deathtrap
            if death_count > len(next_next_moves):
                return True
    return False


def check_winner(board: list) -> list:
    is_tie = True   # part of the codes that check for whether the game will tie

    # boards larger than 6*6 only needs half the board length to win
    if pboard_sz > 6:
        win_len = round(pboard_sz/2)
    else:
        win_len = pboard_sz

    # only start checking a row, column, or diagonal if it is not empty
    for SLOT in range(pboard_sz**2):
        if board[SLOT] != '[ ]':

            # check if any row contain all X or all O...if yes, then the player wins
            # start_row = SLOT // pboard_sz
            # start_col = min(SLOT % pboard_sz, pboard_sz-win_len)
            start_slot = (SLOT // pboard_sz) * pboard_sz + min(SLOT % pboard_sz, pboard_sz-win_len)
            end_slot = start_slot + win_len
            if board[start_slot: end_slot].count('O') >= win_len:
                return ['O', 'horizontally']
            elif board[start_slot: end_slot].count('X') >= win_len:
                return ['X', 'horizontally']
            # part of the codes that check for not tie (there are still rows where one player could win)
            elif (board[start_slot: end_slot].count('O') == 0 or board[start_slot: end_slot].count('X')) == 0:
                is_tie = False

            # check if any column contain all X or all O...if yes, then the player wins
            # start_row = min(SLOT // pboard_sz, pboard_sz - win_len)
            # start_col = SLOT % pboard_sz
            start_slot = min(SLOT // pboard_sz, pboard_sz - win_len) * pboard_sz + (SLOT % pboard_sz)
            # end_row = start_row + win_len = min(SLOT // pboard_sz, pboard_sz - win_len) + win_len
            # end_col = start_col = SLOT % pboard_sz
            end_slot = (min(SLOT // pboard_sz, pboard_sz - win_len) + win_len) * pboard_sz + (SLOT % pboard_sz)
            slots = []
            for Slot in range(start_slot, end_slot, pboard_sz):
                slots.append(board[Slot])
            if slots.count('O') >= win_len:
                return ['O', 'vertically']
            elif slots.count('X') >= win_len:
                return ['X', 'vertically']
            # part of the codes that check for not tie (there are still columns where one player could win)
            elif slots.count('O') == 0 or slots.count('X') == 0:
                is_tie = False

            # check if any diagonal from top left to down right contain all X or all O...if yes, then the player wins
            # start_row = min(SLOT // pboard_sz, pboard_sz - win_len)
            # start_col = min(SLOT % pboard_sz, pboard_sz-win_len)
            start_slot = min(SLOT // pboard_sz, pboard_sz - win_len) * pboard_sz + min(SLOT % pboard_sz, pboard_sz-win_len)
            # end_row = start_row + win_len = min(SLOT // pboard_sz, pboard_sz - win_len) + win_len
            # end_col = start_col + win_len = min(SLOT % pboard_sz, pboard_sz-win_len) + win_len
            end_slot = ((min(SLOT // pboard_sz, pboard_sz - win_len) + win_len) * pboard_sz) + (min(SLOT % pboard_sz, pboard_sz-win_len) + win_len)
            slots = []
            for Slot in range(start_slot, end_slot, pboard_sz+1):
                slots.append(board[Slot])
            if slots.count('O') >= win_len:
                return ['O', 'from top left to down right']
            elif slots.count('X') >= win_len:
                return ['X', 'from top left to down right']
            # part of the codes that check for not tie (there are still diagonals where one player could win)
            elif slots.count('O') == 0 or slots.count('X') == 0:
                is_tie = False

            # check if any diagonal from top right to down left contain all X or all O...if yes, then the player wins
            # start_row = min(SLOT // pboard_sz, pboard_sz - win_len)
            # start_col = max(win_len-1, SLOT % pboard_sz)
            start_slot = min(SLOT // pboard_sz, pboard_sz - win_len) * pboard_sz + max(win_len-1, SLOT % pboard_sz)
            # end_row = start_row + win_len = min(SLOT // pboard_sz, pboard_sz - win_len) + win_len
            # end_col = start_col - win_len = max(win_len-1, SLOT % pboard_sz) - win_len
            end_slot = (min(SLOT // pboard_sz, pboard_sz - win_len) + win_len) * pboard_sz + (max(win_len-1, SLOT % pboard_sz) - win_len)
            slots = []
            for Slot in range(start_slot, end_slot, pboard_sz-1):
                slots.append(board[Slot])
            if slots.count('O') >= win_len:
                return ['O', 'from top right to down left']
            elif slots.count('X') >= win_len:
                return ['X', 'from top right to down left']
            # part of the codes that check for not tie (there are still diagonals where one player could win)
            elif slots.count('O') == 0 or slots.count('X') == 0:
                is_tie = False

    if is_tie and board.count('[ ]') < pboard_sz**2:
        return [' ', 'tie']
    else:
        return [' ', ' ']


def prune(board: list, origin: int) -> list:
    # crops only a 5x5 area of board around where the human player just placed
    # this reduces the number of child nodes needed to simulate when the board size is very large
    if pboard_sz < board_sz:
        p_board = []

        # Find start and end rows and columns of the 5x5 area
        start_row = max(0, min(origin // board_sz - pboard_sz // 2, board_sz - pboard_sz))
        start_col = max(0, min(origin % board_sz - pboard_sz // 2, board_sz - pboard_sz))
        end_row = start_row + pboard_sz
        end_col = start_col + pboard_sz

        # Populate pboard
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                p_board.append(board[row*board_sz + col])

        p_board.append('_')
        return p_board
    else:
        return board


def pboard_slot_to_main(pboard_slot: int, origin: int) -> int:
    # the final move decision made by the computer is played on the pboard, not the actual board
    # we want to convert the slot num on pboard to the slot num on the actual board
    if pboard_sz < board_sz:
        # find the coordinate of the top left slot of the pboard on the actual board
        start_row = max(0, min(origin // board_sz - pboard_sz // 2, board_sz - pboard_sz))
        start_col = max(0, min(origin % board_sz - pboard_sz // 2, board_sz - pboard_sz))
        pboard_slot_row = pboard_slot // pboard_sz
        pboard_slot_col = pboard_slot % pboard_sz

        # add the row distance from the top left slot of the pboard to the coordinate of the final move decision
        # add the column distance from the top left slot of the pboard to the coordinate of the final move decision
        pboard_slot = (board_sz * (start_row + pboard_slot_row)) + start_col + pboard_slot_col
    return pboard_slot


# The actual game starts from here...
# runs the Player versus Computer mode
if mode == 'pvcx':
    pc_symbol = 'X'
elif mode == 'pvco' or mode == 'pvc':
    pc_symbol = 'O'

pboard_sz = board_sz
while (mode == 'pvcx' or mode == 'pvco' or mode == 'pvc') and check_winner(main_board) == [' ', ' ']:
    while (mode == 'pvco' or mode == 'pvc') and check_winner(main_board) == [' ', ' ']:
        print_board(main_board)
        player_coord = input('Your turn [X]! Choose your x,y coordinates: ')
        slot_input = coord_to_slot(player_coord)
        if slot_input is False:
            print('Invalid Position!')
            continue
        else:
            main_board[slot_input] = 'X'
            break

    print_board(main_board)
    if check_winner(main_board) == [' ', ' ']:
        # noinspection PyUnboundLocalVariable
        print(f'Computer [{pc_symbol}]\'s turn! Please wait...')
        pboard_sz = min(board_sz, 3)
        if main_board.count('[ ]') >= board_sz**2:
            fin_move = random.randint(0, board_sz**2 - 1)
        else:
            # noinspection PyUnboundLocalVariable
            pboard = prune(main_board, slot_input)
            # if the 3x3 grid around the opponent's current move are full, find the closest empty slot on the board
            if pboard.count('[ ]') == 0 or check_winner(pboard) != [' ', ' ']:
                slot_input = main_board.index('[ ]')
                pboard = prune(main_board, slot_input)
            # TODO: change pboard_size to 5, use 'landfill' to reduce empty slots
            # TODO: Landfill
            fin_moves = filter_next_moves(pc_symbol, sim_next_moves(pc_symbol, pboard))
            fin_move = pick_init_move(pc_symbol, weight_init_moves(fin_moves))
            fin_move = pboard_slot_to_main(fin_move, slot_input)
            print(fin_moves)
            print(weight_init_moves(fin_moves))
        main_board[int(fin_move)] = pc_symbol
        # noinspection PyRedeclaration
        pboard_sz = board_sz

    while mode == 'pvcx' and check_winner(main_board) == [' ', ' ']:
        print_board(main_board)
        player_coord = input('Your turn [O]! Choose your x,y coordinates: ')
        slot_input = coord_to_slot(player_coord)
        if slot_input is False:
            print('Invalid Position!')
            continue
        else:
            main_board[slot_input] = 'O'
            break

    if check_winner(main_board)[1] == 'tie':
        print_board(main_board)
        print('=' * 50 + '\n' + ' ' * ((51 - len('Game ended in a draw'))//2) + 'Game ended in a draw')
        print(' ' * ((51 - len('So close...but I will NEVER lose!'))//2) + 'So close...but I will NEVER lose!' + '\n' + '=' * 50)
    elif check_winner(main_board)[0] == pc_symbol:
        print_board(main_board)
        print('=' * 50 + '\n' + ' ' * ((51 - len(f'Computer wins {check_winner(main_board)[1]}!'))//2) + f'Computer wins {check_winner(main_board)[1]}!')
        print(' ' * ((51 - len('Humans should\'ve been smarter...'))//2) + 'Humans should\'ve been smarter...' + '\n' + '=' * 50)
    elif check_winner(main_board)[0] == opponent(pc_symbol):
        print_board(main_board)
        print('=' * 50 + '\n' + ' ' * ((51 - len(f'You win {check_winner(main_board)[1]}!'))//2) + f'You win {check_winner(main_board)[1]}!' + '\n' + '=' * 50)


# runs the Player versus Player mode
while mode == 'pvp' and check_winner(main_board) == [' ', ' ']:
    # player 'O' turn
    print_board(main_board)
    while mode == 'pvp' and check_winner(main_board) == [' ', ' ']:
        player_coord = input('Player \'X\"s turn! Choose your x,y coordinates: ')
        slot_input = coord_to_slot(player_coord)
        if slot_input is False:
            print('Invalid Position!')
            continue
        else:
            main_board[slot_input] = 'X'
            break

    # player 'X' turn
    print_board(main_board)
    while mode == 'pvp' and check_winner(main_board) == [' ', ' ']:
        player_coord = input('Player \'O\"s turn! Choose your x,y coordinates: ')
        slot_input = coord_to_slot(player_coord)
        if slot_input is False:
            print('Invalid Position!')
            continue
        else:
            main_board[slot_input] = 'O'
            break

    if check_winner(main_board)[1] == 'tie':
        print_board(main_board)
        print('=' * 50 + '\n' + ' ' * ((51 - len('Game ended in a draw.'))//2) + 'Game ended in a draw.' + '\n' + '=' * 50)
    elif check_winner(main_board) != [' ', ' ']:
        print_board(main_board)
        print('=' * 50 + '\n' + ' ' * ((51 - len(f'Player \'{check_winner(main_board)[0]}\' wins {check_winner(main_board)[1]}!'))//2) + f'Player \'{check_winner(main_board)[0]}\' wins {check_winner(main_board)[1]}!' + '\n' + '=' * 50)
