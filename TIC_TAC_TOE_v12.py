from tkinter import *
from tkinter import messagebox

from TIC_TAC_TOE_func import *


def to_changelog():
    messagebox.showinfo('Changelog', '''
Ver 1 : Added the basics: player vs player mode, infinite board length, winner checker, etc...\n
Ver 2 : Boards are now stored as single list instead of dictionary. Changes player input from slot number to x,y coordinates. Rebuild the entire code to process this new file format.\n
Ver 3 : Added basic AI. Added console GUI. Make boards that are 7*7 or larger needs only half the board length to win.\n
Ver 4 : Added board pruning for boards larger than 3x3 to reduce AI calculations. Added some randomization to the moves made by the AI. Restructured the entire AI code for optimization.\n
Ver 5 : Added deathtrap checker - that's the hardest part of this project! Now the AI is 100% unbeatable for a 3x3 board. Added the option to let AI start first.\n
Ver 6 : Make board pruning only for boards larger than 5x5. Added land-filling to boards larger than 3x3. Added a matplotlib display for AI's Risk Analysis.\n
Ver 7 : Added Tkinter GUI. Rebuild winner checker for HUGE optimization. Changed every code to user-def function. Added user-friendly debugging root.\n
Ver 8 : HUGE OPTIMIZATION: Rebuild the board pruning code to combine both pruning and land-filling into 1 function. Pruned board and main board now have the same dimension - no additional function is needed to convert slots between the two boards!\n
Ver 9 : Rebuild and tidy up all GUI code using class instead of user-def functions. Rebuild to make board pruning dynamic, it can now scale up if that area has not enough empty slots. Added 'Replay' button. Changed empty slots from '[ ]' to ' '. Fixed bug where the endpoint of checking diagonally from top right to down left doesn't move with the start point.\n
Ver 10: Added title animation. Added 4 modes: Traditional, Time Trial, Vanishing Moves, Snake\n
Ver 11: Globalised colors for each feature. Added color settings. Changed O's snake color. Capped length to win at 4. Added 'Total Child Count' to debugger.
Ver 12: Redesign the algorithm to use depth-first search instead of breadth-first-search. Build a specialized, faster winner-checking algo that only checks for whether a specific player wins, instead of checking who wins.\n
Ver 13: \n
    ''')


class MainMenu:
    """
    === Attributes ===\n
    window: Name of window that displays MainMenu.\n
    board_sz: Length of the board.\n
    board_zoom: Magnification of the board.\n
    color: Dict containing colors for different features. Sorted into: player X, player O, all.\n
    """

    def __init__(self, window, board_sz: int = 3, board_zoom: int = 5, colors: dict = None):
        self.window = window
        self.board_sz = tk.IntVar(value=board_sz)
        self.board_zoom = tk.IntVar(value=board_zoom)
        if colors is None:
            self.colors = {
                'X': {
                    'symbol': 'Red4',
                    'snake_head': 'Green Yellow',
                    'snake_body': 'Dark Olive Green1'
                },
                'O': {
                    'symbol': 'Navy',
                    'snake_head': 'Cyan1',
                    'snake_body': 'Dark Slate Gray1',
                },
                '': {
                    'pc_move': 'Khaki1',
                    'winner_area': 'Lavender',
                    'pruned_area': 'Lemon Chiffon2',
                    'nxt_vanish_move0': 'Navajo White',
                    'nxt_vanish_move1': 'Antique White'
                }
            }
        else:
            self.colors = colors

        self.title_line1 = Label(self.window,
                                 takefocus=False,
                                 width=500,
                                 borderwidth=0,
                                 background='Black',
                                 foreground='Sea Green1',
                                 text='=' * 999,
                                 font='TkFixedFont')
        self.title_line2 = Label(self.window,
                                 takefocus=False,
                                 width=500,
                                 borderwidth=0,
                                 background='Black',
                                 foreground='Sea Green1',
                                 text='\n' + '=' * 999,
                                 font='TkFixedFont')
        self.title_label = Label(self.window,
                                 takefocus=False,
                                 borderwidth=0,
                                 width=82,
                                 background='Black',
                                 foreground='Sea Green1',
                                 text='''
████████ ██  ██████       ████████  █████   ██████       ████████  ██████  ███████
   ██    ██ ██               ██    ██   ██ ██               ██    ██    ██ ██
   ██    ██ ██      █████    ██    ███████ ██      █████    ██    ██    ██ █████
   ██    ██ ██               ██    ██   ██ ██               ██    ██    ██ ██
   ██    ██  ██████          ██    ██   ██  ██████          ██     ██████  ███████''',
                                 font='TkFixedFont',
                                 justify='left',
                                 anchor='nw')

        self.subtitle_label = Label(self.window,
                                    takefocus=False,
                                    borderwidth=0,
                                    width=500,
                                    background='Black',
                                    foreground='Sea Green1',
                                    text='',
                                    font='TkFixedFont',
                                    justify='left')
        subtitle_text = '   100% Made by CZY         3 Unprecedented Modes!          Unbeatable AI!        '

        self.b_pvc = Button(self.window,
                            text='Single Player',
                            cursor='hand2',
                            overrelief='sunken',
                            command=lambda _='pvc': self.to_submenu(_),
                            activeforeground='white',
                            activebackground='Sea Green',
                            background='Sea Green1',
                            foreground='Black',
                            width=500,
                            font=('FixedSys', 15),
                            borderwidth=5)

        self.b_pvp = Button(self.window,
                            text='Multi Player',
                            cursor='hand2',
                            overrelief='sunken',
                            command=lambda _='pvp': self.to_submenu(_),
                            activeforeground='white',
                            activebackground='Sea Green',
                            background='Sea Green1',
                            foreground='Black',
                            width=500,
                            font=('FixedSys', 15),
                            borderwidth=5)

        self.b_changelog = Button(self.window,
                                  text='Changelog',
                                  cursor='hand2',
                                  overrelief='sunken',
                                  command=to_changelog,
                                  activeforeground='white',
                                  activebackground='Sea Green',
                                  background='Sea Green1',
                                  foreground='Black',
                                  width=500,
                                  font=('FixedSys', 15),
                                  borderwidth=5)

        self.b_exit = Button(self.window,
                             text='Exit',
                             cursor='hand2',
                             overrelief='sunken',
                             command=self.exit,
                             activeforeground='white',
                             activebackground='Sea Green',
                             background='Sea Green1',
                             foreground='Black',
                             width=500,
                             font=('FixedSys', 15),
                             borderwidth=5)

        self.title_line1.pack(side='top')
        self.title_label.pack(side='top', pady=18)
        self.subtitle_label.pack(side='top')
        self.title_line2.pack(side='top')
        self.b_pvc.pack(side='top')
        self.b_pvp.pack(side='top')
        self.b_changelog.pack(side='top')
        self.b_exit.pack(side='top')

        # Animating title & subtitle:
        # time between frames, in milliseconds
        wait = 250
        # There r total 95 frames (frame 0 - 94) stored in anim_frames. All frames r called at the same time, but their executions r queued up.
        self.anim_frames = []
        # frames 0 - 11: animating title
        self.anim_frames.append(self.window.after(wait * 0, lambda: self.title_label.config(foreground='Black')))
        self.anim_frames.append(self.window.after(wait * 1, lambda _=8: self.title_label.config(width=_, foreground='Sea Green1')))
        self.anim_frames.append(self.window.after(wait * 2, lambda _=11: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 3, lambda _=19: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 4, lambda _=25: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 5, lambda _=34: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 6, lambda _=42: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 7, lambda _=50: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 8, lambda _=56: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 9, lambda _=65: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 10, lambda _=74: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 11, lambda _=82: self.title_label.config(width=_)))

        # frames 12 - 94: animating subtitle
        # loop iterates 82 times  as it's the number of chars in the subtitle
        for i in range(0, 83):
            self.anim_frames.append(self.window.after(wait * (i + 11), lambda _=i: self.subtitle_label.config(
                text=subtitle_text[:_] + '_' * min(1, 82 - _) + ' ' * (81 - _))))

        # disables the close window (X) button in the top right corner
        self.window.protocol('WM_DELETE_WINDOW', self.exit)

        # set the MainMenu window to the correct resolution
        self.window.geometry('700x370')
        self.window.config(background='Black')

    def to_submenu(self, mode: str):
        # stops all queued frames of the title animation
        for frame in self.anim_frames:
            self.window.after_cancel(frame)

        for widget in self.window.winfo_children():
            widget.destroy()
        SubMenu(self.window, self.board_sz, self.board_zoom, self.colors, mode)

    def exit(self):
        messagebox.showinfo('Afterword',
                            'Thank you for playing TIC-TAC-TOE!\n\nI spend over 191+ hours creating this game all by MYSELF.\n\nIn this project, I designed the AI that finds the highest winning probability, arranged the GUI elements in the most ergonomic way, optimized the algorithms, fixed bugs, and learned tkinter.\n\nHope you enjoyed it!')

        self.window.destroy()


