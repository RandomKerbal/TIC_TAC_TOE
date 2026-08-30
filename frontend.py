"""
Compile command:
    pyinstaller --onefile --windowed --optimize 2 frontend.py
"""

import math
import random
import sys
import threading
import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.collections import PathCollection
from matplotlib.container import BarContainer
from matplotlib.font_manager import FontProperties
from matplotlib.legend import Legend
from matplotlib.patches import Patch
from matplotlib.path import Path
from matplotlib.text import Text
from matplotlib.textpath import TextPath
from matplotlib.ticker import MultipleLocator
from matplotlib.transforms import IdentityTransform, Affine2D, Bbox

import backend as tt


class Settings:
    """Settings persist across menus."""

    RECUR_AI_NAME: str = "Recursive And-Or AI"
    ITER_AI_NAME: str = "Iterative And-Or AI"
    PROB_AI_NAME: str = "Recursive Probability AI"
    SNAKE_AI_NAME: str = "Recursive Snake AI"
    AI_NAMES: tuple[str, str, str, str] = (RECUR_AI_NAME, ITER_AI_NAME, PROB_AI_NAME, SNAKE_AI_NAME)
    SHOW_QFRONT_TEXT = "Show queue front"
    DEFAULT_TIME: float = 10
    MAX_TIME_ENTRY_SCALE: int = 5  # odd number for ease-out effect
    MIN_BOARD_LEN: int = 3
    MAX_NODE_FRAME: int = 8

    # matplotlib colors, not tkinter
    NODE_COLORS: dict[int | None, str] = {
        -tt.WIN_SCORE: "Tomato",
        0: "Yellow",
        tt.WIN_SCORE: "MediumSpringGreen",
        None: "White"
    }
    NODE_SIZE: float = 70.0
    EDGE_ALPHA: float = 0.75
    WINDOW_DIM: str = "700x420"
    MENU_FONT: tuple[str, int] = ("FixedSys", 15)
    MENU_LABEL_CFG: dict = {
        "background": "Black",
        "foreground": "Sea Green1"
    }
    MENU_BUTTON_CFG: dict = {
        "font": MENU_FONT,
        "cursor": "hand2",
        "overrelief": tk.SUNKEN,
        "activeforeground": "White",
        "activebackground": "Sea Green",
        "background": "Sea Green1",
        "foreground": "Black",
        "borderwidth": 5
    }
    COLOR_FRAME_CFG: dict = {
        "font": ("FixedSys", 20, "bold"),
        "foreground": "Sea Green1",
        "background": "Black",
        "borderwidth": 3,
        "relief": tk.RIDGE
    }

    def __init__(self):
        self.board_len: tk.IntVar = tk.IntVar(value=self.MIN_BOARD_LEN)
        self.win_len: tk.IntVar = tk.IntVar(value=self.MIN_BOARD_LEN)
        self.board_zoom: tk.IntVar = tk.IntVar(value=5)
        self.ai_type: tk.StringVar = tk.StringVar(value=Settings.RECUR_AI_NAME)
        self.show_ind_and_aimoves: tk.BooleanVar = tk.BooleanVar(value=False)
        self.queue_len: tk.IntVar = tk.IntVar(value=self.MIN_BOARD_LEN)
        self.show_qfront: tk.BooleanVar = tk.BooleanVar(value=False)
        self.is_pvc: bool = True
        self.board_font: tuple[str, int, str] = ('', 0, '')
        self.time_font: tuple[str, int, str] = ('', 0, '')
        self.colors: list[dict] = [
            # general features
            {
                "index": "gray",
                "new_move": "Sea Green1",
                "ai_moves": "Dark Sea Green1",
                "board_button": "HoneyDew2",
                "background": "HoneyDew2",
                "foreground": "Sea Green2",
                "qfront": "Yellow"
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
                "snake_body": "Dark Slate Gray1"
            }
        ]
        self.toolbar_button_cfg: dict = {
            "font": ("Helvetica", 10),
            "background": self.colors[0]["foreground"],
            "activebackground": self.colors[0]["background"],
            "cursor": "hand2",
            "relief": tk.GROOVE,
            "overrelief": tk.SUNKEN,
            "width": 6,
            "borderwidth": 5
        }
        self.slider_cfg: dict = {
            "background": self.colors[0]["foreground"],
            "activebackground": self.colors[0]["foreground"],
            "troughcolor": self.colors[0]["background"],
            "highlightthickness": 0,
            "orient": tk.HORIZONTAL,
            "length": 100,
            "cursor": "sb_h_double_arrow"
        }
        self.checkbox_cfg: dict = {
            "background": self.colors[0]["foreground"],
            "activebackground": self.colors[0]["background"],
            "selectcolor": self.colors[0]["background"],
            "cursor": "hand2"
        }
        self.turn_label_cfg: dict = {
            "font": ("Helvetica", 10, "bold"),
            "foreground": self.colors[1]["char"],
            "background": self.colors[0]["background"],
            "borderwidth": 5,
            "relief": tk.RIDGE
        }


class MainMenu:

    def __init__(self, root: tk.Tk, settings: Settings):
        self.root: tk.Tk = root
        self.settings: Settings = settings
        self.line1 = tk.Label(
            self.root,
            text='=' * 999,
            font="TkFixedFont",
            **Settings.MENU_LABEL_CFG
        )
        self.line2 = tk.Label(
            self.root,
            text='=' * 999,
            font="TkFixedFont",
            **Settings.MENU_LABEL_CFG
        )
        self.title_label = tk.Label(
            self.root,
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
            **Settings.MENU_LABEL_CFG
        )
        self.subtitle_label = tk.Label(
            self.root,
            font="TkFixedFont",
            justify=tk.LEFT,
            **Settings.MENU_LABEL_CFG
        )
        SUBTITLE = "   99% Made by CZY           4 Original Modes               4 Distinct AIs        "

        self.pvc_button = tk.Button(
            self.root,
            text="Single Player",
            command=lambda: self.to_submenu(True),
            **Settings.MENU_BUTTON_CFG
        )
        self.pvp_button = tk.Button(
            self.root,
            text="Multi Player",
            command=lambda: self.to_submenu(False),
            **Settings.MENU_BUTTON_CFG
        )
        self.changelog_button = tk.Button(
            self.root,
            text="Changelog",
            command=changelog,
            **Settings.MENU_BUTTON_CFG
        )
        self.exit_button = tk.Button(
            self.root,
            text="Exit",
            command=self.exit,
            **Settings.MENU_BUTTON_CFG
        )
        self.exit_button.pack(side=tk.BOTTOM, fill=tk.X)
        self.changelog_button.pack(side=tk.BOTTOM, fill=tk.X)
        self.pvp_button.pack(side=tk.BOTTOM, fill=tk.X)
        self.pvc_button.pack(side=tk.BOTTOM, fill=tk.X)
        self.line2.pack(side=tk.BOTTOM, fill=tk.X)
        self.subtitle_label.pack(side=tk.BOTTOM, expand=True, anchor=tk.N, fill=tk.X)
        self.title_label.pack(side=tk.BOTTOM, expand=True, anchor=tk.S)
        self.line1.pack(side=tk.TOP, fill=tk.X)

        # === Animate Title & Subtitle ===
        # time between frames, in milliseconds
        DT: int = 200

        # anim_frames contain id of all 95 (frame 0 - 94) frames of the animation
        self.anim_frames: list[str] = []

        # frames 0 - 11: animating title
        self.anim_frames.append(self.root.after(DT * 0, lambda: self.title_label.config(width=1)))  # width=0 doesn't work
        self.anim_frames.append(self.root.after(DT * 1, lambda: self.title_label.config(width=8)))
        self.anim_frames.append(self.root.after(DT * 2, lambda: self.title_label.config(width=11)))
        self.anim_frames.append(self.root.after(DT * 3, lambda: self.title_label.config(width=19)))
        self.anim_frames.append(self.root.after(DT * 4, lambda: self.title_label.config(width=25)))
        self.anim_frames.append(self.root.after(DT * 5, lambda: self.title_label.config(width=34)))
        self.anim_frames.append(self.root.after(DT * 6, lambda: self.title_label.config(width=42)))
        self.anim_frames.append(self.root.after(DT * 7, lambda: self.title_label.config(width=50)))
        self.anim_frames.append(self.root.after(DT * 8, lambda: self.title_label.config(width=56)))
        self.anim_frames.append(self.root.after(DT * 9, lambda: self.title_label.config(width=65)))
        self.anim_frames.append(self.root.after(DT * 10, lambda: self.title_label.config(width=74)))
        self.anim_frames.append(self.root.after(DT * 11, lambda: self.title_label.config(width=82)))

        # frames 12 - 94: animating subtitle
        # loop iterates 82 times since it's the number of chars (excluding space) in the subtitle
        for frame in range(0, 83):
            self.anim_frames.append(
                self.root.after(
                    DT * (frame + 11),
                    lambda _frame=frame: self.subtitle_label.config(
                        text=SUBTITLE[:_frame] + "_" * min(1, 82 - _frame) + " " * (81 - _frame))
                )
            )

        # disables the close window button
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

        self.root.title(VERSION_TEXT)
        self.root.geometry(Settings.WINDOW_DIM)
        self.root.config(background="Black")

    def to_submenu(self, IS_PVC: bool) -> None:
        """
        :param IS_PVC: is player versus computer.
        """
        # stop all queued frames of the title animation
        for frame in self.anim_frames:
            self.root.after_cancel(frame)

        for widget in self.root.winfo_children():
            widget.destroy()

        self.settings.is_pvc = IS_PVC
        SubMenu(self.root, self.settings)

    def exit(self: "MainMenu | SubMenu | GameMenu") -> None:
        messagebox.showinfo("Afterword",
                            "Thank you for playing TIC-TAC-TOE!\n\nI independently spent over a year building and updating this app.\n\nIn this project, I developed the AI that finds the highest win probability, arranged the GUI elements in the most ergonomic way, optimized the algorithms, fixed bugs, and learned tkinter.\n\nHope you enjoyed it!")
        self.root.destroy()


