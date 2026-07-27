import random
import threading
import tkinter as tk
from tkinter import messagebox
import networkx as nx
import backend as tt
from enum import Enum


class AI(Enum):
    RECUR_AND_OR: str = "Recursive And-Or AI"
    ITER_AND_OR: str = "Iterative And-Or AI"
    RECUR_PROB: str = "Recursive Probability AI"
    RECUR_SNAKE: str = "Recursive Snake AI"


class Settings:
    """Settings persist across menus."""

    def __init__(self):
        self.board_len: tk.IntVar = tk.IntVar(value=3)
        self.win_len: tk.IntVar = tk.IntVar(value=3)
        self.board_zoom: tk.IntVar = tk.IntVar(value=5)
        self.ai_type: tk.StringVar = tk.StringVar(value=AI.RECUR_AND_OR.value)
        self.has_graph: tk.BooleanVar = tk.BooleanVar(value=False)
        self.has_log_n_ind: tk.BooleanVar = tk.BooleanVar(value=False)
        self.is_pvc: bool = True
        self.INIT_TIME: float = 10
        self.board_font: tuple[str, int, str] = ("", 0, "")
        self.time_font: tuple[str, int, str] = ("", 0, "")
        self.TOOLBAR_FONT: tuple[str, int] = ("Helvetica", 10)
        self.TURN_FONT: tuple[str, int, str] = ("Helvetica", 10, "bold")
        self.MENU_FONT: tuple[str, int] = ("FixedSys", 15)
        self.SUBMENU_FONT: tuple[str, int, str, str] = ("FixedSys", 25, "bold", "underline")
        self.COLOR_FONT: tuple[str, int, str] = ("FixedSys", 20, "bold")
        self.MENU_DIM: str = "700x400"

        self.colors: list[dict] = [
            # general features
            {
                "index": "gray",
                "bot_move": "Sea Green1",
                "bot_moves": "Dark Sea Green1",
                "nxt_vanish_move": "Navajo White",
                "board_button": "SystemButtonFace",
                "background": "SystemButtonFace",
                "foreground": "Sea Green2"
            },
            # X features
            {
                "char": "Red4",
                "snake_head": "Green Yellow",
                "snake_body": "Dark Olive Green1"
            },
            # O features
            {
                "char": "Navy",
                "snake_head": "Cyan1",
                "snake_body": "Dark Slate Gray1",
            }
        ]


class MainMenu:
    root: tk.Tk
    settings: Settings

    def __init__(self, root: tk.Tk, settings: Settings):
        self.root = root
        self.settings = settings
        self.title_line1 = tk.Label(
            self.root,
            width=500,
            borderwidth=0,
            background="Black",
            foreground="Sea Green1",
            text='=' * 999,
            font="TkFixedFont",
            takefocus=False
        )
        self.title_line2 = tk.Label(
            self.root,
            width=500,
            borderwidth=0,
            background="Black",
            foreground="Sea Green1",
            text='=' * 999,
            font="TkFixedFont",
            takefocus=False
        )
        self.title_label = tk.Label(
            self.root,
            borderwidth=0,
            width=82,
            background="Black",
            foreground="Sea Green1",
            text="""
████████ ██  ██████       ████████  █████   ██████       ████████  ██████  ███████
   ██    ██ ██               ██    ██   ██ ██               ██    ██    ██ ██
   ██    ██ ██      █████    ██    ███████ ██      █████    ██    ██    ██ █████
   ██    ██ ██               ██    ██   ██ ██               ██    ██    ██ ██
   ██    ██  ██████          ██    ██   ██  ██████          ██     ██████  ███████
   """,
            font="TkFixedFont",
            justify=tk.LEFT,
            anchor=tk.NW,
            takefocus=False
        )
        self.subtitle_label = tk.Label(
            self.root,
            borderwidth=0,
            width=500,
            background="Black",
            foreground="Sea Green1",
            font="TkFixedFont",
            justify=tk.LEFT,
            takefocus=False
        )
        SUBTITLE = "   99% Made by CZY           4 Innovative Modes!            Unbeatable AI?        "

        self.pvc_button = tk.Button(
            self.root,
            text="Single Player",
            cursor="hand2",
            overrelief=tk.SUNKEN,
            command=lambda: self.to_submenu(True),
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=500,
            font=self.settings.MENU_FONT,
            borderwidth=5
        )
        self.pvp_button = tk.Button(
            self.root,
            text="Multi Player",
            cursor="hand2",
            overrelief=tk.SUNKEN,
            command=lambda: self.to_submenu(False),
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=500,
            font=self.settings.MENU_FONT,
            borderwidth=5
        )
        self.changelog_button = tk.Button(
            self.root,
            text="Changelog",
            cursor="hand2",
            overrelief=tk.SUNKEN,
            command=to_changelog,
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=500,
            font=self.settings.MENU_FONT,
            borderwidth=5
        )
        self.exit_button = tk.Button(
            self.root,
            text="Exit",
            cursor="hand2",
            overrelief=tk.SUNKEN,
            command=self.exit,
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=500,
            font=self.settings.MENU_FONT,
            borderwidth=5
        )
        self.exit_button.pack(side=tk.BOTTOM)
        self.changelog_button.pack(side=tk.BOTTOM)
        self.pvp_button.pack(side=tk.BOTTOM)
        self.pvc_button.pack(side=tk.BOTTOM)
        self.title_line2.pack(side=tk.BOTTOM)
        self.subtitle_label.pack(side=tk.BOTTOM, expand=True, anchor=tk.N)
        self.title_label.pack(side=tk.BOTTOM, expand=True, anchor=tk.S)
        self.title_line1.pack(side=tk.TOP)

        # === Animate Title & Subtitle ===
        # time between frames, in milliseconds
        DELTA_TIME: int = 200

        # anim_frames contains id of all 95 (frame 0 - 94) frames of the animation
        self.anim_frames: list[str] = []

        # queue frames 0 - 11: animating title
        self.anim_frames.append(self.root.after(DELTA_TIME * 0, lambda: self.title_label.config(foreground="Black")))
        self.anim_frames.append(self.root.after(DELTA_TIME * 1, lambda: self.title_label.config(width=8, foreground="Sea Green1")))
        self.anim_frames.append(self.root.after(DELTA_TIME * 2, lambda: self.title_label.config(width=11)))
        self.anim_frames.append(self.root.after(DELTA_TIME * 3, lambda: self.title_label.config(width=19)))
        self.anim_frames.append(self.root.after(DELTA_TIME * 4, lambda: self.title_label.config(width=25)))
        self.anim_frames.append(self.root.after(DELTA_TIME * 5, lambda: self.title_label.config(width=34)))
        self.anim_frames.append(self.root.after(DELTA_TIME * 6, lambda: self.title_label.config(width=42)))
        self.anim_frames.append(self.root.after(DELTA_TIME * 7, lambda: self.title_label.config(width=50)))
        self.anim_frames.append(self.root.after(DELTA_TIME * 8, lambda: self.title_label.config(width=56)))
        self.anim_frames.append(self.root.after(DELTA_TIME * 9, lambda: self.title_label.config(width=65)))
        self.anim_frames.append(self.root.after(DELTA_TIME * 10, lambda: self.title_label.config(width=74)))
        self.anim_frames.append(self.root.after(DELTA_TIME * 11, lambda: self.title_label.config(width=82)))

        # frames 12 - 94: animating subtitle
        # loop iterates 82 times since it's the number of chars (excluding space) in the subtitle
        for frame in range(0, 83):
            self.anim_frames.append(
                self.root.after(
                    DELTA_TIME * (frame + 11),
                    lambda _frame=frame: self.subtitle_label.config(
                        text=SUBTITLE[:_frame] + "_" * min(1, 82 - _frame) + " " * (81 - _frame))
                )
            )

        # disables the close window button
        self.root.protocol("WM_DELETE_root", self.exit)

        # set the window to the correct resolution
        self.root.title(ver)
        self.root.geometry(self.settings.MENU_DIM)
        self.root.config(background="Black")

    def to_submenu(self, is_pvc: bool):
        # stop all queued frames of the title animation
        for frame in self.anim_frames:
            self.root.after_cancel(frame)

        for widget in self.root.winfo_children():
            widget.destroy()

        self.settings.is_pvc = is_pvc
        SubMenu(self.root, self.settings)

    def exit(self: "MainMenu | SubMenu | GameMenu"):
        messagebox.showinfo("Afterword",
                            "Thank you for playing TIC-TAC-TOE!\n\nI independently spent over a year building and updating this app.\n\nIn this project, I designed the AI that finds the highest win probability, arranged the GUI elements in the most ergonomic way, optimized the algorithms, fixed bugs, and learned tkinter.\n\nHope you enjoyed it!")

        self.root.destroy()