def default_hint():
    messagebox.showinfo('Hint',
                        'Ah, just like the good ol\' one you played in kindergarten...\n\nYou can select a board length between 2 and... infinity! Boards larger than 3x3 only needs 4 in a row to win!\n\nThe starting player will be X, and the other will be O. No friends? No worries! You can play with my AI:\n\'The First-Gen Tallyman\'.')


def timed_hint():
    messagebox.showinfo('Hint',
                        'At the start, you can set a time limit for each player. Each player will have that amount of time to complete the game.\n\nBut not so fast - you will earn 1 extra second after each move!\n\n(other details are same as the Traditional Mode)')


def vanish_hint():
    messagebox.showinfo('Hint',
                        'Once you placed the minimum number of X/O you need to win, your oldest move will disappear!\n\nBad memory? You can enable \'next vanishing moves\' to see them highlighted in yellow. You can also make your moves last longer by changing the \'remain for\' slider.\n\n(other details are same as the Traditional Mode)')


def snake_hint():
    messagebox.showinfo('Hint',
                        'In your first move, you can place wherever you want. Afterwards, you can only place around your previous move - the head of the snake. Watch where your snake is going, as turning back can take some time.\n\nIf you accidentally get trapped in a dead end, you can continue at your last move before being trapped. I recommend playing this on a 7x7 or larger board.\n\n(other details are same as the Traditional Mode)')


