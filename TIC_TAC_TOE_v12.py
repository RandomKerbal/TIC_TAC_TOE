import random
import tkinter as tk
from tkinter import messagebox
import backend as ttt


def to_changelog():
    messagebox.showinfo('Changelog', '''
Ver 1 : Added the basics: player vs player mode, infinite board length, winner checker, etc...\n
Ver 2 : Boards are now stored as single list instead of dictionary. Changes player input from index number to x,y coordinates. Rebuild the entire code to process this new file format.\n
Ver 3 : Added basic AI. Added console GUI. Make boards that are 7*7 or larger needs only half the board length to win.\n
Ver 4 : Added board pruning for boards larger than 3x3 to reduce AI calculations. Added some randomization to the moves made by the AI. Restructured the entire AI code for optimization.\n
Ver 5 : Added deathtrap checker - that's the hardest part of this project! Now the AI is 100% unbeatable for a 3x3 board. Added the option to let AI start first.\n
Ver 6 : Make board pruning only for boards larger than 5x5. Added land-filling to boards larger than 3x3. Added a matplotlib display for AI's Risk Analysis.\n
Ver 7 : Added Tkinter GUI. Rebuild winner checker for HUGE optimization. Changed every code to user-def function. Added user-friendly debugging root.\n
Ver 8 : HUGE OPTIMIZATION: Rebuild the board pruning code to combine both pruning and land-filling into 1 function. Pruned board and main board now have the same dimension - no additional function is needed to convert indexes between the two boards!\n
Ver 9 : Rebuild and tidy up all GUI code using class instead of user-def functions. Rebuild to make board pruning dynamic, it can now scale up if that area has not enough empty indexes. Added 'Replay' button. Changed empty indexes from '[ ]' to ' '. Fixed bug where the endpoint of checking diagonally from top right to down left doesn't move with the start point.\n
Ver 10: Added title animation. Added 4 modes: Traditional, Time Trial, Vanishing Moves, Snake\n
Ver 11: Globalised colors for each feature. Added color settings. Changed O's snake color. Capped length to win at 4. Added 'Total Child Count' to debugger.
Ver 12: Redesign the algorithm to use depth-first search instead of breadth-first-search. Build a specialized, faster winner-checking algo that only checks for whether a specific player wins, instead of checking who wins.\n
Ver 13: Prunner V2
Ver 14: Prunner V3, Shayan's Algo.
Ver 15: GUI Revamp
Ver 16: 
Ver 17: Base10, int board.\n
    ''')