def default_label():
    messagebox.showinfo("label",
                        "Ah, just like the good ol\' one you played in kindergarten...\n\nYou can select a board length between 2 and... infinity! Boards larger than 3x3 only needs 4 in a row to win!\n\nThe starting player will be X, and the other will be O. No friends? No worries! You can play with 1 of 3 unique AIs designed by me and my friend.")


def time_help():
    messagebox.showinfo("label",
                        "At the start, you can set a time limit for each player. Each player will have that amount of time to complete the game.\n\nBut not so fast - you will earn 1 extra second after each move!\n\n(other details are same as the Traditional mode)")


def vanish_label():
    messagebox.showinfo("label",
                        "Once you placed the minimum number of X/O you need to win, your oldest move will disappear!\n\nBad memory? You can enable \'next vanishing move\' to see them highlighted in yellow. You can also make your moves last longer by changing the \'remain for\' slider.\n\n(other details are same as the Traditional mode)")


def snake_label():
    messagebox.showinfo("label",
                        "In your first move, you can place wherever you want. Afterwards, you can only place around your previous move - the head of the snake. Watch where your snake is going, as turning back can take some time.\n\nIf you accidentally get trapped in a dead end, you can continue at your last move before being trapped. I recommend playing this on a 7x7 or larger board.\n\n(other details are same as the Traditional mode)")


class SubMenu:
    root: tk.Tk
    settings: Settings

    def __init__(self, root: tk.Tk, settings: Settings):
        self.root = root
        self.settings = settings
        self.title = tk.Button(
            self.root,
            state=tk.DISABLED,
            takefocus=False,
            borderwidth=0,
            background="Black",
            disabledforeground="Sea Green1",
            text="\nChoose a Mode",
            font=self.settings.SUBMENU_FONT
        )
        self.default_button = tk.Button(
            self.root,
            text="Traditional",
            cursor="hand2",
            overrelief=tk.SUNKEN,
            command=lambda: self.to_gamemenu(GameMenu),
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=25,
            font=self.settings.MENU_FONT,
            borderwidth=5
        )
        self.default_help_button = tk.Button(
            self.root,
            bitmap="question",
            cursor="question_arrow",
            overrelief=tk.SUNKEN,
            command=default_label,
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=30,
            borderwidth=5
        )
        self.time_button = tk.Button(
            self.root,
            text="Timed Trial",
            cursor="hand2",
            overrelief=tk.SUNKEN,
            command=lambda: self.to_gamemenu(GameMenuT),
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=25,
            font=self.settings.MENU_FONT,
            borderwidth=5
        )
        self.time_help_button = tk.Button(
            self.root,
            bitmap="question",
            cursor="question_arrow",
            overrelief=tk.SUNKEN,
            command=time_help,
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=30,
            borderwidth=5
        )
        self.vanish_button = tk.Button(
            self.root,
            text="Vanishing Moves",
            cursor="hand2",
            overrelief=tk.SUNKEN,
            command=lambda: self.to_gamemenu(GameMenuV),
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=25,
            font=self.settings.MENU_FONT,
            borderwidth=5
        )
        self.vanish_help_button = tk.Button(
            self.root,
            bitmap="question",
            cursor="question_arrow",
            overrelief=tk.SUNKEN,
            command=vanish_label,
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=30,
            borderwidth=5
        )
        self.snake_button = tk.Button(
            self.root,
            text="Snake",
            cursor="hand2",
            overrelief=tk.SUNKEN,
            command=lambda: self.to_gamemenu(GameMenuS),
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=25,
            font=self.settings.MENU_FONT,
            borderwidth=5
        )
        self.snake_help_button = tk.Button(
            self.root,
            bitmap="question",
            cursor="question_arrow",
            overrelief=tk.SUNKEN,
            command=snake_label,
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=30,
            borderwidth=5
        )
        self.non_mode_frame = tk.Frame(
            self.root,
            background="Black",
            width=25
        )
        self.back_button = tk.Button(
            self.non_mode_frame,
            text="Back",
            cursor="hand2",
            overrelief=tk.SUNKEN,
            command=self.to_mainmenu,
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=12,
            font=self.settings.MENU_FONT,
            borderwidth=5
        )
        self.settings_button = tk.Button(
            self.non_mode_frame,
            text=u"\u2699",
            cursor="hand2",
            overrelief=tk.SUNKEN,
            command=self.to_settings,
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=12,
            font=("TkFixedFont", 13, "bold"),
            borderwidth=5
        )

        # disables the close window button
        self.root.protocol("WM_DELETE_root", lambda: MainMenu.exit(self))

        # center buttons horizontally by giving a weight to all columns except the ones with the button
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        self.title.grid(row=0, column=1, columnspan=2)
        self.default_button.grid(row=1, column=1)
        self.default_help_button.grid(row=1, column=2)
        self.time_button.grid(row=2, column=1)
        self.time_help_button.grid(row=2, column=2)
        self.vanish_button.grid(row=3, column=1)
        self.vanish_help_button.grid(row=3, column=2)
        self.snake_button.grid(row=4, column=1)
        self.snake_help_button.grid(row=4, column=2)
        self.non_mode_frame.grid(row=5, column=1, columnspan=2, pady=25)
        self.back_button.pack(side=tk.LEFT, padx=(1, 18))
        self.settings_button.pack(side=tk.LEFT, padx=(18, 1))

    def to_gamemenu(self, mode: type["GameMenu"]):
        for widget in self.root.winfo_children():
            widget.destroy()

        mode(self.root, self.settings)

    def to_mainmenu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        MainMenu(self.root, self.settings)

    def to_settings(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ColMenu(self.root, self.settings)


class ColMenu:
    """
    :ivar col_frames: index 0 stores LabelFrame for general features; index 1 for X features; index 2 for O features
    :ivar col_entries: index 0 stores colors for general features; index 1 for X features; index 2 for O features
    """
    root: tk.Tk
    settings: Settings
    col_frames: list
    col_entries: list[dict]

    def __init__(self, root: tk.Tk, settings: Settings):
        self.root = root
        self.settings = settings
        self.title = tk.Button(
            self.root,
            state=tk.DISABLED,
            takefocus=False,
            borderwidth=0,
            background="Black",
            disabledforeground="Sea Green1",
            text="Settings",
            font=self.settings.SUBMENU_FONT
        )
        self.col_frames = [
            tk.LabelFrame(
                self.root,
                text="General",
                font=self.settings.COLOR_FONT,
                foreground="Sea Green1",
                background="Black",
                borderwidth=3,
                relief=tk.RIDGE,
                takefocus=False
            ),
            tk.LabelFrame(
                self.root,
                text="X colors",
                font=self.settings.COLOR_FONT,
                foreground="Sea Green1",
                background="Black",
                borderwidth=3,
                relief=tk.RIDGE,
                takefocus=False
            ),
            tk.LabelFrame(
                self.root,
                text="O colors",
                font=self.settings.COLOR_FONT,
                foreground="Sea Green1",
                background="Black",
                borderwidth=3,
                relief=tk.RIDGE,
                takefocus=False
            )
        ]
        self.exit_button = tk.Button(
            self.root,
            text="Save and Exit",
            cursor="hand2",
            overrelief=tk.SUNKEN,
            command=self.to_submenu,
            activeforeground="white",
            activebackground="Sea Green",
            background="Sea Green1",
            foreground="Black",
            width=25,
            font=self.settings.MENU_FONT,
            borderwidth=5
        )
        self.col_frames[1].grid(row=0, column=1, pady=(10, 5))
        self.col_frames[2].grid(row=0, column=2, pady=(10, 5))
        self.col_frames[0].grid(row=1, column=1, columnspan=2, pady=5)
        self.exit_button.grid(row=2, column=1, columnspan=2, pady=10)

        self.col_entries = [{}, {}, {}]

        for plyr, feats in enumerate(self.settings.colors):  # plyr = general, X, O
            for row, (feat, color) in enumerate(feats.items()):
                col_label = tk.Label(
                    self.col_frames[plyr],
                    text=feat,
                    font=self.settings.MENU_FONT,
                    foreground="Sea Green1",
                    background="Black",
                    takefocus=False)
                col_entry = tk.Entry(
                    self.col_frames[plyr],
                    textvariable=tk.StringVar(value=color),
                    borderwidth=1,
                    font=self.settings.MENU_FONT,
                    cursor="xterm",
                    foreground="Black",
                    background=color)

                col_label.grid(row=row, column=0, padx=10)
                col_entry.grid(row=row, column=1)

                # make the key release event update bg of textbox
                col_entry.bind("<KeyRelease>", lambda _, _plyr=plyr, _feat=feat: self.update_col(_plyr, _feat))
                self.col_entries[plyr][feat] = col_entry

    def update_col(self, plyr: 1 | 2, feat: str):
        try:
            # try to set background color of the text widget
            self.col_entries[plyr][feat].config(bg=self.col_entries[plyr][feat].get())

        except tk.TclError:
            # if the color is not valid
            pass

    def to_submenu(self):
        # save colors
        for plyr, feats in enumerate(self.col_entries):
            for feat, entry in feats.items():
                try:
                    self.root.winfo_rgb(entry.get())
                    self.settings.colors[plyr][feat] = entry.get()

                except tk.TclError:
                    messagebox.askretrycancel("Settings", f"Please enter a valid color for {feat}!")
                    return

        if messagebox.showinfo("Settings", f"Your settings have been updated!\n\n{self.settings.colors}"):
            for widget in self.root.winfo_children():
                widget.destroy()

            SubMenu(self.root, self.settings)


class LoadMenu:
    def __init__(self, root: tk.Tk, parent: "GameMenu"):
        self.parent = parent
        self.toplevel = tk.Toplevel(
            root,
            background=parent.settings.colors[0]["foreground"]
        )
        self.board_label = tk.Label(
            self.toplevel,
            text="Board in base10",
            background=parent.settings.colors[0]["foreground"],
            takefocus=False
        )
        self.board_entry = tk.Entry(
            self.toplevel,
            cursor="xterm",
            width=30
        )
        self.board_entry.bind("<Return>", self.validate)

        self.note_label = tk.Label(
            self.toplevel,
            text="Note: Will not check for winner on load.",
            background=parent.settings.colors[0]["foreground"],
            takefocus=False
        )
        self.submit_button = tk.Button(
            self.toplevel,
            text="Submit",
            background=parent.settings.colors[0]["foreground"],
            cursor="hand2",
            relief=tk.GROOVE,
            overrelief=tk.SUNKEN,
            width=10,
            borderwidth=4,
            command=self.validate
        )

        self.board_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 0))
        self.board_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 0))
        self.note_label.grid(row=1, column=0, columnspan=2, padx=(10, 5), sticky=tk.W)
        self.submit_button.grid(row=2, columnspan=2, pady=5)
        self.toplevel.title("Load")
        self.toplevel.resizable(False, False)
        self.board_entry.focus_force()

    def validate(self, _=None):
        try:
            # try to convert board_entry to int
            if self.parent.new_game(int(self.board_entry.get())):
                self.parent.new_game_button.config(state=tk.NORMAL)
                self.toplevel.destroy()

        except ValueError:
            # if board_entry is not int
            messagebox.askretrycancel("Warning", "Please enter an integer!")