class SubMenu:

    def __init__(self, root: tk.Tk, settings: Settings):
        self.root: tk.Tk = root
        self.settings: Settings = settings
        self.title_label = tk.Label(
            self.root,
            text="\nChoose a Mode",
            font=("FixedSys", 25, "bold", "underline"),
            **Settings.MENU_LABEL_CFG
        )
        self.default_button = tk.Button(
            self.root,
            text="Traditional",
            width=25,
            command=lambda: self.to_gamemenu(GameMenu),
            **Settings.MENU_BUTTON_CFG
        )
        self.default_help_button = tk.Button(
            self.root,
            bitmap="question",
            height=28,
            width=32,
            command=default_help,
            **Settings.MENU_BUTTON_CFG
        )
        self.time_button = tk.Button(
            self.root,
            text="Timed Trial",
            width=25,
            command=lambda: self.to_gamemenu(GameMenuT),
            **Settings.MENU_BUTTON_CFG
        )
        self.time_help_button = tk.Button(
            self.root,
            bitmap="question",
            height=28,
            width=32,
            command=time_help,
            **Settings.MENU_BUTTON_CFG
        )
        self.vanish_button = tk.Button(
            self.root,
            text="Vanishing Moves",
            width=25,
            command=lambda: self.to_gamemenu(GameMenuV),
            **Settings.MENU_BUTTON_CFG
        )
        self.vanish_help_button = tk.Button(
            self.root,
            bitmap="question",
            height=28,
            width=32,
            command=vanish_help,
            **Settings.MENU_BUTTON_CFG
        )
        self.snake_button = tk.Button(
            self.root,
            text="Snake",
            width=25,
            command=lambda: self.to_gamemenu(GameMenuS),
            **Settings.MENU_BUTTON_CFG
        )
        self.snake_help_button = tk.Button(
            self.root,
            bitmap="question",
            height=28,
            width=32,
            command=snake_help,
            **Settings.MENU_BUTTON_CFG
        )
        self.bottom_frame = tk.Frame(
            self.root,
            background="Black",
            width=25
        )
        self.back_button = tk.Button(
            self.bottom_frame,
            text="Back",
            command=self.to_mainmenu,
            width=12,
            **Settings.MENU_BUTTON_CFG
        )
        self.settings_button = tk.Button(
            self.bottom_frame,
            text="⚙",
            command=self.to_settings,
            width=11,
            font=("FixedSys", 13, "bold"),
            **dict(item for item in Settings.MENU_BUTTON_CFG.items() if item[0] != "font")
        )

        # disables the close window button
        self.root.protocol("WM_DELETE_WINDOW", lambda: MainMenu.exit(self))

        # center buttons horizontally by giving same weight to all columns except the ones with the button
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        self.title_label.grid(row=0, column=1, pady=(0, 25), columnspan=2)
        self.default_button.grid(row=1, column=1)
        self.default_help_button.grid(row=1, column=2)
        self.time_button.grid(row=2, column=1)
        self.time_help_button.grid(row=2, column=2)
        self.vanish_button.grid(row=3, column=1)
        self.vanish_help_button.grid(row=3, column=2)
        self.snake_button.grid(row=4, column=1)
        self.snake_help_button.grid(row=4, column=2)
        self.bottom_frame.grid(row=5, column=1, columnspan=2, pady=25)
        self.back_button.pack(side=tk.LEFT, padx=(1, 18))
        self.settings_button.pack(side=tk.LEFT, padx=(18, 1))

    def to_gamemenu(self, mode: type['GameMenu']) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

        mode(self.root, self.settings)

    def to_mainmenu(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

        MainMenu(self.root, self.settings)

    def to_settings(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

        ColMenu(self.root, self.settings)


class ColMenu:
    """
    :ivar color_frames: index 0 stores LabelFrame for general features; index 1 for X features; index 2 for O features
    :ivar color_entries: index 0 stores colors for general features; index 1 for X features; index 2 for O features
    """

    def __init__(self, root: tk.Tk, settings: Settings):
        self.root: tk.Tk = root
        self.settings: Settings = settings
        self.color_frames: tuple = (
            tk.LabelFrame(
                self.root,
                text="General",
                **Settings.COLOR_FRAME_CFG
            ),
            tk.LabelFrame(
                self.root,
                text="X colors",
                **Settings.COLOR_FRAME_CFG
            ),
            tk.LabelFrame(
                self.root,
                text="O colors",
                **Settings.COLOR_FRAME_CFG
            )
        )
        self.exit_button = tk.Button(
            self.root,
            text="Save and Exit",
            width=25,
            command=self.to_submenu,
            **Settings.MENU_BUTTON_CFG
        )
        self.color_frames[1].grid(row=0, column=1, pady=(10, 5))
        self.color_frames[2].grid(row=0, column=2, pady=(10, 5))
        self.color_frames[0].grid(row=1, column=1, columnspan=2, pady=5)
        self.exit_button.grid(row=2, column=1, columnspan=2, pady=10)

        self.color_entries: list[dict] = [dict(), dict(), dict()]
        color_label: tk.Label
        color_entry: tk.Entry

        for plyr, feats in enumerate(self.settings.colors):  # plyr = general, X, O
            for row, (feat, color) in enumerate(feats.items()):
                color_label = tk.Label(
                    self.color_frames[plyr],
                    text=feat,
                    font=Settings.MENU_FONT,
                    **Settings.MENU_LABEL_CFG
                )
                color_entry = tk.Entry(
                    self.color_frames[plyr],
                    textvariable=tk.StringVar(value=color),
                    borderwidth=1,
                    font=Settings.MENU_FONT,
                    cursor="xterm",
                    foreground="Black",
                    background=color
                )

                color_label.grid(row=row, column=0, padx=10)
                color_entry.grid(row=row, column=1)

                # make the key release event update bg of textbox
                color_entry.bind("<KeyRelease>", lambda _, _plyr=plyr, _feat=feat: self.update_color(_plyr, _feat))
                self.color_entries[plyr][feat] = color_entry

    def update_color(self, PLYR: int, FEAT: str) -> None:
        try:
            # try to set background color of the text widget
            self.color_entries[PLYR][FEAT].config(bg=self.color_entries[PLYR][FEAT].get())

        except tk.TclError:
            # if the color is not valid
            pass

    def to_submenu(self) -> None:
        # save colors
        for plyr, feats in enumerate(self.color_entries):
            for feat, entry in feats.items():
                try:
                    self.root.winfo_rgb(entry.get())
                    self.settings.colors[plyr][feat] = entry.get()

                except tk.TclError:
                    messagebox.askretrycancel("Settings", f"Enter a valid color for {feat}!")
                    return

        if messagebox.showinfo("Settings", f"Your settings have been updated!\n\n{self.settings.colors}"):
            for widget in self.root.winfo_children():
                widget.destroy()

            SubMenu(self.root, self.settings)


class LoadMenu:

    def __init__(self, parent: 'GameMenu'):
        self.parent: GameMenu = parent
        self.toplevel = tk.Toplevel(
            parent.root,
            background=parent.settings.colors[0]["foreground"]
        )
        self.board_label = tk.Label(
            self.toplevel,
            text="Board in base10",
            background=parent.settings.colors[0]["foreground"],
        )
        self.board_entry = tk.Entry(
            self.toplevel,
            background=parent.settings.colors[0]["background"],
            cursor="xterm",
            width=30
        )
        self.board_entry.bind("<Return>", self.validate)

        self.note_label = tk.Label(
            self.toplevel,
            text="Will not check for winner on load.",
            background=parent.settings.colors[0]["foreground"]
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

    def validate(self, _=None) -> None:
        try:
            # try to convert board_entry to int
            if self.parent.new_game(int(self.board_entry.get())):
                self.parent.new_game_button.config(state=tk.NORMAL)
                self.toplevel.destroy()

        except ValueError:
            # if board_entry is not int
            messagebox.askretrycancel("Warning", "Enter an integer!")


class GameMenu:
    """
    :ivar board: base10 integer representing a base3 number. Each base3 digit is a square on board. Last digit is player.
    :ivar moved: contain previous moves in chronological order: front = earlier, back = later
    :ivar ai_moves: contain moves that AI is allowed to search
    """

    def __init__(self, root: tk.Tk, settings: Settings):
        self.root: tk.Tk = root
        self.settings: Settings = settings
        self.root.bind("<Configure>", self.update_scrollbars)  # update_scrollbars when resize window
        self.root.bind("<MouseWheel>", self.scroll_vertical)  # scroll canvas vertically when any part of window has mouse wheel input
        self.root.bind("<Shift-MouseWheel>", self.scroll_horizontal)  # scroll canvas horizontally when any part of window has mouse wheel input

        tt.set_consts(self.settings.board_len.get(), self.settings.win_len.get())

        self.board: int = tt.EMPTY_BOARD
        self.moved: list[int | None] = []
        self.board_buttons: list[tk.Button] = []
        self.ai_moves: list[int] = []
        self.ai_thread: threading.Thread | None = None
        self.graph: nx.DiGraph | dict[int, float] | None = None
        self.textpaths: list[TextPath] = []

        self.settings_frame = tk.Frame(
            self.root,
            background=self.settings.colors[0]["foreground"],
            relief=tk.RAISED,
            borderwidth=4
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
        self.turn_labels: list[tk.Label | tk.LabelFrame | None] = [
            None,
            # index 1 is X's
            tk.Label(
                self.board_frame,
                text="X turn",
                width=13,
                **self.settings.turn_label_cfg
            ),
            # index 2 is O's
            tk.Label(
                self.board_frame,
                text="O turn",
                width=13,
                **self.settings.turn_label_cfg
            )
        ]
        self.back_button = tk.Button(
            self.toolbar_frame,
            text="Back",
            command=self.to_submenu,
            **self.settings.toolbar_button_cfg
        )
        self.new_game_button = tk.Button(
            self.toolbar_frame,
            text="Replay",
            state=tk.DISABLED,
            command=lambda: self.new_game(tt.EMPTY_BOARD),
            **self.settings.toolbar_button_cfg
        )
        self.load_button = tk.Button(
            self.toolbar_frame,
            text="Load",
            command=lambda: LoadMenu(self),
            **self.settings.toolbar_button_cfg
        )
        self.cheat_button = tk.Button(
            self.toolbar_frame,
            text="Cheat",
            command=self.ai_play,
            **self.settings.toolbar_button_cfg
        )
        self.hide_button = tk.Button(
            self.handle_frame,
            text="❮",
            font=Settings.MENU_FONT,
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["foreground"],
            cursor="hand2",
            height=5,
            relief=tk.RAISED,
            borderwidth=4,
            command=self.toggle_settings,
        )
        self.board_len_label = tk.Label(
            self.settings_frame,
            background=self.settings.colors[0]["foreground"],
            text="\nBoard length"
        )
        self.board_len_slider = tk.Scale(
            self.settings_frame,
            variable=self.settings.board_len,
            from_=Settings.MIN_BOARD_LEN,
            to=19,
            command=self.update_len,
            **self.settings.slider_cfg
        )
        self.win_len_label = tk.Label(
            self.settings_frame,
            background=self.settings.colors[0]["foreground"],
            text="\nWin length"
        )
        self.win_len_slider = tk.Scale(
            self.settings_frame,
            variable=self.settings.win_len,
            **self.settings.slider_cfg,

            # new value is automatically passed by slider when it changes
            # cast since new value is str
            command=lambda win_len: tt.set_consts(TK_WIN_LEN=int(win_len))
        )
        self.board_zoom_label = tk.Label(
            self.settings_frame,
            background=self.settings.colors[0]["foreground"],
            text="\nZoom"
        )
        self.board_zoom_slider = tk.Scale(
            self.settings_frame,
            variable=self.settings.board_zoom,
            from_=4,
            to=13,
            command=self.update_zoom,
            **self.settings.slider_cfg
        )
        self.ai_first_checkbox = tk.Checkbutton(
            self.settings_frame,
            text="AI starts first",
            command=self.ai_play,
            **self.settings.checkbox_cfg
        )
        self.ai_dropdown = tk.OptionMenu(
            self.settings_frame,
            self.settings.ai_type,
            *Settings.AI_NAMES
        )
        self.ai_dropdown.config(
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["foreground"],
            highlightthickness=0,
            cursor="hand2",
            relief=tk.GROOVE,
            borderwidth=4,
            width=len(max(Settings.AI_NAMES, key=len)) - 3
        )

        self.is_dropdown_open: bool = False
        self.ai_dropdown["menu"].config(
            background=self.settings.colors[0]["background"],
            cursor="hand2",
            postcommand=self.open_dropdown
        )
        self.root.bind("<Button-1>", self.close_dropdown)

        self.graph_button = tk.Button(
            self.settings_frame,
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["background"],
            cursor="hand2",
            relief=tk.GROOVE,
            borderwidth=4,
            width=len(max(Settings.AI_NAMES, key=len)) - 1,
            command=self.print_graph
        )
        self.ind_checkbox = tk.Checkbutton(
            self.settings_frame,
            text="Show indexes & AI moves",
            variable=self.settings.show_ind_and_aimoves,
            command=self.update_ind_and_aimoves_buttons,
            **self.settings.checkbox_cfg
        )
        self.log = tk.Text(
            self.settings_frame,
            background=self.settings.colors[0]["background"],
            wrap=tk.NONE,
            relief=tk.SUNKEN,
            borderwidth=4,
            height=15,
            width=27,
            takefocus=False  # log cause focus to stuck
        )
        self.log_clear = tk.Button(
            self.log,
            background=self.settings.colors[0]["background"],
            activebackground=self.settings.colors[0]["background"],
            text="🗑",
            command=lambda: self.log.delete("1.0", tk.END),
            borderwidth=0,
            cursor="hand2"
        )
        self.log.tag_config("X_TURN_TAG", foreground=self.settings.colors[1]["char"])
        self.log.tag_config("O_TURN_TAG", foreground=self.settings.colors[2]["char"])
        self.log.bind("<Key>", lambda event: None if event.keysym in ("Up", "Down", tk.LEFT, tk.RIGHT) else "break")  # disable all user inputs in log except arrow keys
        self.log.bind("<Control-c>", lambda _: self.log.event_generate("<<Copy>>"))  # enable copy
        self.log.bind("<Control-a>", lambda _: self.log.event_generate("<<SelectAll>>"))  # enable select all

        self.root.config(background=self.settings.colors[0]["background"])
        self.settings_frame.pack(side=tk.LEFT, expand=False, fill=tk.Y)
        self.handle_frame.pack(side=tk.LEFT, expand=False, fill=tk.Y)
        self.board_frame.pack(side=tk.LEFT, expand=True, fill=tk.NONE)
        self.settings_frame.grid_columnconfigure(0, minsize=10)  # left padding for all settings widget
        self.settings_frame.grid_columnconfigure(3, minsize=15)  # right padding for all settings widget
        self.settings_frame.grid_rowconfigure(11, weight=1)  # ensures log's row (row 11) can expand
        self.toolbar_frame.grid(row=0, column=0, columnspan=4, pady=(0, 8), sticky=tk.W)

        # configure row & column weights to divide the vertical & horizontal space evenly
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
        self.cheat_button.pack(side=tk.LEFT)
        self.hide_button.pack(side=tk.LEFT, padx=(0, 10))
        self.board_len_label.grid(row=4, column=1, sticky=tk.E)
        self.board_len_slider.grid(row=4, column=2)
        self.win_len_label.grid(row=5, column=1, sticky=tk.E)
        self.win_len_slider.grid(row=5, column=2)
        self.board_zoom_label.grid(row=6, column=1, sticky=tk.E)
        self.board_zoom_slider.grid(row=6, column=2, pady=(0, 8))
        if self.settings.is_pvc:
            self.ai_first_checkbox.grid(columnspan=2, row=7, column=1, pady=(0, 8))
            self.ai_dropdown.grid(columnspan=2, row=8, column=1, pady=(0, 10))
            self.graph_button.grid(columnspan=2, row=9, column=1, pady=(0, 8))
        self.ind_checkbox.grid(columnspan=2, row=10, column=1, pady=(0, 10))
        self.log.grid(columnspan=2, row=11, column=1, sticky=tk.NSEW)
        self.log_clear.place(relx=1.0, rely=1.0, anchor=tk.SE)  # take the SE corner, stick to bottom-right corner of parent

        self.__init_child__()

        self.update_ai_type()
        self.update_len()  # init buttons, win_len
        self.update_turn()  # init turn labels
        self.update_zoom()  # init fonts
        self.update_ind_and_aimoves_buttons()  # in case this setting is on from last time

        # rebinds the close window button
        self.root.protocol("WM_DELETE_WINDOW", lambda: MainMenu.exit(self))

    def __init_child__(self):
        """Used by child classes."""
        pass

    def toggle_settings(self) -> None:
        # if
        if self.settings_frame.winfo_ismapped():
            self.settings_frame.pack_forget()
            self.hide_button.config(text="❯")
        else:
            self.settings_frame.pack(side=tk.LEFT, fill=tk.Y, before=self.handle_frame)
            self.hide_button.config(text="❮")

    def open_dropdown(self) -> None:
        def keep_dropdown_raised() -> None:
            if self.is_dropdown_open:
                self.ai_dropdown.config(relief=tk.RAISED)
                self.root.after(0, keep_dropdown_raised)

            # dropdown closed
            else:
                self.ai_dropdown.config(relief=tk.GROOVE)
                self.update_ai_type()

        self.is_dropdown_open = True
        keep_dropdown_raised()

    def close_dropdown(self, _) -> None:
        self.is_dropdown_open = False

    def update_ai_type(self) -> None:
        tt.t_table.clear()
        self.print_log("Cleared Ttable")
        self.print_log(f"Selected AI:\n{self.settings.ai_type.get()}")
        self.graph = None

        if self.settings.ai_type.get() == Settings.PROB_AI_NAME:
            self.graph_button.config(text="Show search histogram\n(impacts performance)")
        else:
            self.graph_button.config(text="Show search tree\n(impacts performance)")

    def scroll_vertical(self, EVENT: tk.Event) -> None:
        self.board_canvas.yview_scroll(-1 * (EVENT.delta // 120), tk.UNITS)

    def scroll_horizontal(self, EVENT: tk.Event) -> None:
        self.board_canvas.xview_scroll(-1 * (EVENT.delta // 120), tk.UNITS)

    def update_scrollbars(self, *_) -> None:
        """
        1. Resize board_canvas to the size of button_frame.
        2. Update the scrollregion to match the new button_frame size.
        3. Show/hide scrollbars based on whether the new canvas size is smaller/larger than the button_frame.
        """
        bbox: tuple[int, int, int, int] = self.board_canvas.bbox(tk.ALL)  # bbox = x1, y1, x2, y2. bbox size is the same as button_frame size

        # update canvas width & height to bbox width & height +7 padding
        self.board_canvas.config(width=bbox[2] - bbox[0] + 7, height=bbox[3] - bbox[1] + 7)

        # update scrollregion
        self.board_canvas.config(scrollregion=bbox)

        # if button_frame size overflows horizontally
        if bbox[2] > self.board_canvas.winfo_width():
            # show h_scrollbar
            # MUST pack h_scrollbar before board_frame
            self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X, before=self.board_frame)
        else:
            self.h_scrollbar.pack_forget()

        # if button_frame size overflows vertically
        if bbox[3] > self.board_canvas.winfo_height():
            # show v_scrollbar
            # MUST pack v_scrollbar before board_frame
            self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, before=self.board_frame)
        else:
            self.v_scrollbar.pack_forget()

    def update_len(self, _=None) -> None:
        """
        1. Update backend constants.
        2. Create/hide buttons.
        3. Position old & new buttons.
        4. Create textpaths.
        """
        # 1.
        tt.set_consts(TK_BOARD_LEN=self.settings.board_len.get())
        self.print_log("Cleared Ttable")

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
                    command=lambda SQ=len(self.board_buttons): self.human_play(SQ),
                    width=3,
                    borderwidth=5,
                    state=tk.NORMAL
                )
            )
        self.print_log(f"Board button count:\n{len(self.board_buttons)} ({len(self.board_buttons) - tt.BOARD_AREA} hidden)")

        # hide buttons if BOARD_AREA decreased
        # no need to destroy since reusable next time BOARD_AREA increase
        for button in self.board_buttons[tt.BOARD_AREA:]:
            button.grid_forget()

        # 3.
        # DO NOT iterate over board_buttons[] since can have buttons outside BOARD_AREA
        for sq in range(tt.BOARD_AREA):
            self.board_buttons[sq].grid(row=sq // tt.BOARD_LEN, column=sq % tt.BOARD_LEN)

        # 4.
        # create textpaths if BOARD_AREA increased
        while len(self.textpaths) < tt.BOARD_AREA:
            textpath: TextPath = TextPath(
                (0, 0),
                str(len(self.textpaths)),
                prop=FontProperties(size=1)
            )
            # textpath is offset since its bottom-right corner is at label's center
            # use Affine2D to center it
            BBOX: Bbox = textpath.get_extents()
            MID_X, MID_Y = tt.midpoint(BBOX.p0, BBOX.p1)
            textpath = textpath.transformed(
                Affine2D().translate(
                    -MID_X, -MID_Y
                )
            )
            self.textpaths.append(textpath)

        # no need to delete textpaths since reusable next time BOARD_AREA increase

        # update win_len since X always win if it is shorter
        # no need to update backend win_len since the slider's command will
        self.win_len_slider.config(from_=min(tt.BOARD_LEN, 4), to=tt.BOARD_LEN)
        self.update_ind_and_aimoves_buttons()
        self.update_scrollbars()
        self.root.update_idletasks()

    def update_ind_and_aimoves_buttons(self) -> None:
        """
        Show/hide button indexes.
        Color/uncolor buttons with ai_moves[]
        """
        # DO NOT iterate over board_buttons[] since can have buttons outside BOARD_AREA
        for sq in range(tt.BOARD_AREA):

            # if empty
            if not tt.plyr_at(self.board, sq):
                # 1.
                self.board_buttons[sq].config(
                    text=sq if self.settings.show_ind_and_aimoves.get() else ''
                )
                # if currently searched by AI, don't update color
                if self.moved and sq == self.moved[-1]:
                    pass
                # 2.
                # if not currently searched by AI, color/uncolor button
                else:
                    self.board_buttons[sq].config(
                        background=self.settings.colors[0][
                            "ai_moves" if (self.settings.show_ind_and_aimoves.get() and sq in self.ai_moves) else "board_button"
                        ]
                    )

        self.root.update_idletasks()

    def update_zoom(self, _=None) -> None:
        self.settings.board_font = (
            "Helvetica",
            self.settings.board_zoom.get() * 4,
            "bold" if self.settings.board_zoom.get() > 4 else "normal"  # bold font when board_zoom <= 4 makes button not square
        )

        for button in self.board_buttons:
            # button scales automatically with font size
            button.config(font=self.settings.board_font)

    def lock_settings(self) -> None:
        self.board_len_slider.config(state=tk.DISABLED)
        self.board_len_label.config(state=tk.DISABLED)
        self.win_len_slider.config(state=tk.DISABLED)
        self.win_len_label.config(state=tk.DISABLED)
        self.new_game_button.config(state=tk.NORMAL)
        self.ai_first_checkbox.config(state=tk.DISABLED)

    def unlock_settings(self) -> None:
        self.board_len_label.config(state=tk.NORMAL)
        self.board_len_slider.config(state=tk.NORMAL)
        self.win_len_label.config(state=tk.NORMAL)
        self.win_len_slider.config(state=tk.NORMAL)
        self.new_game_button.config(state=tk.DISABLED)
        self.ai_first_checkbox.config(state=tk.NORMAL)
        self.ai_first_checkbox.deselect()

    def lock_board(self) -> None:
        self.cheat_button.config(state=tk.DISABLED)
        for button in self.board_buttons:
            button.config(
                state=tk.DISABLED,
                cursor="no"
            )

    def set_end_flags(self) -> None:
        self.graph = None
        self.ai_thread = None

    def unlock_board(self) -> None:
        self.cheat_button.config(state=tk.ACTIVE)

        # DO NOT iterate over board_buttons[] since can have buttons outside BOARD_AREA
        for sq in range(tt.BOARD_AREA):
            self.board_buttons[sq].config(cursor="plus")

            if not tt.plyr_at(self.board, sq):
                self.board_buttons[sq].config(state=tk.NORMAL)

    def ai_play(self) -> None:
        self.place_pretasks()
        self.ai_thread_start()

    def human_play(self, SQ: int) -> None:
        self.place_pretasks()
        self.moved.append(SQ)
        self.place()

        if self.settings.is_pvc:

            # DO NOT exclude first move since first move can win with loaded board
            if not self.check_result_pvc(False):
                self.ai_play()

        # pvp
        else:
            self.check_result_pvp()

    def place_pretasks(self) -> None:
        # if first move
        if not self.moved:
            self.lock_settings()

        # if not first move and not snake mode
        elif not isinstance(self, GameMenuS):

            # uncolor last move
            self.board_buttons[self.moved[-1]].config(background=self.settings.colors[0]["board_button"])

    def place(self) -> None:
        """
        Move-to-place is passed to place_ai() via moved[-1].
        """
        self.board = tt.place(self.board, self.moved[-1])

        self.board_buttons[self.moved[-1]].config(
            text=tt.char_of(tt.plyr_of(self.board)),
            disabledforeground=self.settings.colors[tt.plyr_of(self.board)]["char"],
            background=self.settings.colors[0]["new_move"],
            state=tk.DISABLED
        )
        self.print_log(None)

    def ai_thread_start(self) -> None:
        self.lock_board()
        self.graph_button.config(state=tk.DISABLED)
        self.ai_thread = threading.Thread(target=self.ai_thread_work, daemon=True)
        self.ai_thread.start()
        self.print_log(f"Spawned thread:\n{self.ai_thread.name}")

    def ai_thread_work(self) -> None:

        # create index for AI's move
        self.moved.append(None)

        # if AI starts first
        if len(self.moved) == 1:
            # moved[-1] is AI's move
            self.moved[-1] = random.randint(0, tt.BOARD_AREA - 1)

        # if AI starts second or loaded board
        else:
            # choose AI
            AI: Callable
            args: tuple

            def send(NEXT_MOVE: int) -> None:
                """
                Injected into AI(), run in AI thread.
                Send NEXT_MOVE to main thread.
                """
                # if game ended early, end thread
                if self.ai_thread is None:
                    sys.exit()

                # use root.after() to run update_aimove() in main thread
                # since matplotlib & tkinter must run in main thread
                self.root.after(0, self.update_aimove, NEXT_MOVE)

            # if AI is snake and placed before, no need ai_moves[]
            if self.settings.ai_type.get() == Settings.SNAKE_AI_NAME and len(self.moved) >= 3:
                AI = tt.snake_search
                self.graph = nx.DiGraph()
                args = (
                    *divmod(self.moved[-3], tt.BOARD_LEN),
                    *divmod(self.moved[-2], tt.BOARD_LEN),
                )

                # only for show, AI doesn't need ai_moves[]
                self.ai_moves = list(
                    tt.sq_of(y, x)
                    for y, x in tt.snake_gen_moves(self.board, *divmod(self.moved[-3], tt.BOARD_LEN))
                )

            else:
                PREV_AI_MOVES: set[int | None] = set(self.ai_moves)
                self.ai_moves = tt.gen_moves(self.board, self.moved[-2])

                if self.settings.ai_type.get() == Settings.RECUR_AI_NAME:
                    AI = tt.recur_search
                    self.ai_moves = self.ai_moves[:14]  # can only search 14 squares in reasonable time
                    self.graph = nx.DiGraph()
                    args = (self.ai_moves.copy(),)  # must copy so AI thread doesn't refill main thread's ai_moves[] after end_game()

                elif self.settings.ai_type.get() == Settings.ITER_AI_NAME:
                    AI = tt.iter_search
                    self.ai_moves = self.ai_moves[:17]
                    self.graph = nx.DiGraph()
                    args = (set(self.ai_moves),)

                elif self.settings.ai_type.get() == Settings.PROB_AI_NAME:
                    AI = tt.prob_search
                    self.ai_moves = self.ai_moves[:14]
                    self.graph = dict.fromkeys(self.ai_moves, 0)
                    args = (self.ai_moves.copy(),)

                # if self.settings.ai_type.get() == Settings.SNAKE_AI_NAME
                else:
                    AI = tt.snake_search_first_move
                    self.ai_moves = self.ai_moves[:16]
                    self.graph = nx.DiGraph()
                    args = (
                        self.ai_moves,  # no need copy since AI thread doesn't modify
                        *divmod(self.moved[-2], tt.BOARD_LEN),
                    )

                # if pruned board different from last search, t_table is unusable
                # DO NOT clear t_table after search since needed to print tree
                if not set(self.ai_moves).issubset(PREV_AI_MOVES):
                    tt.t_table.clear()
                    self.print_log("Cleared Ttable")

            # uncolor last ai_moves[], color new ones
            self.root.after(0, self.update_ind_and_aimoves_buttons)

            self.print_log(f"AI moves:\n{self.ai_moves}")
            self.print_log("Searching...")
            AI(self.board, *args, self.graph, send)

        self.root.after(0, self.ai_thread_end)

    def update_aimove(self, NEXT_MOVE: int) -> None:
        """
        1. Uncolor move that AI last searched.
        2. Color move that AI is currently searching.
        3. Record NEXT_MOVE in moved[-1].
        """
        # moved[-1] is AI's move
        if self.moved[-1] is not None:

            # uncolor last move
            self.board_buttons[self.moved[-1]].config(
                background=self.settings.colors[0][
                    "ai_moves" if self.settings.show_ind_and_aimoves.get() else "board_button"
                ]
            )

        # color current move
        self.board_buttons[NEXT_MOVE].config(
            background=self.settings.colors[0]["new_move"]
        )
        self.root.update_idletasks()
        self.moved[-1] = NEXT_MOVE

    def ai_thread_end(self) -> None:
        self.print_log(f"Thread ended:\n{self.ai_thread.name}")

        # moved[-1] is AI's move
        if self.moved[-1] is None:
            self.lock_board()
            messagebox.showinfo("Result", "AI resigns.\n\nAI: 'I have already computed my inevitable fate ...'")
            return

        self.place()
        self.unlock_board()
        self.graph_button.config(state=tk.NORMAL)

        # check_result_pvc() must run after unlock_board()
        # since in snake mode, check_result_pvc() modify button state
        self.check_result_pvc(True)

    def check_result_pvc(self, IS_AI: bool) -> bool:
        """
        :return: whether game ends.
        """
        WIN_DIR: str | None = tt.win_dir(self.board, self.moved[-1])

        # if someone win
        if WIN_DIR is not None:
            self.lock_board()
            self.set_end_flags()
            if IS_AI:
                if messagebox.askyesno("Result", f"AI won {WIN_DIR}!\n\nAI: 'Shouldn\'t humans be smarter?'") is True:
                    self.new_game(tt.EMPTY_BOARD)
            else:
                if messagebox.askyesno("Result", f"You won {WIN_DIR}!\n\nAI: 'NOT MY DIGNITY! LET US HAVE ANOTHER DUEL!'") is True:
                    self.new_game(tt.EMPTY_BOARD)

            return True

        # if no one win and board is full
        elif len(self.moved) == tt.BOARD_AREA:
            # no need lock_board()
            self.set_end_flags()
            if messagebox.askyesno("Result", "Ended in draw.\n\nAI: 'You\'ll never win ... not satisfied? new_game!'") is True:
                self.new_game(tt.EMPTY_BOARD)

            return True

        # if no one win and board not full
        self.update_turn()
        return False

    def check_result_pvp(self) -> None:
        WIN_DIR: str | None = tt.win_dir(self.board, self.moved[-1])

        # if someone win
        if WIN_DIR is not None:
            self.lock_board()
            self.set_end_flags()
            messagebox.showinfo("Result", f"Player \'{tt.char_of(tt.plyr_of(self.board))}\' won {WIN_DIR}!")

        # if no one win and board is full
        elif len(self.moved) == tt.BOARD_AREA:
            # no need lock_board()
            self.set_end_flags()
            messagebox.showinfo("Result", "Ended in a draw.")

        # if no one win and board not full
        self.update_turn()

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

    def to_submenu(self) -> bool:
        if messagebox.askyesno("Confirmation", "Are you sure you want to quit?\n\nYou will lose all your progress."):
            self.root.unbind("<Configure>")
            self.root.unbind("<MouseWheel>")
            self.root.unbind("<Shift-MouseWheel>")
            self.set_end_flags()

            for widget in self.root.winfo_children():
                widget.destroy()

            # set window to the SubMenu resolution & color
            self.root.geometry(Settings.WINDOW_DIM)
            self.root.config(background="Black")
            SubMenu(self.root, self.settings)
            return True

        return False

    def new_game(self, BOARD: int) -> bool:
        # if game is going, ask user
        if not self.moved or messagebox.askyesno(
                "Confirmation",
                "Are you sure you want to restart?\n\nYou will lose all your progress."):

            # if no last player in loaded board
            if not tt.plyr_of(BOARD):
                messagebox.askretrycancel("Warning", "Enter a board with last player!")
                return False

            self.set_end_flags()
            self.ai_moves.clear()
            if self.moved and self.moved[-1] is not None:

                # uncolor last move
                self.board_buttons[self.moved[-1]].config(background=self.settings.colors[0]["foreground"])

            self.moved.clear()
            self.board = BOARD

            # DO NOT iterate over board_buttons[] since can have buttons outside BOARD_AREA
            for sq in range(tt.BOARD_AREA):
                PLYR: int = tt.plyr_at(self.board, sq)

                # if not empty
                if PLYR:
                    self.board_buttons[sq].config(
                        text=tt.char_of(PLYR),
                        disabledforeground=self.settings.colors[PLYR]["char"],
                        state=tk.DISABLED
                    )
                    # place move from loaded board into moved[]
                    self.moved.append(sq)

                else:
                    self.board_buttons[sq].config(
                        disabledforeground=self.settings.colors[PLYR]["index"],
                        relief=tk.RAISED,  # for snake mode
                    )

            self.update_turn()
            self.update_ind_and_aimoves_buttons()
            self.unlock_settings()
            self.print_log(None)
            self.unlock_board()
            return True

        return False

    def print_log(self, TEXT: str | None) -> None:
        BEGIN: str = self.log.index(f"{tk.END}-1c")

        # common case
        if TEXT is None:
            self.log.insert(
                tk.END,
                f"Move: {self.moved[-1] if self.moved else None}\n" +
                f"Last player: {tt.plyr_of(self.board)}\n" +
                f"Board: {self.board}\n" +
                f"Ttable len: {len(tt.t_table)}\n\n"
            )

        else:
            self.log.insert(tk.END, f"{TEXT}\n\n")

        # color text only when game ongoing
        if self.moved:
            self.log.tag_add(
                f"{tt.char_of(tt.plyr_of(self.board))}_TURN_TAG",
                f"{BEGIN}",
                f"{tk.END}-1c"
            )
        self.log.see(tk.END)

    def print_graph(self) -> None:
        if self.graph is None:
            messagebox.showinfo("Warning", f"Perform an AI search first!")
            return

        if self.settings.ai_type.get() == Settings.PROB_AI_NAME:
            HistogramPrinter(self)
        else:
            TreePrinter(self)


class GameMenuT(GameMenu):
    """
    :ivar entry_scale: inflation of the active timer, used for animation. Resets to 0 at the beginning of each turn.
    :ivar time: how much time each player still has: index 1 is X's, index 2 is O's.
    """

    def __init__(self, root: tk.Tk, settings: Settings):

        self.is_countdown: bool | None = None
        self.entry_scale: int = 0

        super().__init__(root, settings)

    def __init_child__(self):
        self.time = [
            None,
            tk.DoubleVar(value=Settings.DEFAULT_TIME),
            tk.DoubleVar(value=Settings.DEFAULT_TIME)
        ]
        self.trace1 = self.time[1].trace_add("write", lambda _, __, ___: self.validate(1))
        self.trace2 = self.time[2].trace_add("write", lambda _, __, ___: self.validate(2))

        # change widget class of turn_labels from Label to LabelFrame
        self.turn_labels[1].destroy()
        self.turn_labels[2].destroy()
        self.turn_labels[1] = tk.LabelFrame(
            self.board_frame,
            text="X timer",
            **self.settings.turn_label_cfg
        )
        self.turn_labels[2] = tk.LabelFrame(
            self.board_frame,
            text="O timer",
            **self.settings.turn_label_cfg
        )

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
                justify=tk.CENTER,
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
                justify=tk.CENTER,
                textvariable=self.time[2]
            )
        ]

        self.turn_labels[1].grid(row=0, column=0, sticky=tk.E)  # stick to the right edge of column 1
        self.turn_labels[2].grid(row=0, column=1, sticky=tk.W)  # stick to the left edge of column 2
        self.time_entry[1].pack()
        self.time_entry[2].pack()

    def update_zoom(self, _=None) -> None:
        super().update_zoom()

        self.settings.time_font = ("Courier", self.settings.board_zoom.get() * 3 + 2, "bold")
        self.time_entry[1].config(font=self.settings.time_font)
        self.time_entry[2].config(font=self.settings.time_font)

    def lock_settings(self) -> None:
        super().lock_settings()

        self.time_entry[1].config(state=tk.DISABLED)
        self.time_entry[2].config(state=tk.DISABLED)
        self.is_countdown = True
        self.countdown()

    def unlock_settings(self) -> None:
        super().unlock_settings()

        self.time_entry[1].config(state=tk.NORMAL)
        self.time_entry[2].config(state=tk.NORMAL)
        self.time[1].set(Settings.DEFAULT_TIME)
        self.time[2].set(Settings.DEFAULT_TIME)

        # reset time_entry inflation
        self.update_zoom()

    def validate(self, PLYR: int) -> None:
        # try to convert entered time to float
        try:
            self.time[PLYR].get()

        # if time is not float
        except tk.TclError:
            messagebox.askretrycancel("Warning", f"Enter a decimal number for {tt.char_of(PLYR)} timer!")
            self.time[PLYR].set(Settings.DEFAULT_TIME)

    def countdown(self) -> None:
        """Recursively decrement time."""

        # if game ended
        if not self.is_countdown:
            return

        TIME: float = self.time[tt.opp_of(tt.plyr_of(self.board))].get()

        # if player run out of time, opponent wins
        if TIME <= 0:
            messagebox.showinfo("Result", f"Time's up! Player {tt.char_of(tt.plyr_of(self.board))} won!")
            self.lock_board()
            self.set_end_flags()
            return

        # update scale of current plyr's timer
        # update entry_scale after time_entry in case update_turn() resets scale
        self.time_entry[tt.opp_of(tt.plyr_of(self.board))].config(
            font=("Courier", self.settings.board_zoom.get() * 3 + 2 + self.entry_scale, "bold")
        )
        self.entry_scale = min(self.entry_scale + 2, Settings.MAX_TIME_ENTRY_SCALE)

        # if X has under 5 secs left
        if TIME < 5.0:
            # flash the timer
            if TIME % 1 < 0.4:
                self.time_entry[tt.opp_of(tt.plyr_of(self.board))].config(
                    relief=tk.SUNKEN,
                    disabledbackground="White",
                )
            else:
                self.time_entry[tt.opp_of(tt.plyr_of(self.board))].config(
                    relief=tk.GROOVE,
                    disabledbackground="yellow"
                )
        self.root.update_idletasks()

        # decrease the time value by 0.1 every 100ms and display only 1 decimal point using round()
        # DO NOT decrease by 1 every 1000ms as it slows down the whole app.
        self.time[tt.opp_of(tt.plyr_of(self.board))].set(round(TIME - 0.1, 1))
        self.root.after(100, self.countdown)

    def set_end_flags(self) -> None:
        super().set_end_flags()
        self.is_countdown = False

    def update_turn(self) -> None:
        """
        Overload to include disable timer entry, switch timer and add bonus time.
        """
        # reset timer scale
        self.entry_scale = 0

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
            disabledbackground="White"
        )

        if self.moved:
            # current plyr gets bonus time
            self.time[tt.plyr_of(self.board)].set(self.time[tt.plyr_of(self.board)].get() + 1)

    def to_submenu(self) -> None:
        if super().to_submenu():
            self.time[1].trace_remove("write", self.trace1)
            self.time[2].trace_remove("write", self.trace2)


class GameMenuV(GameMenu):
    """
    :var settings.queue_len: number of X (or O) allowed on the board at any moment.
    :var settings.show_qfront: show/hide the moves about to pop in the next turns.
    """

    def __init_child__(self):

        self.queue_len_label = tk.Label(
            self.settings_frame,
            background=self.settings.colors[0]["foreground"],
            text="\nQueue length"
        )
        self.queue_len_slider = tk.Scale(
            self.settings_frame,
            variable=self.settings.queue_len,
            **self.settings.slider_cfg
        )
        self.show_qfront_checkbox = tk.Checkbutton(
            self.settings_frame,
            text=Settings.SHOW_QFRONT_TEXT,
            variable=self.settings.show_qfront,
            command=self.update_qfront_buttons,
            **self.settings.checkbox_cfg
        )

        self.queue_len_label.grid(row=2, column=1, sticky=tk.E)
        self.queue_len_slider.grid(row=2, column=2, pady=(0, 8))
        self.show_qfront_checkbox.grid(columnspan=2, row=3, column=1)

    def lock_settings(self) -> None:
        super().lock_settings()

        self.queue_len_slider.config(state=tk.DISABLED)
        self.queue_len_label.config(state=tk.DISABLED)

    def unlock_settings(self) -> None:
        super().unlock_settings()

        self.queue_len_slider.config(state=tk.NORMAL)
        self.queue_len_label.config(state=tk.NORMAL)

    def update_qfront_buttons(self) -> None:

        # queue_len is # moves allowed PER player
        # FULL_QUEUE_LEN is for both players
        FULL_QUEUE_LEN: int = 2 * self.settings.queue_len.get()

        # color move-to-pop in current & next turns
        if len(self.moved) >= FULL_QUEUE_LEN:
            COL: str = self.settings.colors[0]["qfront" if self.settings.show_qfront.get() else "board_button"]

            self.board_buttons[self.moved[0]].config(background=COL)
            self.board_buttons[self.moved[1]].config(background=COL)

    def pop_move(self) -> None:
        FULL_QUEUE_LEN: int = 2 * self.settings.queue_len.get()

        if len(self.moved) > FULL_QUEUE_LEN:
            POP_MOVE: int = self.moved.pop(0)
            self.board = tt.unplace(self.board, POP_MOVE)
            self.board_buttons[POP_MOVE].config(
                text='',
                background=self.settings.colors[0]["board_button"],
                state=tk.NORMAL
            )
            self.print_log(
                f"Pop move: {POP_MOVE}\n" +
                f"Queue:\n{self.moved}"
            )

        self.update_qfront_buttons()

    def update_len(self, _=None) -> None:
        super().update_len()
        self.queue_len_slider.config(from_=tt.WIN_LEN, to=tt.BOARD_AREA // 2)

    def check_result_pvc(self, IS_AI: bool) -> bool:
        self.pop_move()
        return super().check_result_pvc(IS_AI)

    def check_result_pvp(self) -> None:
        self.pop_move()
        super().check_result_pvp()


class GameMenuS(GameMenu):

    def __init_child__(self):
        # X always win if board_len is < 4. The slider automatically call update_len() to update cross-file vars.
        self.board_len_slider.config(from_=4)
        self.settings.ai_type.set(Settings.SNAKE_AI_NAME)

    def update_len(self, _=None) -> None:
        super().update_len()
        self.win_len_slider.config(from_=min(tt.BOARD_LEN // 2 + 1, 3))

    def check_result_pvc(self, IS_AI: bool) -> bool:
        if not self.update_snake():
            return super().check_result_pvc(IS_AI)
        return True

    def check_result_pvp(self) -> None:
        if not self.update_snake():
            super().check_result_pvp()

    def update_snake(self) -> bool:
        """
        :return: whether game ends.
        """
        # color the new head
        if self.moved:
            self.board_buttons[self.moved[-1]].config(
                background=self.settings.colors[tt.plyr_of(self.board)]["snake_head"]
            )

        # change the old head color to body color
        if len(self.moved) >= 3:
            self.board_buttons[self.moved[-3]].config(
                background=self.settings.colors[tt.plyr_of(self.board)]["snake_body"]
            )

        # prepare for opponent's turn
        if len(self.moved) >= 2:
            adjs: set = set(tt.sq_of(y, x) for y, x in tt.snake_gen_moves(self.board, *divmod(self.moved[-2], tt.BOARD_LEN)))

            # if opponent is stuck, current wins
            if not adjs:
                messagebox.showinfo("Result", f" Player {tt.char_of(tt.opp_of(tt.plyr_of(self.board)))} is trapped! Player {tt.char_of(tt.plyr_of(self.board))} won!")
                self.lock_board()
                self.set_end_flags()
                return True

            # disable buttons that are empty, enable buttons adjacent to head
            for sq in set(range(tt.BOARD_AREA)).difference(self.moved):
                if sq in adjs:
                    self.board_buttons[sq].config(
                        state=tk.NORMAL,
                        relief=tk.RAISED
                    )
                else:
                    self.board_buttons[sq].config(
                        state=tk.DISABLED,
                        relief=tk.SUNKEN
                    )


class HistogramPrinter:

    X_LABEL_TEXT: str = "Root Move"
    Y_LABEL_TEXT: str = "Normalized Squared Score"
    PAD_WIDTH: float = 0.7

    def __init__(self, parent: GameMenu):
        self.fig = plt.figure(
            num="Histogram" + str(len(plt.get_fignums()) + 1)
        )
        self.ax: Axes = plt.gca()
        self.bar: BarContainer = self.ax.bar(
            tuple(parent.graph.keys()),
            tuple(parent.graph.values()),
            color=tuple(
                Settings.NODE_COLORS[tt.WIN_SCORE]
                if score >= 0 else Settings.NODE_COLORS[-tt.WIN_SCORE]
                for score in parent.graph.values()
            ),
            edgecolor="Black",
            linewidth=0.5,
            zorder=2  # show above x-axis
        )
        self.bar_labels: list[Text] = self.ax.bar_label(
            self.bar,
            label_type=tk.CENTER
        )
        # set x-axis range and interval
        self.ax.set_xbound(lower=min(parent.ai_moves) - self.PAD_WIDTH, upper=max(parent.ai_moves) + self.PAD_WIDTH)
        self.ax.xaxis.set_major_locator(MultipleLocator(1))

        # draw y=0 line
        self.ax.axhline(
            color="Black",
            linewidth=0.5,
            zorder=1  # show below bars
        )
        self.ax.set_xlabel(self.X_LABEL_TEXT)
        self.ax.set_title(f"{self.Y_LABEL_TEXT} of Each {self.X_LABEL_TEXT}")
        # no need set_ylabel() since update_y_offset() later will

        # prevent long y-axis tick values that push label outside window
        self.ax.ticklabel_format(axis=tk.Y, style="sci", scilimits=(-3, 3))

        # initialize y_offset
        # need draw() so get_major_formatter().get_offset() is not empty
        self.fig.canvas.draw()
        self.update_y_offset()

        self.fig.canvas.mpl_connect('resize_event', self.update_bar_labels)
        self.ax.callbacks.connect("xlim_changed", self.update_bar_labels)
        self.ax.callbacks.connect("ylim_changed", self.update_y_offset)
        plt.show()

    def update_y_offset(self, _=None) -> None:

        # needed since offset show again every redraw
        self.ax.yaxis.offsetText.set_visible(False)

        OFFSET: str = self.ax.yaxis.get_major_formatter().get_offset()
        self.ax.set_ylabel(self.Y_LABEL_TEXT + (" × " + OFFSET if OFFSET else ''))
        self.fig.canvas.draw_idle()

    def update_bar_labels(self, _=None) -> None:
        for patch, label in zip(self.bar, self.bar_labels):

            # get bar endpoints to get width
            X0: float = self.ax.transData.transform((patch.get_x(), 0))[0]
            X1: float = self.ax.transData.transform((patch.get_x() + patch.get_width(), 0))[0]
            WIDTH: float = abs(X1 - X0)

            SCORE: float = patch.get_height()

            # reduce # significant digits until label fit in bar
            for digit_cnt in range(10, -1, -1):
                label.set_text(f"{SCORE:.{digit_cnt}e}")

                if label.get_window_extent(self.fig.canvas.get_renderer()).width <= WIDTH:
                    break

        self.fig.canvas.draw_idle()


class TreePrinter:

    def __init__(self, parent: GameMenu):
        self.parent: GameMenu = parent
        self.tree: nx.DiGraph = parent.graph
        self.NODES: tuple[int] = tuple(self.tree.nodes)
        self.TREE_INFO: str = (
                f"Total # Nodes: {len(self.NODES)}\n" +
                "Click a node for more details!"
        )
        LEGEND_HANDLES: tuple[Patch] = (
            Patch(facecolor=f"{Settings.NODE_COLORS[-tt.WIN_SCORE]}", edgecolor="Black", label="Lose"),
            Patch(facecolor=f"{Settings.NODE_COLORS[0]}", edgecolor="Black", label="Tie"),
            Patch(facecolor=f"{Settings.NODE_COLORS[tt.WIN_SCORE]}", edgecolor="Black", label="Win"),
            Patch(facecolor=f"{Settings.NODE_COLORS[None]}", edgecolor="Black", label="Unvisited"),

            # use last legend to show node/tree info
            Patch(facecolor=tk.NONE, label=self.TREE_INFO)
        )
        self.fig = plt.figure(
            num="Depth-first-search Tree" + str(len(plt.get_fignums()) + 1),
            layout="constrained"
        )
        self.ax: Axes = plt.gca()
        self.ax.axis(False)

        # store node attributes in nx.DiGraph instead of new lists
        self.set_nodes_pos()
        self.set_nodes_attrs()
        self.set_edges_attrs()

        # draw all nodes as one artist
        # optimization: did not draw one artist per node
        self.nodes_collection: PathCollection = PathCollection(
            paths=(Path.unit_circle(),),
            offset_transform=self.ax.transData,  # treat offsets as data coords instead of pixel coords
            transform=IdentityTransform(),  # prevent any other transformations
            edgecolors=(0, 0, 0, Settings.EDGE_ALPHA),
            picker=True,
            zorder=3,  # show above edges
            **self.get_nodes_attrs()
        )
        self.ax.add_collection(self.nodes_collection)

        # draw all edges as one artist
        nx.draw_networkx_edges(
            self.tree,
            nx.get_node_attributes(self.tree, "pos"),
            alpha=Settings.EDGE_ALPHA,
            arrows=False
        )

        # draw all edge labels as one artist
        self.e_labels_collection: PathCollection = PathCollection(
            offset_transform=self.ax.transData,
            transform=IdentityTransform(),
            facecolors="Black",
            sizes=(Settings.NODE_SIZE * 2,),
            zorder=2,  # show above background
            **self.get_edges_attrs()
        )
        self.ax.add_collection(self.e_labels_collection)

        # draw all edge label backgrounds as one artist
        self.e_labels_bg_collection: PathCollection = PathCollection(
            paths=(Path.unit_circle(),),
            offsets=tuple(nx.get_edge_attributes(self.tree, "pos").values()),
            offset_transform=self.ax.transData,
            transform=IdentityTransform(),
            facecolors="White",
            sizes=(Settings.NODE_SIZE * 0.4,),
            alpha=Settings.EDGE_ALPHA,
            zorder=1
        )
        self.ax.add_collection(self.e_labels_bg_collection)

        self.legend: Legend = self.ax.legend(
            handles=LEGEND_HANDLES,
            loc="lower left",
            handlelength=1,
            handleheight=1,
            handletextpad=0.5,
            prop=FontProperties(family="Consolas")
        )
        self.info_text: Text = self.legend.get_texts()[-1]
        self.info_text.set_position((-19, 0))

        self.func_animation: 'Callable | None' = None

        self.ax.callbacks.connect("xlim_changed", self.repos_edge_labels)
        self.ax.callbacks.connect("ylim_changed", self.repos_edge_labels)
        self.fig.canvas.mpl_connect("button_press_event", self.update_info_text)
        self.fig.canvas.mpl_connect("motion_notify_event", self.update_cursor)
        self.parent.print_log(f"Artist count: {len(self.ax.get_children())}")
        plt.show()

    def update_info_text(self, EVENT: MouseEvent) -> None:
        """
        If clicked on node, update info_text to show information about the node.
        If not, update info_text to show information about the tree.
        """
        IS_NODE, INFO = self.nodes_collection.contains(EVENT)

        # if clicked on node
        if IS_NODE:
            # last index in INFO["ind"] is the highest node's
            IND: int = INFO["ind"][-1]

            NODE: int = self.NODES[IND]
            attrs: dict = self.tree.nodes[NODE]
            DEPTH: int = attrs["pos"][1]
            PARENTS = tuple(self.tree.predecessors(NODE))
            CHILDS = tuple(self.tree.successors(NODE))

            # copy node to clipboard
            self.parent.root.clipboard_clear()
            self.parent.root.clipboard_append(NODE)
            self.parent.root.update()
            self.parent.print_log(f"Copied to clipboard:\n{NODE}")

            self.info_text.set_text(
                f"Board:\n{tt.print_board(NODE, False)}" +
                f"Last Player: {tt.char_of(tt.plyr_of(NODE))}\n" +
                f"Board in Base10: {NODE}\n" +

                # can have multiple parent due to transposition
                f"{len(PARENTS)} Parent(s): {", ".join(map(str, PARENTS))}\n" +

                f"{len(CHILDS)} Visited Child(s): {", ".join(map(str, CHILDS))}\n" +

                # total # childs of root (assume root has max # childs) - depth + # visited childs
                # since DEPTH is negative, + DEPTH instead of - DEPTH
                # doesn't work for snake AI since assume permutation tree
                f"{len(self.parent.ai_moves) + DEPTH - len(CHILDS)} Skipped Child(s)"
            )
            # no need draw_idle() since FuncAnimation() automatically redraw

            # MUST assign FuncAnimation() to variable that lasts the entire animation so it is not garbage-collected
            self.func_animation = FuncAnimation(
                self.fig,
                self.update_node_scale,
                fargs=(attrs,),
                frames=Settings.MAX_NODE_FRAME + 1,  # +1 since frames is exclusive
                interval=0,
                blit=True,
                repeat=False
            )

        # if not clicked on node
        else:
            self.info_text.set_text(self.TREE_INFO)
            self.fig.canvas.draw_idle()

    def update_node_scale(self, FRAME: int, attrs: dict) -> tuple[Artist, ...]:
        """
        :return: iterable of artists that were changed, required by FuncAnimation() to blit.
        """
        SCALE: float = (
            Settings.NODE_SIZE
            + 100 * math.sin(
                    math.pi * math.sqrt(FRAME / Settings.MAX_NODE_FRAME)
            )
        )
        attrs["size"] = SCALE
        self.nodes_collection.set_sizes(tuple(nx.get_node_attributes(self.tree, "size").values()))

        return self.nodes_collection, self.legend

    def update_cursor(self, EVENT: MouseEvent) -> None:
        """If mouse hover over node, change cursor to hand2."""

        IS_NODE, _ = self.nodes_collection.contains(EVENT)
        self.fig.canvas.get_tk_widget().config(cursor="hand2" if IS_NODE else '')

    def repos_edge_labels(self, _) -> None:

        # get window size in pixel coords
        BBOX: Bbox = self.ax.get_window_extent()

        for parent, child, attrs in self.tree.edges(data=True):

            # transform into pixel coords
            p0 = self.ax.transData.transform(self.tree.nodes[parent]["pos"])
            p1 = self.ax.transData.transform(self.tree.nodes[child]["pos"])

            TRIMMED: tuple[tuple[float, float]] = tt.trim_line(
                p0, p1,
                BBOX
            )
            if TRIMMED is not None:
                # center label at midpoint of visible section
                # then transform back to data coords
                NEW_POS: tuple[float, float] = self.ax.transData.inverted().transform(
                    tt.midpoint(
                        *TRIMMED
                    )
                )
                self.tree[parent][child]["pos"] = NEW_POS

        LABELS_POS: tuple[tuple[float, float]] = tuple(nx.get_edge_attributes(self.tree, "pos").values())
        self.e_labels_collection.set_offsets(LABELS_POS)
        self.e_labels_bg_collection.set_offsets(LABELS_POS)
        self.fig.canvas.draw_idle()

    # every subtree has two pads on both sides, this is for one side
    # this is relative to CHILD_DX
    # absolute pad width = 0.5 * CHILD_DX
    PAD_WIDTH: float = 0.5

    def set_nodes_pos(self) -> None:
        """
        Calculate coord for each node and store in its "pos" attribute.
        """

        def traverse(NODE: int, X: float, Y: float, SUBTREE_WIDTH: float) -> None:
            """
            Called Recursively.
            1. Store coord of current node.
            2. Calculate coord for child nodes.
            :param SUBTREE_WIDTH: width of subtree with NODE as root, including paddings.
            """
            self.tree.nodes[NODE]["pos"] = (X, Y)

            # only childs without pos yet
            CHILDS: tuple[int] = tuple(node for node in self.tree.successors(NODE) if "pos" not in self.tree.nodes[node])
            if CHILDS:
                INTERVAL_CNT: int = len(CHILDS) - 1

                # x-dist between each child
                CHILD_DX: float = SUBTREE_WIDTH / (INTERVAL_CNT + self.PAD_WIDTH * 2)

                # x-coord of leftmost child
                LEFTMOST_X: float = X - SUBTREE_WIDTH / 2 + self.PAD_WIDTH * CHILD_DX

                # assign positions for each unvisited child
                for i, child in enumerate(CHILDS):
                    traverse(child, LEFTMOST_X + CHILD_DX * i, Y - 1, CHILD_DX)

        # select the first node as root
        # no need to check if tree is empty
        ROOT: int = next(iter(self.tree))
        traverse(ROOT, 0.0, 0, 1)

    def set_nodes_attrs(self) -> None:
        """
        Calculate attributes below for each node:
            1. color
            2. size
        """
        node_color: str

        for node, attrs in self.tree.nodes(data=True):

            # node not in t_table is possible during iter search
            if node not in tt.t_table:
                node_color = Settings.NODE_COLORS[None]
            else:
                node_color = Settings.NODE_COLORS[tt.t_table[node]]

            attrs["color"] = node_color
            attrs["size"] = Settings.NODE_SIZE

    def set_edges_attrs(self) -> None:
        """
        Calculate attributes below for each edge:
            1. pos
            2. textpath: path of label text
        """

        for parent, child, attrs in self.tree.edges(data=True):
            # place label in between parent & child
            attrs["pos"] = tt.midpoint(
                self.tree.nodes[parent]["pos"],
                self.tree.nodes[child]["pos"]
            )
            attrs["textpath"] = self.parent.textpaths[attrs["move"]]

    def get_nodes_attrs(self) -> dict[str, list]:
        offsets: list[tuple[float, float]] = []
        facecolors: list[str] = []
        sizes: list[float] = []

        for _, attrs in self.tree.nodes(data=True):
            offsets.append(attrs["pos"])
            facecolors.append(attrs["color"])
            sizes.append(attrs["size"])

        return {
            "offsets": offsets,
            "facecolors": facecolors,
            "sizes": sizes
        }

    def get_edges_attrs(self) -> dict[str, list]:
        offsets: list[tuple[float, float]] = []
        paths: list[TextPath] = []

        for _, _, attrs in self.tree.edges(data=True):
            paths.append(attrs["textpath"])
            offsets.append(attrs["pos"])

        return {
            "offsets": offsets,
            "paths": paths
        }


# === Help Pop-ups ===
MORE_INFO_TEXT: str = "For more information, read the ⍰ of the Traditional mode."
VERSION_TEXT: str = "Tic Tac Toe v18"


def default_help() -> None:
    messagebox.showinfo("Help",
                        f"Just like the good ol\' one you played in kindergarten...\n\nYou can select a board length between {Settings.MIN_BOARD_LEN} and... infinity? Boards larger than 3x3 only needs 4 in a row to win!\n\nThe starting player is always X, and the other is O. No friends? No worries! You can play with one of four unique AIs designed by me and my friend.\n\nAbout the AIs:\n\nThe {Settings.RECUR_AI_NAME} is the strongest. It uses a special case of the Negamax + Alpha-Beta Prunning Algorithm that my friend told me.\n\nThe {Settings.ITER_AI_NAME} uses a similar algorithm that cannot distinguish tie branch nodes, and assumes tie is win if it played the last move. This makes it weaker but faster than the {Settings.RECUR_AI_NAME}.\n\nThe {Settings.PROB_AI_NAME} traverses the entire tree and might have Statistical Traps, making it the slowest and weakest AI. However, it is special since it is my first original AI and closest to machine learning.\n\nThe {Settings.SNAKE_AI_NAME} uses the same algorithm as the {Settings.RECUR_AI_NAME}, and follows snake rules even if not in Snake mode.")


def time_help() -> None:
    messagebox.showinfo("Help",
                        f"Each player has a certain amount of time to complete the game. At the start, you can set the time.\n\nAfter each move, you earn 1 extra second!\n\nThe AIs don't know there's a time limit, but they might get faster after a few games.\n\n{MORE_INFO_TEXT}")


def vanish_help() -> None:
    messagebox.showinfo("Help",
                        f"After a certain number of moves, your oldest move will vanish!\n\nPoor memory? Enable '{Settings.SHOW_QFRONT_TEXT}' to show your oldest move in yellow.\n\nThe number of moves you can have on the board at any time is determined by 'Queue length'. What is a queue you asked? Go study computer science!\n\nBefore you go, here's a tip: the AIs don't know that moves vanish!\n\n{MORE_INFO_TEXT}")


def snake_help() -> None:
    messagebox.showinfo("Help",
                        f"For your first move, you can place wherever you want.\n\nAfterwards, you can only place around your last move ( your snake's head ). Watch where your snake is going, as turning around can take some time.\n\nBesides winning traditionally, you can also win by trapping your opponent in a corner! I recommend playing on a 7x7 or larger board.\n\n{MORE_INFO_TEXT}")


def changelog() -> None:
    messagebox.showinfo("Changelog", """
v1 : Added the basics: player vs player, infinite board length, winner check, etc...\n
v2 : Boards are now stored as single list instead of dictionary. Changes player input from index number to x,y coordinates. Rebuild the entire code to process this new file format.\n
v3 : Added basic AI. Added console GUI. Make boards that are 7*7 or larger needs only half the board length to win.\n
v4 : Added board pruning for boards larger than 3x3 to reduce AI calculations. Added some randomization to the moves made by the AI. Restructured the entire AI code for optimization.\n
v5 : Added deathtrap check - that's the hardest part of this project! Now the AI is 100% unbeatable for a 3x3 board. Added the option to let AI start first.\n
v6 : Make board pruning only for boards larger than 5x5. Added land-filling to boards larger than 3x3. Added a matplotlib display for AI's Risk Analysis.\n
v7 : Added Tkinter GUI. Rebuild winner check for HUGE optimization. Changed every code to function. Added user-friendly log window.\n
v8 : HUGE OPTIMIZATION: Rebuild the board pruning code to combine both pruning and land-filling into 1 function. Pruned board and main board now have the same dimension - no additional function is needed to convert squares between the two boards!\n
v9 : Rebuild and tidy up all GUI code using class instead of functions. Rebuild to make board pruning dynamic, it can now scale up if that area has not enough empty squares. Added 'new_game' button. Changed empty squares from '[ ]' to ' '. Fixed bug where the endpoint of checking diagonally from top right to down left doesn't move with the start point.\n
v10: Added title animation. Added 4 modes: Traditional, Time Trial, Vanishing Moves, Snake\n
v11: Globalised colors for each feature. Added color self.settings. Changed O's snake color. Capped length to win at 4. Added 'Total Child Count' to log.
v12: Redesign the algorithm to use depth-first search instead of breadth-first-search. Build a specialized, faster check winner algo that only checks for whether a specific player wins, instead of checking who wins.\n
v13: Prunner V2
v14: Prunner V3, Shayan's Algo.
v15: GUI Revamp
v16, v17, v18: see GitHub\n
    """)


if __name__ == "__main__":
    _root = tk.Tk()
    MainMenu(_root, Settings())
    _root.mainloop()