class SubMenu:
    """
    === Attributes ===\n
    window: Name of window that displays MainMenu.\n
    board_sz: Length of the board.\n
    board_zoom: Magnification of the board.\n
    win_len: How many X in a row/column/diagonal to win.\n
    color: Dict containing colors for different features. Sorted into: player X, player O, all.\n
    mode: pvp = Player versus player; pvc = Player versus pc.\n
    """

    def __init__(self, window, board_sz, board_zoom, colors, mode: str):
        self.window = window
        self.board_sz = board_sz
        self.win_len = set_win_len(self.board_sz.get())
        self.check_winner_area = set_check_winner_area(board_sz.get(), self.win_len)
        self.board_zoom = board_zoom
        self.colors = colors
        self.mode = mode

        self.title = Button(self.window,
                            state='disabled',
                            takefocus=False,
                            borderwidth=0,
                            background='Black',
                            disabledforeground='Sea Green1',
                            text='\nChoose a mode',
                            font=('FixedSys', 25, 'underline', 'bold'))

        self.b_default = Button(self.window,
                                text='Traditional',
                                cursor='hand2',
                                overrelief='sunken',
                                command=lambda _=self.mode: self.to_gamemenu(_),
                                activeforeground='white',
                                activebackground='Sea Green',
                                background='Sea Green1',
                                foreground='Black',
                                width=25,
                                font=('FixedSys', 15),
                                borderwidth=5)

        self.b_default_hint = Button(self.window,
                                     bitmap='question',
                                     cursor='question_arrow',
                                     overrelief='sunken',
                                     command=default_hint,
                                     activeforeground='white',
                                     activebackground='Sea Green',
                                     background='Sea Green1',
                                     foreground='Black',
                                     width=30,
                                     borderwidth=5)

        self.b_timed = Button(self.window,
                              text='Timed Trial',
                              cursor='hand2',
                              overrelief='sunken',
                              command=lambda _=self.mode: self.to_gamemenu_t(_),
                              activeforeground='white',
                              activebackground='Sea Green',
                              background='Sea Green1',
                              foreground='Black',
                              width=25,
                              font=('FixedSys', 15),
                              borderwidth=5)

        self.b_timed_hint = Button(self.window,
                                   bitmap='question',
                                   cursor='question_arrow',
                                   overrelief='sunken',
                                   command=timed_hint,
                                   activeforeground='white',
                                   activebackground='Sea Green',
                                   background='Sea Green1',
                                   foreground='Black',
                                   width=30,
                                   borderwidth=5)

        self.b_vanish = Button(self.window,
                               text='Vanishing Moves',
                               cursor='hand2',
                               overrelief='sunken',
                               command=lambda _=self.mode: self.to_gamemenu_v(_),
                               activeforeground='white',
                               activebackground='Sea Green',
                               background='Sea Green1',
                               foreground='Black',
                               width=25,
                               font=('FixedSys', 15),
                               borderwidth=5)

        self.b_vanish_hint = Button(self.window,
                                    bitmap='question',
                                    cursor='question_arrow',
                                    overrelief='sunken',
                                    command=vanish_hint,
                                    activeforeground='white',
                                    activebackground='Sea Green',
                                    background='Sea Green1',
                                    foreground='Black',
                                    width=30,
                                    borderwidth=5)

        self.b_snake = Button(self.window,
                              text='Snake',
                              cursor='hand2',
                              overrelief='sunken',
                              command=lambda _=self.mode: self.to_gamemenu_s(_),
                              activeforeground='white',
                              activebackground='Sea Green',
                              background='Sea Green1',
                              foreground='Black',
                              width=25,
                              font=('FixedSys', 15),
                              borderwidth=5)

        self.b_snake_hint = Button(self.window,
                                   bitmap='question',
                                   cursor='question_arrow',
                                   overrelief='sunken',
                                   command=snake_hint,
                                   activeforeground='white',
                                   activebackground='Sea Green',
                                   background='Sea Green1',
                                   foreground='Black',
                                   width=30,
                                   borderwidth=5)

        self.non_mode_frame = Frame(self.window, background='Black', width=25)

        self.b_back = Button(self.non_mode_frame,
                             text='Back',
                             cursor='hand2',
                             overrelief='sunken',
                             command=self.to_mainmenu,
                             activeforeground='white',
                             activebackground='Sea Green',
                             background='Sea Green1',
                             foreground='Black',
                             width=12,
                             font=('FixedSys', 15),
                             borderwidth=5)

        self.b_settings = Button(self.non_mode_frame,
                                 text=u'\u2699',
                                 cursor='hand2',
                                 overrelief='sunken',
                                 command=self.to_settings,
                                 activeforeground='white',
                                 activebackground='Sea Green',
                                 background='Sea Green1',
                                 foreground='Black',
                                 width=12,
                                 font=('TkFixedFont', 13, 'bold'),
                                 borderwidth=5)

        # disables the close window (X) button in the top right corner
        self.window.protocol('WM_DELETE_WINDOW', lambda _=self: MainMenu.exit(_))

        # set the SubMenu window to the correct resolution
        self.window.geometry('700x370')
        self.window.configure(background='Black')
        # center buttons horizontally by giving a weight to all columns except the ones with the button
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(3, weight=1)

        self.title.grid(row=0, column=1, columnspan=2)
        self.b_default.grid(row=1, column=1)
        self.b_default_hint.grid(row=1, column=2)
        self.b_timed.grid(row=2, column=1)
        self.b_timed_hint.grid(row=2, column=2)
        self.b_vanish.grid(row=3, column=1)
        self.b_vanish_hint.grid(row=3, column=2)
        self.b_snake.grid(row=4, column=1)
        self.b_snake_hint.grid(row=4, column=2)
        self.non_mode_frame.grid(row=5, column=1, columnspan=2, pady=25)
        self.b_back.pack(side='left', padx=(1, 18))
        self.b_settings.pack(side='left', padx=(18, 1))

    def to_gamemenu(self, mode: str):
        for widget in self.window.winfo_children():
            widget.destroy()

        GameMenu(self.window, self.board_sz, self.board_zoom, self.colors, mode)

    def to_gamemenu_t(self, mode: str):
        for widget in self.window.winfo_children():
            widget.destroy()

        GameMenuT(self.window, self.board_sz, self.board_zoom, self.colors, mode)

    def to_gamemenu_v(self, mode: str):
        for widget in self.window.winfo_children():
            widget.destroy()

        GameMenuV(self.window, self.board_sz, self.board_zoom, self.colors, mode)

    def to_gamemenu_s(self, mode: str):
        for widget in self.window.winfo_children():
            widget.destroy()

        GameMenuS(self.window, self.board_sz, self.board_zoom, self.colors, mode)

    def to_mainmenu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        MainMenu(self.window, self.board_sz.get(), self.board_zoom.get(), self.colors)

    def to_settings(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        ColMenu(self.window, self.board_sz, self.board_zoom, self.colors, self.mode)


class ColMenu:

    def __init__(self, window, board_sz, board_zoom, colors, mode):
        self.window = window
        self.board_sz = board_sz
        self.win_len = set_win_len(self.board_sz.get())
        self.check_winner_area = set_check_winner_area(self.board_sz.get(), self.win_len)
        self.board_zoom = board_zoom
        self.colors = colors
        self.mode = mode

        self.title = Button(self.window,
                            state='disabled',
                            takefocus=False,
                            borderwidth=0,
                            background='Black',
                            disabledforeground='Sea Green1',
                            text='Settings',
                            font=('FixedSys', 25, 'underline', 'bold'))
        self.col_frames = {
            'X': LabelFrame(self.window,
                            text='X colors',
                            font=('FixedSys', 20, 'bold'),
                            foreground='Sea Green1',
                            background='Black',
                            borderwidth=3,
                            relief='ridge',
                            takefocus=False),
            'O': LabelFrame(self.window,
                            text='O colors',
                            font=('FixedSys', 20, 'bold'),
                            foreground='Sea Green1',
                            background='Black',
                            borderwidth=3,
                            relief='ridge',
                            takefocus=False),
            '': LabelFrame(self.window,
                           text='General',
                           font=('FixedSys', 20, 'bold'),
                           foreground='Sea Green1',
                           background='Black',
                           borderwidth=3,
                           relief='ridge',
                           takefocus=False)
        }

        self.b_exit = Button(self.window,
                             text='Save and Exit',
                             cursor='hand2',
                             overrelief='sunken',
                             command=self.to_submenu,
                             activeforeground='white',
                             activebackground='Sea Green',
                             background='Sea Green1',
                             foreground='Black',
                             width=25,
                             font=('FixedSys', 15),
                             borderwidth=5)

        self.col_frames['X'].grid(row=0, column=1, pady=(10, 5))
        self.col_frames['O'].grid(row=0, column=2, pady=(10, 5))
        self.col_frames[''].grid(row=1, column=1, columnspan=2, pady=5)
        self.b_exit.grid(row=2, column=1, columnspan=2, pady=10)

        # self.col_entries is a copy of self.colors, but containing col_entry instead of color str for each feature.
        self.col_entries = {
            'X': {},
            'O': {},
            '': {}
        }
        for plyr, feats in self.colors.items():
            _ = 0
            for feat, col in feats.items():
                _ += 1
                col_label = Label(
                    self.col_frames[plyr],
                    text=feat,
                    font=('FixedSys', 15),
                    foreground='Sea Green1',
                    background='Black',
                    takefocus=False)
                col_entry = Entry(
                    self.col_frames[plyr],
                    textvariable=StringVar(value=col),
                    borderwidth=1,
                    font=('FixedSys', 15),
                    cursor='xterm',
                    foreground='Black',
                    background=col)

                col_label.grid(row=_, column=0, padx=10)
                col_entry.grid(row=_, column=1)
                # make the key release event update bg of textbox
                col_entry.bind('<KeyRelease>', lambda event, _p=plyr, _f=feat: self.update_col(_p, _f))
                self.col_entries[plyr][feat] = col_entry
        self.col_entries['']['pruned_area'].config(state='disabled', cursor='no')

    def update_col(self, plyr: str, feat: str):
        try:
            # Try to set the background color of the text widget
            self.col_entries[plyr][feat].config(bg=self.col_entries[plyr][feat].get())
        except tk.TclError:
            # If the color is not valid, do nothing
            pass

    def to_submenu(self):
        # update self.color with new colors
        for plyr, feats in self.col_entries.items():
            for feat, entry in feats.items():
                try:
                    self.window.winfo_rgb(entry.get())
                    self.colors[plyr][feat] = entry.get()
                except tk.TclError:
                    messagebox.askretrycancel('Settings', f'Please enter a valid color for {feat}!')
                    return None

        if messagebox.showinfo('Settings', f'Your settings have been updated!\n\n{self.colors}'):
            for widget in self.window.winfo_children():
                widget.destroy()

            SubMenu(self.window, self.board_sz, self.board_zoom, self.colors, self.mode)


class GameMenu:
    """
    === Attributes ===\n
    window: Name of window that displays MainMenu.\n
    board_sz: Length of the board.\n
    check_winner_area = List containing slots where the winning chain will fall on.\n
    board_zoom: Magnification of the board.\n
    win_len: How many X in a row/column/diagonal to win.\n
    color: Dict containing colors for different features. Sorted into: player X, player O, all.\n
    mode: pvp = Player versus player; pvc = Player versus pc.\n
    plyr: Player playing in the current turn.\n
    main_board: List containing the board on screen.\n
    filled_slots_ind: List containing the index of filled slots of main_board.\n
    slot_buttons: List containing all the buttons that represent slots on the GUI.\n
    is_debugging: Show/hide the debugger.\n
    is_game_active: Whether the game is ongoing. Returns True from the moment the first player moved until there's a winner, else False.\n
    """

    def __init__(self, window, board_sz, board_zoom, colors, mode: str):
        self.window = window
        self.board_sz = board_sz
        self.win_len = set_win_len(self.board_sz.get())
        self.check_winner_area = set_check_winner_area(self.board_sz.get(), self.win_len)
        self.board_zoom = board_zoom
        self.mode = mode
        self.colors = colors

        self.plyr = 'X'
        self.main_board = setup_board(self.board_sz.get())
        self.filled_slots_ind = []
        self.slot_buttons = []
        self.is_debugging = BooleanVar(value=False)
        self.is_game_active = False

        self.settings_frame = Frame(self.window)
        self.board_frame = Frame(self.window)
        self.turn_hint_frame = Frame(self.board_frame, background='SystemButtonFace')
        self.turn_hint = {
            'X': Label(
                self.turn_hint_frame,
                text='X turn',
                font=('Helvetica', self.board_zoom.get() * 2, 'bold'),
                foreground=self.colors['X']['symbol'],
                width=13,
                borderwidth=5,
                relief='ridge',
                takefocus=False),
            'O': Label(
                self.turn_hint_frame,
                text='O turn',
                font=('Helvetica', self.board_zoom.get() * 2, 'bold'),
                foreground=self.colors['O']['symbol'],
                width=13,
                borderwidth=5,
                relief='ridge',
                takefocus=False)
        }
        self.b_back = Button(
            self.settings_frame,
            text='Back',
            cursor='hand2',
            relief='groove',
            overrelief='sunken',
            command=self.to_submenu,
            width=5,
            borderwidth=5
        )
        self.replay_button = Button(
            self.settings_frame,
            text='Replay',
            cursor='hand2',
            relief='groove',
            overrelief='sunken',
            state='disabled',
            command=self.replay,
            width=5,
            borderwidth=5
        )
        self.board_sz_label = Label(
            self.settings_frame,
            text='\nBoard Length'
        )
        self.board_sz_slider = Scale(
            self.settings_frame,
            orient='horizontal',
            variable=self.board_sz,
            length=100,
            from_=2,
            to=9,
            cursor='sb_h_double_arrow'
        )
        # Set up a trace to update the number and pos of buttons on the grid whenever the value changes
        self.trace1 = self.board_sz.trace_add('write', self.adjust_length)
        self.board_sz_tip = Label(
            self.settings_frame,
            text='Amount in a row to win: ' + str(self.win_len)
        )
        self.board_zoom_label = Label(
            self.settings_frame,
            text='\nZoom'
        )
        self.board_zoom_slider = Scale(
            self.settings_frame,
            orient='horizontal',
            variable=self.board_zoom,
            length=100,
            from_=5,
            to=13,
            cursor='sb_h_double_arrow'
        )
        # Set up a trace to update scale of buttons on the grid whenever the value changes
        self.trace2 = self.board_zoom.trace_add('write', self.adjust_zoom)
        self.pvco_checkbox = Checkbutton(
            self.settings_frame,
            text='Computer starts first',
            height=2,
            cursor='hand2',
            command=self.pvc_first
        )
        self.debug_checkbox = Checkbutton(
            self.settings_frame,
            text='Show debugging data (may\nimpact performance)',
            height=2,
            cursor='hand2',
            variable=self.is_debugging,
            command=self.toggle_debugger
        )
        self.debugger = Text(
            self.settings_frame,
            wrap='none',
            height=15,
            width=27
        )

        # set the GameMenu window to the correct resolution
        self.window.geometry('')
        self.window.config(background='SystemButtonFace')
        self.settings_frame.pack(side='left', expand=True, fill='both')
        self.settings_frame.grid_rowconfigure(10)
        self.board_frame.pack(side='left', expand=True, fill='x')
        self.turn_hint_frame.grid(columnspan=self.board_sz.get(), row=0, column=2)
        self.turn_hint['X'].pack()
        self.turn_hint['O'].pack()
        self.b_back.grid(row=1, column=0, pady=(0, 15))
        self.replay_button.grid(row=1, column=1, pady=(0, 15))
        self.board_sz_label.grid(row=4, column=1)
        self.board_sz_slider.grid(row=4, column=2)
        self.board_sz_tip.grid(columnspan=2, row=5, column=1)
        self.board_zoom_label.grid(row=6, column=1)
        self.board_zoom_slider.grid(row=6, column=2)
        if self.mode == 'pvc':
            self.pvco_checkbox.grid(columnspan=2, row=7, column=1)
        self.debug_checkbox.grid(columnspan=2, row=8, column=1)

        # initialize the board_frame and settings_frame
        self.create_boardframe()
        # rebinds the close window (X) slot_button in the top right corner
        self.window.protocol('WM_DELETE_WINDOW', self.to_submenu)

    def toggle_debugger(self):
        # reset all previous debugging info
        for button in self.slot_buttons:
            # if the slot has a number on, it has no X/O
            if type(button.cget('text')) == int:
                button.config(text='')
            if button.cget('background') in [self.colors['']['pruned_area'], self.colors['']['winner_area']]:
                button.config(background='SystemButtonFace')

        if self.is_debugging.get() is True:
            self.debugger.grid(columnspan=3, row=10, column=0, sticky='ns')
            for slot in range(len(self.slot_buttons)):
                if slot not in self.filled_slots_ind:
                    self.slot_buttons[slot].config(text=slot, foreground='gray')
                if slot in self.check_winner_area:
                    self.slot_buttons[slot].config(background=self.colors['']['winner_area'])
        else:
            self.debugger.grid_forget()
            for button in self.slot_buttons:
                if button.cget('background') == self.colors['']['pc_move']:
                    button.config(background='SystemButtonFace')
                    break

    def create_boardframe(self):
        self.slot_buttons = []
        # create buttons in board_frame
        for row in range(self.board_sz.get()):
            for col in range(self.board_sz.get()):
                button_num = row * self.board_sz.get() + col
                button = Button(
                    self.board_frame,
                    font=('Helvetica', self.board_zoom.get() * 4, 'bold'),
                    cursor='plus',
                    command=lambda _=button_num: self.update_slot(_),
                    width=3,
                    borderwidth=5
                )
                self.slot_buttons.append(button)
                button.grid(row=row + 3, column=col + 2)

    def adjust_length(self, *args):
        # When I adjust the board length, I must delete the old buttons as I cannot change their position
        for button in self.slot_buttons:
            button.destroy()

        # Generate new board and attributes with the correct dimension at backend
        self.main_board = setup_board(self.board_sz.get())
        self.win_len = set_win_len(self.board_sz.get())
        self.check_winner_area = set_check_winner_area(self.board_sz.get(), self.win_len)

        # Generate new buttons and symbol indicator at frontend
        self.create_boardframe()
        self.turn_hint_frame.grid(columnspan=self.board_sz.get())
        self.board_sz_tip.config(text='Amount in a row to win: ' + str(self.win_len))
        self.toggle_debugger()

    def adjust_zoom(self, *args):
        # Update the position of the turn indicator and the scale of the buttons.
        for slot_button in self.slot_buttons:
            slot_button.config(font=('Helvetica', self.board_zoom.get() * 4, 'bold'))
        self.turn_hint['X'].config(font=('Helvetica', self.board_zoom.get() * 2, 'bold'))
        self.turn_hint['O'].config(font=('Helvetica', self.board_zoom.get() * 2, 'bold'))

    def pvc_first(self):
        self.mode = 'pvc'
        self.plyr = 'O'
        self.turn_hint['X'].config(foreground='SystemDisabledText')
        self.turn_hint['O'].config(foreground=self.colors['O']['symbol'])
        self.board_sz_slider.config(state='disabled')
        self.board_sz_label.config(state='disabled')
        self.pvco_checkbox.config(state='disabled')
        self.replay_button.config(state='normal')
        self.update_slot_pvc(-1)
        self.is_game_active = True

    def update_slot(self, prev_input: int):
        # clear debugger window
        self.debugger.delete('1.0', 'end')
        # If the game is not ongoing before, this is the first move. Change some settings.
        if self.is_game_active is False:
            self.board_sz_slider.config(state='disabled')
            self.board_sz_label.config(state='disabled')
            self.replay_button.config(state='normal')
            self.pvco_checkbox.config(state='disabled')
            self.is_game_active = True

        if self.mode == 'pvp':
            self.update_slot_pvp(prev_input)
            self.check_winner_pvp()

        elif self.mode == 'pvc':
            self.update_slot_pvp(prev_input)
            self.check_winner_pvc()
            if self.is_game_active:
                self.update_slot_pvc(prev_input)
                self.check_winner_pvc()

    def update_slot_pvc(self, prev_input: int) -> int:
        self.debugger.insert(tk.END, f'Player\'s move:\n\t{prev_input}\n')
        # win_len must be <= 4 as the pruned area can be 4 slots wide if player moved at corners.
        pc_move = pc_input(opp(self.plyr), self.main_board, self.board_sz.get(),
                           min(self.win_len, 4), set_check_winner_area(self.board_sz.get(), min(self.win_len, 4)),
                           prev_input, self.is_debugging.get(), self.debugger,
                           self.slot_buttons)
        self.filled_slots_ind.append(pc_move)
        self.main_board[pc_move] = opp(self.plyr)
        # Update frontend board. If player = O, PC = opponent(O). If player = X, PC = opponent(X).
        self.slot_buttons[pc_move].config(text=self.main_board[pc_move],
                                          disabledforeground=self.colors[opp(self.plyr)]['symbol'], background=self.colors['']['pc_move'], state='disabled')
        self.debugger.insert('end', f'PC\'s move:\n\t{pc_move}\n')

        return pc_move

    def check_winner_pvc(self):
        # used to check winner after each turn in PVC mode
        winner = check_winner_anywhere(self.main_board, self.board_sz.get(), self.win_len, self.check_winner_area)
        if winner[1] == 'tie':
            self.stop_game()
            if messagebox.askyesno('Outcome', 'Ended in tie!\n\n"You\'ll never win ... not satisfied? Replay!"') is True:
                self.replay()
        elif winner[0] == opp(self.plyr):
            self.stop_game()
            if messagebox.askyesno('Outcome', f'Computer wins {winner[1]}!\n\n"Shouldn\'t humans be smarter?"') is True:
                self.replay()
        elif winner[0] == self.plyr:
            self.stop_game()
            if messagebox.askyesno('Outcome', f'You win {winner[1]}!\n\n"That shouldn\'t happen ... replay?"') is True:
                self.replay()

    def update_slot_pvp(self, prev_input: int):
        # reset tint for pruned area and last pc move
        self.toggle_debugger()
        # update backend board
        self.main_board[prev_input] = self.plyr
        self.filled_slots_ind.append(prev_input)
        # update frontend board
        self.slot_buttons[prev_input].config(text=self.main_board[prev_input],
                                             disabledforeground=self.colors[self.plyr]['symbol'],
                                             state='disabled')

    def check_winner_pvp(self):
        # used to check winner after each turn in PVP mode
        winner = check_winner_anywhere(self.main_board, self.board_sz.get(), self.win_len, self.check_winner_area)
        if winner[1] == 'tie':
            self.stop_game()
            messagebox.showinfo('Outcome', 'Tie game!')
        elif winner != (' ', ' ',):
            self.stop_game()
            messagebox.showinfo('Outcome', f'Player \'{winner[0]}\' wins {winner[1]}!')

        else:
            # If no one wins, disable this plyr's indicator and update next plyr's indicators.
            self.turn_hint[self.plyr].config(foreground='SystemDisabledText', background='SystemButtonFace', relief='flat')
            self.turn_hint[opp(self.plyr)].config(foreground=self.colors[opp(self.plyr)]['symbol'], background='white', relief='ridge')
            self.plyr = opp(self.plyr)

    def stop_game(self):
        self.is_game_active = False
        for button in self.slot_buttons:
            button.config(state='disabled')

    def to_submenu(self):
        if messagebox.askyesno('Confirmation', 'Are you sure you want to quit?\n\nYou will loose all your progress.'):
            self.is_game_active = False
            self.board_sz.trace_remove('write', self.trace1)
            self.board_sz.trace_remove('write', self.trace2)
            for widget in self.window.winfo_children():
                widget.destroy()

            SubMenu(self.window, self.board_sz, self.board_zoom, self.colors, self.mode)

    def replay(self):
        if messagebox.askyesno('Confirmation',
                               'Are you sure you want to restart?\n\nYou will loose all your progress.'):
            self.is_game_active = False
            self.board_sz.trace_remove('write', self.trace1)
            self.board_sz.trace_remove('write', self.trace2)
            for widget in self.window.winfo_children():
                widget.destroy()

            GameMenu(self.window, self.board_sz, self.board_zoom, self.colors, self.mode)


class GameMenuT(GameMenu):
    """
    === Attributes ===\n
    remain_time: Dict containing how much time does each player still have.\n
    hint_scale: Used to animate the inflate of timer at the start of each turn.\n
    """

    def __init__(self, window, board_sz, board_zoom, colors, mode: str):
        super().__init__(window, board_sz, board_zoom, colors, mode)
        self.remain_time = {
            'X': StringVar(value='10'),
            'O': StringVar(value='10')
        }
        self.hint_scale = 0
        self.next_countdown = None

        # destroy the original x_turn_hint and o_turn_hint created by superclass
        self.turn_hint['X'].destroy()
        self.turn_hint['O'].destroy()
        self.turn_hint = {
            'X': LabelFrame(self.turn_hint_frame,
                            text='X turn',
                            font=('Helvetica', self.board_zoom.get() * 2 + 1, 'bold'),
                            foreground=self.colors['X']['symbol'],
                            borderwidth=5,
                            relief='ridge',
                            takefocus=False),
            'O': LabelFrame(self.turn_hint_frame,
                            text='O turn',
                            font=('Helvetica', self.board_zoom.get() * 2 + 1, 'bold'),
                            foreground=self.colors['O']['symbol'],
                            borderwidth=5,
                            relief='ridge',
                            takefocus=False)
        }
        self.time_entry = {
            'X': Entry(self.turn_hint['X'],
                       width=4,
                       borderwidth=1,
                       font=('Courier', self.board_zoom.get() * 3 + 1, 'bold'),
                       foreground=self.colors['X']['symbol'],
                       disabledforeground=self.colors['X']['symbol'],
                       disabledbackground='white',
                       justify='center',
                       textvariable=self.remain_time['X']),
            'O': Entry(self.turn_hint['O'],
                       width=4,
                       borderwidth=1,
                       font=('Courier', self.board_zoom.get() * 3 + 1, 'bold'),
                       foreground=self.colors['O']['symbol'],
                       disabledforeground=self.colors['O']['symbol'],
                       disabledbackground='white',
                       justify='center',
                       textvariable=self.remain_time['O'])
        }

        self.turn_hint['X'].pack(side='left')
        self.turn_hint['O'].pack(side='left')
        self.time_entry['X'].pack()
        self.time_entry['O'].pack()

    def adjust_zoom(self, *args):
        super().adjust_zoom()
        self.time_entry['X'].config(font=('Helvetica', self.board_zoom.get() * 3 + 1, 'bold'))
        self.time_entry['O'].config(font=('Helvetica', self.board_zoom.get() * 3 + 1, 'bold'))

    def countdown(self):
        remain_time = float(self.remain_time[self.plyr].get())

        # If (time's not up) and (game has started and no one wins yet):
        if remain_time > 0.0 and self.is_game_active is True:
            # animate inflate of the current plyr's timer
            self.time_entry[self.plyr].config(font=('Courier', self.board_zoom.get() * 3 + 1 + self.hint_scale, 'bold'))
            self.hint_scale = min(self.hint_scale + 2, 3)

            # Decrease the remain_time value by 0.1 every 100ms and display only 1 deci point using round().
            # I didn't decrease by 1 every 1000ms (1sec) as the timer delayed update when switching turns.
            self.remain_time[self.plyr].set(str(round(remain_time - 0.1, 1)))
            self.next_countdown = self.window.after(100, self.countdown)

        # If player runs out of time, opponent wins and stop all recursions.
        elif remain_time <= 0.0:
            messagebox.showinfo('Outcome', f"Time's up! Player {opp(self.plyr)} wins")
            self.stop_game()
            return None

        # If X is not playing this turn or the game has ended, stop X's countdown and flash.
        else:
            self.time_entry[self.plyr].config(relief='sunken', disabledforeground=self.colors[self.plyr]['symbol'],
                                              disabledbackground='white')
            return None

        # If X has under 5 secs left, flash the timer.
        if remain_time < 5.0 and remain_time % 1 < 0.4:
            self.time_entry[self.plyr].config(relief='sunken', disabledbackground='white')
        elif remain_time < 5.0 and remain_time % 1 >= 0.4:
            self.time_entry[self.plyr].config(relief='groove', disabledbackground='yellow')

    def update_slot(self, prev_input: int):
        # If the game is not ongoing before, this is the first move.
        if self.is_game_active is False:
            # If the input time is not valid:
            if not self.remain_time['X'].get().isdigit() or not self.remain_time['O'].get().isdigit():
                messagebox.askretrycancel('Warning', f'Please enter a decimal number!')
                return None
            # If the input time is valid:
            self.board_sz_slider.config(state='disabled')
            self.board_sz_label.config(state='disabled')
            self.replay_button.config(state='normal')
            self.pvco_checkbox.config(state='disabled')
            self.time_entry['X'].config(state='disabled')
            self.time_entry['O'].config(state='disabled')
            # If game is started by player, PC must be O. So, hide O's timer.
            self.turn_hint['O'].pack_forget()

            # I put update_slot before countdown in X's first move to prevent X losing 0.1 sec.
            super().update_slot(prev_input)
            self.countdown()
        else:
            self.hint_scale = 0
            super().update_slot(prev_input)

    # Below, I override update_slot_pvc and check_winner_pvp to include timer switching.
    # I chose these as: update_slot_pvc is only executed once in PVC; check_winner_pvp is the only func used in PVP and not PVC
    def update_slot_pvc(self, prev_input):
        if self.is_game_active is True and len(self.filled_slots_ind) > 1:
            # this plyr gets bonus time
            self.remain_time[self.plyr].set(str(float(self.remain_time[self.plyr].get()) + 1))
        super().update_slot_pvc(prev_input)

    def check_winner_pvp(self):
        super().check_winner_pvp()
        # Grey out this plyr's timer, colorize next plyr's timer.
        self.time_entry[opp(self.plyr)].config(relief='flat', disabledforeground='SystemDisabledText',
                                               disabledbackground='SystemButtonFace',
                                               font=('Courier', self.board_zoom.get() * 3 + 1, 'bold'))
        self.time_entry[self.plyr].config(relief='sunken', disabledforeground=self.colors[self.plyr]['symbol'], disabledbackground='white')

        if self.is_game_active is True and len(self.filled_slots_ind) > 1:
            # This plyr gets bonus time. Note: self.plyr is the NEXT plyr
            self.remain_time[opp(self.plyr)].set(str(float(self.remain_time[opp(self.plyr)].get()) + 1))

    def pvc_first(self):
        self.turn_hint['X'].pack_forget()
        self.time_entry['O'].config(state='disabled')
        super().pvc_first()
        self.countdown()

    def replay(self):
        if messagebox.askyesno('Confirmation',
                               'Are you sure you want to restart?\n\nYou will loose all your progress.'):
            self.is_game_active = False
            self.board_sz.trace_remove('write', self.trace1)
            self.board_sz.trace_remove('write', self.trace2)
            # stops the next queued countdown()
            self.window.after_cancel(self.next_countdown)
            for widget in self.window.winfo_children():
                widget.destroy()

            GameMenuT(self.window, self.board_sz, self.board_zoom, self.colors, self.mode)


class GameMenuV(GameMenu):
    """
    === Attributes ===\n
    prev_inputs: A list containing the l most recent moves on the board, in chronological order. Leftmost element = earliest move. Rightmost element = latest move.\n
    remain_steps: How many steps into the future will an X/O last.\n
    show_nxt_vanish_move: Show/hide which move is going to vanish in the next turn.
    """

    def __init__(self, window, board_sz, board_zoom, colors, mode: str):
        super().__init__(window, board_sz, board_zoom, colors, mode)
        self.prev_inputs = []
        self.remain_steps = IntVar()
        self.show_nxt_vanish_move = BooleanVar(value=False)

        self.remain_stps_label = Label(
            self.settings_frame,
            text='\nRemain for'
        )
        self.remain_stps_slider = Scale(
            self.settings_frame,
            orient='horizontal',
            variable=self.remain_steps,
            length=100,
            from_=self.win_len,
            to=self.win_len * 2,
            cursor='sb_h_double_arrow'
        )
        self.nxt_vanish_checkbox = Checkbutton(
            self.settings_frame,
            text='Show next vanishing moves',
            cursor='hand2',
            variable=self.show_nxt_vanish_move,
            command=self.delete_moves
        )

        self.remain_stps_label.grid(row=2, column=1)
        self.remain_stps_slider.grid(row=2, column=2)
        self.nxt_vanish_checkbox.grid(columnspan=2, row=3, column=1)

    def delete_moves(self):
        # If (num of moves by X & O so far) + (moves by X & O in this turn) is more than remain_steps*2, the num of moves by X is more than remain_steps. So X's moves start to vanish.
        if (len(self.prev_inputs) > self.remain_steps.get() * 2) and self.is_game_active:
            self.debugger.insert('end', f'Most recent moves:\n{self.prev_inputs}')
            self.main_board[self.prev_inputs[0]] = ' '
            self.slot_buttons[self.prev_inputs[0]].config(text='', background='SystemButtonFace', state='normal')
            self.filled_slots_ind.remove(self.prev_inputs[0])
            self.prev_inputs = self.prev_inputs[1:]
            self.toggle_debugger()

        # if (num of moves by X & O so far) + (moves by X & O in this turn) is one less before vanishing begins, tint the 3 oldest moves about to vanish.
        if (len(self.prev_inputs) + 2 > self.remain_steps.get() * 2 - 1) and self.show_nxt_vanish_move.get():
            self.slot_buttons[self.prev_inputs[1]].config(background=self.colors['']['nxt_vanish_move1'])
            self.slot_buttons[self.prev_inputs[0]].config(background=self.colors['']['nxt_vanish_move0'])

    def adjust_length(self, *args):
        super().adjust_length(*args)
        self.remain_stps_slider.config(from_=self.win_len, to=self.win_len * 2)

    def update_slot_pvc(self, prev_input: int):
        pc_move = super().update_slot_pvc(prev_input)
        self.prev_inputs.append(pc_move)

    def check_winner_pvc(self):
        super().check_winner_pvc()
        self.delete_moves()

    def update_slot_pvp(self, prev_input: int):
        super().update_slot_pvp(prev_input)
        self.prev_inputs.append(prev_input)

    def check_winner_pvp(self):
        super().check_winner_pvp()
        self.delete_moves()

    def replay(self):
        if messagebox.askyesno('Confirmation',
                               'Are you sure you want to restart?\n\nYou will loose all your progress.'):
            self.is_game_active = False
            self.board_sz.trace_remove('write', self.trace1)
            self.board_sz.trace_remove('write', self.trace2)
            for widget in self.window.winfo_children():
                widget.destroy()

            GameMenuV(self.window, self.board_sz, self.board_zoom, self.colors, self.mode)


class GameMenuS(GameMenu):
    """
    === Attributes ===\n
    prev_inputs: Dict containing 2 lists: one containing all the moves made by X in chronological order, the other containing O's. Leftmost element = earliest move. Rightmost element = latest move.\n
    """

    def __init__(self, window, board_sz, board_zoom, colors, mode: str):
        super().__init__(window, board_sz, board_zoom, colors, mode)
        self.prev_inputs = {
            'X': [],
            'O': []
        }
        self.win_len = self.board_sz.get()
        self.check_winner_area = set_check_winner_area(self.board_sz.get(), self.win_len)
        self.board_sz_tip.config(text='Amount in a row to win: ' + str(self.win_len))

    def adjust_length(self, *args):
        super().adjust_length(*args)
        self.win_len = self.board_sz.get()
        self.check_winner_area = set_check_winner_area(self.board_sz.get(), self.win_len)
        self.board_sz_tip.config(text='Amount in a row to win: ' + str(self.win_len))
        self.toggle_debugger()

    def update_slot_pvc(self, prev_input: int) -> int:
        is_surrounded = True

        # while (next plyr is not stuck) and (both X and O alr placed their first move):
        while is_surrounded is True and len(self.prev_inputs['X']) + len(self.prev_inputs['O']) > 1 and self.is_game_active is True:
            for slot in range(self.board_sz.get() ** 2):
                pass

        # win_len must be <= 4 as the pruned area can be 4 slots wide if player moved at corners.
        pc_move = pc_input(opp(self.plyr), self.main_board, self.board_sz.get(),
                           min(self.win_len, 4), set_check_winner_area(self.board_sz.get(), min(self.win_len, 4)),
                           self.prev_inputs[opp(self.plyr)][-1], self.is_debugging.get(), self.debugger,
                           self.slot_buttons)
        self.filled_slots_ind.append(pc_move)
        self.main_board[pc_move] = opp(self.plyr)
        # Update frontend board. If player = O, PC = opponent(O). If player = X, PC = opponent(X).
        self.slot_buttons[pc_move].config(text=self.main_board[pc_move],
                                          disabledforeground=self.colors[opp(self.plyr)]['symbol'], background=self.colors['']['pc_move'], state='disabled')
        self.debugger.insert('end', f'PC\'s move:{pc_move}\n')

        return pc_move

    def update_slot_pvp(self, prev_input: int):
        super().update_slot_pvp(prev_input)
        self.slot_buttons[prev_input].config(background=self.colors[self.plyr]['snake_head'])

        if len(self.prev_inputs[self.plyr]) > 0:
            # turn the snake's previous head to body color
            self.slot_buttons[self.prev_inputs[self.plyr][-1]].config(background=self.colors[self.plyr]['snake_body'])
        self.prev_inputs[self.plyr].append(prev_input)

    def check_winner_pvp(self):
        super().check_winner_pvp()
        # I override check_winner_pvp to include code switching snake head
        is_surrounded = True
        # while (next plyr is not stuck) and (both X and O alr placed their first move):
        while is_surrounded is True and len(self.prev_inputs['X']) + len(self.prev_inputs['O']) > 1 and self.is_game_active is True:
            for slot in range(self.board_sz.get() ** 2):
                # If a slot is in the 3x3 area of the next plyr's last input and has nothing on it, make it pressable. Note: self.plyr is the NEXT plyr
                if self.prev_inputs[self.plyr][-1] // self.board_sz.get() - 1 <= slot // self.board_sz.get() <= self.prev_inputs[self.plyr][-1] // self.board_sz.get() + 1 and \
                        self.prev_inputs[self.plyr][-1] % self.board_sz.get() - 1 <= slot % self.board_sz.get() <= self.prev_inputs[self.plyr][-1] % self.board_sz.get() + 1 and self.main_board[slot] == ' ':
                    self.slot_buttons[slot].config(state='normal', relief='raised')
                    is_surrounded = False
                # If a slot is around the next plyr's last input and has nothing on it, make it unpressable.
                elif self.main_board[slot] == ' ':
                    self.slot_buttons[slot].config(state='disabled', relief='sunken')

            # if next plyr is stuck, recursively go back to the last move before stuck and activates surrounding slots
            if is_surrounded is True:
                self.prev_inputs[self.plyr] = self.prev_inputs[self.plyr][:-1]

    def replay(self):
        if messagebox.askyesno('Confirmation',
                               'Are you sure you want to restart?\n\nYou will loose all your progress.'):
            self.is_game_active = False
            self.board_sz.trace_remove('write', self.trace1)
            self.board_sz.trace_remove('write', self.trace2)
            for widget in self.window.winfo_children():
                widget.destroy()

            GameMenuS(self.window, self.board_sz, self.board_zoom, self.colors, self.mode)


ver_no = 'Tic Tac Toe v11'

window = tk.Tk()
MainMenu(window)
window.title(ver_no)

window.mainloop()
