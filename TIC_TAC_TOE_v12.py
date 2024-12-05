import random
import tkinter as tk
from tkinter import messagebox

from TIC_TAC_TOE_func import *


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
Ver 16: \n
    ''')


class MainMenu:
    """
    :ivar window: name of window that displays MainMenu.
    :ivar board_sz: length of the board.
    :ivar board_zoom: magnification of the board.
    :ivar colors: dict containing colors for different features. Sorted into: player X, player O, all.
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
                    'simmable_inds': 'Lemon Chiffon2',
                    'nxt_vanish_move0': 'Navajo White',
                    'nxt_vanish_move1': 'Antique White'
                }
            }
        else:
            self.colors = colors

        self.title_line1 = tk.Label(self.window,
                                    takefocus=False,
                                    width=500,
                                    borderwidth=0,
                                    background='Black',
                                    foreground='Sea Green1',
                                    text='=' * 999,
                                    font='TkFixedFont')
        self.title_line2 = tk.Label(self.window,
                                    takefocus=False,
                                    width=500,
                                    borderwidth=0,
                                    background='Black',
                                    foreground='Sea Green1',
                                    text='\n' + '=' * 999,
                                    font='TkFixedFont')
        self.title_label = tk.Label(self.window,
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

        self.subtitle_label = tk.Label(self.window,
                                       takefocus=False,
                                       borderwidth=0,
                                       width=500,
                                       background='Black',
                                       foreground='Sea Green1',
                                       text='',
                                       font='TkFixedFont',
                                       justify='left')
        subtitle_text = '   99% Made by CZY          3 Unprecedented Modes!          Unbeatable AI!        '

        self.b_pvc = tk.Button(self.window,
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

        self.b_pvp = tk.Button(self.window,
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
    :ivar window: name of window that displays MainMenu.
    :ivar board_sz: length of the board.
    :ivar board_zoom: magnification of the board.
    :ivar win_len: how many X in a row/column/diagonal to win.
    :ivar colors: dict containing colors for different features. Sorted into: player X, player O, all.
    :ivar mode: pvp = player versus player; pvc = player versus pc.
    """

    def __init__(self, window, board_sz, board_zoom, colors, mode: str):
        self.window = window
        self.board_sz = board_sz
        self.win_len = set_win_len(self.board_sz.get())
        self.board_zoom = board_zoom
        self.colors = colors
        self.mode = mode

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
    """
    :ivar window, board_sz, board_zoom, colors, mode: same as SubMenu.
    """

    def __init__(self, window, board_sz, board_zoom, colors, mode):
        self.window = window
        self.board_sz = board_sz
        self.win_len = set_win_len(self.board_sz.get())
        self.board_zoom = board_zoom
        self.colors = colors
        self.mode = mode

        self.title = tk.Button(self.window,
                               state='disabled',
                               takefocus=False,
                               borderwidth=0,
                               background='Black',
                               disabledforeground='Sea Green1',
                               text='Settings',
                               font=('FixedSys', 25, 'underline', 'bold'))
        self.col_frames = {
            'X': tk.LabelFrame(self.window,
                               text='X colors',
                               font=('FixedSys', 20, 'bold'),
                               foreground='Sea Green1',
                               background='Black',
                               borderwidth=3,
                               relief='ridge',
                               takefocus=False),
            'O': tk.LabelFrame(self.window,
                               text='O colors',
                               font=('FixedSys', 20, 'bold'),
                               foreground='Sea Green1',
                               background='Black',
                               borderwidth=3,
                               relief='ridge',
                               takefocus=False),
            '': tk.LabelFrame(self.window,
                              text='General',
                              font=('FixedSys', 20, 'bold'),
                              foreground='Sea Green1',
                              background='Black',
                              borderwidth=3,
                              relief='ridge',
                              takefocus=False)
        }

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
                col_label = tk.Label(
                    self.col_frames[plyr],
                    text=feat,
                    font=('FixedSys', 15),
                    foreground='Sea Green1',
                    background='Black',
                    takefocus=False)
                col_entry = tk.Entry(
                    self.col_frames[plyr],
                    textvariable=tk.StringVar(value=col),
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
    :ivar window, board_sz, board_zoom, colors, mode: same as SubMenu.
    :ivar win_len: how many X in a row/column/diagonal to win.
    :ivar plyr: player playing in the current turn.
    :ivar main_board: list containing the board on screen.
    :ivar simmable_inds: list containing the 12 indexes PC is allowed to simulate.
    :ivar filled_inds: list containing the indexes that are filled on main_board, in chronological order. Left element = earlier; right element = later.
    :ivar board_buttons: list containing all the buttons that represent buttons on the GUI.
    :ivar is_debugging: show/hide the debugger.
    """

    def __init__(self, window, board_sz, board_zoom, colors, mode: str):
        self.window = window
        self.board_sz = board_sz
        self.win_len = set_win_len(self.board_sz.get())
        self.board_zoom = board_zoom
        self.mode = mode
        self.colors = colors

        self.plyr = 'X'
        self.main_board = setup_board(self.board_sz.get())
        self.simmable_inds = []
        self.filled_inds = []
        self.board_buttons = []
        self.is_debugging = tk.BooleanVar(value=False)

        self.settings_frame = tk.Frame(self.window)
        self.board_frame = tk.Frame(self.window)
        self.turn_hint_frame = tk.Frame(self.board_frame, background='SystemButtonFace')
        self.turn_hint = {
            'X': tk.Label(
                self.turn_hint_frame,
                text='X turn',
                font=('Helvetica', self.board_zoom.get() * 2, 'bold'),
                foreground=self.colors['X']['symbol'],
                background='white',
                width=13,
                borderwidth=5,
                relief='ridge',
                takefocus=False),
            'O': tk.Label(
                self.turn_hint_frame,
                text='O turn',
                font=('Helvetica', self.board_zoom.get() * 2, 'bold'),
                foreground=self.colors['O']['symbol'],
                background='white',
                width=13,
                borderwidth=5,
                relief='ridge',
                takefocus=False)
        }
        self.b_back = tk.Button(
            self.settings_frame,
            text='Back',
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
            cursor='hand2',
            relief='groove',
            overrelief='sunken',
            state='disabled',
            command=self.replay,
            width=5,
            borderwidth=5
        )
        self.board_sz_label = tk.Label(
            self.settings_frame,
            text='\nBoard Length'
        )
        self.board_sz_slider = tk.Scale(
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
        self.board_sz_tip = tk.Label(
            self.settings_frame,
            text='Amount in a row to win: ' + str(self.win_len)
        )
        self.board_zoom_label = tk.Label(
            self.settings_frame,
            text='\nZoom'
        )
        self.board_zoom_slider = tk.Scale(
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
        self.pvco_checkbox = tk.Checkbutton(
            self.settings_frame,
            text='Computer starts first',
            height=2,
            cursor='hand2',
            command=self.pvc_first
        )
        self.debug_checkbox = tk.Checkbutton(
            self.settings_frame,
            text='Show debugging data (may\nimpact performance)',
            height=2,
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
        # rebinds the close window (X) ind_button in the top right corner
        self.window.protocol('WM_DELETE_WINDOW', self.to_submenu)

    def toggle_debugger(self):
        if self.is_debugging.get() is True:  # DO NOT use set.difference(filled_inds) as filled_inds is cleared when game ends
            self.debugger.grid(columnspan=3, row=10, column=0, sticky='ns')

            for ind, symbol in enumerate(self.main_board):
                if symbol == ' ':
                    button = self.board_buttons[ind]
                    button.config(text=ind, foreground='gray')

                    if ind in self.simmable_inds:
                        button.config(background=self.colors['']['simmable_inds'])

        else:
            self.debugger.grid_forget()

            for ind, symbol in enumerate(self.main_board):  # DO NOT use set.difference(filled_inds) as filled_inds is cleared when game ends
                if symbol == ' ':
                    self.board_buttons[ind].config(text='', background='SystemButtonFace')

        self.window.update_idletasks()  # refresh GUI

    def create_boardframe(self):
        self.board_buttons = []
        # create buttons in board_frame
        for row in range(self.board_sz.get()):
            for col in range(self.board_sz.get()):
                button_num = row * self.board_sz.get() + col
                button = tk.Button(
                    self.board_frame,
                    font=('Helvetica', self.board_zoom.get() * 4, 'bold'),
                    cursor='plus',
                    command=lambda _=button_num: self.update_ind(_),
                    width=3,
                    borderwidth=5
                )
                self.board_buttons.append(button)
                button.grid(row=row + 3, column=col + 2)

    def adjust_length(self, *args):
        # When I adjust the board length, I must delete the old buttons as I cannot change their position
        for button in self.board_buttons:
            button.destroy()

        # Generate new board and attributes with the correct dimension at backend
        self.main_board = setup_board(self.board_sz.get())
        self.win_len = set_win_len(self.board_sz.get())

        # Generate new buttons and symbol indicator at frontend
        self.create_boardframe()
        self.turn_hint_frame.grid(columnspan=self.board_sz.get())
        self.board_sz_tip.config(text='Amount in a row to win: ' + str(self.win_len))
        self.toggle_debugger()

    def adjust_zoom(self, *args):
        # Update the position of the turn indicator and the scale of the buttons.
        for ind_button in self.board_buttons:
            ind_button.config(font=('Helvetica', self.board_zoom.get() * 4, 'bold'))
        self.turn_hint['X'].config(font=('Helvetica', self.board_zoom.get() * 2, 'bold'))
        self.turn_hint['O'].config(font=('Helvetica', self.board_zoom.get() * 2, 'bold'))

    def lock_settings(self):
        self.board_sz_slider.config(state='disabled')
        self.board_sz_label.config(state='disabled')
        self.replay_button.config(state='normal')
        self.pvco_checkbox.config(state='disabled')

        # disable X's indicator
        self.turn_hint['X'].config(foreground='SystemDisabledText', background='SystemButtonFace', relief='flat')

        # enable O's indicator
        self.turn_hint['O'].config(foreground=self.colors['O']['symbol'], background='white', relief='ridge')

    def pvc_first(self):
        self.plyr = 'O'
        self.lock_settings()
        self.update_ind_pc(None)

    def update_ind(self, prev_input: int):
        self.update_ind_plyr(prev_input)

        if self.mode == 'pvp':

            if len(self.filled_inds) > 1:  # if both players alr moved once and there is no outcome
                self.check_winner_pvp(prev_input)

            else:  # if this is the first move
                self.plyr = opp(self.plyr)
                self.lock_settings()

        elif self.mode == 'pvc':

            if len(self.filled_inds) > 1:
                self.board_buttons[self.filled_inds[-2]].config(background='SystemButtonFace')  # unhighlight previous pc move
                for ind in self.simmable_inds:
                    self.board_buttons[ind].config(background='SystemButtonFace')  # unhighlight simmable_inds from the previous turn

                if self.check_winner_pvc(prev_input, self.plyr) is False:
                    self.update_ind_pc(prev_input)
                    self.check_winner_pvc(self.filled_inds[-1], opp(self.plyr))  # filled_inds[-1] is pc's latest move

            else:
                self.lock_settings()

                self.update_ind_pc(prev_input)
                self.check_winner_pvc(prev_input, opp(self.plyr))

    def update_ind_pc(self, prev_input: int | None):
        self.debugger.insert(tk.END, f'Player\'s move:  {prev_input}\n')

        # initialize pc_move
        if prev_input is not None:  # if PC start second

            self.simmable_inds = prune(self.main_board, self.board_sz.get(), self.plyr, prev_input)
            self.debugger.insert(tk.END, 'Empty indexes after prunning:\n' + str(self.simmable_inds) + '\n')
            self.toggle_debugger()  # highlight new simmable_inds

            pc_move = pc_input(opp(self.plyr), self.main_board, self.board_sz.get(), self.win_len, prev_input, self.simmable_inds, self.is_debugging.get(), self.debugger)
            if pc_move is None:
                self.stop_game()
                messagebox.showinfo('Outcome', 'Computer resigns.\n\nPC: "I have already computed my inevitable fate ..."')
                return

        else:  # if PC starts first
            pc_move = random.randint(0, self.board_sz.get() ** 2 - 1)

        self.filled_inds.append(pc_move)
        self.main_board[pc_move] = opp(self.plyr)
        self.board_buttons[pc_move].config(text=opp(self.plyr),
                                           disabledforeground=self.colors[opp(self.plyr)]['symbol'], background=self.colors['']['pc_move'], state='disabled')

        self.debugger.insert('end', f'PC\'s move:  {pc_move}\n\n')

    def check_winner_pvc(self, prev_input: int, cur_plyr: str) -> bool:
        """
        Check winner after each turn in PVC mode. Executes only after both players already moved once and also contains special functions in Timed and Vanishing modes.
        :return: whether the game has an outcome
        """
        formation = plyr_win_formation(self.main_board, self.board_sz.get(), self.win_len, cur_plyr, prev_input)
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
            if len(self.filled_inds) == self.board_sz.get() ** 2:  # if no one win and the whole board is filled
                self.stop_game()
                if messagebox.askyesno('Outcome', 'Ended in tie.\n\nPC: "You\'ll never win ... not satisfied? Replay!"') is True:
                    self.replay()
                return True

            else:  # if no one win and the whole board is not filled
                self.turn_hint[cur_plyr].config(foreground='SystemDisabledText', background='SystemButtonFace', relief='flat')
                self.turn_hint[opp(cur_plyr)].config(foreground=self.colors[opp(cur_plyr)]['symbol'], background='white', relief='ridge')
                return False

    def update_ind_plyr(self, prev_input: int):
        # update backend board
        self.main_board[prev_input] = self.plyr
        self.filled_inds.append(prev_input)

        # update frontend board
        self.board_buttons[prev_input].config(text=self.main_board[prev_input],
                                              disabledforeground=self.colors[self.plyr]['symbol'],
                                              state='disabled')

    def check_winner_pvp(self, prev_input: int) -> bool:
        """
        Check winner after each turn in PVP mode. Executes only after both players already moved once and also contains special functions in Timed and Vanishing modes.
        :return: whether the game has an outcome
        """
        formation = plyr_win_formation(self.main_board, self.board_sz.get(), self.win_len, self.plyr, prev_input)
        if formation is not None:
            self.stop_game()
            messagebox.showinfo('Outcome', f'Player \'{self.plyr}\' wins {formation}!')
            return True

        else:
            if len(self.filled_inds) == self.board_sz.get() ** 2:  # if no one win and the whole board is filled
                self.stop_game()
                messagebox.showinfo('Outcome', 'Ended in a tie.')
                return True

            else:  # if no one win and the whole board is not filled
                self.turn_hint[self.plyr].config(foreground='SystemDisabledText', background='SystemButtonFace', relief='flat')
                self.plyr = opp(self.plyr)
                self.turn_hint[self.plyr].config(foreground=self.colors[self.plyr]['symbol'], background='white', relief='ridge')
                return False

    def stop_game(self):
        self.filled_inds = []
        for button in self.board_buttons:
            button.config(state='disabled')

    def to_submenu(self):
        if messagebox.askyesno('Confirmation', 'Are you sure you want to quit?\n\nYou will loose all your progress.'):
            self.filled_inds = []
            self.board_sz.trace_remove('write', self.trace1)
            self.board_sz.trace_remove('write', self.trace2)
            for widget in self.window.winfo_children():
                widget.destroy()

            SubMenu(self.window, self.board_sz, self.board_zoom, self.colors, self.mode)

    def replay(self):
        if messagebox.askyesno('Confirmation',
                               'Are you sure you want to restart?\n\nYou will loose all your progress.'):
            self.filled_inds = []
            self.board_sz.trace_remove('write', self.trace1)
            self.board_sz.trace_remove('write', self.trace2)
            for widget in self.window.winfo_children():
                widget.destroy()

            GameMenu(self.window, self.board_sz, self.board_zoom, self.colors, self.mode)


class GameMenuT(GameMenu):
    """
    :ivar window, board_sz, board_zoom, colors, mode: same as SubMenu.
    :ivar remain_time: dict containing how much time does each player still have.
    :ivar hint_scale: used to animate the inflate of timer at the start of each turn.
    """

    # noinspection PyTypeChecker
    def __init__(self, window, board_sz, board_zoom, colors, mode: str):
        super().__init__(window, board_sz, board_zoom, colors, mode)
        self.remain_time = {
            'X': tk.StringVar(value='10'),
            'O': tk.StringVar(value='10')
        }
        self.hint_scale = 0
        self.next_countdown = None

        # destroy the original x_turn_hint and o_turn_hint created by superclass
        self.turn_hint['X'].destroy()
        self.turn_hint['O'].destroy()
        self.turn_hint = {
            'X': tk.LabelFrame(self.turn_hint_frame,
                               text='X turn',
                               font=('Helvetica', self.board_zoom.get() * 2 + 1, 'bold'),
                               foreground=self.colors['X']['symbol'],
                               borderwidth=5,
                               relief='ridge',
                               takefocus=False),
            'O': tk.LabelFrame(self.turn_hint_frame,
                               text='O turn',
                               font=('Helvetica', self.board_zoom.get() * 2 + 1, 'bold'),
                               foreground=self.colors['O']['symbol'],
                               borderwidth=5,
                               relief='ridge',
                               takefocus=False)
        }
        self.time_entry = {
            'X': tk.Entry(self.turn_hint['X'],
                          width=4,
                          borderwidth=1,
                          font=('Courier', self.board_zoom.get() * 3 + 1, 'bold'),
                          foreground=self.colors['X']['symbol'],
                          disabledforeground=self.colors['X']['symbol'],
                          disabledbackground='white',
                          justify='center',
                          textvariable=self.remain_time['X']),
            'O': tk.Entry(self.turn_hint['O'],
                          width=4,
                          borderwidth=1,
                          font=('Courier', self.board_zoom.get() * 3 + 1, 'bold'),
                          foreground=self.colors['O']['symbol'],
                          disabledforeground=self.colors['O']['symbol'],
                          disabledbackground='white',
                          justify='center',
                          textvariable=self.remain_time['O'])
        }
        self.trace3 = self.remain_time['X'].trace_add('write', lambda *args: self.validate_timer('X', *args))
        self.trace4 = self.remain_time['O'].trace_add('write', lambda *args: self.validate_timer('O', *args))

        self.turn_hint['X'].pack(side='left')
        self.turn_hint['O'].pack(side='left')
        self.time_entry['X'].pack()
        self.time_entry['O'].pack()

    def adjust_zoom(self, *args):
        super().adjust_zoom()

        self.time_entry['X'].config(font=('Helvetica', self.board_zoom.get() * 3 + 1, 'bold'))
        self.time_entry['O'].config(font=('Helvetica', self.board_zoom.get() * 3 + 1, 'bold'))

    def lock_settings(self):
        super().lock_settings()

        self.time_entry['X'].config(state='disabled')
        self.time_entry['O'].config(state='disabled')

        # disable X's timer
        self.time_entry['X'].config(relief='flat', disabledforeground='SystemDisabledText',
                                    disabledbackground='SystemButtonFace',
                                    font=('Courier', self.board_zoom.get() * 3 + 1, 'bold'))

        # enable O's timer
        self.time_entry['O'].config(relief='sunken', disabledforeground=self.colors['O']['symbol'], disabledbackground='white')

        self.countdown()

    def validate_timer(self, key: str, *args):
        try:
            # Try to convert the value of the key to a float
            float(self.remain_time[key].get())
        except ValueError:
            # Show a messagebox and reset the value if conversion fails
            messagebox.askretrycancel('Warning', f'Please enter a decimal number for {key}!')
            self.remain_time[key].set('10')

    def countdown(self):
        remain_time = float(self.remain_time[self.plyr].get())

        if remain_time > 0.0:
            # animate inflate of the current plyr's timer
            self.hint_scale = min(self.hint_scale + 2, 3)
            self.time_entry[self.plyr].config(font=('Courier', self.board_zoom.get() * 3 + 1 + self.hint_scale, 'bold'))

            # decrease the remain_time value by 0.1 every 100ms and display only 1 deci point using round().
            # DO NOT decrease by 1 every 1000ms (1sec) as the timer slows down the whole app.
            self.remain_time[self.plyr].set(str(round(remain_time - 0.1, 1)))
            self.next_countdown = self.window.after(100, self.countdown)

            self.window.update_idletasks()

            # If X has under 5 secs left, flash the timer.
            if remain_time < 5.0 and remain_time % 1 < 0.4:
                self.time_entry[self.plyr].config(relief='sunken', disabledbackground='white')
            elif remain_time < 5.0 and remain_time % 1 >= 0.4:
                self.time_entry[self.plyr].config(relief='groove', disabledbackground='yellow')

        # if player runs out of time, opponent wins and stop all recursions.
        else:
            messagebox.showinfo('Outcome', f"Time's up! Player {opp(self.plyr)} wins!")
            self.stop_game()
            return None

    def check_winner_pvc(self, prev_input: int, cur_plyr: str) -> bool:
        """
        Modified to include disabling timer entry, switching timer and adding bonus time.
        """
        if super().check_winner_pvc(prev_input, cur_plyr) is False:
            # grey out current plyr's timer, colorize next plyr's timer.
            self.time_entry[cur_plyr].config(relief='flat', disabledforeground='SystemDisabledText',
                                             disabledbackground='SystemButtonFace',
                                             font=('Courier', self.board_zoom.get() * 3 + 1, 'bold'))
            self.time_entry[opp(cur_plyr)].config(relief='sunken', disabledforeground=self.colors[opp(cur_plyr)]['symbol'], disabledbackground='white')

            self.remain_time[cur_plyr].set(str(float(self.remain_time[cur_plyr].get()) + 1))
            return False

    def check_winner_pvp(self, prev_input: int) -> bool:
        """
        Modified to include disabling timer entry, switching timer and adding bonus time.
        """
        if super().check_winner_pvp(prev_input) is False:  # changes self.plyr to next plyr
            # grey out current plyr's timer, colorize next plyr's timer.
            self.time_entry[opp(self.plyr)].config(relief='flat', disabledforeground='SystemDisabledText',
                                                   disabledbackground='SystemButtonFace',
                                                   font=('Courier', self.board_zoom.get() * 3 + 1, 'bold'))
            self.time_entry[self.plyr].config(relief='sunken', disabledforeground=self.colors[self.plyr]['symbol'], disabledbackground='white')

            # current plyr gets bonus time
            self.remain_time[opp(self.plyr)].set(str(float(self.remain_time[opp(self.plyr)].get()) + 1))
            return False

    def stop_game(self):
        super().stop_game()

        # stop player's countdown and timer flash
        self.window.after_cancel(self.next_countdown)

    def to_submenu(self):
        if messagebox.askyesno('Confirmation', 'Are you sure you want to quit?\n\nYou will loose all your progress.'):
            self.filled_inds = []
            self.board_sz.trace_remove('write', self.trace1)
            self.board_sz.trace_remove('write', self.trace2)
            self.remain_time['X'].trace_remove('write', self.trace3)
            self.remain_time['O'].trace_remove('write', self.trace4)

            # stops the next queued countdown()
            self.window.after_cancel(self.next_countdown)
            for widget in self.window.winfo_children():
                widget.destroy()

            SubMenu(self.window, self.board_sz, self.board_zoom, self.colors, self.mode)

    def replay(self):
        if messagebox.askyesno('Confirmation',
                               'Are you sure you want to restart?\n\nYou will loose all your progress.'):
            self.filled_inds = []
            self.board_sz.trace_remove('write', self.trace1)
            self.board_sz.trace_remove('write', self.trace2)
            self.remain_time['X'].trace_remove('write', self.trace3)
            self.remain_time['O'].trace_remove('write', self.trace4)

            # stops the next queued countdown()
            self.window.after_cancel(self.next_countdown)
            for widget in self.window.winfo_children():
                widget.destroy()

            GameMenuT(self.window, self.board_sz, self.board_zoom, self.colors, self.mode)


class GameMenuV(GameMenu):
    """
    :ivar window, board_sz, board_zoom, colors, mode: same as SubMenu.
    :ivar remain_steps: how many steps into the future will an X/O last.
    :ivar show_nxt_vanish_move: show/hide which move is going to vanish in the next turn.
    """

    def __init__(self, window, board_sz, board_zoom, colors, mode: str):
        super().__init__(window, board_sz, board_zoom, colors, mode)
        self.remain_steps = tk.IntVar()
        self.show_nxt_vanish_move = tk.BooleanVar(value=False)

        self.remain_stps_label = tk.Label(
            self.settings_frame,
            text='\nRemain for'
        )
        self.remain_count_slider = tk.Scale(
            self.settings_frame,
            orient='horizontal',
            variable=self.remain_steps,
            length=100,
            from_=self.win_len,
            to=self.win_len * 2,
            cursor='sb_h_double_arrow'
        )
        self.nxt_vanish_checkbox = tk.Checkbutton(
            self.settings_frame,
            text='Show next vanishing moves',
            cursor='hand2',
            variable=self.show_nxt_vanish_move,
            command=self.del_moves
        )

        self.remain_stps_label.grid(row=2, column=1)
        self.remain_count_slider.grid(row=2, column=2)
        self.nxt_vanish_checkbox.grid(columnspan=2, row=3, column=1)

    def del_moves(self):
        # if half of the total num of moves by X + O > remain_steps, X's moves start to vanish.
        if len(self.filled_inds) / 2 > self.remain_steps.get():
            self.debugger.insert('end', f'Vanish order:\n{self.filled_inds}')

            vanish_ind = self.filled_inds.pop(0)

            self.main_board[vanish_ind] = ' '
            self.board_buttons[vanish_ind].config(text='', background='SystemButtonFace', state='normal')

        # if half of the total num of moves by X + O is one less before vanishing begins, tint the 2 oldest moves about to vanish.
        if self.show_nxt_vanish_move.get() is True and len(self.filled_inds) / 2 >= self.remain_steps.get():
            self.board_buttons[self.filled_inds[1]].config(background=self.colors['']['nxt_vanish_move1'])
            self.board_buttons[self.filled_inds[0]].config(background=self.colors['']['nxt_vanish_move0'])

    def adjust_length(self, *args):
        super().adjust_length(*args)
        self.remain_count_slider.config(from_=self.win_len, to=self.win_len * 2)

    def check_winner_pvc(self, prev_input: int, cur_plyr: str) -> bool:
        self.del_moves()
        return super().check_winner_pvc(prev_input, cur_plyr)

    def check_winner_pvp(self, prev_input: int) -> bool:
        self.del_moves()
        return super().check_winner_pvp(prev_input)

    def replay(self):
        if messagebox.askyesno('Confirmation',
                               'Are you sure you want to restart?\n\nYou will loose all your progress.'):
            self.filled_inds = []
            self.board_sz.trace_remove('write', self.trace1)
            self.board_sz.trace_remove('write', self.trace2)

            for widget in self.window.winfo_children():
                widget.destroy()

            GameMenuV(self.window, self.board_sz, self.board_zoom, self.colors, self.mode)


class GameMenuS(GameMenu):
    """
    :ivar window, board_sz, board_zoom, colors, mode: same as SubMenu.
    :ivar prev_inputs: dict containing 2 lists: one containing all the moves made by X in chronological order, the other containing O's. Leftmost element = earliest move. Rightmost element = latest move.
    """

    def __init__(self, window, board_sz, board_zoom, colors, mode: str):
        super().__init__(window, board_sz, board_zoom, colors, mode)
        self.prev_inputs = {
            'X': [],
            'O': []
        }
        self.win_len = self.board_sz.get()
        self.board_sz_tip.config(text='Amount in a row to win: ' + str(self.win_len))

    def adjust_length(self, *args):
        super().adjust_length(*args)

        self.win_len = self.board_sz.get()
        self.board_sz_tip.config(text='Amount in a row to win: ' + str(self.win_len))

    def update_ind_pc(self, prev_input: int) -> int:
        pass

    def update_ind_plyr(self, prev_input: int):
        super().update_ind_plyr(prev_input)

        self.board_buttons[prev_input].config(background=self.colors[self.plyr]['snake_head'])
        if len(self.prev_inputs[self.plyr]) > 0:
            # turn the snake's previous head to body color
            self.board_buttons[self.prev_inputs[self.plyr][-1]].config(background=self.colors[self.plyr]['snake_body'])

        self.prev_inputs[self.plyr].append(prev_input)

    def check_winner_pvp(self, prev_input: int) -> bool:
        """
        Modified to:
         1. give snake a new head when the old head stuck.
         2. disable the adj cells from the previous turn and enable the adj cells for the next turn.
        """
        if super().check_winner_pvp(prev_input) is False:  # changes self.plyr to next player

            # setup coords (x_coord, y_coord) of 8 indexes around a center
            relative_adj = {
                (-1, -1), (0, -1), (1, -1),  # Top-left, Top-right
                (-1, 0),           (1, 0),  # Left, Right
                (-1, 1),  (0, 1),  (1, 1)  # Bottom-left, Bottom-right
            }

            def gen_adj(row: int, col: int) -> set:
                """
                (generate adjacents)
                :return: set containing the valid indexes of the adjacents around the previous input of opponent.
                """
                absolute_adj = set()

                for dir_x, dir_y in relative_adj:
                    adj_row = row + dir_y
                    adj_col = col + dir_x

                    if 0 <= adj_row < self.board_sz.get() and 0 <= adj_col < self.board_sz.get():
                        adj_ind = adj_row * self.board_sz.get() + adj_col

                        if self.main_board[adj_ind] == ' ':
                            self.board_buttons[adj_ind].config(state='normal', relief='raised')
                            absolute_adj.add(adj_ind)

                if not absolute_adj:  # if absolute_adj is empty, next player is stuck
                    self.prev_inputs[self.plyr].pop()
                    prev_input = self.prev_inputs[self.plyr][-1]
                    absolute_adj = gen_adj(prev_input // self.board_sz.get(), prev_input % self.board_sz.get())  # recursion for the previous-previous input

                return absolute_adj

            prev_input = self.prev_inputs[self.plyr][-1]
            absolute_adj = gen_adj(prev_input // self.board_sz.get(), prev_input % self.board_sz.get())

            for ind in set(range(self.board_sz.get() ** 2)).difference(self.filled_inds, absolute_adj):  # is empty and not in absolute_adj
                self.board_buttons[ind].config(state='disabled', relief='sunken')

            return False


ver_no = 'Tic Tac Toe v16'

window = tk.Tk()
MainMenu(window)
window.title(ver_no)

window.mainloop()
