from TIC_TAC_TOE_func_v1 import *

print(r"""
* ============================================================================================================== *
*                                                                                                                *
*    ████████ ██  ██████       ████████  █████   ██████       ████████  ██████  ███████     ██    ██  ██████╗    *
*       ██    ██ ██               ██    ██   ██ ██               ██    ██    ██ ██          ██    ██ ██╔════╝    * 
*       ██    ██ ██      █████    ██    ███████ ██      █████    ██    ██    ██ █████       ██    ██ ███████╗    *  
*       ██    ██ ██               ██    ██   ██ ██               ██    ██    ██ ██           ██  ██  ██╔═══██╗   *
*       ██    ██  ██████          ██    ██   ██  ██████          ██     ██████  ███████       ████   ╚██████╔╝   *     
*       100% Made by Zhong Yan      Infinite boards!               Unbeatable AI!                     ╚═════╝    *
*                                                                                                                *
* ============================================================================================================== *""")

mode = ''
while mode == '':
    # ask player for mode pvp, pvcx, or pvco
    mode = input(
        'Type:\n>PvP  - play against another player\n>PvCX - play against the computer with the computer starting first\n>PvCO - play against the computer with you starting first\n>')
    mode = mode.lower()

    # if player input rubbish, ask again
    if mode != 'pvp' and mode != 'pvcx' and mode != 'pvco' and mode != 'pvc':
        print('Invalid Answer!')
        mode = ''

board_sz: str | int = ''
while board_sz == '':
    # ask player for board length
    board_sz = input(
       'Select a board length.\n>')
    # if player input rubbish, ask again
    if board_sz.isdigit() is False:
        print('Board length must be an integer!')
        board_sz = ''
    elif int(board_sz) < 2:
        print('Board length must be 2 or larger!')
        board_sz = ''

# initialize the board len and how many slots in a row/column/diagonal to win
board_sz = int(board_sz)
filled_slots_ind = []
WIN_LEN = set_win_len(board_sz)
check_winner_area = set_check_winner_area(board_sz, WIN_LEN)

# initialize the board based on board_sz
main_board = setup_board(board_sz)

# initialize the sign for player and computer (if not pvp)
if mode == 'pvp':
    plyr = 'X'
elif mode == 'pvcx':
    plyr = 'O'
    # computer's turn if computer starts first
    print_board(main_board, board_sz)
    print(f'Computer [X]\'s turn! Please wait...')
    # prev_input = -1 means there is no prev_input yet and the computer will randomly generate a number
    main_board[pc_input(opp(plyr), main_board, board_sz, filled_slots_ind, min(WIN_LEN, 4), set_check_winner_area(board_sz, min(WIN_LEN, 4)), prev_input=-1, is_debugging=False)] = opp(plyr)
elif mode == 'pvco' or mode == 'pvc':
    plyr = 'X'

# start of the Player versus Computer mode
while mode == 'pvcx' or mode == 'pvco' or mode == 'pvc':
    # human's turn if human starts first
    # noinspection PyUnboundLocalVariable
    prev_input = ask_input(plyr, main_board, board_sz, filled_slots_ind, WIN_LEN, check_winner_area)
    main_board[prev_input] = plyr

    # computer's turn regardless computer or human starts first
    print_board(main_board, board_sz)
    print(f'Computer [{opp(plyr)}]\'s turn! Please wait...')
    main_board[pc_input(opp(plyr), main_board, board_sz, filled_slots_ind, min(WIN_LEN, 4), set_check_winner_area(board_sz, min(WIN_LEN, 4)), prev_input, is_debugging=False)] = opp(plyr)

    winner = check_winner_anywhere(main_board, board_sz, WIN_LEN, check_winner_area)
    if winner[1] == 'tie':
        print_board(main_board, board_sz)
        print('=' * 50 + '\n' + ' ' * ((51 - len('Game ended in a draw'))//2) + 'Game ended in a draw')
        print(' ' * ((51 - len('So close...but I will NEVER lose!'))//2) + 'So close...but I will NEVER lose!' + '\n' + '=' * 50)
        break
    elif winner[0] == opp(plyr):
        print_board(main_board, board_sz)
        print('=' * 50 + '\n' + ' ' * ((51 - len(f'Computer wins {winner[1]}!')) // 2) + f'Computer wins {winner[1]}!')
        print(' ' * ((51 - len('Humans should\'ve been smarter...'))//2) + 'Humans should\'ve been smarter...' + '\n' + '=' * 50)
        break
    elif winner[0] == plyr:
        print_board(main_board, board_sz)
        print('=' * 50 + '\n' + ' ' * ((51 - len(f'You win {winner[1]}!')) // 2) + f'You win {winner[1]}!' + '\n' + '=' * 50)
        break

# start of the Player versus Player mode
while mode == 'pvp':
    # player 'X' turn
    main_board[ask_input(plyr, main_board, board_sz, filled_slots_ind, WIN_LEN, check_winner_area)] = plyr

    # player 'O' turn
    main_board[ask_input(opp(plyr), main_board, board_sz, filled_slots_ind, WIN_LEN, check_winner_area)] = opp(plyr)

    winner = check_winner_anywhere(main_board, board_sz, WIN_LEN, check_winner_area)
    if winner[1] == 'tie':
        print_board(main_board, board_sz)
        print('=' * 50 + '\n' + ' ' * ((51 - len('Game ended in a draw.'))//2) + 'Game ended in a draw.' + '\n' + '=' * 50)
        break
    elif winner != (' ', ' ',):
        print_board(main_board, board_sz)
        print('=' * 50 + '\n' + ' ' * ((51 - len(f'Player \'{winner[0]}\' wins {winner[1]}!')) // 2) + f'Player \'{winner[0]}\' wins {winner[1]}!' + '\n' + '=' * 50)
        break
