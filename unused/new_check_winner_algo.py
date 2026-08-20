from backend import *

relative_adj4 = (
    (0, -1), (1, -1), (1, 0), (1, 1)  # top-left, top-center, top-right, right

)
"""A pre-calculated universal tuple containing the relative coordinates (x, y) of"""  # TODO
lines_table: dict[int, list[int]] = {}
"""
key = line id, val = (line plyr, line magnitude)
"""
cell_to_line: list[list[tuple[int, int, int]]] = []
"""
board[ cell num[ 1st connected line(line id, next cell x, next cell y), 2nd connected line(line id, next cell x, next cell y), ...]]
"""


def is_plyr_win(board: int, plyr: int, origin: int) -> bool:
    """
    """
    origin_x, origin_y = origin % BOARD_LEN, origin // BOARD_LEN

    if cell_to_line[origin]:  # if cell is connected to at least 1 line

        for i, line_id, dir_x, dir_y in enumerate(cell_to_line[origin]):  # iterate through each line connected to the cell
            line = lines_table[line_id]
            if line[0] == plyr:  # index 0 = plyr. If line belongs to player in the cell
                line[1] += 1  # index 1 = magnitude

                for ii, a, b, c in enumerate(cell_to_line[origin][i:]):  # handle case 1: both sides lines. Check if the cell is connected to an opp dir line.
                    if lines_table[a][0] == plyr and -b == dir_x and -c == dir_y:
                        line[1] += lines_table[a][1]  # merge the other line's length with current line's
                        lines_table[a] = line  # redirect the other line

                        del cell_to_line[origin][i]  # del the opp dir line to prevent checking again
                        break

                else:  # continue if the inner loop wasn't broken
                    fwd1_x, fwd1_y = origin_x + dir_x, origin_y + dir_y
                    if 0 <= fwd1_x < BOARD_LEN and 0 <= fwd1_y < BOARD_LEN:

                        fwd1_ind = fwd1_y * BOARD_LEN + fwd1_x
                        if plyr_at(board, fwd1_ind) == 0:  # handle case 2: one side line, one side empty
                            cell_to_line[fwd1_ind].append((line_id, dir_x, dir_y,))

                        else:  # handle case 3: one side line, one side solo-filled cell
                            line[1] += 1

                            fwd2_x, fwd2_y = fwd1_x + dir_x, fwd1_y + dir_y
                            if 0 <= fwd2_x < BOARD_LEN and 0 <= fwd2_y < BOARD_LEN:

                                fwd2_ind = fwd2_y * BOARD_LEN + fwd2_x
                                if plyr_at(board, fwd2_ind) == 0:
                                    cell_to_line[fwd2_ind].append((line_id, dir_x, dir_y,))

                if line[1] >= WIN_LEN:
                    return True

    else:  # handle case 4: both sides empty or solo-filled cell
        for dir_x, dir_y in relative_adj4:
            line_id = random.getrandbits(128)  # TODO

            fwd1_x, fwd1_y = origin_x + dir_x, origin_y + dir_y
            back1_x, back1_y = origin_x - dir_x, origin_y - dir_y

            is_fwd_filled = 0 <= fwd1_x < BOARD_LEN and 0 <= fwd1_y < BOARD_LEN and plyr_at(board, fwd1_y * BOARD_LEN + fwd1_x) == plyr
            is_back_filled = 0 <= back1_x < BOARD_LEN and 0 <= back1_y < BOARD_LEN and plyr_at(board, back1_y * BOARD_LEN + back1_x) == plyr

            if is_fwd_filled or is_back_filled:
                lines_table[line_id] = [plyr, 1]  # create new line
                line = lines_table[line_id]

                if is_fwd_filled:
                    line[1] += 1

                    fwd2_x, fwd2_y = fwd1_x + dir_x, fwd1_y + dir_y
                    if 0 <= fwd2_x < BOARD_LEN and 0 <= fwd2_y < BOARD_LEN:
                        cell_to_line[fwd2_y * BOARD_LEN + fwd2_x].append((line_id, dir_x, dir_y,))

                if is_back_filled:
                    line[1] += 1

                    back2_x, back2_y = back1_x - dir_x, back1_y - dir_y
                    if 0 <= back2_x < BOARD_LEN and 0 <= back2_y < BOARD_LEN:
                        cell_to_line[back2_y * BOARD_LEN + back2_x].append((line_id, -dir_x, -dir_y,))

                if line[1] >= WIN_LEN:
                    return True

    return False