class MainMenu:
    """
    :ivar window: name of window that displays MainMenu.
    :ivar board_len: length of the board.
    :ivar board_zoom: magnification of the board.
    :ivar colors: list containing 3 dicts: list[0] stores colors for general features; list[1] stores colors for X features; list[2] stores colors for O features.
    """

    def __init__(self, window, board_len: int = 3, board_zoom: int = 5, colors: dict = None, ai_type: int = 0):
        self.window = window
        self.board_len = tk.IntVar(value=board_len)
        self.board_zoom = tk.IntVar(value=board_zoom)
        self.ai_type = tk.IntVar(value=ai_type)
        if colors is None:
            self.colors = [
                {
                    'pc_move': 'Khaki1',
                    'simmable_inds': 'Lemon Chiffon2',
                    'nxt_vanish_move': 'Navajo White',
                    'background': 'SystemButtonFace',
                    'foreground': 'SystemButtonFace'
                },
                {
                    'symbol': 'Red4',
                    'snake_head': 'Green Yellow',
                    'snake_body': 'Dark Olive Green1'
                },
                {
                    'symbol': 'Navy',
                    'snake_head': 'Cyan1',
                    'snake_body': 'Dark Slate Gray1',
                }
            ]
        else:
            self.colors = colors

        self.title_line1 = tk.Label(self.window,
                                    width=500,
                                    borderwidth=0,
                                    background='Black',
                                    foreground='Sea Green1',
                                    text='=' * 999,
                                    font='TkFixedFont',
                                    takefocus=False
                                    )
        self.title_line2 = tk.Label(self.window,
                                    width=500,
                                    borderwidth=0,
                                    background='Black',
                                    foreground='Sea Green1',
                                    text='\n' + '=' * 999,
                                    font='TkFixedFont',
                                    takefocus=False
                                    )
        self.title_label = tk.Label(self.window,
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
                                    anchor='nw',
                                    takefocus=False
                                    )

        self.subtitle_label = tk.Label(self.window,
                                       borderwidth=0,
                                       width=500,
                                       background='Black',
                                       foreground='Sea Green1',
                                       text='',
                                       font='TkFixedFont',
                                       justify='left',
                                       takefocus=False
                                       )
        subtitle_text = '   99% Made by CZY          4 Unprecedented Modes!          Unbeatable AI!        '

        self.b_pvc = tk.Button(self.window,
                               text='Single Player',
                               cursor='hand2',
                               overrelief='sunken',
                               command=lambda _=0: self.to_submenu(_),
                               activeforeground='white',
                               activebackground='Sea Green',
                               background='Sea Green1',
                               foreground='Black',
                               width=500,
                               font=('FixedSys', 15),
                               borderwidth=5)

        self.b_pvp = tk.Button(self.window,
                               text='Multi Player',
                               cursor='hand2',
                               overrelief='sunken',
                               command=lambda _=1: self.to_submenu(_),
                               activeforeground='white',
                               activebackground='Sea Green',
                               background='Sea Green1',
                               foreground='Black',
                               width=500,
                               font=('FixedSys', 15),
                               borderwidth=5)

        self.b_changelog = tk.Button(self.window,
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

        self.b_exit = tk.Button(self.window,
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

        # animate title & subtitle:
        # time between frames, in milliseconds
        wait = 250
        # anim_frames contains 95 (frame 0 - 94) frames of the animation. All frames r called at the same time, but their executions r queued up.
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

    def to_submenu(self, mode: int):
        # stops all queued frames of the title animation
        for frame in self.anim_frames:
            self.window.after_cancel(frame)

        for widget in self.window.winfo_children():
            widget.destroy()
        SubMenu(self.window, self.board_len, self.board_zoom, self.colors, mode, self.ai_type)

    def exit(self):
        messagebox.showinfo('Afterword',
                            'Thank you for playing TIC-TAC-TOE!\n\nI spend over 221+ hours creating this game all by MYSELF.\n\nIn this project, I designed the AI that finds the highest winning probability, arranged the GUI elements in the most ergonomic way, optimized the algorithms, fixed bugs, and learned tkinter.\n\nHope you enjoyed it!')

        self.window.destroy()


def default_hint():
    messagebox.showinfo('Hint',
                        'Ah, just like the good ol\' one you played in kindergarten...\n\nYou can select a board length between 2 and... infinity! Boards larger than 3x3 only needs 4 in a row to win!\n\nThe starting player will be X, and the other will be O. No friends? No worries! You can play with my AI:\n\'The Initial Move Tallyman\'.')


def timed_hint():
    messagebox.showinfo('Hint',
                        'At the start, you can set a time limit for each player. Each player will have that amount of time to complete the game.\n\nBut not so fast - you will earn 1 extra second after each move!\n\n(other details are same as the Traditional Mode)')


def vanish_hint():
    messagebox.showinfo('Hint',
                        'Once you placed the minimum number of X/O you need to win, your oldest move will disappear!\n\nBad memory? You can enable \'next vanishing move\' to see them highlighted in yellow. You can also make your moves last longer by changing the \'remain for\' slider.\n\n(other details are same as the Traditional Mode)')


def snake_hint():
    messagebox.showinfo('Hint',
                        'In your first move, you can place wherever you want. Afterwards, you can only place around your previous move - the head of the snake. Watch where your snake is going, as turning back can take some time.\n\nIf you accidentally get trapped in a dead end, you can continue at your last move before being trapped. I recommend playing this on a 7x7 or larger board.\n\n(other details are same as the Traditional Mode)')


class SubMenu:
    """
    :ivar window, board_len, board_zoom, colors: same as GameMenu.
    :ivar win_len: how many X in a row/column/diagonal to win.
    :ivar mode: 0 = player versus pc; 1 = player versus player.
    """

    def __init__(self, window, board_len, board_zoom, colors: dict, mode: int, ai_type):
        self.window = window
        self.board_len = board_len
        self.win_len = ttt.set_win_len(self.board_len.get())
        self.board_zoom = board_zoom
        self.colors = colors
        self.mode = mode
        self.ai_type = ai_type

        self.title = tk.Button(self.window,
                               state='disabled',
                               takefocus=False,
                               borderwidth=0,
                               background='Black',
                               disabledforeground='Sea Green1',
                               text='\nChoose a mode',
                               font=('FixedSys', 25, 'underline', 'bold'))

        self.b_default = tk.Button(self.window,
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

        self.b_default_hint = tk.Button(self.window,
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

        self.b_timed = tk.Button(self.window,
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

        self.b_timed_hint = tk.Button(self.window,
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

        self.b_vanish = tk.Button(self.window,
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

        self.b_vanish_hint = tk.Button(self.window,
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

        self.b_snake = tk.Button(self.window,
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

        self.b_snake_hint = tk.Button(self.window,
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

        self.non_mode_frame = tk.Frame(self.window, background='Black', width=25)

        self.b_back = tk.Button(self.non_mode_frame,
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

        self.b_settings = tk.Button(self.non_mode_frame,
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
        self.window.config(background='Black')
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

    def to_gamemenu(self, mode: int):
        for widget in self.window.winfo_children():
            widget.destroy()

        GameMenu(self.window, self.board_len, self.board_zoom, self.colors, mode, self.ai_type)

    def to_gamemenu_t(self, mode: int):
        for widget in self.window.winfo_children():
            widget.destroy()

        GameMenuT(self.window, self.board_len, self.board_zoom, self.colors, mode, self.ai_type)

    def to_gamemenu_v(self, mode: int):
        for widget in self.window.winfo_children():
            widget.destroy()

        GameMenuV(self.window, self.board_len, self.board_zoom, self.colors, mode, self.ai_type)

    def to_gamemenu_s(self, mode: int):
        for widget in self.window.winfo_children():
            widget.destroy()

        GameMenuS(self.window, self.board_len, self.board_zoom, self.colors, mode, self.ai_type)

    def to_mainmenu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        MainMenu(self.window, self.board_len.get(), self.board_zoom.get(), self.colors)

    def to_settings(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        ColMenu(self.window, self.board_len, self.board_zoom, self.colors, self.mode, self.ai_type)


class ColMenu:
    """
    :ivar window, board_len, board_zoom, colors, mode: same as SubMenu.
    :ivar col_frames: list containing the LabelFrame for general features, X features, and O features.
    :ivar col_entries: list containing 3 dicts: list[0] stores entries for general features; list[1] stores entries for X features; list[2] stores entries for O features.
    """

    def __init__(self, window, board_len, board_zoom, colors: dict, mode: int, ai_type):
        self.window = window
        self.board_len = board_len
        self.win_len = ttt.set_win_len(self.board_len.get())
        self.board_zoom = board_zoom
        self.colors = colors
        self.ai_type = ai_type
        self.mode = mode

        self.title = tk.Button(self.window,
                               state='disabled',
                               takefocus=False,
                               borderwidth=0,
                               background='Black',
                               disabledforeground='Sea Green1',
                               text='Settings',
                               font=('FixedSys', 25, 'underline', 'bold'))
        self.col_frames = [
            tk.LabelFrame(self.window,
                          text='General',
                          font=('FixedSys', 20, 'bold'),
                          foreground='Sea Green1',
                          background='Black',
                          borderwidth=3,
                          relief='ridge',
                          takefocus=False),
            tk.LabelFrame(self.window,
                          text='X colors',
                          font=('FixedSys', 20, 'bold'),
                          foreground='Sea Green1',
                          background='Black',
                          borderwidth=3,
                          relief='ridge',
                          takefocus=False),
            tk.LabelFrame(self.window,
                          text='O colors',
                          font=('FixedSys', 20, 'bold'),
                          foreground='Sea Green1',
                          background='Black',
                          borderwidth=3,
                          relief='ridge',
                          takefocus=False)
        ]

        self.b_exit = tk.Button(self.window,
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

        self.col_frames[1].grid(row=0, column=1, pady=(10, 5))
        self.col_frames[2].grid(row=0, column=2, pady=(10, 5))
        self.col_frames[0].grid(row=1, column=1, columnspan=2, pady=5)
        self.b_exit.grid(row=2, column=1, columnspan=2, pady=10)

        self.col_entries = [{}, {}, {}]

        for plyr, feats in enumerate(self.colors):  # plyr = general, X, O
            for row, (feat, color) in enumerate(feats.items()):
                col_label = tk.Label(
                    self.col_frames[plyr],
                    text=feat,
                    font=('FixedSys', 15),
                    foreground='Sea Green1',
                    background='Black',
                    takefocus=False)
                col_entry = tk.Entry(
                    self.col_frames[plyr],
                    textvariable=tk.StringVar(value=color),
                    borderwidth=1,
                    font=('FixedSys', 15),
                    cursor='xterm',
                    foreground='Black',
                    background=color)

                col_label.grid(row=row, column=0, padx=10)
                col_entry.grid(row=row, column=1)

                # make the key release event update bg of textbox
                col_entry.bind('<KeyRelease>', lambda event, _plyr=plyr, _feat=feat: self.update_col(_plyr, _feat))
                self.col_entries[plyr][feat] = col_entry

    def update_col(self, plyr: int, feat: str):
        try:
            # try to set the background color of the text widget
            self.col_entries[plyr][feat].config(bg=self.col_entries[plyr][feat].get())

        except tk.TclError:
            # if the color is not valid
            pass

    def to_submenu(self):
        # update self.color with new colors
        for plyr, feats in enumerate(self.col_entries):
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

            SubMenu(self.window, self.board_len, self.board_zoom, self.colors, self.mode, self.ai_type)


class GameMenu:
    """
    :ivar window, board_len, board_zoom, colors, mode: same as SubMenu.
    :ivar win_len: how many X in a row/column/diagonal to win.
    :ivar plyr: player playing in the current turn. 1 = X; 2 = O.
    :ivar main_board: base10 int containing the encoded form of the current board. To decode, convert to base3.
    :ivar simmable_inds: list containing the 12 indexes PC is allowed to simulate.
    :ivar filled_inds: list containing the indexes that are filled on main_board, in chronological order. Left element = earlier; right element = later.
    :ivar board_buttons: list containing all the buttons that represent buttons on the GUI.
    :ivar is_debugging: show/hide the debugger.
    """

    def __init__(self, window, board_len, board_zoom, colors: dict, mode: int, ai_type):
        self.window = window
        self.board_len = board_len
        ttt.set_three_pow(self.board_len.get())  # initialize universal var three_pow in TIC_TAC_TOE_func
        self.win_len = ttt.set_win_len(self.board_len.get())
        self.board_zoom = board_zoom
        self.mode = mode
        self.ai_type = ai_type
        self.colors = colors

        self.plyr = 1
        self.main_board = 0
        self.simmable_inds = []
        self.filled_inds = []
        self.board_buttons = []
        self.is_debugging = tk.BooleanVar(value=False)

        self.settings_frame = tk.Frame(self.window, background=self.colors[0]['background'])
        self.board_frame = tk.Frame(self.window, background=self.colors[0]['background'])
        self.turn_hint = [0,
                          tk.Label(  # ind 1 = X's turn_hint
                              self.board_frame,
                              text='X turn',
                              font=('Helvetica', self.board_zoom.get() * 2, 'bold'),
                              foreground=self.colors[1]['symbol'],
                              background=self.colors[0]['foreground'],
                              highlightbackground=self.colors[0]['foreground'],
                              width=13,
                              borderwidth=5,
                              relief='ridge',
                              takefocus=False),
                          tk.Label(  # ind 2 = O's turn_hint
                              self.board_frame,
                              text='O turn',
                              font=('Helvetica', self.board_zoom.get() * 2, 'bold'),
                              foreground=self.colors[2]['symbol'],
                              background=self.colors[0]['foreground'],
                              width=13,
                              borderwidth=5,
                              relief='ridge',
                              takefocus=False)
                          ]

        self.board_canvas = tk.Canvas(
            self.board_frame,
            background=self.colors[0]['background'],
            highlightthickness=0
        )
        self.board_canvas.bind('<Configure>', self.update_scrollbars)
        self.h_scrollbar = tk.Scrollbar(
            self.window,
            background=self.colors[0]['background'],
            activebackground=self.colors[0]['background'],
            troughcolor=self.colors[0]['foreground'] if self.colors[0]['foreground'] != 'SystemButtonFace' else None,
            orient='horizontal',
            command=self.board_canvas.xview
        )
        self.v_scrollbar = tk.Scrollbar(
            self.window,
            background=self.colors[0]['background'],
            activebackground=self.colors[0]['background'],
            troughcolor=self.colors[0]['foreground'] if self.colors[0]['foreground'] != 'SystemButtonFace' else None,
            orient='vertical',
            command=self.board_canvas.yview
        )
        self.board_canvas.config(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        self.button_frame = tk.Frame(self.board_canvas, background=self.colors[0]['background'], relief='groove', borderwidth=7)

        self.b_back = tk.Button(
            self.settings_frame,
            text='Back',
            background=self.colors[0]['background'],
            cursor='hand2',
            relief='groove',
            overrelief='sunken',
            command=self.to_submenu,
            width=5,
            borderwidth=5
        )
        self.replay_button = tk.Button(
            self.settings_frame,
            text='Replay',
            background=self.colors[0]['background'],
            cursor='hand2',
            relief='groove',
            overrelief='sunken',
            state='disabled',
            command=self.replay,
            width=5,
            borderwidth=5
        )
        self.load_button = tk.Button(
            self.settings_frame,
            text='Load',
            background=self.colors[0]['background'],
            cursor='hand2',
            relief='groove',
            overrelief='sunken',
            command=self.ask_board,
            width=5,
            borderwidth=5
        )
        self.board_len_label = tk.Label(
            self.settings_frame,
            background=self.colors[0]['background'],
            text='\nBoard Length',
            takefocus=False
        )
        self.board_len_slider = tk.Scale(
            self.settings_frame,
            background=self.colors[0]['background'],
            activebackground=self.colors[0]['background'],
            troughcolor=self.colors[0]['foreground'] if self.colors[0]['foreground'] != 'SystemButtonFace' else None,
            highlightthickness=0,
            orient='horizontal',
            variable=self.board_len,
            length=100,
            from_=3,
            to=19,
            cursor='sb_h_double_arrow'
        )
        self.trace1 = self.board_len.trace_add('write', self.update_len)
        self.board_len_tip = tk.Label(
            self.settings_frame,
            text='Amount in a row to win: ' + str(self.win_len),
            background=self.colors[0]['background'],
            takefocus=False
        )
        self.board_zoom_label = tk.Label(
            self.settings_frame,
            text='\nZoom',
            background=self.colors[0]['background'],
            takefocus=False
        )
        self.board_zoom_slider = tk.Scale(
            self.settings_frame,
            background=self.colors[0]['background'],
            activebackground=self.colors[0]['background'],
            troughcolor=self.colors[0]['foreground'] if self.colors[0]['foreground'] != 'SystemButtonFace' else None,
            highlightthickness=0,
            orient='horizontal',
            variable=self.board_zoom,
            length=100,
            from_=4,
            to=13,
            cursor='sb_h_double_arrow'
        )
        self.trace2 = self.board_zoom.trace_add('write', self.update_zoom)
        self.pvco_checkbox = tk.Checkbutton(
            self.settings_frame,
            text='Computer starts first',
            background=self.colors[0]['background'],
            activebackground=self.colors[0]['background'],
            selectcolor=self.colors[0]['foreground'] if self.colors[0]['foreground'] != 'SystemButtonFace' else None,
            cursor='hand2',
            command=self.pvc_first
        )
        self.shayan_ai_radiobutton = tk.Radiobutton(
            self.settings_frame,
            text='Shayan\'s AI',
            background=self.colors[0]['background'],
            activebackground=self.colors[0]['background'],
            selectcolor=self.colors[0]['foreground'] if self.colors[0]['foreground'] != 'SystemButtonFace' else None,
            cursor='hand2',
            variable=self.ai_type,
            value=0
        )
        self.czy_ai_radiobutton = tk.Radiobutton(
            self.settings_frame,
            text='CZY\'s AI',
            background=self.colors[0]['background'],
            activebackground=self.colors[0]['background'],
            selectcolor=self.colors[0]['foreground'] if self.colors[0]['foreground'] != 'SystemButtonFace' else None,
            cursor='hand2',
            variable=self.ai_type,
            value=1
        )
        self.debug_checkbox = tk.Checkbutton(
            self.settings_frame,
            text='Show debugging data (will\nimpact performance)',
            background=self.colors[0]['background'],
            activebackground=self.colors[0]['background'],
            selectcolor=self.colors[0]['foreground'] if self.colors[0]['foreground'] != 'SystemButtonFace' else None,
            cursor='hand2',
            variable=self.is_debugging,
            command=self.toggle_debugger
        )
        self.debugger = tk.Text(
            self.settings_frame,
            wrap='none',
            height=15,
            width=27
        )
        self.debugger.bind('<Key>', lambda e: None if e.keysym in ('Up', 'Down', 'Left', 'Right') else 'break')  # disable all user inputs in debugger except arrow keys
        self.debugger.bind('<Control-c>', lambda e: self.debugger.event_generate('<<Copy>>'))  # explicitly enable copy
        self.debugger.bind('<Control-a>', lambda e: self.debugger.event_generate('<<SelectAll>>'))  # explicitly enable select all

        # set the GameMenu window to the correct resolution
        self.window.geometry('')
        self.window.config(background=self.colors[0]['background'])
        self.settings_frame.pack(side='left', expand=False, fill='y')
        self.settings_frame.grid_rowconfigure(11, weight=1)  # ensures debugger's row (row 11) can expand
        self.board_frame.pack(side='left', expand=True, fill='none')

        # configure row and column weights to divide the vertical and horizontal space evenly
        self.board_frame.grid_rowconfigure(2, weight=1)
        self.board_frame.grid_columnconfigure(0, weight=1)
        self.board_frame.grid_columnconfigure(1, weight=1)

        self.turn_hint[1].grid(row=0, column=0, columnspan=2, pady=(5, 0))
        self.turn_hint[2].grid(row=1, column=0, columnspan=2, pady=(0, 5))
        self.board_canvas.grid(row=2, column=0, columnspan=2, sticky='nsew')
        self.button_frame_id = self.board_canvas.create_window(
            (0, 0),
            window=self.button_frame,
            anchor='nw')

        self.b_back.grid(row=1, column=0, pady=(0, 15))
        self.replay_button.grid(row=1, column=1, pady=(0, 15))
        self.load_button.grid(row=1, column=2, pady=(0, 15), sticky='w')
        self.board_len_label.grid(row=4, column=1, sticky='e')
        self.board_len_slider.grid(row=4, column=2, padx=(0, 5))
        self.board_len_tip.grid(columnspan=2, row=5, column=1)
        self.board_zoom_label.grid(row=6, column=1, sticky='e')
        self.board_zoom_slider.grid(row=6, column=2, padx=(0, 5), pady=(0, 8))
        if self.mode == 0:
            self.pvco_checkbox.grid(columnspan=2, row=7, column=1, pady=(0, 5))
            self.shayan_ai_radiobutton.grid(columnspan=1, row=8, column=1, pady=(0, 5))
            self.czy_ai_radiobutton.grid(columnspan=1, row=8, column=2, pady=(0, 5))
        self.debug_checkbox.grid(columnspan=2, row=10, column=1)

        # initialize the button_frame and buttons
        self.update_buttonframe()
        # rebinds the close window (X) ind_button in the top right corner
        self.window.protocol('WM_DELETE_WINDOW', self.to_submenu)

    def ask_board(self):
        def load_board(event=None):
            try:
                if len(self.filled_inds) == 0 or messagebox.askyesno('Confirmation',
                                                                     'Are you sure you want to load?\n\nYou will loose all your progress.'):  # if board is empty: continue; else ask user

                    # try to convert the board_entry to int
                    self.main_board = int(board_entry.get())
                    self.debugger.insert('end', f'Base10 board:  {self.main_board}\n\n')
                    self.debugger.see(tk.END)
                    self.filled_inds = []  # clear filled_inds but DO NOT reassign as filled filled_inds skips lock_settings()
                    self.update_buttonframe()

            except ValueError:
                # if the board_entry is not int
                messagebox.askretrycancel('Warning', 'Please enter an integer!')

            dialogue.destroy()

        dialogue = tk.Toplevel(
            self.window,
            background=self.colors[0]['background']
        )

        board_label = tk.Label(
            dialogue,
            text='Board in base10',
            background=self.colors[0]['background'],
            takefocus=False
        )
        board_entry = tk.Entry(
            dialogue,
            cursor='xterm',
            width=30
        )
        board_entry.bind('<Return>', load_board)

        submit_button = tk.Button(
            dialogue,
            text='Submit',
            background=self.colors[0]['foreground'],
            cursor='hand2',
            relief='groove',
            overrelief='sunken',
            width=10,
            borderwidth=3,
            command=load_board
        )

        board_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 0), sticky='e')
        board_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 0))
        submit_button.grid(row=1, columnspan=2, pady=5)
        dialogue.title('Load')
        dialogue.resizable(False, False)
        board_entry.focus_force()

    def update_buttonframe(self):
        """
        1. If board_len increased, create new buttons to match the new board length, but DO NOT place yet. If the board_len decreased, destroy extra buttons.

        2. Update remaining and newly-created buttons' position, color, text, and state.

        3. Determine if more cells belongs to player X or O (in case of a loaded board). The player who owns lesser cells starts first.
        """
        max_ind = self.board_len.get() ** 2
        font_style = ('Helvetica', self.board_zoom.get() * 4, 'bold' if self.board_zoom.get() > 4 else 'normal')  # if font was bold when board_zoom == 4: button is not square

        # create new buttons if board_len increased
        while len(self.board_buttons) < max_ind:
            self.board_buttons.append(
                tk.Button(
                    self.button_frame,
                    font=font_style,
                    foreground='gray',
                    background=self.colors[0]['foreground'],
                    cursor='plus',
                    command=lambda _=len(self.board_buttons): self.update_ind(_),
                    width=3,
                    borderwidth=5
                )
            )

        # destroy extra buttons if board_len decreased
        for button in self.board_buttons[max_ind:]:
            button.destroy()
        self.board_buttons = self.board_buttons[:max_ind]

        # update remaining and newly-created buttons
        plyr_balance = 0  # track which player owns more cells (in case of a loaded board)

        for ind, button in enumerate(self.board_buttons):
            button.grid(row=ind // self.board_len.get(), column=ind % self.board_len.get())  # reposition button

            plyr = ttt.get_symbol(self.main_board, ind)
            if plyr != 0:  # if cell is not empty
                plyr_balance += plyr * 2 - 3  # if plyr = X (1): count-1; if plyr = O (2): count+1
                button.config(text=ttt.convert_symbol(plyr),
                              disabledforeground=self.colors[plyr]['symbol'],
                              state='disabled')

            elif self.is_debugging.get():  # if cell is empty but debugger is on
                button.config(text=ind, state='normal')

            else:  # if cell is empty and debugger is off
                button.config(text='', state='normal')

        self.board_buttons = self.board_buttons[:max_ind]  # slice off the extra buttons

        if plyr_balance >= 0:  # if there are more O than X: X starts first
            self.plyr = 1
        else:  # if there are more X than O or equal numbers: O starts first
            self.plyr = 2

        # enable first player's indicator
        self.turn_hint[self.plyr].config(foreground=self.colors[self.plyr]['symbol'], background=self.colors[0]['foreground'], relief='ridge')
        # disable other player's indicator
        self.turn_hint[ttt.opp(self.plyr)].config(foreground='SystemDisabledText', background=self.colors[0]['background'], relief='flat')

    def toggle_debugger(self):
        if self.is_debugging.get() is True:
            self.debugger.grid(columnspan=3, row=11, column=0, pady=(0, 10), sticky='ns')

            for ind, button in enumerate(self.board_buttons):  # DO NOT use set.difference(filled_inds) as filled_inds is cleared when game ends
                if ttt.get_symbol(self.main_board, ind) == 0:
                    button.config(text=ind)

                    if ind in self.simmable_inds:
                        button.config(background=self.colors[0]['simmable_inds'])

        else:
            self.debugger.grid_forget()

            for ind, button in enumerate(self.board_buttons):  # DO NOT use set.difference(filled_inds) as filled_inds is cleared when game ends
                if ttt.get_symbol(self.main_board, ind) == 0:
                    button.config(text='', background=self.colors[0]['foreground'])

        self.window.update_idletasks()  # refresh GUI

    def update_scrollbars(self, *args):
        """
        1. Resize board_canvas to the size of button_frame.
        2. Update the scrollregion to match the new button_frame size.
        3. Show/hide scrollbars based on whether the new canvas size is smaller/larger than the button_frame.
        """
        bbox = self.board_canvas.bbox('all')  # bbox = x1, y1, x2, y2. bbox size is the same as button_frame size

        # update canvas width and height to bbox width and height +7 padding
        self.board_canvas.config(width=bbox[2] - bbox[0] + 7, height=bbox[3] - bbox[1] + 7)

        # update scrollregion
        self.board_canvas.config(scrollregion=bbox)

        if bbox[2] > self.board_canvas.winfo_width():  # if button_frame size overflows horizontally
            self.h_scrollbar.pack(side='bottom', fill='x', before=self.board_frame)  # show h_scrollbar. Pack order of h_scrollbar must be before board_frame.
        else:
            self.h_scrollbar.pack_forget()

        if bbox[3] > self.board_canvas.winfo_height():  # if button_frame size overflows horizontally
            self.v_scrollbar.pack(side='right', fill='y', before=self.board_frame)  # show v_scrollbar. Pack order of v_scrollbar must be before board_frame.
        else:
            self.v_scrollbar.pack_forget()

    def update_len(self, *args):
        # assign new three_pow and win_len
        ttt.set_three_pow(self.board_len.get())
        self.win_len = ttt.set_win_len(self.board_len.get())

        # update position of buttons and window size at frontend
        self.update_buttonframe()
        self.board_len_tip.config(text='Amount in a row to win: ' + str(self.win_len))
        self.window.update_idletasks()
        self.update_scrollbars()

    def update_zoom(self, *args):
        # update the position of the turn indicator and the scale of the buttons
        font_style = ('Helvetica', self.board_zoom.get() * 4, 'bold' if self.board_zoom.get() > 4 else 'normal')  # if font was bold when board_zoom == 4: button is not square

        for button in self.board_buttons:
            button.config(font=font_style)

        self.turn_hint[1].config(font=('Helvetica', self.board_zoom.get() * 2, 'bold'))
        self.turn_hint[2].config(font=('Helvetica', self.board_zoom.get() * 2, 'bold'))

    def lock_settings(self):
        self.board_len_slider.config(state='disabled')
        self.board_len_label.config(state='disabled')
        self.replay_button.config(state='normal')
        self.pvco_checkbox.config(state='disabled')

        self.turn_hint[self.plyr].config(foreground='SystemDisabledText', background=self.colors[0]['background'], relief='flat')
        self.turn_hint[ttt.opp(self.plyr)].config(foreground=self.colors[ttt.opp(self.plyr)]['symbol'], background=self.colors[0]['foreground'], relief='ridge')

    def pvc_first(self):
        self.plyr = 2
        self.lock_settings()
        self.update_ind_pc()

    def update_ind(self, ind: int):
        self.filled_inds.append(ind)
        self.update_ind_plyr()

        if self.mode == 1:

            if len(self.filled_inds) > 1:  # if both players alr moved once and there is no outcome
                self.check_winner_pvp()

            else:  # if this is the first move
                self.lock_settings()

                self.plyr = ttt.opp(self.plyr)

        elif self.mode == 0:

            if len(self.filled_inds) > 1:
                for ind in self.simmable_inds:
                    self.board_buttons[ind].config(background=self.colors[0]['foreground'])  # unhighlight simmable_inds and pc move from the previous turn

                if self.check_winner_pvc(self.plyr) is False:
                    self.update_ind_pc()

                    if len(self.filled_inds) > 1:  # if PC did not resign
                        self.check_winner_pvc(ttt.opp(self.plyr))

            else:
                self.lock_settings()

                self.update_ind_pc()
                self.check_winner_pvc(ttt.opp(self.plyr))

    def update_ind_pc(self):
        # initialize pc_move
        if self.filled_inds:  # if PC starts second or pre-filled board is loaded

            self.simmable_inds = ttt.prune(self.main_board, self.board_len.get(), self.plyr, self.filled_inds[-1])
            self.debugger.insert(tk.END, 'Simulatable indexes:\n' + str(self.simmable_inds) + '\n')
            self.debugger.see(tk.END)
            self.toggle_debugger()  # highlight new simmable_inds

            if self.ai_type.get() == 0:  # if using Shayan's AI
                pc_move = ttt.pc_input(ttt.opp(self.plyr), self.main_board, self.board_len.get(), self.win_len, self.simmable_inds, self.is_debugging.get())
            else:  # if using CZY's AI
                pc_move = ttt.pc_input_v1(ttt.opp(self.plyr), self.main_board, self.board_len.get(), self.win_len, self.simmable_inds, self.is_debugging.get())

            if pc_move is None:
                self.stop_game()
                messagebox.showinfo('Outcome', 'Computer resigns.\n\nPC: "I have already computed my inevitable fate ..."')
                return

        else:  # if PC starts first
            pc_move = random.randint(0, self.board_len.get() ** 2 - 1)
            self.simmable_inds = [pc_move]  # allow toggle_debugger() to unhighlight this move next turn

        self.filled_inds.append(pc_move)
        self.main_board += ttt.opp(self.plyr) * ttt.three_pow[pc_move]
        self.board_buttons[pc_move].config(text=ttt.convert_symbol(ttt.opp(self.plyr)),
                                           disabledforeground=self.colors[ttt.opp(self.plyr)]['symbol'], background=self.colors[0]['pc_move'], state='disabled')

        self.debugger.insert('end', f'PC\'s move:  {pc_move}\n')
        self.debugger.insert('end', f'Base10 board:  {self.main_board}\n\n')
        self.debugger.see(tk.END)

    def check_winner_pvc(self, cur_plyr: int) -> bool:
        """
        Check winner after each turn in PVC mode. Executes only after both players already moved once and also contains special functions in Timed and Vanishing modes.
        :return: whether the game has an outcome
        """
        formation = ttt.plyr_win_formation(self.main_board, self.board_len.get(), self.win_len, cur_plyr, self.filled_inds[-1])
        if formation is not None:
            self.stop_game()

            if cur_plyr == self.plyr:  # if someone won and the current turn is human
                if messagebox.askyesno('Outcome', f'You win {formation}!\n\nPC: "NOT MY DIGNITY! LET US HAVE ANOTHER DUEL!"') is True:
                    self.replay()
                return True

            else:  # if someone won and the current turn is pc
                if messagebox.askyesno('Outcome', f'Computer wins {formation}!\n\nPC: "Shouldn\'t humans be smarter?"') is True:
                    self.replay()
                return True

        else:
            if len(self.filled_inds) == self.board_len.get() ** 2:  # if no one win and the whole board is filled
                self.stop_game()
                if messagebox.askyesno('Outcome', 'Ended in tie.\n\nPC: "You\'ll never win ... not satisfied? Replay!"') is True:
                    self.replay()
                return True

            else:  # if no one win and the whole board is not filled
                self.turn_hint[cur_plyr].config(foreground='SystemDisabledText', background=self.colors[0]['background'], relief='flat')
                self.turn_hint[ttt.opp(cur_plyr)].config(foreground=self.colors[ttt.opp(cur_plyr)]['symbol'], background=self.colors[0]['foreground'], relief='ridge')
                return False

    def update_ind_plyr(self):
        # update backend board
        self.main_board += self.plyr * ttt.three_pow[self.filled_inds[-1]]

        # update frontend board
        self.board_buttons[self.filled_inds[-1]].config(text=ttt.convert_symbol(self.plyr),
                                                        disabledforeground=self.colors[self.plyr]['symbol'],
                                                        state='disabled')

        self.debugger.insert(tk.END, f'Player {self.plyr}\'s move:  {self.filled_inds[-1]}\n')
        self.debugger.insert('end', f'Base10 board:  {self.main_board}\n\n')
        self.debugger.see(tk.END)

    def check_winner_pvp(self) -> bool:
        """
        Check winner after each turn in PVP mode. Executes only after both players already moved once and also contains special functions in Timed and Vanishing modes.
        :return: whether the game has an outcome
        """
        formation = ttt.plyr_win_formation(self.main_board, self.board_len.get(), self.win_len, self.plyr, self.filled_inds[-1])
        if formation is not None:
            self.stop_game()
            messagebox.showinfo('Outcome', f'Player \'{ttt.convert_symbol(self.plyr)}\' wins {formation}!')
            return True

        else:
            if len(self.filled_inds) == self.board_len.get() ** 2:  # if no one win and the whole board is filled
                self.stop_game()
                messagebox.showinfo('Outcome', 'Ended in a tie.')
                return True

            else:  # if no one win and the whole board is not filled
                self.turn_hint[self.plyr].config(foreground='SystemDisabledText', background=self.colors[0]['background'], relief='flat')
                self.plyr = ttt.opp(self.plyr)
                self.turn_hint[self.plyr].config(foreground=self.colors[self.plyr]['symbol'], background=self.colors[0]['foreground'], relief='ridge')
                return False

    def stop_game(self):
        self.filled_inds = []
        for button in self.board_buttons:
            button.config(state='disabled')

    def to_submenu(self):
        if messagebox.askyesno('Confirmation', 'Are you sure you want to quit?\n\nYou will loose all your progress.'):
            self.filled_inds = []
            self.board_len.trace_remove('write', self.trace1)
            self.board_len.trace_remove('write', self.trace2)
            for widget in self.window.winfo_children():
                widget.destroy()

            SubMenu(self.window, self.board_len, self.board_zoom, self.colors, self.mode, self.ai_type)

    def replay(self):
        if messagebox.askyesno('Confirmation',
                               'Are you sure you want to restart?\n\nYou will loose all your progress.'):
            self.filled_inds = []
            self.board_len.trace_remove('write', self.trace1)
            self.board_len.trace_remove('write', self.trace2)
            for widget in self.window.winfo_children():
                widget.destroy()

            GameMenu(self.window, self.board_len, self.board_zoom, self.colors, self.mode, self.ai_type)


class GameMenuT(GameMenu):
    """
    :ivar window, board_len, board_zoom, colors, mode: same as SubMenu.
    :ivar remain_time: dict containing how much time does each player still have.
    :ivar hint_scale: used to animate the inflate of timer at the start of each turn.
    """

    # noinspection PyTypeChecker
    def __init__(self, window, board_len, board_zoom, colors: dict, mode: int, ai_type):
        super().__init__(window, board_len, board_zoom, colors, mode, ai_type)
        self.remain_time = [0,
                            tk.StringVar(value='10'),  # ind 1 = X's remain_time
                            tk.StringVar(value='10')  # ind 2 = O's remain_time
                            ]
        self.hint_scale = 0
        self.next_countdown = None

        # destroy the original X's turn_hint and O's turn_hint created by superclass
        self.turn_hint[1].destroy()
        self.turn_hint[2].destroy()
        self.turn_hint = [0,
                          tk.LabelFrame(
                              self.board_frame,
                              text='X turn',
                              font=('Helvetica', self.board_zoom.get() * 2 + 1, 'bold'),
                              foreground=self.colors[1]['symbol'],
                              borderwidth=5,
                              relief='ridge',
                              takefocus=False),
                          tk.LabelFrame(
                              self.board_frame,
                              text='O turn',
                              font=('Helvetica', self.board_zoom.get() * 2 + 1, 'bold'),
                              foreground=self.colors[2]['symbol'],
                              borderwidth=5,
                              relief='ridge',
                              takefocus=False)
                          ]
        self.time_entry = [0,
                           tk.Entry(  # ind 1 = X's time_entry
                               self.turn_hint[1],
                               width=4,
                               borderwidth=1,
                               font=('Courier', self.board_zoom.get() * 3 + 2, 'bold'),
                               foreground=self.colors[1]['symbol'],
                               disabledforeground=self.colors[1]['symbol'],
                               disabledbackground='white',
                               justify='center',
                               textvariable=self.remain_time[1]),
                           tk.Entry(  # ind 2 = O's remain_time
                               self.turn_hint[2],
                               width=4,
                               borderwidth=1,
                               font=('Courier', self.board_zoom.get() * 3 + 2, 'bold'),
                               foreground=self.colors[2]['symbol'],
                               disabledforeground=self.colors[2]['symbol'],
                               disabledbackground='white',
                               justify='center',
                               textvariable=self.remain_time[2])
                           ]
        self.trace3 = self.remain_time[1].trace_add('write', lambda *args: self.validate_timer(1, *args))
        self.trace4 = self.remain_time[2].trace_add('write', lambda *args: self.validate_timer(2, *args))

        self.turn_hint[1].grid(row=0, column=0, sticky="e")  # stick to the right edge of column 1
        self.turn_hint[2].grid(row=0, column=1, sticky="w")  # stick to the left edge of column 2
        self.time_entry[1].pack()
        self.time_entry[2].pack()

    def update_zoom(self, *args):
        super().update_zoom()

        self.time_entry[1].config(font=('Helvetica', self.board_zoom.get() * 3 + 2, 'bold'))
        self.time_entry[2].config(font=('Helvetica', self.board_zoom.get() * 3 + 2, 'bold'))

    def lock_settings(self):
        super().lock_settings()

        self.time_entry[1].config(state='disabled')
        self.time_entry[2].config(state='disabled')

        # disable X's timer
        self.time_entry[1].config(relief='flat', disabledforeground='SystemDisabledText',
                                  disabledbackground=self.colors[0]['foreground'],
                                  font=('Courier', self.board_zoom.get() * 3 + 2, 'bold'))

        # enable O's timer
        self.time_entry[2].config(relief='sunken', disabledforeground=self.colors[2]['symbol'], disabledbackground='white')

        self.countdown()

    def validate_timer(self, plyr: int, *args):
        try:
            # try to convert the remain time to float
            float(self.remain_time[plyr].get())

        except ValueError:
            # if the remain time is not float: show a messagebox and reset the value
            messagebox.askretrycancel('Warning', f'Please enter a decimal number for {ttt.convert_symbol(plyr)}!')
            self.remain_time[plyr].set('10')

    def countdown(self):
        remain_time = float(self.remain_time[self.plyr].get())

        if remain_time > 0.0:
            # animate inflate of the current plyr's timer
            self.hint_scale = min(self.hint_scale + 2, 4)
            self.time_entry[self.plyr].config(font=('Courier', self.board_zoom.get() * 3 + 2 + self.hint_scale, 'bold'))

            # decrease the remain_time value by 0.1 every 100ms and display only 1 deci point using round().
            # DO NOT decrease by 1 every 1000ms (1sec) as the timer slows down the whole app.
            self.remain_time[self.plyr].set(str(round(remain_time - 0.1, 1)))
            self.next_countdown = self.window.after(100, self.countdown)

            self.window.update_idletasks()

            # if X has under 5 secs left: flash the timer
            if remain_time < 5.0 and remain_time % 1 < 0.4:
                self.time_entry[self.plyr].config(relief='sunken', disabledbackground='white')
            elif remain_time < 5.0 and remain_time % 1 >= 0.4:
                self.time_entry[self.plyr].config(relief='groove', disabledbackground='yellow')

        # if player runs out of time: opponent wins and stop all recursions.
        else:
            messagebox.showinfo('Outcome', f"Time's up! Player {ttt.convert_symbol(ttt.opp(self.plyr))} wins!")
            self.stop_game()
            return None

    def check_winner_pvc(self, cur_plyr: int) -> bool:
        """
        Modified to include disabling timer entry, switching timer and adding bonus time.
        """
        self.hint_scale = 0  # reset inflate animation

        if super().check_winner_pvc(cur_plyr) is False:
            # disable and reset font size of current plyr's timer
            self.time_entry[cur_plyr].config(relief='flat', disabledforeground='SystemDisabledText',
                                             disabledbackground=self.colors[0]['foreground'],
                                             font=('Courier', self.board_zoom.get() * 3 + 2, 'bold'))
            # enable next plyr's timer
            self.time_entry[ttt.opp(cur_plyr)].config(relief='sunken', disabledforeground=self.colors[ttt.opp(cur_plyr)]['symbol'], disabledbackground='white')

            self.remain_time[cur_plyr].set(str(float(self.remain_time[cur_plyr].get()) + 1))
            return False

    def check_winner_pvp(self) -> bool:
        """
        Modified to include disabling timer entry, switching timer and adding bonus time.
        """
        self.hint_scale = 0  # reset inflate animation

        if super().check_winner_pvp() is False:  # changes self.plyr to next plyr
            # disable and reset font size of current plyr's timer
            self.time_entry[ttt.opp(self.plyr)].config(relief='flat', disabledforeground='SystemDisabledText',
                                                       disabledbackground=self.colors[0]['foreground'],
                                                       font=('Courier', self.board_zoom.get() * 3 + 2, 'bold'))
            # enable next plyr's timer
            self.time_entry[self.plyr].config(relief='sunken', disabledforeground=self.colors[self.plyr]['symbol'], disabledbackground='white')

            # current plyr gets bonus time
            self.remain_time[ttt.opp(self.plyr)].set(str(float(self.remain_time[ttt.opp(self.plyr)].get()) + 1))
            return False

    def stop_game(self):
        super().stop_game()

        # stop player's countdown and timer flash
        self.window.after_cancel(self.next_countdown)

    def to_submenu(self):
        if messagebox.askyesno('Confirmation', 'Are you sure you want to quit?\n\nYou will loose all your progress.'):
            self.filled_inds = []
            self.board_len.trace_remove('write', self.trace1)
            self.board_len.trace_remove('write', self.trace2)
            self.remain_time[1].trace_remove('write', self.trace3)
            self.remain_time[2].trace_remove('write', self.trace4)

            # stops the next queued countdown()
            if self.next_countdown:
                self.window.after_cancel(self.next_countdown)
            for widget in self.window.winfo_children():
                widget.destroy()

            SubMenu(self.window, self.board_len, self.board_zoom, self.colors, self.mode, self.ai_type)

    def replay(self):
        if messagebox.askyesno('Confirmation',
                               'Are you sure you want to restart?\n\nYou will loose all your progress.'):
            self.filled_inds = []
            self.board_len.trace_remove('write', self.trace1)
            self.board_len.trace_remove('write', self.trace2)
            self.remain_time[1].trace_remove('write', self.trace3)
            self.remain_time[2].trace_remove('write', self.trace4)

            # stops the next queued countdown()
            self.window.after_cancel(self.next_countdown)
            for widget in self.window.winfo_children():
                widget.destroy()

            GameMenuT(self.window, self.board_len, self.board_zoom, self.colors, self.mode, self.ai_type)


class GameMenuV(GameMenu):
    """
    :ivar window, board_len, board_zoom, colors, mode: same as SubMenu.
    :ivar remain_steps: how many steps into the future will an X/O last.
    :ivar show_nxt_vanish_move: show/hide which move is going to vanish in the next turn.
    """

    def __init__(self, window, board_len, board_zoom, colors: dict, mode: int, ai_type):
        super().__init__(window, board_len, board_zoom, colors, mode, ai_type)
        self.remain_steps = tk.IntVar()
        self.show_nxt_vanish_move = tk.BooleanVar(value=False)

        self.remain_stps_label = tk.Label(
            self.settings_frame,
            text='\nRemain for',
            takefocus=False
        )
        self.remain_count_slider = tk.Scale(
            self.settings_frame,
            background=self.colors[0]['background'],
            activebackground=self.colors[0]['background'],
            troughcolor=self.colors[0]['foreground'] if self.colors[0]['foreground'] != 'SystemButtonFace' else None,
            orient='horizontal',
            variable=self.remain_steps,
            length=100,
            from_=self.win_len,
            to=self.win_len * 2,
            cursor='sb_h_double_arrow'
        )
        self.nxt_vanish_checkbox = tk.Checkbutton(
            self.settings_frame,
            text='Show next vanishing move',
            background=self.colors[0]['background'],
            activebackground=self.colors[0]['background'],
            selectcolor=self.colors[0]['foreground'] if self.colors[0]['foreground'] != 'SystemButtonFace' else None,
            cursor='hand2',
            variable=self.show_nxt_vanish_move,
            command=self.del_moves
        )

        self.remain_stps_label.grid(row=2, column=1)
        self.remain_count_slider.grid(row=2, column=2)
        self.nxt_vanish_checkbox.grid(columnspan=2, row=3, column=1)

    def del_moves(self):
        # if half of the total num of moves by X + O > remain_steps: X's moves start to vanish.
        if len(self.filled_inds) / 2 > self.remain_steps.get():
            self.debugger.insert('end', f'Vanish order:\n{self.filled_inds}')  # debugger.see(END) not needed here

            vanish_ind = self.filled_inds.pop(0)

            self.main_board -= self.plyr * ttt.three_pow[vanish_ind]
            self.board_buttons[vanish_ind].config(text='', background=self.colors[0]['foreground'], state='normal')

        # if half of the total num of moves by X + O is one less before vanishing begins: tint the 2 oldest moves about to vanish.
        if self.show_nxt_vanish_move.get() is True and len(self.filled_inds) / 2 >= self.remain_steps.get():
            self.board_buttons[self.filled_inds[1]].config(background=self.colors[0]['nxt_vanish_move'])
            self.board_buttons[self.filled_inds[0]].config(background=self.colors[0]['nxt_vanish_move'])

    def update_len(self, *args):
        super().update_len(*args)
        self.remain_count_slider.config(from_=self.win_len, to=self.win_len * 2)

    def check_winner_pvc(self, cur_plyr: int) -> bool:
        self.del_moves()
        return super().check_winner_pvc(cur_plyr)

    def check_winner_pvp(self) -> bool:
        self.del_moves()
        return super().check_winner_pvp()

    def replay(self):
        if messagebox.askyesno('Confirmation',
                               'Are you sure you want to restart?\n\nYou will loose all your progress.'):
            self.filled_inds = []
            self.board_len.trace_remove('write', self.trace1)
            self.board_len.trace_remove('write', self.trace2)

            for widget in self.window.winfo_children():
                widget.destroy()

            GameMenuV(self.window, self.board_len, self.board_zoom, self.colors, self.mode, self.ai_type)


class GameMenuS(GameMenu):
    """
    :ivar window, board_len, board_zoom, colors, mode: same as SubMenu.
    :ivar prev_inputs: dict containing 2 lists: one containing all the moves made by X in chronological order, the other containing O's. Leftmost element = earliest move. Rightmost element = latest move.
    """

    def __init__(self, window, board_len, board_zoom, colors: dict, mode: int, ai_type):
        super().__init__(window, board_len, board_zoom, colors, mode, ai_type)
        self.prev_inputs = [0,
                            [],
                            []
                            ]
        self.win_len = self.board_len.get()
        self.board_len_tip.config(text='Amount in a row to win: ' + str(self.win_len))

    def update_len(self, *args):
        super().update_len(*args)

        self.win_len = self.board_len.get()
        self.board_len_tip.config(text='Amount in a row to win: ' + str(self.win_len))

    def update_ind_pc(self) -> int:
        pass

    def update_ind_plyr(self):
        super().update_ind_plyr()

        self.board_buttons[self.filled_inds[-1]].config(background=self.colors[self.plyr]['snake_head'])
        if len(self.prev_inputs[self.plyr]) > 0:
            # turn the snake's previous head to body color
            self.board_buttons[self.prev_inputs[self.plyr][-1]].config(background=self.colors[self.plyr]['snake_body'])

        self.prev_inputs[self.plyr].append(self.filled_inds[-1])

    def check_winner_pvp(self) -> bool:
        """
        Modified to:
         1. give snake a new head when the old head stuck.
         2. disable the adj cells from the previous turn and enable the adj cells for the next turn.
        """
        if super().check_winner_pvp() is False:  # changes self.plyr to next player

            # setup coords (x_coord, y_coord) of 8 indexes around a center
            relative_adj = {
                (-1, -1), (0, -1), (1, -1),  # top-left, top-right
                (-1, 0), (1, 0),  # left, right
                (-1, 1), (0, 1), (1, 1)  # bottom-left, bottom-right
            }

            def get_adj(row: int, col: int) -> set:
                """
                :return: set containing the valid indexes of the adjacents around the previous input of opponent.
                """
                absolute_adj = set()

                for dir_x, dir_y in relative_adj:
                    adj_row = row + dir_y
                    adj_col = col + dir_x

                    if 0 <= adj_row < self.board_len.get() and 0 <= adj_col < self.board_len.get():
                        adj_ind = adj_row * self.board_len.get() + adj_col

                        if ttt.get_symbol(self.main_board, adj_ind) == ' ':
                            self.board_buttons[adj_ind].config(state='normal', relief='raised')
                            absolute_adj.add(adj_ind)

                if not absolute_adj:  # empty absolute_adj means next player is stuck
                    self.prev_inputs[self.plyr].pop()
                    prev_input = self.prev_inputs[self.plyr][-1]
                    absolute_adj = get_adj(prev_input // self.board_len.get(), prev_input % self.board_len.get())  # recursion for the previous-previous input

                return absolute_adj

            prev_input = self.prev_inputs[self.plyr][-1]
            absolute_adj = get_adj(prev_input // self.board_len.get(), prev_input % self.board_len.get())

            for ind in set(range(self.board_len.get() ** 2)).difference(self.filled_inds, absolute_adj):  # is empty and not in absolute_adj
                self.board_buttons[ind].config(state='disabled', relief='sunken')

            return False


ver_no = 'Tic Tac Toe v17'

window = tk.Tk()
MainMenu(window)
window.title(ver_no)

window.mainloop()
