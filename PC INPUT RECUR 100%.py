# ALL FUNCTIONS BELOW ARE FOR THE AI
import networkx as nx
from matplotlib import pyplot as plt

import backend as t





if __name__ == "__main__":
    t.set_universals(4,4)
    main_board = 0
    plyr = 1
    while True:
        t.print_board(main_board)
        inputt = int(input('Cell Index:'))
        main_board += plyr * t.three_pow[inputt]
        simmable_inds = set(t.prune(plyr, main_board, inputt))
        pc_inputt = pc_input_iter(t.opp(plyr), main_board, simmable_inds, True)
        main_board += t.opp(plyr) * t.three_pow[pc_inputt]