class GameMenu:
    """
    :ivar board: base10 integer representing a base3 number. Each base3 digit is a square on board. Last digit is player.
    :ivar moves: contains moves bot is allowed to search
    :ivar moved: contains previous moves, in chronological order (front = earlier; back = later)
    """

    def __init__(self, root: tk.Tk, settings: Settings):
        self.root: tk.Tk = root
        self.settings: Settings = settings
        self.root.bind("<Configure>", self.update_scrollbars)  # update_scrollbars when window is resized
        self.root.bind("<MouseWheel>", self.scroll_vertical)  # scroll canvas vertically when any part of window has mouse wheel input
        self.root.bind("<Shift-MouseWheel>", self.scroll_horizontal)  # scroll canvas horizontally when any part of window has mouse wheel input

        tt.set_consts(self.settings.board_len.get(), self.settings.win_len.get())

        self.board: int = tt.EMPTY_BOARD
        self.moves: list[int] = []
        self.moved: list[int] = []
        self.board_buttons: list[tk.Button] = []

        self.settings_frame = tk.Frame(
            self.root,
            background=self.settings.colors[0]["foreground"]
        )
        self.toolbar_frame = tk.Frame(
            self.settings_frame,
            background=self.settings.colors[0]["background"]
        )
        self.handle_frame = tk.Frame(
            self.root,
            background=self.settings.colors[0]["background"]
        )
        self.board_frame = tk.Frame(
            self.root,
            background=self.settings.colors[0]["background"]
        )
        self.board_canvas = tk.Canvas(
            self.board_frame,
            background=self.settings.colors[0]["background"],
            highlightthickness=0
        )
        self.h_scrollbar = tk.Scrollbar(
            self.root,
            background=self.settings.colors[0]["background"],
            activebackground=self.settings.colors[0]["background"],
            troughcolor=self.settings.colors[0]["foreground"],
            orient=tk.HORIZONTAL,
            command=self.board_canvas.xview
        )
        self.v_scrollbar = tk.Scrollbar(
            self.root,
            background=self.settings.colors[0]["background"],
            activebackground=self.settings.colors[0]["background"],
            troughcolor=self.settings.colors[0]["foreground"],
            orient=tk.VERTICAL,
            command=self.board_canvas.yview
        )
        self.board_canvas.config(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        self.button_frame = tk.Frame(
            self.board_canvas,
            relief=tk.GROOVE,
            background=self.settings.colors[0]["background"],
            borderwidth=8
        )
        self.turn_labels: list[tk.Label | None] = [
            None,
            # index 1 is X's
            tk.Label(
                self.board_frame,
                text="X turn",
                font=self.settings.TURN_FONT,
                foreground=self.settings.colors[1]["char"],
                width=13,
                borderwidth=5,
                relief=tk.RIDGE,
                takefocus=False
            ),
            # index 2 is O's
            tk.Label(
                self.board_frame,
                text="O turn",
                font=self.settings.TURN_FONT,
                foreground=self.settings.colors[2]["char"],
                width=13,
                borderwidth=5,
                relief=tk.RIDGE,
                takefocus=False
            )
        ]
        self.back_button = tk.Button(
            self.toolbar_frame,
            text="Back",
            font=self.settings.TOOLBAR_FONT,
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["foreground"],
            cursor="hand2",
            relief=tk.GROOVE,
            overrelief=tk.SUNKEN,
            command=self.to_submenu,
            width=6,
            borderwidth=5
        )
        self.new_game_button = tk.Button(
            self.toolbar_frame,
            text="Replay",
            font=self.settings.TOOLBAR_FONT,
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["foreground"],
            cursor="hand2",
            relief=tk.GROOVE,
            overrelief=tk.SUNKEN,
            state=tk.DISABLED,
            command=lambda: self.new_game(tt.EMPTY_BOARD),
            width=6,
            borderwidth=5
        )
        self.load_button = tk.Button(
            self.toolbar_frame,
            text="Load",
            font=self.settings.TOOLBAR_FONT,
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["foreground"],
            cursor="hand2",
            relief=tk.GROOVE,
            overrelief=tk.SUNKEN,
            command=lambda: LoadMenu(self.root, self),
            width=6,
            borderwidth=5
        )
        self.hide_button = tk.Button(
            self.handle_frame,
            text="❮",
            font=self.settings.TOOLBAR_FONT,
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["foreground"],
            cursor="hand2",
            relief=tk.FLAT,
            command=self.toggle_settings,
            height=4
        )
        self.board_len_label = tk.Label(
            self.settings_frame,
            background=self.settings.colors[0]["foreground"],
            text="\nBoard length",
            takefocus=False
        )
        self.board_len_slider = tk.Scale(
            self.settings_frame,
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["foreground"],
            troughcolor=self.settings.colors[0]["background"],
            highlightthickness=0,
            orient=tk.HORIZONTAL,
            variable=self.settings.board_len,
            length=100,
            from_=3,
            to=19,
            cursor="sb_h_double_arrow",
            command=self.update_len
        )
        self.win_len_label = tk.Label(
            self.settings_frame,
            background=self.settings.colors[0]["foreground"],
            text="\nWin length",
            takefocus=False
        )
        self.win_len_slider = tk.Scale(
            self.settings_frame,
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["foreground"],
            troughcolor=self.settings.colors[0]["background"],
            highlightthickness=0,
            orient=tk.HORIZONTAL,
            variable=self.settings.win_len,
            length=100,
            from_=min(tt.BOARD_LEN, 5),
            to=tt.BOARD_LEN,
            cursor="sb_h_double_arrow",
            command=lambda win_len: tt.set_consts(tk_win_len=int(win_len))  # val is automatically passed by slider when it changes and is a str
        )
        self.board_zoom_label = tk.Label(
            self.settings_frame,
            text="\nZoom",
            background=self.settings.colors[0]["foreground"],
            takefocus=False
        )
        self.board_zoom_slider = tk.Scale(
            self.settings_frame,
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["foreground"],
            troughcolor=self.settings.colors[0]["background"],
            highlightthickness=0,
            orient=tk.HORIZONTAL,
            variable=self.settings.board_zoom,
            length=100,
            from_=4,
            to=13,
            cursor="sb_h_double_arrow",
            command=self.update_zoom
        )
        self.bot_first_checkbox = tk.Checkbutton(
            self.settings_frame,
            text="Computer starts first",
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["background"],
            selectcolor=self.settings.colors[0]["background"],
            cursor="hand2",
            command=self.bot_first
        )
        self.ai_dropdown = tk.OptionMenu(
            self.settings_frame,
            self.settings.ai_type,
            *(item.value for item in AI)
        )
        self.ai_dropdown.config(
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["foreground"],
            highlightthickness=0,
            cursor="hand2",
            relief=tk.GROOVE,
            borderwidth=4,
            width=max(len(ai.value) for ai in AI) - 3,
            takefocus=True
        )

        self.is_dropdown_open: bool = False
        self.ai_dropdown["menu"].config(
            # activebackground=self.settings.colors[0]["foreground"],
            background=self.settings.colors[0]["background"],
            cursor="hand2",
            postcommand=self.open_dropdown
        )
        self.root.bind("<Button-1>", self.close_dropdown)

        self.graph_checkbox = tk.Checkbutton(
            self.settings_frame,
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["background"],
            selectcolor=self.settings.colors[0]["background"],
            cursor="hand2",
            variable=self.settings.has_graph
        )
        self.log_checkbox = tk.Checkbutton(
            self.settings_frame,
            text="Show log and indexes",
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["background"],
            selectcolor=self.settings.colors[0]["background"],
            cursor="hand2",
            variable=self.settings.has_log_n_ind,
            command=self.update_log_n_ind
        )
        self.log = tk.Text(
            self.settings_frame,
            background=self.settings.colors[0]["background"],
            wrap=tk.NONE,
            relief=tk.RIDGE,
            borderwidth=2,
            height=15,
            width=27
        )
        self.log.bind("<Key>", lambda event: None if event.keysym in ("Up", "Down", tk.LEFT, tk.RIGHT) else "break")  # disable all user inputs in log except arrow keys
        self.log.bind("<Control-c>", lambda _: self.log.event_generate("<<Copy>>"))  # explicitly enable copy
        self.log.bind("<Control-a>", lambda _: self.log.event_generate("<<SelectAll>>"))  # explicitly enable select all

        self.root.config(background=self.settings.colors[0]["background"])
        self.settings_frame.pack(side=tk.LEFT, expand=False, fill=tk.Y)
        self.handle_frame.pack(side=tk.LEFT, expand=False, fill=tk.Y)
        self.board_frame.pack(side=tk.LEFT, expand=True, fill=tk.NONE)
        self.settings_frame.grid_columnconfigure(0, minsize=16)  # left padding
        self.settings_frame.grid_columnconfigure(3, minsize=16)  # right padding
        self.settings_frame.grid_rowconfigure(11, weight=1)  # ensures log's row (row 11) can expand
        self.toolbar_frame.grid(row=0, column=0, columnspan=3, pady=(0, 16), sticky=tk.W)

        # configure row and column weights to divide the vertical and horizontal space evenly
        self.board_frame.grid_rowconfigure(2, weight=1)
        self.board_frame.grid_columnconfigure(0, weight=1)
        self.board_frame.grid_columnconfigure(1, weight=1)

        self.turn_labels[1].grid(row=0, column=0, columnspan=2, pady=(5, 0))
        self.turn_labels[2].grid(row=1, column=0, columnspan=2, pady=(0, 5))
        self.board_canvas.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW)
        self.board_canvas.create_window(
            (0, 0),
            window=self.button_frame,
            anchor=tk.NW
        )

        self.back_button.pack(side=tk.LEFT)
        self.new_game_button.pack(side=tk.LEFT)
        self.load_button.pack(side=tk.LEFT)
        self.hide_button.pack(side=tk.LEFT, padx=(0, 10))
        self.board_len_label.grid(row=4, column=1, sticky=tk.E)
        self.board_len_slider.grid(row=4, column=2)
        self.win_len_label.grid(row=5, column=1, sticky=tk.E)
        self.win_len_slider.grid(row=5, column=2)
        self.board_zoom_label.grid(row=6, column=1, sticky=tk.E)
        self.board_zoom_slider.grid(row=6, column=2, pady=(0, 8))
        if self.settings.is_pvc:
            self.bot_first_checkbox.grid(columnspan=2, row=7, column=1, pady=(0, 8))
            self.ai_dropdown.grid(columnspan=2, row=8, column=1, pady=(0, 8))
        self.graph_checkbox.grid(columnspan=2, row=9, column=1, pady=(0, 8))
        self.log_checkbox.grid(columnspan=2, row=10, column=1, pady=(0, 8))

        self.__init_child__()  # must be before update_zoom() & after init all widgets since see GameMenuT

        self.update_graph_type()
        self.update_len()  # init buttons
        self.update_turn()  # init turn labels
        self.update_zoom()  # init fonts
        self.update_log_n_ind()  # in case has_log_n_ind setting is on from last time

        # rebinds the close window button
        self.root.protocol("WM_DELETE_root", lambda: MainMenu.exit(self))

    def __init_child__(self):
        pass

    def toggle_settings(self):
        if self.settings_frame.winfo_ismapped():
            self.settings_frame.pack_forget()
            self.hide_button.config(text="❯")
        else:
            self.settings_frame.pack(side="left", fill="y", before=self.handle_frame)
            self.hide_button.config(text="❮")

    def open_dropdown(self):
        def keep_dropdown_raised():
            if self.is_dropdown_open:
                self.ai_dropdown.config(relief=tk.RAISED)
                self.root.after(0, keep_dropdown_raised)
            else:
                self.ai_dropdown.config(relief=tk.GROOVE)
                self.update_graph_type()

        self.is_dropdown_open = True
        keep_dropdown_raised()

    def close_dropdown(self, _):
        self.is_dropdown_open = False

    def update_graph_type(self):
        if self.settings.ai_type.get() == AI.RECUR_PROB:
            self.graph_checkbox.config(text="Show search histogram\n(impacts performance)")
        else:
            self.graph_checkbox.config(text="Show search tree\n(impacts performance)")

    def scroll_vertical(self, event):
        self.board_canvas.yview_scroll(-1 * (event.delta // 120), tk.UNITS)

    def scroll_horizontal(self, event):
        self.board_canvas.xview_scroll(-1 * (event.delta // 120), tk.UNITS)

    def update_scrollbars(self, *_):
        """
        1. Resize board_canvas to the size of button_frame.
        2. Update the scrollregion to match the new button_frame size.
        3. Show/hide scrollbars based on whether the new canvas size is smaller/larger than the button_frame.
        """
        bbox: tuple[int, int, int, int] = self.board_canvas.bbox(tk.ALL)  # bbox = x1, y1, x2, y2. bbox size is the same as button_frame size

        # update canvas width and height to bbox width and height +7 padding
        self.board_canvas.config(width=bbox[2] - bbox[0] + 7, height=bbox[3] - bbox[1] + 7)

        # update scrollregion
        self.board_canvas.config(scrollregion=bbox)

        # if button_frame size overflows horizontally
        if bbox[2] > self.board_canvas.winfo_width():
            # show h_scrollbar; pack order of h_scrollbar MUST be before board_frame
            self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X, before=self.board_frame)
        else:
            self.h_scrollbar.pack_forget()

        # if button_frame size overflows vertically
        if bbox[3] > self.board_canvas.winfo_height():
            # show v_scrollbar; pack order of v_scrollbar MUST be before board_frame
            self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, before=self.board_frame)
        else:
            self.v_scrollbar.pack_forget()

    def update_log_n_ind(self):
        """
        1. Show / hide log.
        2. Show / hide indexes.
        3. Highlight / unhighlight moves.
        :return:
        """
        if self.settings.has_log_n_ind.get() is True:
            self.log.grid(columnspan=2, row=11, column=1, pady=0, padx=0, sticky=tk.NSEW)

            for sq, button in enumerate(self.board_buttons):  # DO NOT use set.difference(moved) as moved is cleared when game ends
                # if empty
                if not tt.plyr_at(self.board, sq):
                    button.config(text=sq)

                    if sq in self.moves:
                        button.config(background=self.settings.colors[0]["bot_moves"])

        else:
            self.log.grid_forget()

            for sq, button in enumerate(self.board_buttons):

                if not tt.plyr_at(self.board, sq):
                    button.config(text='')

                    if sq in self.moves:
                        button.config(background=self.settings.colors[0]["board_button"])

        self.root.update_idletasks()

    def update_len(self, _=None):
        """
        1. Update backend constants.
        2. Create / destory buttons to match new BOARD_AREA.
        3. Position new and old buttons.
        """
        # 1.
        tt.set_consts(tk_board_len=self.settings.board_len.get())
        self.log.insert(tk.END, "Cleared win table\n\n")

        # 2.
        # create buttons if BOARD_AREA increased
        while len(self.board_buttons) < tt.BOARD_AREA:
            self.board_buttons.append(
                tk.Button(
                    self.button_frame,
                    font=self.settings.board_font,
                    foreground=self.settings.colors[0]["index"],
                    background=self.settings.colors[0]["board_button"],
                    activebackground=self.settings.colors[0]["board_button"],
                    cursor="plus",
                    overrelief=tk.RIDGE,
                    command=lambda sq=len(self.board_buttons): self.place(sq),
                    width=3,
                    borderwidth=5,
                    state=tk.NORMAL
                )
            )

        # destroy buttons if BOARD_AREA decreased
        for button in self.board_buttons[tt.BOARD_AREA:]:
            button.destroy()
        self.board_buttons = self.board_buttons[:tt.BOARD_AREA]

        # 3.
        for sq, button in enumerate(self.board_buttons):
            button.grid(row=sq // tt.BOARD_LEN, column=sq % tt.BOARD_LEN)

        # update win_len since X always win if it is shorter. No need to update backend win_len since the slider's command will.
        self.win_len_slider.config(from_=min(tt.BOARD_LEN, 5), to=tt.BOARD_LEN)
        self.update_log_n_ind()
        self.update_scrollbars()
        self.root.update_idletasks()

    def update_zoom(self, _=None):
        self.settings.board_font = (
            "Helvetica",
            self.settings.board_zoom.get() * 4,
            "bold" if self.settings.board_zoom.get() > 4 else "normal"  # bold font when board_zoom <= 4 makes button not square
        )

        for button in self.board_buttons:
            # button scales automatically with font size
            button.config(font=self.settings.board_font)

    def insert_log(self):
        self.log.insert(
            tk.END,
            f"Move: {self.moves[-1] if self.moves else None}\n" +
            f"Last player: {tt.plyr_of(self.board)}\n" +
            f"Board: {self.board}\n" +
            f"Moved size: {len(self.moved)}\n" +
            f"Win table size: {len(tt.win_table)}\n\n"
        )
        self.log.see(tk.END)

    def lock_settings(self):
        self.board_len_slider.config(state=tk.DISABLED)
        self.board_len_label.config(state=tk.DISABLED)
        self.win_len_slider.config(state=tk.DISABLED)
        self.win_len_label.config(state=tk.DISABLED)
        self.new_game_button.config(state=tk.NORMAL)
        self.bot_first_checkbox.config(state=tk.DISABLED)

    def lock_board(self):
        for button in self.board_buttons:
            button.config(state=tk.DISABLED)

    def unlock_board(self):
        for sq, button in enumerate(self.board_buttons):
            if not tt.plyr_at(self.board, sq):
                button.config(state=tk.NORMAL)

    def bot_first(self) -> None:
        self.lock_settings()

        # don't need multithreading since random move
        self.place_bot()

        # check even if first move since first move can win with loaded boards
        self.check_winner_pvc(True)

    def place(self, sq: int) -> None:
        self.moved.append(sq)
        self.place_plyr()

        if self.settings.is_pvc is True:
            # if first move
            if len(self.moved) == 1:
                self.lock_settings()
            else:
                self.board_buttons[self.moved[-2]].config(background=self.settings.colors[0]["board_button"])  # unhighlight last bot move

            # check even if first move since first move can win with loaded boards
            if not self.check_winner_pvc(False):
                threading.Thread(target=self.place_bot, daemon=True).start()
                self.log.insert(tk.END, "Spawn new thread\n\n")

        else:  # pvp
            if len(self.moved) == 1:
                self.lock_settings()

            self.check_winner_pvp()

    def place_bot(self):
        self.lock_board()

        move: int | None = None

        # if bot starts second or loaded board
        if self.moved:

            # choose ai
            ai: "collections.Iterator[int] | int"
            params: tuple
            if self.settings.ai_type.get() == AI.RECUR_SNAKE.value:
                ai = tt.snake_search

                # if bot never placed before but human has
                # set y0, x0, to human's so bot place adjacent to human
                if len(self.moved) == 1:
                    params = (
                        self.board,
                        *divmod(self.moved[-1], tt.BOARD_LEN),
                        *divmod(self.moved[-1], tt.BOARD_LEN),
                        True,
                        nx.DiGraph() if self.settings.has_graph.get() else None
                    )

                # if bot placed before
                else:
                    params = (
                        self.board,
                        *divmod(self.moved[-2], tt.BOARD_LEN),
                        *divmod(self.moved[-1], tt.BOARD_LEN),
                        True,
                        nx.DiGraph() if self.settings.has_graph.get() else None
                    )

            else:
                self.moves = tt.sort_moves(self.board, self.moved[-1])
                preprune_len: int = len(self.moves)

                if self.settings.ai_type.get() == AI.RECUR_AND_OR.value:
                    self.moves = self.moves[:17]  # test shows can only search 16 squares in reasonable time
                    ai = tt.recur_search
                    params = (self.board, self.moves, True, nx.DiGraph() if self.settings.has_graph.get() else None)

                elif self.settings.ai_type.get() == AI.ITER_AND_OR.value:
                    self.moves = self.moves[:17]
                    ai = tt.iter_search
                    params = (self.board, set(self.moves), nx.DiGraph() if self.settings.has_graph.get() else None)

                elif self.settings.ai_type.get() == AI.RECUR_PROB.value:
                    self.moves = self.moves[:10]
                    ai = tt.prob_ai
                    params = (self.board, self.moves, self.settings.has_graph.get())

                self.log.insert(tk.END, f"Moves:\n{self.moves}\n\n")
                self.log.see(tk.END)

            for next_move in ai(*params):
                # if game ends from external control
                if not self.is_game_on:
                    return

                if move is not None:
                    # unhighlight previous move
                    self.board_buttons[move].config(background=self.settings.colors[0]["bot_moves" if self.settings.has_log_n_ind.get() else "board_button"])

                # highlight current move. When the loop ends, square remains highlighted.
                self.board_buttons[next_move].config(background=self.settings.colors[0]["bot_move"])
                self.root.update_idletasks()
                move = next_move

            # if move is None:
            #     self.end_game()
            #     messagebox.showinfo("Outcome", "Computer resigns.\n\nBot: 'I have already computed my inevitable fate ...'")
            #     return

            if preprune_len != len(self.moves):
                tt.win_table.clear()  # unusable next time since board shape changed
                self.log.insert(tk.END, "Cleared Win Table\n\n")

        # if bot starts first
        else:
            move = random.randint(0, tt.BOARD_AREA - 1)
            self.moves.append(move)  # allow update_log_n_ind() to unhighlight this move next turn

        self.moved.append(move)
        self.board = tt.place(self.board, move)
        self.board_buttons[move].config(
            text=tt.char_of(tt.plyr_of(self.board)),
            disabledforeground=self.settings.colors[tt.plyr_of(self.board)]["char"],
            background=self.settings.colors[0]["bot_move"],
            state=tk.DISABLED
        )
        self.insert_log()
        self.check_winner_pvc(True)
        self.unlock_board()
        return

    def place_plyr(self):
        self.board = tt.place(self.board, self.moved[-1])

        self.board_buttons[self.moved[-1]].config(
            text=tt.char_of(tt.plyr_of(self.board)),
            disabledforeground=self.settings.colors[tt.plyr_of(self.board)]["char"],
            background=self.settings.colors[0]["board_button"],  # unhighlight in case this is previously in moves
            state=tk.DISABLED
        )
        self.insert_log()

    def check_winner_pvc(self, is_bot: bool) -> bool:
        """
        1. Check if the LAST move won, and show who and how.
        2. Updates turn labels if no player won.
        :return: whether any player won.
        """
        dir: str | None = tt.win_dir(self.board, self.moved[-1])
        if dir is not None:
            self.end_game()

            if is_bot:
                if messagebox.askyesno("Outcome", f"Computer won {dir}!\n\nBot: 'Shouldn\'t humans be smarter?'") is True:
                    self.new_game(tt.EMPTY_BOARD)
                return True

            else:
                if messagebox.askyesno("Outcome", f"You won {dir}!\n\nBot: 'NOT MY DIGNITY! LET US HAVE ANOTHER DUEL!'") is True:
                    self.new_game(tt.EMPTY_BOARD)
                return True

        else:
            # if no one win
            # if board is full
            if len(self.moved) == tt.BOARD_AREA:
                self.end_game()
                if messagebox.askyesno("Outcome", "Ended in draw.\n\nBot: 'You\'ll never win ... not satisfied? new_game!'") is True:
                    self.new_game(tt.EMPTY_BOARD)
                return True

            else:
                # if board is not full
                self.update_turn()
                return False

    def check_winner_pvp(self) -> bool:
        """See :func:`check_winner_pvc()`"""
        dir: str | None = tt.win_dir(self.board, self.moved[-1])
        if dir is not None:
            self.end_game()
            messagebox.showinfo("Outcome", f"Player \'{tt.char_of(tt.plyr_of(self.board))}\' won {dir}!")
            return True

        else:
            # if no one win
            # if board is full
            if len(self.moved) == tt.BOARD_AREA:
                self.end_game()
                messagebox.showinfo("Outcome", "Ended in a draw.")
                return True

            # if board is not full
            else:
                self.update_turn()
                return False

    def update_turn(self) -> None:
        # disable current player's label
        self.turn_labels[tt.plyr_of(self.board)].config(
            foreground="SystemDisabledText",
            relief=tk.FLAT
        )
        # enable opponent's label
        self.turn_labels[tt.opp_of(tt.plyr_of(self.board))].config(
            foreground=self.settings.colors[tt.opp_of(tt.plyr_of(self.board))]["char"],
            relief=tk.RIDGE
        )

    def is_game_on(self) -> bool:
        return bool(self.moved)

    def end_game(self):
        self.moved.clear()  # empty moved signals endgame
        self.lock_board()

    def to_submenu(self) -> bool:
        if messagebox.askyesno("Confirmation", "Are you sure you want to quit?\n\nYou will lose all your progress."):
            self.moved.clear()
            self.root.unbind("<Configure>")
            self.root.unbind("<MouseWheel>")
            self.root.unbind("<Shift-MouseWheel>")

            for widget in self.root.winfo_children():
                widget.destroy()

            # set window to the SubMenu resolution & color
            self.root.geometry(self.settings.MENU_DIM)
            self.root.config(background="Black")
            SubMenu(self.root, self.settings)
            return True

        return False

    def new_game(self, board: int) -> bool:
        if not self.is_game_on() or messagebox.askyesno(
                "Confirmation",
                "Are you sure you want to restart?\n\nYou will lose all your progress."):  # if game is going, ask user

            if self.moved:
                self.board_buttons[self.moved[-1]].config(background=self.settings.colors[0]["foreground"])  # unhighlight last bot move

            # if no last player in loaded board
            if not tt.plyr_of(board):
                messagebox.askretrycancel("Warning", "Please enter a board with last player!")
                return False

            self.board = board
            self.moves.clear()
            self.moved.clear()
            self.unlock_board()

            for sq, button in enumerate(self.board_buttons):
                plyr: 1 | 2 = tt.plyr_at(self.board, sq)

                # if not empty
                if plyr:
                    button.config(
                        text=tt.char_of(plyr),
                        disabledforeground=self.settings.colors[plyr]["char"],
                        state=tk.DISABLED
                    )
                    # place move from loaded board into moved[]
                    self.moved.append(sq)

                else:
                    button.config(disabledforeground=self.settings.colors[plyr]["index"])

                button.config(background=self.settings.colors[0]["board_button"])  # unhighlight in case this is previously in moves

            self.update_turn()
            self.update_log_n_ind()

            # unlock settings
            self.board_len_label.config(state=tk.NORMAL)
            self.board_len_slider.config(state=tk.NORMAL)
            self.win_len_label.config(state=tk.NORMAL)
            self.win_len_slider.config(state=tk.NORMAL)
            self.new_game_button.config(state=tk.DISABLED)
            self.bot_first_checkbox.config(state=tk.NORMAL)
            self.bot_first_checkbox.deselect()

            self.log.insert(tk.END, f"Reset game menu\n\n")
            self.insert_log()
            self.log.see(tk.END)
            return True

        return False


class GameMenuT(GameMenu):
    """
    :ivar label_scale: Inflation of the active timer, used for animation. Resets to 0 at the beginning of each turn.
    :ivar time: How much time each player still has: index 1 is X's; index 2 is O's.
    """

    def __init__(self, root: tk.Tk, settings: Settings):
        self.label_scale: int = 0
        self.next_countdown: str | None = None

        super().__init__(root, settings)

    def __init_child__(self):
        self.time = [
            None,
            tk.DoubleVar(value=self.settings.INIT_TIME),
            tk.DoubleVar(value=self.settings.INIT_TIME)
        ]
        # noinspection PyTypeChecker
        self.trace1 = self.time[1].trace_add("write", lambda *_: self.validate(1))
        # noinspection PyTypeChecker
        self.trace2 = self.time[2].trace_add("write", lambda *_: self.validate(2))

        # change widget class of turn_labels from Label to LabelFrame
        self.turn_labels[1].destroy()
        self.turn_labels[2].destroy()
        self.turn_labels = [
            None,
            tk.LabelFrame(
                self.board_frame,
                text="X turn",
                font=self.settings.TURN_FONT,
                foreground=self.settings.colors[1]["char"],
                borderwidth=5,
                relief=tk.RIDGE,
                takefocus=False
            ),
            tk.LabelFrame(
                self.board_frame,
                text="O turn",
                font=self.settings.TURN_FONT,
                foreground=self.settings.colors[2]["char"],
                borderwidth=5,
                relief=tk.RIDGE,
                takefocus=False
            )
        ]
        self.time_entry = [
            None,
            # index 1 is X's
            tk.Entry(
                self.turn_labels[1],
                width=5,
                borderwidth=1,
                foreground=self.settings.colors[1]["char"],
                disabledforeground=self.settings.colors[1]["char"],
                disabledbackground=self.settings.colors[0]["background"],
                justify="center",
                textvariable=self.time[1]
            ),
            # index 2 is O's
            tk.Entry(
                self.turn_labels[2],
                width=5,
                borderwidth=1,
                foreground=self.settings.colors[2]["char"],
                disabledforeground=self.settings.colors[2]["char"],
                disabledbackground=self.settings.colors[0]["background"],
                justify="center",
                textvariable=self.time[2]
            )
        ]

        self.turn_labels[1].grid(row=0, column=0, sticky=tk.E)  # stick to the right edge of column 1
        self.turn_labels[2].grid(row=0, column=1, sticky=tk.W)  # stick to the left edge of column 2
        self.time_entry[1].pack()
        self.time_entry[2].pack()

    def update_zoom(self, _=None):
        super().update_zoom()

        self.settings.time_font = ("Courier", self.settings.board_zoom.get() * 3 + 2, "bold")
        self.time_entry[1].config(font=self.settings.time_font)
        self.time_entry[2].config(font=self.settings.time_font)

    def lock_settings(self):
        super().lock_settings()

        self.time_entry[1].config(state=tk.DISABLED)
        self.time_entry[2].config(state=tk.DISABLED)
        self.countdown()

    def validate(self, plyr: 1 | 2):
        try:
            # try to convert the remain time to float
            self.time[plyr].get()

        except tk.TclError:
            # if the remain time is not float, show a messagebox and reset the value
            messagebox.askretrycancel("Warning", f"Please enter a decimal number for {tt.char_of(plyr)}!")
            self.time[plyr].set(self.settings.INIT_TIME)

    def countdown(self):
        """Recursively decrement time."""
        time: float = self.time[tt.opp_of(tt.plyr_of(self.board))].get()

        if time > 0.0:
            # animate inflate of the current plyr's timer
            # max scale must be odd number for ease-out
            self.label_scale = min(self.label_scale + 2, 5)
            self.time_entry[tt.opp_of(tt.plyr_of(self.board))].config(
                font=("Courier", self.settings.board_zoom.get() * 3 + 2 + self.label_scale, "bold")
            )

            # if X has under 5 secs left
            if time < 5.0:
                # flash the timer
                if time % 1 < 0.4:
                    self.time_entry[tt.opp_of(tt.plyr_of(self.board))].config(
                        relief=tk.SUNKEN,
                        disabledbackground=self.settings.colors[0]["background"],
                    )
                else:
                    self.time_entry[tt.opp_of(tt.plyr_of(self.board))].config(
                        relief=tk.GROOVE,
                        disabledbackground="yellow"
                    )
            self.root.update_idletasks()

            # decrease the time value by 0.1 every 100ms and display only 1 decimal point using round().
            # DO NOT decrease by 1 every 1000ms as it slows down the whole app.
            self.time[tt.opp_of(tt.plyr_of(self.board))].set(round(time - 0.1, 1))
            self.next_countdown = self.root.after(100, self.countdown)

        # if player runs out of time, opponent wins and stop recursion
        else:
            messagebox.showinfo("Outcome", f"Time's up! Player {tt.char_of(tt.plyr_of(self.board))} won!")
            self.end_game()
            return

    def update_turn(self):
        """
        Overload to include disable timer entry, switch timer and add bonus time.
        """
        self.label_scale = 0  # reset inflate animation

        super().update_turn()

        # disable and reset size of current plyr's timer
        self.time_entry[tt.plyr_of(self.board)].config(
            relief=tk.FLAT,
            disabledforeground="SystemDisabledText",
            disabledbackground=self.settings.colors[0]["background"],
            font=self.settings.time_font
        )
        # enable next plyr's timer
        self.time_entry[tt.opp_of(tt.plyr_of(self.board))].config(
            relief=tk.SUNKEN,
            disabledforeground=self.settings.colors[tt.opp_of(tt.plyr_of(self.board))]["char"],
            disabledbackground="white"
        )
        # current plyr gets bonus time
        self.time[tt.plyr_of(self.board)].set(self.time[tt.plyr_of(self.board)].get() + 1)

    def place_bot(self):
        threading.Thread(target=super().place_bot, daemon=True).start()

    def end_game(self):
        super().end_game()

        # stop player's countdown & timer flash
        self.root.after_cancel(self.next_countdown)

    def to_submenu(self):
        if super().to_submenu():
            self.time[1].trace_remove("write", self.trace1)
            self.time[2].trace_remove("write", self.trace2)
            if self.next_countdown is not None:
                self.root.after_cancel(self.next_countdown)

    def new_game(self, board: int):
        if super().new_game(board):
            self.time_entry[1].config(font=self.settings.time_font, state=tk.NORMAL)
            self.time_entry[2].config(font=self.settings.time_font, state=tk.NORMAL)
            self.time[1].set(self.settings.INIT_TIME)
            self.time[2].set(self.settings.INIT_TIME)
            # reset time_entry inflation
            self.update_zoom()
            self.root.after_cancel(self.next_countdown)


class GameMenuV(GameMenu):
    """
    :ivar remain_steps: how many steps into the future will an X/O last.
    :ivar show_nxt_vanish_move: show/hide which move is going to vanish in the next turn.
    """

    def __init__(self, root: tk.Tk, settings: Settings):
        super().__init__(root, settings)
        self.remain_steps = tk.IntVar()
        self.show_nxt_vanish_move = tk.BooleanVar(value=False)

        self.remain_stps_label = tk.Label(
            self.settings_frame,
            text="\nRemain for",
            takefocus=False
        )
        self.remain_count_slider = tk.Scale(
            self.settings_frame,
            background=self.settings.colors[0]["background"],
            activebackground=self.settings.colors[0]["background"],
            troughcolor=self.settings.colors[0]["foreground"],
            orient=tk.HORIZONTAL,
            variable=self.remain_steps,
            length=100,
            from_=tt.WIN_LEN,
            to=tt.WIN_LEN * 2,
            cursor="sb_h_double_arrow"
        )
        self.nxt_vanish_checkbox = tk.Checkbutton(
            self.settings_frame,
            text="Show next vanishing move",
            background=self.settings.colors[0]["background"],
            activebackground=self.settings.colors[0]["background"],
            selectcolor=self.settings.colors[0]["background"],
            cursor="hand2",
            variable=self.show_nxt_vanish_move,
            command=self.del_moves
        )

        self.remain_stps_label.grid(row=2, column=1)
        self.remain_count_slider.grid(row=2, column=2)
        self.nxt_vanish_checkbox.grid(columnspan=2, row=3, column=1)

    def del_moves(self):
        # if half of the total num of moves by X + O > remain_steps: X's moves start to vanish.
        vanish_sq: int
        if len(self.moved) / 2 > self.remain_steps.get():
            self.log.insert(tk.END, f"Vanish order:\n{self.moved}")  # log.see(END) not needed here

            vanish_sq = self.moved.pop(0)

            self.board = tt.unplace(self.board, vanish_sq)
            self.board_buttons[vanish_sq].config(
                text='',
                background=self.settings.colors[0]["foreground"],
                state=tk.NORMAL
            )

        # if half of the total num of moves by X + O is one less before vanishing begins: tint the 2 oldest moves about to vanish.
        if self.show_nxt_vanish_move.get() is True and len(self.moved) / 2 >= self.remain_steps.get():
            self.board_buttons[self.moved[1]].config(background=self.settings.colors[0]["nxt_vanish_move"])
            self.board_buttons[self.moved[0]].config(background=self.settings.colors[0]["nxt_vanish_move"])

    def update_len(self, _=None):
        super().update_len()
        self.remain_count_slider.config(from_=tt.WIN_LEN, to=tt.WIN_LEN * 2)

    def check_winner_pvc(self, is_bot: bool) -> bool:
        self.del_moves()
        return super().check_winner_pvc(is_bot)

    def check_winner_pvp(self) -> bool:
        self.del_moves()
        return super().check_winner_pvp()


class GameMenuS(GameMenu):
    """
    :ivar root, board_len, win_len, board_zoom, colors, is_pvp: same as SubMenu
    :ivar prev_inputs: index 1 contains the (x, y) of all previous moves made by X in chronological order  (front = earlier; back = later); index 2 contains O's
    """
    prev_inputs: list[list[int] | None]

    def __init__(self, root: tk.Tk, settings: Settings):
        super().__init__(root, settings)
        self.prev_inputs = [None, [], []]
        self.board_len_slider.config(from_=4)  # TODO: X always win if board_len is shorter? The slider will automatically call update_len to update cross-file vars.
        self.win_len_slider.config(from_=min(tt.BOARD_LEN // 2 + 1, 3))
        self.settings.win_len.set(tt.WIN_LEN)  # TODO reassign as calling superclass __init__ changes tk win_len?
        self.settings.ai_type.set(AI.RECUR_SNAKE.value)
        self.load_button.destroy()

    def update_len(self, _=None):
        super().update_len()
        self.win_len_slider.config(from_=min(tt.BOARD_LEN // 2 + 1, 3))

    def update_turn(self):
        """
        Overload to include:
         1. Enable empty adjacent buttons around the opponent's last move and disable all other buttons.
         2. Trace back to the last square that has valid adjacent squares if the head square is stuck
        """

        def get_adj(y: int, x: int) -> set:
            """
            Enable valid adjacent buttons around the previous input of opponent.
            :return: Set containing the valid adjacent squares around the previous input of opp_ofonent.
            """
            adjs = set()

            for x1, y1 in tt.snake_gen_moves(self.board, y, x):
                sq = tt.sq_of(y1, x1)
                self.board_buttons[sq].config(state=tk.NORMAL, relief=tk.RAISED)
                adjs.add(sq)

            if not adjs:  # if next player is stuck
                # recursively go back to previous input
                self.prev_inputs[tt.opp_of(tt.plyr_of(self.board))].pop()
                prev_input = self.prev_inputs[tt.opp_of(tt.plyr_of(self.board))][-1]
                adjs = get_adj(*divmod(prev_input, tt.BOARD_LEN))

            return adjs

        super().update_turn()

        # color the new head
        self.board_buttons[self.moved[-1]].config(
            background=self.settings.colors[tt.plyr_of(self.board)]["snake_head"]
        )
        if self.prev_inputs[tt.plyr_of(self.board)]:
            # change the previous head color to body color
            self.board_buttons[self.prev_inputs[tt.plyr_of(self.board)][-1]].config(
                background=self.settings.colors[tt.plyr_of(self.board)]["snake_body"]
            )

        self.prev_inputs[tt.plyr_of(self.board)].append(self.moved[-1])

        adjs: set = get_adj(*divmod(self.prev_inputs[tt.opp_of(tt.plyr_of(self.board))][-1], tt.BOARD_LEN))
        for sq in set(range(tt.BOARD_AREA)).difference(self.moved, adjs):  # disable buttons that are empty and not adjacent to input
            self.board_buttons[sq].config(state=tk.DISABLED, relief=tk.SUNKEN)


def to_changelog():
    messagebox.showinfo("Changelog", """
v1 : Added the basics: player vs player, infinite board length, winner check, etc...\n
v2 : Boards are now stored as single list instead of dictionary. Changes player input from index number to x,y coordinates. Rebuild the entire code to process this new file format.\n
v3 : Added basic AI. Added console GUI. Make boards that are 7*7 or larger needs only half the board length to win.\n
v4 : Added board pruning for boards larger than 3x3 to reduce AI calculations. Added some randomization to the moves made by the AI. Restructured the entire AI code for optimization.\n
v5 : Added deathtrap check - that's the hardest part of this project! Now the AI is 100% unbeatable for a 3x3 board. Added the option to let AI start first.\n
v6 : Make board pruning only for boards larger than 5x5. Added land-filling to boards larger than 3x3. Added a matplotlib display for AI's Risk Analysis.\n
v7 : Added Tkinter GUI. Rebuild winner check for HUGE optimization. Changed every code to user-def function. Added user-friendly log window.\n
v8 : HUGE OPTIMIZATION: Rebuild the board pruning code to combine both pruning and land-filling into 1 function. Pruned board and main board now have the same dimension - no additional function is needed to convert squares between the two boards!\n
v9 : Rebuild and tidy up all GUI code using class instead of user-def functions. Rebuild to make board pruning dynamic, it can now scale up if that area has not enough empty squares. Added 'new_game' button. Changed empty squares from '[ ]' to ' '. Fixed bug where the endpoint of checking diagonally from top right to down left doesn't move with the start point.\n
v10: Added title animation. Added 4 modes: Traditional, Time Trial, Vanishing Moves, Snake\n
v11: Globalised colors for each feature. Added color self.settings. Changed O's snake color. Capped length to win at 4. Added 'Total Child Count' to log.
v12: Redesign the algorithm to use depth-first search instead of breadth-first-search. Build a specialized, faster check winner algo that only checks for whether a specific player wins, instead of checking who wins.\n
v13: Prunner V2
v14: Prunner V3, Shayan's Algo.
v15: GUI Revamp
v16, v17, v18: see GitHub\n
    """)


if __name__ == "__main__":
    ver = "Tic Tac Toe v18"

    root = tk.Tk()
    MainMenu(root, Settings())
    root.mainloop()
