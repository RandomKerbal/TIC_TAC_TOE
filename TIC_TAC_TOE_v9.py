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
Ver 10: Added title animation. Added 4 modes: Traditional, Time Trial, Vanishing Moves, Colonizer\n
    ''')


class MainMenu:
    """
    === Attributes ===\n
    window: Name of window that displays MainMenu.\n
    board_sz: Length of the board.\n
    board_zoom: Magnification of the board.\n
    """

    def __init__(self, window, board_sz_: int = 3, board_zoom_: int = 5):
        self.window = window
        self.board_sz = tk.IntVar(value=board_sz_)
        self.board_zoom = tk.IntVar(value=board_zoom_)

        self.title_line1 = Label(self.window,
                                 takefocus=False,
                                 width=500,
                                 borderwidth=0,
                                 background='black',
                                 foreground='sea green1',
                                 text='=' * 999,
                                 font='TkFixedFont')
        self.title_line2 = Label(self.window,
                                 takefocus=False,
                                 width=500,
                                 borderwidth=0,
                                 background='black',
                                 foreground='sea green1',
                                 text='\n' + '=' * 999,
                                 font='TkFixedFont')
        self.title_label = Label(self.window,
                                 takefocus=False,
                                 borderwidth=0,
                                 width=1,
                                 background='black',
                                 foreground='sea green1',
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
                                    background='black',
                                    foreground='sea green1',
                                    text='',
                                    font='TkFixedFont',
                                    justify='left')
        subtitle_text = '   100% Made by Zhong Yan      Infinite boards!             Unbeatable AI!        '

        self.b_pvc = Button(self.window,
                            text='Single Player',
                            cursor='hand2',
                            overrelief='sunken',
                            command=lambda _='pvc': self.to_submenu(_),
                            activeforeground='white',
                            activebackground='sea green',
                            background='sea green1',
                            foreground='black',
                            width=500,
                            font=('FixedSys', 15),
                            borderwidth=5)

        self.b_pvp = Button(self.window,
                            text='Multi Player',
                            cursor='hand2',
                            overrelief='sunken',
                            command=lambda _='pvp': self.to_submenu(_),
                            activeforeground='white',
                            activebackground='sea green',
                            background='sea green1',
                            foreground='black',
                            width=500,
                            font=('FixedSys', 15),
                            borderwidth=5)

        self.b_changelog = Button(self.window,
                                  text='Changelog',
                                  cursor='hand2',
                                  overrelief='sunken',
                                  command=to_changelog,
                                  activeforeground='white',
                                  activebackground='sea green',
                                  background='sea green1',
                                  foreground='black',
                                  width=500,
                                  font=('FixedSys', 15),
                                  borderwidth=5)

        self.b_exit = Button(self.window,
                             text='Exit',
                             cursor='hand2',
                             overrelief='sunken',
                             command=self.exit,
                             activeforeground='white',
                             activebackground='sea green',
                             background='sea green1',
                             foreground='black',
                             width=500,
                             font=('FixedSys', 15),
                             borderwidth=5)

        self.title_line1.pack(side='top')
        self.title_label.pack(side='top')
        self.subtitle_label.pack(side='top')
        self.title_line2.pack(side='top')
        self.b_pvc.pack(side='top')
        self.b_pvp.pack(side='top')
        self.b_changelog.pack(side='top')
        self.b_exit.pack(side='top')

        # Animating title & subtitle:
        # time between frames, in milliseconds
        wait = 200
        # There r total 94 frames (frame 0 - 93) stored in anim_frames. All frames r called at the same time, but their executions r queued up.
        self.anim_frames = []
        # frames 0 - 10: animating title
        self.anim_frames.append(self.window.after(wait * 0, lambda _=8: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 1, lambda _=11: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 2, lambda _=19: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 3, lambda _=25: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 4, lambda _=34: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 5, lambda _=42: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 6, lambda _=50: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 7, lambda _=56: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 8, lambda _=65: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 9, lambda _=74: self.title_label.config(width=_)))
        self.anim_frames.append(self.window.after(wait * 10, lambda _=82: self.title_label.config(width=_)))

        # frames 11 - 93: animating subtitle
        # loop iterates to 82 as it's the number of chars in the subtitle
        for i in range(0, 83):
            self.anim_frames.append(self.window.after(wait*(i+11), lambda _=i: self.subtitle_label.config(text=subtitle_text[:_] + '_'*min(1, 82-_) + ' '*(81-_))))

        # disables the close window (X) button in the top right corner
        self.window.protocol('WM_DELETE_WINDOW', self.exit)

        # set the MainMenu window to the correct resolution
        self.window.geometry('700x400')
        self.window.config(background='black')

    def to_submenu(self, mode: str):
        # stops all queued frames of the title animation
        for frame in self.anim_frames:
            self.window.after_cancel(frame)

        for widget in self.window.winfo_children():
            widget.destroy()
        SubMenu(self.window, self.board_sz, self.board_zoom, mode)

    def exit(self):
        messagebox.showinfo('Afterword',
                            'Thank you for playing TIC-TAC-TOE!\n\nI spend over 71+ hours creating this game all by MYSELF.\n\nIn this project, I designed the AI that finds the highest winning probability, arranged the GUI elements in the most ergonomic way, optimized the algorithms, fixed bugs, and learned tkinter.\n\nHope you enjoyed it!')

        self.window.destroy()


def default_hint():
    messagebox.showinfo('Hint',
                        'Ah, just like the good ol\' one you played in kindergarten...\n\nYou can select a board length between 2 and... infinity! Length 7 or larger only needs half the length to win.\n\nThe starting player will be X, and the other will be O. No friends? No worries! You can play with my AI:\n\'The First-Gen Tallyman\'.')


def timed_hint():
    messagebox.showinfo('Hint',
                        'At the start, you can set a time limit for each player. Each player will have that amount of time to complete the game.\n\nBut not so fast - you will earn 1 extra second after each move!\n\n(other details are same as the Traditional Mode)')


def vanish_hint():
    messagebox.showinfo('Hint',
                        'Once you placed the minimum number of X/O you need to win, your oldest move will disappear!\n\nBad memory? You can enable \'next vanishing moves\' to see them highlighted in yellow. You can also make your moves last longer by changing the \'remain for\' slider.\n\n(other details are same as the Traditional Mode)')


def colonise_hint():
    messagebox.showinfo('Hint',
                        'Let\'s expand your territories like 1500\'s Great Britain!\n\nIn your first move, you can place wherever you want. Be strategic with your first move, as you can ONLY place your next move in the + around any existing moves (including your opponent\'s)!\n\nI would recommend playing this mode on a 7x7 or larger board.\n\n(other details are same as the Traditional Mode)')


class SubMenu:
    """
    === Attributes ===\n
    window: Name of window that displays MainMenu.\n
    board_sz: Length of the board.\n
    board_zoom: Magnification of the board.\n
    win_len: How many X in a row/column/diagonal to win.\n
    mode: pvp = Player versus player; pvc = Player versus pc.\n
    """

    def __init__(self, window, board_sz, board_zoom, mode: str):
        self.window = window
        self.board_sz = board_sz
        self.win_len = set_win_len(self.board_sz.get())
        self.check_winner_area = set_check_winner_area(board_sz.get(), self.win_len)
        self.board_zoom = board_zoom
        self.mode = mode

        self.title = Button(self.window,
                            state='disabled',
                            takefocus=False,
                            borderwidth=0,
                            background='black',
                            disabledforeground='sea green1',
                            text='\nChoose a mode',
                            font=('FixedSys', 25, 'underline', 'bold'))

        self.b_default = Button(self.window,
                                text='Traditional',
                                cursor='hand2',
                                overrelief='sunken',
                                command=lambda _=self.mode: self.to_gamemenu(_),
                                activeforeground='white',
                                activebackground='sea green',
                                background='sea green1',
                                foreground='black',
                                width=25,
                                font=('FixedSys', 15),
                                borderwidth=5)

        self.b_default_hint = Button(self.window,
                                     bitmap='question',
                                     cursor='question_arrow',
                                     overrelief='sunken',
                                     command=default_hint,
                                     activeforeground='white',
                                     activebackground='sea green',
                                     background='sea green1',
                                     foreground='black',
                                     width=30,
                                     borderwidth=5)

        self.b_timed = Button(self.window,
                              text='Timed Trial',
                              cursor='hand2',
                              overrelief='sunken',
                              command=lambda _=self.mode: self.to_gamemenu_t(_),
                              activeforeground='white',
                              activebackground='sea green',
                              background='sea green1',
                              foreground='black',
                              width=25,
                              font=('FixedSys', 15),
                              borderwidth=5)

        self.b_timed_hint = Button(self.window,
                                   bitmap='question',
                                   cursor='question_arrow',
                                   overrelief='sunken',
                                   command=timed_hint,
                                   activeforeground='white',
                                   activebackground='sea green',
                                   background='sea green1',
                                   foreground='black',
                                   width=30,
                                   borderwidth=5)

        self.b_vanish = Button(self.window,
                               text='Vanishing Moves',
                               cursor='hand2',
                               overrelief='sunken',
                               command=lambda _=self.mode: self.to_gamemenu_v(_),
                               activeforeground='white',
                               activebackground='sea green',
                               background='sea green1',
                               foreground='black',
                               width=25,
                               font=('FixedSys', 15),
                               borderwidth=5)

        self.b_vanish_hint = Button(self.window,
                                    bitmap='question',
                                    cursor='question_arrow',
                                    overrelief='sunken',
                                    command=vanish_hint,
                                    activeforeground='white',
                                    activebackground='sea green',
                                    background='sea green1',
                                    foreground='black',
                                    width=30,
                                    borderwidth=5)

        self.b_colonize = Button(self.window,
                                 text='Colonizer',
                                 cursor='hand2',
                                 overrelief='sunken',
                                 command=lambda _=self.mode: self.to_gamemenu_c(_),
                                 activeforeground='white',
                                 activebackground='sea green',
                                 background='sea green1',
                                 foreground='black',
                                 width=25,
                                 font=('FixedSys', 15),
                                 borderwidth=5)

        self.b_colonise_hint = Button(self.window,
                                     bitmap='question',
                                     cursor='question_arrow',
                                     overrelief='sunken',
                                     command=colonise_hint,
                                     activeforeground='white',
                                     activebackground='sea green',
                                     background='sea green1',
                                     foreground='black',
                                     width=30,
                                     borderwidth=5)

        self.b_back = Button(self.window,
                             text='Back',
                             cursor='hand2',
                             overrelief='sunken',
                             command=self.to_mainmenu,
                             activeforeground='white',
                             activebackground='sea green',
                             background='sea green1',
                             foreground='black',
                             width=25,
                             font=('FixedSys', 15),
                             borderwidth=5)

        # disables the close window (X) button in the top right corner
        self.window.protocol('WM_DELETE_WINDOW', lambda _=self: MainMenu.exit(_))

        # set the MainMenu window to the correct resolution and color
        self.window.geometry('700x400')
        self.window.configure(background='black')
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
        self.b_colonize.grid(row=4, column=1)
        self.b_colonise_hint.grid(row=4, column=2)
        self.b_back.grid(row=5, column=1, columnspan=2, pady=25)

    def to_gamemenu(self, mode: str):
        for widget in self.window.winfo_children():
            widget.destroy()

        GameMenu(self.window, self.board_sz, self.board_zoom, mode)

    def to_gamemenu_t(self, mode: str):
        for widget in self.window.winfo_children():
            widget.destroy()

        GameMenuT(self.window, self.board_sz, self.board_zoom, mode)

    def to_gamemenu_v(self, mode: str):
        for widget in self.window.winfo_children():
            widget.destroy()

        GameMenuV(self.window, self.board_sz, self.board_zoom, mode)

    def to_gamemenu_c(self, mode: str):
        for widget in self.window.winfo_children():
            widget.destroy()

        GameMenuC(self.window, self.board_sz, self.board_zoom, mode)

    def to_mainmenu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        MainMenu(self.window, self.board_sz.get(), self.board_zoom.get())


class GameMenu:
    """
    === Attributes ===\n
    window: Name of window that displays MainMenu.\n
    board_sz: Length of the board.\n
    check_winner_area = List containing slots where the winning chain will fall on.\n
    board_zoom: Magnification of the board.\n
    win_len: How many X in a row/column/diagonal to win.\n
    mode: pvp = Player versus player; pvc = Player versus pc.\n
    plyr: Player playing in the current turn.\n
    main_board: List containing the board on screen.\n
    filled_slots_ind: List containing the index of filled slots of main_board.\n
    slot_buttons: List containing all the buttons that represent slots on the GUI.\n
    is_debugging: Show/hide the debugger.\n
    is_game_active: Whether the game is ongoing. Returns True from the moment the first player moved until there's a winner, else False.\n
    """

    def __init__(self, window, board_sz, board_zoom, mode: str):
        self.window = window
        self.board_sz = board_sz
        self.win_len = set_win_len(self.board_sz.get())
        self.check_winner_area = set_check_winner_area(board_sz.get(), self.win_len)
        self.board_zoom = board_zoom
        self.mode = mode

        self.plyr = 'X'
        self.main_board = setup_board(self.board_sz.get())
        self.filled_slots_ind = []
        self.slot_buttons = []
        self.is_debugging = BooleanVar(value=False)
        self.is_game_active = False

        self.settings_frame = Frame(self.window)
        self.board_frame = Frame(self.window)
        self.turn_hint = Frame(self.board_frame)
        self.x_turn_hint = Label(
            self.turn_hint,
            text='X turn',
            font=('Helvetica', 10, 'bold'),
            foreground='red4',
            width=13,
            borderwidth=5,
            relief='ridge',
            takefocus=False
        )
        self.o_turn_hint = Label(
            self.turn_hint,
            text='O turn',
            font=('Helvetica', 10, 'bold'),
            foreground='navy',
            width=13,
            borderwidth=5,
            relief='ridge',
            takefocus=False
        )
        self.b_back = Button(
            self.settings_frame,
            text='Back',
            cursor='hand2',
            relief='groove',
            overrelief='sunken',
            command=self.to_menu,
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
        self.board_sz.trace_add('write', self.adjust_length)
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
        self.board_zoom.trace_add('write', self.adjust_zoom)
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
            width=25
        )

        # set the GameMenu window to the correct resolution
        self.window.geometry('')
        self.window.config(background='SystemButtonFace')
        self.settings_frame.pack(side='left', expand=True, fill='both')
        self.settings_frame.grid_rowconfigure(10)
        self.board_frame.pack(side='left', expand=True, fill='x')
        self.turn_hint.grid(columnspan=3, row=0, column=self.board_sz.get() // 2 + 1)
        self.x_turn_hint.pack()
        self.o_turn_hint.pack()
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
        self.window.protocol('WM_DELETE_WINDOW', self.to_menu)

    def create_boardframe(self):
        self.slot_buttons = []
        # Create or update buttons in the board_frame.
        for row in range(self.board_sz.get()):
            for col in range(self.board_sz.get()):
                last_input = row * self.board_sz.get() + col
                slot_button = Button(
                    self.board_frame,
                    font=('Helvetica', self.board_zoom.get() * 4, 'bold'),
                    cursor='crosshair',
                    command=lambda _=last_input: self.update_slot(_),
                    width=3,
                    borderwidth=5
                )
                self.slot_buttons.append(slot_button)
                slot_button.grid(row=row + 3, column=col + 2)

    def adjust_length(self, *args):
        # When I adjust the board length, I must delete the old buttons as I cannot change their position
        # Iterate over all widgets inside the Toplevel window, check their grid pos. Delete buttons after row 3.
        for widget in self.board_frame.winfo_children():
            if widget.grid_info()['row'] >= 3:
                widget.destroy()

        # Generate new board with the correct dimension and descriptions at backend
        self.main_board = setup_board(self.board_sz.get())
        self.win_len = set_win_len(self.board_sz.get())
        self.check_winner_area = set_check_winner_area(self.board_sz.get(), self.win_len)

        # Generate new buttons and symbol indicator at their new positions
        self.create_boardframe()
        self.board_sz_tip.config(text='Amount in a row to win: ' + str(self.win_len))
        self.turn_hint.grid(column=self.board_sz.get() // 2 + 1)

        self.debugger.insert('end', f'Set board len to {self.board_sz.get()}.\n')
        self.debugger.insert('end', f'Checking slot{self.check_winner_area} for winner.\n')

    def adjust_zoom(self, *args):
        # Update the position of the turn indicator and the scale of the buttons.
        for slot_button in self.slot_buttons:
            slot_button.config(font=('Helvetica', self.board_zoom.get() * 4, 'bold'))
            self.x_turn_hint.config(font=('Helvetica', self.board_zoom.get() * 2, 'bold'))
            self.o_turn_hint.config(font=('Helvetica', self.board_zoom.get() * 2, 'bold'))

    def pvc_first(self):
        self.mode = 'pvc'
        self.plyr = 'O'
        self.x_turn_hint.config(foreground='SystemDisabledText')
        self.o_turn_hint.config(foreground='navy')
        self.board_sz_slider.config(state='disabled')
        self.board_sz_label.config(state='disabled')
        self.pvco_checkbox.config(state='disabled')
        self.replay_button.config(state='normal')
        self.update_slot_pvc(-1)
        self.is_game_active = True

    def toggle_debugger(self):
        if self.is_debugging.get():
            self.debugger.grid(columnspan=3, row=10, column=0, sticky='ns')
            for button in self.slot_buttons:
                if button.cget('text') == '':
                    button.config(text=self.slot_buttons.index(button), foreground='gray')
        else:
            self.debugger.grid_forget()
            for slot_button in self.slot_buttons:
                slot_button.config(background='SystemButtonFace')
                # if the slot has a number on, it has no X/O
                if type(slot_button.cget('text')) == int:
                    slot_button.config(text='')

    def update_slot(self, last_input: int):
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
            self.update_slot_pvp(last_input)
            self.check_winner_pvp()

        elif self.mode == 'pvc':
            self.update_slot_pvp(last_input)
            self.check_winner_pvc()
            if self.is_game_active:
                self.update_slot_pvc(last_input)
                self.check_winner_pvc()

    def update_slot_pvc(self, last_input: int) -> int:
        # win_len must be <= 4 as the pruned area can be 4 slots wide if player moved at corners.
        pc_move = pc_input(opponent(self.plyr), self.main_board, self.board_sz.get(), self.filled_slots_ind,
                           min(self.win_len, 4), set_check_winner_area(self.board_sz.get(), min(self.win_len, 4)),
                           last_input, self.is_debugging.get(), self.debugger,
                           self.slot_buttons)
        self.filled_slots_ind.append(pc_move)
        self.main_board[pc_move] = opponent(self.plyr)
        # Update frontend board. If player = O, PC = X so 'red4'. If player = X, PC = O so 'navy'.
        self.slot_buttons[pc_move].config(text=self.main_board[pc_move],
                                          disabledforeground='red4' if self.plyr == 'O' else 'navy', state='disabled')
        self.debugger.insert('end', f'PC\'s move:{pc_move}\n')

        # Why return? See method post-filtering in GameMenuV
        return pc_move

    def check_winner_pvc(self):
        # used to check winner after each turn in PVC mode
        winner = check_winner_anywhere(self.main_board, self.board_sz.get(), self.win_len, self.check_winner_area)
        if winner[1] == 'tie':
            self.stop_game()
            messagebox.showinfo('Result', 'Game ended in a draw\n\n"So close...but the AI will NEVER lose!"')
        elif winner[0] == opponent(self.plyr):
            self.stop_game()
            messagebox.showinfo('Result', f'Computer wins {winner[1]}\n\n"Humans should\'ve been smarter..."')
        elif winner[0] == self.plyr:
            self.stop_game()
            messagebox.showinfo('Result', f'You win {winner[1]}!\n\n"Time to fix more bugs..."')

        # If no one wins, update frontend indicators and player for the next turn.
        elif self.plyr == 'O':
            self.x_turn_hint.config(foreground='SystemDisabledText', relief='flat')
            self.o_turn_hint.config(foreground='navy', relief='ridge')
        elif self.plyr == 'X':
            self.x_turn_hint.config(foreground='red4', relief='ridge')
            self.o_turn_hint.config(foreground='SystemDisabledText', relief='flat')

    def update_slot_pvp(self, last_input: int):
        # reset tint from peach puff back to default color
        for slot_button in self.slot_buttons:
            slot_button.config(background='SystemButtonFace')

        # update backend board
        self.main_board[last_input] = self.plyr
        self.filled_slots_ind.append(last_input)
        # update frontend board
        self.slot_buttons[last_input].config(text=self.main_board[last_input],
                                             disabledforeground='red4' if self.plyr == 'X' else 'navy',
                                             state='disabled')
        self.debugger.insert('end', f'Player\'s move:{last_input}\n')

    def check_winner_pvp(self):
        # used to check winner after each turn in PVP mode
        winner = check_winner_anywhere(self.main_board, self.board_sz.get(), self.win_len, self.check_winner_area)
        if winner[1] == 'tie':
            self.stop_game()
            messagebox.showinfo('Result', 'Game ended in a draw.')
        elif winner != (' ', ' ',):
            self.stop_game()
            messagebox.showinfo('Result', f'Player \'{winner[0]}\' wins {winner[1]}!')

        # If no one wins, update frontend indicators for the next turn.
        elif self.plyr == 'X':
            self.x_turn_hint.config(foreground='SystemDisabledText', relief='flat')
            self.o_turn_hint.config(foreground='navy', relief='ridge')
            self.plyr = 'O'
        elif self.plyr == 'O':
            self.x_turn_hint.config(foreground='red4', relief='ridge')
            self.o_turn_hint.config(foreground='SystemDisabledText', relief='flat')
            self.plyr = 'X'

    def stop_game(self):
        self.is_game_active = False
        for button in self.slot_buttons:
            button.config(state='disabled')

    def to_menu(self):
        if messagebox.askyesno('Confirmation', 'Are you sure you want to quit?\n\nYou will loose all your progress.'):
            self.is_game_active = False
            for widget in self.window.winfo_children():
                widget.destroy()

            MainMenu(self.window, self.board_sz.get(), self.board_zoom.get())

    def replay(self):
        if messagebox.askyesno('Confirmation',
                               'Are you sure you want to restart?\n\nYou will loose all your progress.'):
            self.is_game_active = False
            for widget in self.window.winfo_children():
                widget.destroy()

            GameMenu(self.window, self.board_sz, self.board_zoom, self.mode)


class GameMenuT(GameMenu):
    """
    === Attributes ===\n
    x_remain_time: How much time does player X still have.\n
    o_remain_time: How much time does player O still have.\n
    hint_scale: Used to animate the inflate of timer at the start of each turn.\n
    """

    def __init__(self, window, board_sz, board_zoom, mode: str):
        super().__init__(window, board_sz, board_zoom, mode)
        self.x_remain_time = StringVar(value='10')
        self.o_remain_time = StringVar(value='10')
        self.hint_scale = 0

        # destroy the original x_turn_hint and o_turn_hint created by superclass
        self.x_turn_hint.destroy()
        self.o_turn_hint.destroy()
        self.x_turn_hint = LabelFrame(self.turn_hint,
                                      text='X turn',
                                      font=('Helvetica', self.board_zoom.get() * 2 + 1, 'bold'),
                                      foreground='red4',
                                      borderwidth=5,
                                      relief='ridge',
                                      takefocus=False
                                      )
        self.x_time_entry = Entry(self.x_turn_hint,
                                  width=4,
                                  borderwidth=1,
                                  font=('Courier', self.board_zoom.get() * 3 + 1, 'bold'),
                                  foreground='red4',
                                  disabledforeground='red4',
                                  disabledbackground='white',
                                  justify='center',
                                  textvariable=self.x_remain_time)
        self.o_turn_hint = LabelFrame(self.turn_hint,
                                      text='O turn',
                                      font=('Helvetica', self.board_zoom.get() * 2 + 1, 'bold'),
                                      foreground='navy',
                                      borderwidth=5,
                                      relief='ridge',
                                      takefocus=False
                                      )
        self.o_time_entry = Entry(self.o_turn_hint,
                                  width=4,
                                  borderwidth=1,
                                  font=('Courier', self.board_zoom.get() * 3 + 1, 'bold'),
                                  foreground='navy',
                                  disabledforeground='navy',
                                  disabledbackground='white',
                                  justify='center',
                                  textvariable=self.o_remain_time)

        self.x_turn_hint.pack(side='left')
        self.o_turn_hint.pack(side='left')
        self.x_time_entry.pack()
        self.o_time_entry.pack()

        if mode == 'pvc':
            self.o_turn_hint.pack_forget()

    def x_countdown(self):
        # If (time's not up) and (X is playing this turn) and (game is ongoing):
        if float(self.x_remain_time.get()) > 0.0 and self.plyr == 'X' and self.is_game_active is True:
            # inflate X timer
            self.x_time_entry.config(font=('Courier', self.board_zoom.get() * 3 + 1 + self.hint_scale, 'bold'))
            self.hint_scale = min(self.hint_scale + 2, 3)

            # Decrease the remain_time value by 0.1 every 100ms and display only 1 deci point using round().
            # I didn't decrease by 1 every 1000ms (1sec) as the timer delayed update when switching turns.
            self.x_remain_time.set(str(round(float(self.x_remain_time.get()) - 0.1, 1)))
            self.window.after(100, self.x_countdown)

        # If player runs out of time, opponent wins and stop all recursions.
        elif float(self.x_remain_time.get()) <= 0.0:
            messagebox.showinfo('Result', f"Time's up! Player O wins")
            self.stop_game()
            return None

        # If X is not playing this turn or the game has ended, stop X's countdown and flash.
        else:
            self.x_time_entry.config(relief='sunken', disabledforeground=self.x_turn_hint.cget('foreground'),
                                     disabledbackground='white')
            return None

        # If X has under 5 secs left, flash the timer.
        if float(self.x_remain_time.get()) < 5.0 and float(self.x_remain_time.get()) % 1 < 0.4:
            self.x_time_entry.config(relief='sunken', disabledbackground='white')
        elif float(self.x_remain_time.get()) < 5.0 and float(self.x_remain_time.get()) % 1 >= 0.4:
            self.x_time_entry.config(relief='groove', disabledbackground='yellow')

    def o_countdown(self):
        if float(self.o_remain_time.get()) > 0.0 and self.plyr == 'O' and self.is_game_active is True:
            self.o_time_entry.config(font=('Courier', self.board_zoom.get() * 3 + 1 + self.hint_scale, 'bold'))
            self.hint_scale = min(self.hint_scale + 2, 3)

            self.o_remain_time.set(str(round(float(self.o_remain_time.get()) - 0.1, 1)))
            self.window.after(100, self.o_countdown)

        elif float(self.o_remain_time.get()) <= 0.0:
            messagebox.showinfo('Result', f"Time's up! Player X wins")
            self.stop_game()
            return None

        else:
            self.o_time_entry.config(relief='sunken', disabledforeground=self.o_turn_hint.cget('foreground'),
                                     disabledbackground='white')
            return None

        if float(self.o_remain_time.get()) < 5.0 and float(self.o_remain_time.get()) % 1 < 0.4:
            self.o_time_entry.config(relief='sunken', disabledbackground='white')
        elif float(self.o_remain_time.get()) < 5.0 and float(self.o_remain_time.get()) % 1 >= 0.4:
            self.o_time_entry.config(relief='groove', disabledbackground='yellow')

    def update_slot(self, last_input: int):
        # If the game is not ongoing before, this is the first move. Check if the input time is valid.
        if self.is_game_active is False:
            if not self.x_remain_time.get().isdigit() or not self.o_remain_time.get().isdigit():
                messagebox.askretrycancel('Warning', f'Please enter a decimal number!')
                return None
            # If the time is valid, change some settings
            self.board_sz_slider.config(state='disabled')
            self.board_sz_label.config(state='disabled')
            self.replay_button.config(state='normal')
            self.pvco_checkbox.config(state='disabled')
            self.x_time_entry.config(state='disabled')
            self.o_time_entry.config(state='disabled')
            self.is_game_active = True

            # If playing against PC, there r no turns to stop a player's timer. So the timer only start once.
            if self.mode == 'pvc' and self.plyr == 'X':
                self.x_countdown()
            elif self.mode == 'pvc' and self.plyr == 'O':
                self.o_countdown()

        if self.mode == 'pvp':
            self.update_slot_pvp(last_input)
            self.check_winner_pvp()

        elif self.mode == 'pvc':
            self.update_slot_pvp(last_input)
            self.check_winner_pvc()
            if self.is_game_active:
                self.update_slot_pvc(last_input)
                self.check_winner_pvc()

    # Below, update_slot_pvc and check_winner_pvp r override to include code of the timer.
    # I chose these as: update_slot_pvc is the only func only used in PVC; check_winner_pvp is the only func only used in PVP
    def update_slot_pvc(self, last_input):
        # If X is the human and no one wins yet:
        self.hint_scale = 0
        if self.plyr == 'X' and self.is_game_active is True:
            # X gets bonus time
            self.x_remain_time.set(str(float(self.x_remain_time.get()) + 1))

        elif self.plyr == 'O' and self.is_game_active is True:
            self.o_remain_time.set(str(float(self.o_remain_time.get()) + 1))

        super().update_slot_pvc(last_input)

    def check_winner_pvp(self):
        # Check for any winner. Switch turn if there r no winner.
        super().check_winner_pvp()
        # If O is next and no one wins yet:
        self.hint_scale = 0
        if self.plyr == 'O' and self.is_game_active is True:
            # X gets bonus time
            self.x_remain_time.set(str(float(self.x_remain_time.get()) + 1))
            # Reset X's timer inflate and grey it out. Start O's timer.
            self.x_time_entry.config(relief='flat', disabledforeground='SystemDisabledText',
                                     disabledbackground='SystemButtonFace',
                                     font=('Courier', self.board_zoom.get() * 3 + 1, 'bold'))
            self.o_time_entry.config(relief='sunken', disabledforeground='navy', disabledbackground='white')
            self.o_countdown()

        elif self.plyr == 'X' and self.is_game_active is True:
            self.o_remain_time.set(str(float(self.o_remain_time.get()) + 1))

            self.o_time_entry.config(relief='flat', disabledforeground='SystemDisabledText',
                                     disabledbackground='SystemButtonFace',
                                     font=('Courier', self.board_zoom.get() * 3 + 1, 'bold'))
            self.x_time_entry.config(relief='sunken', disabledforeground='red4', disabledbackground='white')
            self.x_countdown()

    def pvc_first(self):
        self.o_turn_hint.pack()
        self.x_turn_hint.pack_forget()
        self.o_time_entry.config(state='disabled')
        super().pvc_first()
        self.o_countdown()

    def adjust_zoom(self, *args):
        self.x_turn_hint.config(font=('Helvetica', self.board_zoom.get() * 2 + 1, 'bold'))
        self.o_turn_hint.config(font=('Helvetica', self.board_zoom.get() * 2 + 1, 'bold'))
        self.x_time_entry.config(font=('Helvetica', self.board_zoom.get() * 3 + 1, 'bold'))
        self.o_time_entry.config(font=('Helvetica', self.board_zoom.get() * 3 + 1, 'bold'))
        super().adjust_zoom()

    def replay(self):
        if messagebox.askyesno('Confirmation',
                               'Are you sure you want to restart?\n\nYou will loose all your progress.'):
            self.is_game_active = False
            for widget in self.window.winfo_children():
                widget.destroy()

            GameMenuT(self.window, self.board_sz, self.board_zoom, self.mode)


class GameMenuV(GameMenu):
    """
    === Attributes ===\n
    last_inputs: A list containing the l most recent moves on the board, in chronological order. Leftmost element = earliest move. Rightmost element = latest move.\n
    remain_steps: How many steps into the future will an X/O last.\n
    is_showing_nxt_vanishing_move: Show/hide which move is going to vanish in the next turn.
    """

    def __init__(self, window, board_sz, board_zoom, mode: str):
        super().__init__(window, board_sz, board_zoom, mode)
        self.last_inputs = []
        self.remain_steps = IntVar(value=1)
        self.is_showing_nxt_vanish_move = BooleanVar(value=False)

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
            variable=self.is_showing_nxt_vanish_move,
            command=self.delete_moves
        )

        self.remain_stps_label.grid(row=2, column=1)
        self.remain_stps_slider.grid(row=2, column=2)
        self.nxt_vanish_checkbox.grid(columnspan=2, row=3, column=1)

    def delete_moves(self):
        # If (num of moves by X & O so far) + (moves by X & O in this turn) is more than remain_steps*2, the num of moves by X is more than remain_steps. So X's moves start to vanish.
        if (len(self.last_inputs) + 2 > self.remain_steps.get() * 2) and self.is_game_active:
            self.debugger.insert('end', f'Most recent moves:\n{self.last_inputs}')
            self.main_board[self.last_inputs[0]] = ' '
            self.slot_buttons[self.last_inputs[0]].config(text='', background='SystemButtonFace', state='normal')
            self.filled_slots_ind.remove(self.last_inputs[0])
            self.last_inputs = self.last_inputs[1:]

        # if (num of moves by X & O so far) + (moves by X & O in this turn) is one less before vanishing begins, tint the 3 oldest moves about to vanish.
        if (len(self.last_inputs) + 2 > self.remain_steps.get() * 2 - 1) and self.is_showing_nxt_vanish_move.get():
            self.slot_buttons[self.last_inputs[0]].config(background='khaki')
            self.slot_buttons[self.last_inputs[1]].config(background='lemon chiffon2')

    def adjust_length(self, *args):
        super().adjust_length()
        self.remain_stps_slider.config(from_=self.win_len, to=self.win_len * 2)

    def update_slot_pvc(self, last_input: int):
        pc_move = super().update_slot_pvc(last_input)
        self.last_inputs.append(pc_move)

    def check_winner_pvc(self):
        super().check_winner_pvc()
        self.delete_moves()

    def update_slot_pvp(self, last_input: int):
        super().update_slot_pvp(last_input)
        self.last_inputs.append(last_input)

    def check_winner_pvp(self):
        super().check_winner_pvp()
        self.delete_moves()

    def replay(self):
        if messagebox.askyesno('Confirmation',
                               'Are you sure you want to restart?\n\nYou will loose all your progress.'):
            self.is_game_active = False
            for widget in self.window.winfo_children():
                widget.destroy()

            GameMenuV(self.window, self.board_sz, self.board_zoom, self.mode)


class GameMenuC(GameMenu):
    # def update_slot_pvp(self, last_input: int):
    #     super().update_slot_pvp(last_input)
    #     [button.config(background='MistyRose', state='disabled') for button in self.slot_buttons]
    #     for row in range(self.board_sz.get()):
    #         for col in range(self.board_sz.get()):
    #             c = row*self.board_sz.get() + col
    #             n = max(0, row-1)*self.board_sz.get() + col
    #             s = min(row+1, self.board_sz.get()-1)*self.board_sz.get() + col
    #             e = row*self.board_sz.get() + min(col+1, self.board_sz.get()-1)
    #             w = row*self.board_sz.get() + max(0, col-1)
    #             if self.main_board[c] != ' ':
    #                 self.slot_buttons[n].config(background='SystemButtonFace', state='normal')
    #                 self.slot_buttons[s].config(background='SystemButtonFace', state='normal')
    #                 self.slot_buttons[e].config(background='SystemButtonFace', state='normal')
    #                 self.slot_buttons[w].config(background='SystemButtonFace', state='normal')



ver_no = 'Tic Tac Toe v9'

window = tk.Tk()
MainMenu(window)
window.title(ver_no)

window.mainloop()
