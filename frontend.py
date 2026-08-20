import math
import random
import sys
import threading
import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox

import matplotlib.pyplot as plt
import networkx as nx

import backend as tt

RECUR_AND_OR_AI: str = "Recursive And-Or AI"
ITER_AND_OR_AI: str = "Iterative And-Or AI"
RECUR_PROB_AI: str = "Recursive Probability AI"
RECUR_SNAKE_AI: str = "Recursive Snake AI"
AI: tuple[str, str, str, str] = (RECUR_AND_OR_AI, ITER_AND_OR_AI, RECUR_PROB_AI, RECUR_SNAKE_AI)


class Settings:
    """Settings persist across menus."""

    def __init__(self):
        self.board_len: tk.IntVar = tk.IntVar(value=3)
        self.win_len: tk.IntVar = tk.IntVar(value=3)
        self.board_zoom: tk.IntVar = tk.IntVar(value=5)
        self.ai_type: tk.StringVar = tk.StringVar(value=RECUR_AND_OR_AI)
        self.show_ind: tk.BooleanVar = tk.BooleanVar(value=False)
        self.queue_len: tk.IntVar = tk.IntVar(value=3)
        self.show_qfront: tk.BooleanVar = tk.BooleanVar(value=False)
        self.is_pvc: bool = True
        self.INIT_TIME: float = 10

        self.board_font: tuple[str, int, str] = ("", 0, "")
        self.time_font: tuple[str, int, str] = ("", 0, "")
        self.MENU_FONT: tuple[str, int] = ("FixedSys", 15)
        self.WINDOW_DIM: str = "700x420"
        self.colors: list[dict] = [
            # general features
            {
                "index": "gray",
                "new_move": "Sea Green1",
                "ai_moves": "Dark Sea Green1",
                "board_button": "HoneyDew2",
                "background": "HoneyDew2",
                "foreground": "Sea Green2",
                "queue_front": "Yellow",
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
        self.MENU_LABEL_CFG: dict = {
            "background": "Black",
            "foreground": "Sea Green1"
        }
        self.MENU_BUTTON_CFG: dict = {
            "font":  self.MENU_FONT,
            "cursor": "hand2",
            "overrelief": tk.SUNKEN,
            "activeforeground": "white",
            "activebackground": "Sea Green",
            "background": "Sea Green1",
            "foreground": "Black",
            "borderwidth": 5
        }
        self.COL_FRAME_CFG: dict = {
            "font": ("FixedSys", 20, "bold"),
            "foreground": "Sea Green1",
            "background": "Black",
            "borderwidth": 3,
            "relief": tk.RIDGE
        }
        self.TOOLBAR_BUTTON_CFG: dict = {
            "font": ("Helvetica", 10),
            "background": self.colors[0]["foreground"],
            "activebackground": self.colors[0]["foreground"],
            "cursor": "hand2",
            "relief": tk.GROOVE,
            "overrelief": tk.SUNKEN,
            "width": 6,
            "borderwidth": 5
        }
        self.SETTINGS_SLIDER_CFG: dict = {
            "background": self.colors[0]["foreground"],
            "activebackground": self.colors[0]["foreground"],
            "troughcolor": self.colors[0]["background"],
            "highlightthickness": 0,
            "orient": tk.HORIZONTAL,
            "length": 100,
            "cursor": "sb_h_double_arrow"
        }
        self.SETTINGS_CHECKBOX_CFG: dict = {
            "background": self.colors[0]["foreground"],
            "activebackground": self.colors[0]["background"],
            "selectcolor": self.colors[0]["background"],
            "cursor": "hand2"
        }
        self.TURN_LABEL_CFG: dict = {
            "font": ("Helvetica", 10, "bold"),
            "foreground": self.colors[1]["char"],
            "background": self.colors[0]["background"],
            "borderwidth": 5,
            "relief": tk.RIDGE
        }


class MainMenu:
    root: tk.Tk
    settings: Settings

    def __init__(self, root: tk.Tk, settings: Settings):
        self.root = root
        self.settings = settings
        self.line1 = tk.Label(
            self.root,
            text='=' * 999,
            font="TkFixedFont",
            **self.settings.MENU_LABEL_CFG
        )
        self.line2 = tk.Label(
            self.root,
            text='=' * 999,
            font="TkFixedFont",
            **self.settings.MENU_LABEL_CFG
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
            **self.settings.MENU_LABEL_CFG
        )
        self.subtitle_label = tk.Label(
            self.root,
            font="TkFixedFont",
            justify=tk.LEFT,
            **self.settings.MENU_LABEL_CFG
        )
        SUBTITLE = "   99% Made by CZY           4 Innovative Modes!            Unbeatable AI?        "

        self.pvc_button = tk.Button(
            self.root,
            text="Single Player",
            command=lambda: self.to_submenu(True),
            **self.settings.MENU_BUTTON_CFG
        )
        self.pvp_button = tk.Button(
            self.root,
            text="Multi Player",
            command=lambda: self.to_submenu(False),
            **self.settings.MENU_BUTTON_CFG
        )
        self.changelog_button = tk.Button(
            self.root,
            text="Changelog",
            command=changelog,
            **self.settings.MENU_BUTTON_CFG
        )
        self.exit_button = tk.Button(
            self.root,
            text="Exit",
            command=self.exit,
            **self.settings.MENU_BUTTON_CFG
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
        DELTA_TIME: int = 200

        # anim_frames contains id of all 95 (frame 0 - 94) frames of the animation
        self.anim_frames: list[str] = []

        # frames 0 - 11: animating title
        self.anim_frames.append(self.root.after(DELTA_TIME * 0, lambda: self.title_label.config(width=1)))  # width=0 doesn't work
        self.anim_frames.append(self.root.after(DELTA_TIME * 1, lambda: self.title_label.config(width=8)))
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
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

        self.root.title(VER)
        self.root.geometry(self.settings.WINDOW_DIM)
        self.root.config(background="Black")

    def to_submenu(self, is_pvc: bool) -> None:
        # stop all queued frames of the title animation
        for frame in self.anim_frames:
            self.root.after_cancel(frame)

        for widget in self.root.winfo_children():
            widget.destroy()

        self.settings.is_pvc = is_pvc
        SubMenu(self.root, self.settings)

    def exit(self: "MainMenu | SubMenu | GameMenu") -> None:
        messagebox.showinfo("Afterword",
                            "Thank you for playing TIC-TAC-TOE!\n\nI independently spent over a year building and updating this app.\n\nIn this project, I designed the AI that finds the highest win probability, arranged the GUI elements in the most ergonomic way, optimized the algorithms, fixed bugs, and learned tkinter.\n\nHope you enjoyed it!")

        self.root.destroy()


class SubMenu:
    root: tk.Tk
    settings: Settings

    def __init__(self, root: tk.Tk, settings: Settings):
        self.root = root
        self.settings = settings
        self.title_label = tk.Label(
            self.root,
            text="\nChoose a Mode",
            font=("FixedSys", 25, "bold", "underline"),
            **self.settings.MENU_LABEL_CFG
        )
        self.default_button = tk.Button(
            self.root,
            text="Traditional",
            width=25,
            command=lambda: self.to_gamemenu(GameMenu),
            **self.settings.MENU_BUTTON_CFG
        )
        self.default_help_button = tk.Button(
            self.root,
            bitmap="question",
            width=30,
            command=default_help,
            **self.settings.MENU_BUTTON_CFG
        )
        self.time_button = tk.Button(
            self.root,
            text="Timed Trial",
            width=25,
            command=lambda: self.to_gamemenu(GameMenuT),
            **self.settings.MENU_BUTTON_CFG
        )
        self.time_help_button = tk.Button(
            self.root,
            bitmap="question",
            width=30,
            command=time_help,
            **self.settings.MENU_BUTTON_CFG
        )
        self.vanish_button = tk.Button(
            self.root,
            text="Vanishing Moves",
            width=25,
            command=lambda: self.to_gamemenu(GameMenuV),
            **self.settings.MENU_BUTTON_CFG
        )
        self.vanish_help_button = tk.Button(
            self.root,
            bitmap="question",
            width=30,
            command=vanish_help,
            **self.settings.MENU_BUTTON_CFG
        )
        self.snake_button = tk.Button(
            self.root,
            text="Snake",
            width=25,
            command=lambda: self.to_gamemenu(GameMenuS),
            **self.settings.MENU_BUTTON_CFG
        )
        self.snake_help_button = tk.Button(
            self.root,
            bitmap="question",
            width=30,
            command=snake_help,
            **self.settings.MENU_BUTTON_CFG
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
            **self.settings.MENU_BUTTON_CFG
        )
        self.settings_button = tk.Button(
            self.bottom_frame,
            text="⚙",
            command=self.to_settings,
            width=12,
            **self.settings.MENU_BUTTON_CFG
        )

        # disables the close window button
        self.root.protocol("WM_DELETE_WINDOW", lambda: MainMenu.exit(self))

        # center buttons horizontally by giving a weight to all columns except the ones with the button
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

    def to_gamemenu(self, mode: type["GameMenu"]) -> None:
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
        self.col_frames = [
            tk.LabelFrame(
                self.root,
                text="General",
                **self.settings.COL_FRAME_CFG
            ),
            tk.LabelFrame(
                self.root,
                text="X colors",
                **self.settings.COL_FRAME_CFG
            ),
            tk.LabelFrame(
                self.root,
                text="O colors",
                **self.settings.COL_FRAME_CFG
            )
        ]
        self.exit_button = tk.Button(
            self.root,
            text="Save and Exit",
            width=25,
            command=self.to_submenu,
            **self.settings.MENU_BUTTON_CFG
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
                    **self.settings.MENU_LABEL_CFG
                )
                col_entry = tk.Entry(
                    self.col_frames[plyr],
                    textvariable=tk.StringVar(value=color),
                    borderwidth=1,
                    font=self.settings.MENU_FONT,
                    cursor="xterm",
                    foreground="Black",
                    background=color
                )

                col_label.grid(row=row, column=0, padx=10)
                col_entry.grid(row=row, column=1)

                # make the key release event update bg of textbox
                col_entry.bind("<KeyRelease>", lambda _, _plyr=plyr, _feat=feat: self.update_col(_plyr, _feat))
                self.col_entries[plyr][feat] = col_entry

    def update_col(self, plyr: int, feat: str) -> None:
        try:
            # try to set background color of the text widget
            self.col_entries[plyr][feat].config(bg=self.col_entries[plyr][feat].get())

        except tk.TclError:
            # if the color is not valid
            pass

    def to_submenu(self) -> None:
        # save colors
        for plyr, feats in enumerate(self.col_entries):
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
    :ivar moved: contains previous moves, in chronological order: front = earlier, back = later
    :ivar ai_moves: contains moves that AI is allowed to search
    """

    def __init__(self, root: tk.Tk, settings: Settings):
        self.root: tk.Tk = root
        self.settings: Settings = settings
        self.root.bind("<Configure>", self.update_scrollbars)  # update_scrollbars when window is resized
        self.root.bind("<MouseWheel>", self.scroll_vertical)  # scroll canvas vertically when any part of window has mouse wheel input
        self.root.bind("<Shift-MouseWheel>", self.scroll_horizontal)  # scroll canvas horizontally when any part of window has mouse wheel input

        tt.set_consts(self.settings.board_len.get(), self.settings.win_len.get())

        self.board: int = tt.EMPTY_BOARD
        self.moved: list[int | None] = []
        self.board_buttons: list[tk.Button] = []
        self.ai_moves: list[int] = []
        self.ai_thread: threading.Thread | None = None
        self.graph: nx.DiGraph | dict[int, float] | None = None

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
        self.turn_labels: list[tk.Label | None] = [
            None,
            # index 1 is X's
            tk.Label(
                self.board_frame,
                text="X turn",
                width=13,
                **self.settings.TURN_LABEL_CFG
            ),
            # index 2 is O's
            tk.Label(
                self.board_frame,
                text="O turn",
                width=13,
                **self.settings.TURN_LABEL_CFG
            )
        ]
        self.back_button = tk.Button(
            self.toolbar_frame,
            text="Back",
            command=self.to_submenu,
            **self.settings.TOOLBAR_BUTTON_CFG
        )
        self.new_game_button = tk.Button(
            self.toolbar_frame,
            text="Replay",
            state=tk.DISABLED,
            command=lambda: self.new_game(tt.EMPTY_BOARD),
            **self.settings.TOOLBAR_BUTTON_CFG
        )
        self.load_button = tk.Button(
            self.toolbar_frame,
            text="Load",
            command=lambda: LoadMenu(self.root, self),
            **self.settings.TOOLBAR_BUTTON_CFG
        )
        self.cheat_button = tk.Button(
            self.toolbar_frame,
            text="Cheat",
            command=self.cheat_button_press,
            **self.settings.TOOLBAR_BUTTON_CFG
        )
        self.hide_button = tk.Button(
            self.handle_frame,
            text="❮",
            font=self.settings.MENU_FONT,
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
            from_=3,
            to=19,
            command=self.update_len,
            **self.settings.SETTINGS_SLIDER_CFG
        )
        self.win_len_label = tk.Label(
            self.settings_frame,
            background=self.settings.colors[0]["foreground"],
            text="\nWin length"
        )
        self.win_len_slider = tk.Scale(
            self.settings_frame,
            variable=self.settings.win_len,
            command=lambda win_len: tt.set_consts(tk_win_len=int(win_len)),  # val is automatically passed by slider when it changes and is a str
            **self.settings.SETTINGS_SLIDER_CFG
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
            **self.settings.SETTINGS_SLIDER_CFG
        )
        self.ai_first_checkbox = tk.Checkbutton(
            self.settings_frame,
            text="Computer starts first",
            command=self.cheat_button_press,
            **self.settings.SETTINGS_CHECKBOX_CFG
        )
        self.ai_dropdown = tk.OptionMenu(
            self.settings_frame,
            self.settings.ai_type,
            *AI
        )
        self.ai_dropdown.config(
            background=self.settings.colors[0]["foreground"],
            activebackground=self.settings.colors[0]["foreground"],
            highlightthickness=0,
            cursor="hand2",
            relief=tk.GROOVE,
            borderwidth=4,
            width=len(max(AI, key=len)) - 3
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
            width=len(max(AI, key=len)) - 2,
            command=self.print_graph
        )
        self.ind_checkbox = tk.Checkbutton(
            self.settings_frame,
            text="Show indexes & highlights",
            variable=self.settings.show_ind,
            command=self.update_ind_and_highlight,
            **self.settings.SETTINGS_CHECKBOX_CFG
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
        self.log.bind("<Key>", lambda event: None if event.keysym in ("Up", "Down", tk.LEFT, tk.RIGHT) else "break")  # disable all user inputs in log except arrow keys
        self.log.bind("<Control-c>", lambda _: self.log.event_generate("<<Copy>>"))  # explicitly enable copy
        self.log.bind("<Control-a>", lambda _: self.log.event_generate("<<SelectAll>>"))  # explicitly enable select all

        self.root.config(background=self.settings.colors[0]["background"])
        self.settings_frame.pack(side=tk.LEFT, expand=False, fill=tk.Y)
        self.handle_frame.pack(side=tk.LEFT, expand=False, fill=tk.Y)
        self.board_frame.pack(side=tk.LEFT, expand=True, fill=tk.NONE)
        self.settings_frame.grid_columnconfigure(0, minsize=10)  # left padding for all settings widget
        self.settings_frame.grid_columnconfigure(3, minsize=15)  # right padding for all settings widget
        self.settings_frame.grid_rowconfigure(11, weight=1)  # ensures log's row (row 11) can expand
        self.toolbar_frame.grid(row=0, column=0, columnspan=4, pady=(0, 8), sticky=tk.W)

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
            self.ai_dropdown.grid(columnspan=2, row=8, column=1, pady=(0, 8))
            self.graph_button.grid(columnspan=2, row=9, column=1, pady=(0, 8))
        self.ind_checkbox.grid(columnspan=2, row=10, column=1, pady=(0, 13))
        self.log.grid(columnspan=2, row=11, column=1, sticky=tk.NSEW)

        self.__init_child__()  # must be before update_zoom() & after init all widgets since see GameMenuT

        self.update_ai_type()
        self.update_len()  # init buttons, win_len
        self.update_turn()  # init turn labels
        self.update_zoom()  # init fonts
        self.update_ind_and_highlight()  # in case this setting is on from last time

        # rebinds the close window button
        self.root.protocol("WM_DELETE_WINDOW", lambda: MainMenu.exit(self))

    def __init_child__(self):
        """Used by child classes."""
        pass

    def toggle_settings(self) -> None:
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
        self.insert_log("Cleared Ttable")

        if self.settings.ai_type.get() == RECUR_PROB_AI:
            self.graph_button.config(text="Show search histogram\n(impacts performance)")
        else:
            self.graph_button.config(text="Show search tree\n(impacts performance)")

    def scroll_vertical(self, event) -> None:
        self.board_canvas.yview_scroll(-1 * (event.delta // 120), tk.UNITS)

    def scroll_horizontal(self, event) -> None:
        self.board_canvas.xview_scroll(-1 * (event.delta // 120), tk.UNITS)

    def update_scrollbars(self, *_) -> None:
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

    def update_ind_and_highlight(self) -> None:
        """
        1. Show/hide indexes.
        2. Highlight/unhighlight moves.
        :return:
        """
        for sq, button in enumerate(self.board_buttons):
            # if empty
            if not tt.plyr_at(self.board, sq):
                button.config(
                    text=sq if self.settings.show_ind.get() else '',
                    background=self.settings.colors[0][
                        "ai_moves" if (self.settings.show_ind.get() and sq in self.ai_moves) else "board_button"
                    ]
                )

        self.root.update_idletasks()

    def update_len(self, _=None) -> None:
        """
        1. Update backend constants.
        2. Create / destory buttons to match new BOARD_AREA.
        3. Position new and old buttons.
        """
        # 1.
        tt.set_consts(tk_board_len=self.settings.board_len.get())
        self.insert_log("Cleared Ttable")

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
                    command=lambda SQ=len(self.board_buttons): self.board_button_press(SQ),
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
        self.win_len_slider.config(from_=min(tt.BOARD_LEN, 4), to=tt.BOARD_LEN)
        self.update_ind_and_highlight()
        self.update_scrollbars()
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
        for sq, button in enumerate(self.board_buttons):
            button.config(cursor="plus")

            if not tt.plyr_at(self.board, sq):
                button.config(state=tk.NORMAL)

    def place_pretasks(self) -> None:
        # if first move
        if not self.moved:
            self.lock_settings()

        # if not first move and not snake mode
        elif not isinstance(self, GameMenuS):

            # unhighlight last move
            self.board_buttons[self.moved[-1]].config(background=self.settings.colors[0]["board_button"])

    def cheat_button_press(self) -> None:
        self.place_pretasks()
        self.start_ai_thread()

    def board_button_press(self, SQ: int) -> None:
        self.place_pretasks()
        self.moved.append(SQ)
        self.place()

        if self.settings.is_pvc:

            # DO NOT exclude first move since first move can win with loaded board
            if not self.check_result_pvc(False):

                # in case need unhighlight last move
                self.place_pretasks()

                self.start_ai_thread()

        # pvp
        else:
            self.check_result_pvp()

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
        self.insert_log()

    def start_ai_thread(self) -> None:
        self.ai_thread = threading.Thread(target=self.ai_thread_work, daemon=True)
        self.ai_thread.start()
        self.insert_log(f"Spawned thread:\n{self.ai_thread.name}")
        self.poll_ai()

    def ai_thread_work(self) -> None:
        self.lock_board()

        # add slot for AI's move
        self.moved.append(None)

        # if AI starts first
        if len(self.moved) == 1:
            # moved[-1] is AI's move
            self.moved[-1] = random.randint(0, tt.BOARD_AREA - 1)

        # if AI starts second or loaded board
        else:
            PREPRUNE_LEN: int | None = None

            # function to inject into ai()
            def temp_highlight(NEXT_MOVE: int, BOARD: int) -> None:
                # if not root
                if BOARD != self.board:
                    return

                # if user ended game early, end thread
                if self.ai_thread is None:
                    sys.exit()

                if self.moved[-1] is not None:
                    # unhighlight previous move
                    self.board_buttons[self.moved[-1]].config(background=self.settings.colors[0]["ai_moves" if self.settings.show_ind.get() else "board_button"])

                # highlight current move
                self.board_buttons[NEXT_MOVE].config(background=self.settings.colors[0]["new_move"])
                self.root.update_idletasks()
                self.moved[-1] = NEXT_MOVE

            # choose ai
            ai: Callable
            args: tuple

            # if AI is snake and placed before, no need ai_moves
            if self.settings.ai_type.get() == RECUR_SNAKE_AI and len(self.moved) >= 3:
                ai = tt.snake_search
                self.ai_moves = list(
                    tt.sq_of(y, x)
                    for y, x in tt.snake_gen_moves(self.board, *divmod(self.moved[-3], tt.BOARD_LEN))
                )
                self.graph = nx.DiGraph()
                args = (
                    *divmod(self.moved[-3], tt.BOARD_LEN),
                    *divmod(self.moved[-2], tt.BOARD_LEN),
                )

            else:
                self.ai_moves = tt.gen_moves(self.board, self.moved[-2])
                self.insert_log(f"Preprune moves[]:\n{self.ai_moves}")
                PREPRUNE_LEN: int = len(self.ai_moves)

                if self.settings.ai_type.get() == RECUR_AND_OR_AI:
                    ai = tt.recur_search
                    self.ai_moves = self.ai_moves[:15]  # test shows can only search 15 squares in reasonable time
                    self.graph = nx.DiGraph()
                    args = (self.ai_moves.copy(),)  # must copy so AI thread doesn't refill main thread's ai_moves after end_game()

                elif self.settings.ai_type.get() == ITER_AND_OR_AI:
                    ai = tt.iter_search
                    self.ai_moves = self.ai_moves[:17]
                    self.graph = nx.DiGraph()
                    args = (set(self.ai_moves),)

                elif self.settings.ai_type.get() == RECUR_PROB_AI:
                    ai = tt.prob_search
                    self.ai_moves = self.ai_moves[:10]
                    self.graph = dict.fromkeys(self.ai_moves, 0)
                    args = (self.ai_moves.copy(),)

                elif self.settings.ai_type.get() == RECUR_SNAKE_AI:
                    ai = tt.snake_search_first_move
                    self.ai_moves = self.ai_moves[:16]
                    self.graph = nx.DiGraph()
                    args = (
                        self.ai_moves,  # no need copy since AI thread doesn't modify
                        *divmod(self.moved[-2], tt.BOARD_LEN),
                    )

            # unhighlight previous ai_moves, highlight new ones
            self.update_ind_and_highlight()

            # noinspection PyTypeChecker, PyUnboundLocalVariable
            ai(self.board, *args, self.graph, temp_highlight)

            if PREPRUNE_LEN is not None and PREPRUNE_LEN != len(self.ai_moves):
                # t_table unusable next time since board shape changed
                tt.t_table.clear()
                self.insert_log("Cleared Ttable")

    def poll_ai(self) -> None:
        """
        Poll for the finished AI thread.
        DO NOT merge with ai_thread_work() since matplotlib and tkinter should run in main thread.
        """
        # thread ended early
        if self.ai_thread is None:
            return

        if self.ai_thread.is_alive():
            self.root.after(50, self.poll_ai)
            return

        # thread ended normally
        self.insert_log(f"Thread ended:\n{self.ai_thread.name}")

        # moved[-1] is AI's move
        if self.moved[-1] is None:
            self.lock_board()
            messagebox.showinfo("Result", "Computer resigns.\n\nAI: 'I have already computed my inevitable fate ...'")
            return

        self.place()
        self.unlock_board()

        # check_result_pvc() must be after unlock_board()
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
                if messagebox.askyesno("Result", f"Computer won {WIN_DIR}!\n\nAI: 'Shouldn\'t humans be smarter?'") is True:
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
            self.root.geometry(self.settings.WINDOW_DIM)
            self.root.config(background="Black")
            SubMenu(self.root, self.settings)
            return True

        return False

    def new_game(self, board: int) -> bool:
        # if game is going, ask user
        if not self.moved or messagebox.askyesno(
                "Confirmation",
                "Are you sure you want to restart?\n\nYou will lose all your progress."):

            # if no last player in loaded board
            if not tt.plyr_of(board):
                messagebox.askretrycancel("Warning", "Enter a board with last player!")
                return False

            self.set_end_flags()
            self.ai_moves.clear()
            if self.moved and self.moved[-1] is not None:
                # unhighlight last move
                self.board_buttons[self.moved[-1]].config(background=self.settings.colors[0]["foreground"])
            self.moved.clear()

            # load new board
            self.board = board
            plyr: int
            for sq, button in enumerate(self.board_buttons):
                plyr = tt.plyr_at(self.board, sq)

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
                    button.config(
                        disabledforeground=self.settings.colors[plyr]["index"],
                        relief=tk.RAISED,  # for snake mode
                    )

            self.update_turn()
            self.update_ind_and_highlight()
            self.unlock_settings()
            self.insert_log("Reset game menu")
            self.insert_log()
            self.unlock_board()
            return True

        return False

    def insert_log(self, TEXT: str | None = None):

        # common case
        if TEXT is None:
            self.log.insert(
                tk.END,
                f"Move: {self.moved[-1] if self.moved else None}\n" +
                f"Last player: {tt.plyr_of(self.board)}\n" +
                f"Board: {self.board}\n" +
                f"Ttable size: {len(tt.t_table)}\n\n"
            )
        else:
            self.log.insert(tk.END, f"{TEXT}\n\n")

        self.log.see(tk.END)

    def print_graph(self) -> None:
        if self.graph is None:
            messagebox.showinfo("Warning", f"Perform an AI search first!")
            return

        if self.settings.ai_type.get() == RECUR_PROB_AI:
            self.print_histogram()
        else:
            self.print_tree()

    def print_histogram(self) -> None:
        plt.figure(num="Histogram")
        bar = plt.bar(list(self.graph.keys()), list(self.graph.values()), color="MediumSpringGreen")
        plt.bar_label(bar, label_type=tk.CENTER)
        plt.locator_params(axis=tk.X)  # set x tick interval
        plt.xlabel("Root Move")
        plt.ylabel("Weighted Win Probability")
        plt.title(f"{plt.gca().get_ylabel()} of each {plt.gca().get_xlabel()}")
        plt.show()

    def print_tree(self) -> None:
        def recapture_bg(_=None) -> None:
            """Retake screenshot after zoom or pan."""
            nonlocal bg
            fig.canvas.draw()  # redraw canvas to get correct bbox
            bg = fig.canvas.copy_from_bbox(fig.bbox)

        def on_click(event) -> None:
            """If mouse clicked on a node, update infobox to show its detailed information and animate scaling of clicked node."""
            IS_NODE, INFO = fig_nodes.contains(event)

            if IS_NODE:  # if clicked on a node
                # get the node under cursor and its label
                NODE = NODES[INFO["ind"][0]]
                NEG_DEPTH: int = int(POS[NODE][1])
                LABEL: plt.Text = fig_labels[NODE]

                # update infobox
                PARENTS = list(self.graph.predecessors(NODE))
                CHILDS = list(self.graph.successors(NODE))

                infobox.set_text(
                    f"Node: {NODE}\n"
                    f"Decoded:\n{tt.print_board(NODE, False)}"
                    f"Last Player: {tt.char_of(tt.plyr_of(NODE))}\n"
                    f"{len(PARENTS)} Parent: {PARENTS}\n"
                    f"{len(PARENTS)} Eldest Sibling: {[next(self.graph.successors(parent)) for parent in PARENTS]}\n"
                    
                    # total # of children of root (assume root has max # of children) - depth + # of visited children
                    # doesn't work for snake mode since assume factorial tree layout.
                    f"{len(self.ai_moves) + NEG_DEPTH - len(CHILDS)} Skipped Children\n"

                    f"{len(CHILDS)} Visited Children: {CHILDS}"
                )

                # draw
                def on_timer() -> None:
                    nonlocal frame
                    K: int = 8  # must be integer
                    scale = 1 + 0.5 * math.sin(math.pi * frame / K)
                    LABEL.set_fontsize(10 * scale)  # 10 is moveal size of node

                    fig.canvas.restore_region(bg)  # revert background to erase previous frame
                    fig.draw_artist(infobox)  # show temporary infobox while waiting for label animation
                    fig.draw_artist(LABEL)
                    fig.canvas.blit(fig.bbox)

                    frame += 1
                    if frame > 8:
                        timer.stop()
                        fig.canvas.draw_idle()
                        return

                frame = 0
                timer = fig.canvas.new_timer(interval=20, callbacks=[(on_timer, (), {})])
                timer.start()

            else:
                infobox.set_text(EMPTY_INFOBOX_TEXT)
                fig.canvas.draw_idle()

        def on_move(event) -> None:
            """If mouse hover over a node, change cursor to hand2."""
            IS_NODE, _ = fig_nodes.contains(event)
            fig.canvas.get_tk_widget().config(cursor="hand2" if IS_NODE else "")

        EMPTY_INFOBOX_TEXT: str = f"Total # of Nodes: {self.graph.number_of_nodes()}\nClick a node for more details!"
        NODES: list = list(self.graph.nodes)
        POS: dict[..., tuple[float, float]] = tt.recip_tree_pos(self.graph)
        fig = plt.figure(num="Depth-first-search Tree")

        # draw nodes and edges separately to set picker on nodes
        fig_nodes = nx.draw_networkx_nodes(
            self.graph,
            POS,
            node_shape='s',
            alpha=0.0
        )
        # noinspection PyTypeChecker
        fig_nodes.set_picker(True)

        # use fig_labels insead of nx.draw_networkx_labels to color each label separately
        fig_labels: dict = dict()
        node_col: str
        for node, (x, y) in POS.items():
            # node not in t_table is possible during iter search
            if node not in tt.t_table:
                node_col = "White"
            elif tt.t_table[node] == tt.WIN_SCORE:
                node_col = "MediumSpringGreen"
            elif tt.t_table[node] == 0:
                node_col = "Yellow"
            else:
                node_col = "Tomato"

            fig_labels[node] = plt.text(
                x, y, node,
                ha=tk.CENTER,
                va=tk.CENTER,
                bbox=dict(facecolor=node_col, boxstyle="round", pad=0.4, linewidth=0.5),
                color="Black",
                family="Arial",
                weight="bold",
                size=10
            )

        nx.draw_networkx_edges(
            self.graph, POS, arrows=False, alpha=0.75
        )
        nx.draw_networkx_edge_labels(
            self.graph, POS, nx.get_edge_attributes(self.graph, "label"),
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.5, boxstyle="circle", pad=0),
            font_color="black",
            font_family="Arial",
            # font_size=10,
            rotate=False
        )

        bg = None
        recapture_bg()  # screenshot background WITHOUT infobox

        infobox = plt.text(
            0.0, 0.0, EMPTY_INFOBOX_TEXT,
            transform=plt.gca().transAxes,  # use axes fraction for positioning
            bbox=dict(facecolor="white", edgecolor="gray", alpha=0.8, boxstyle="square", pad=0.75),
            family="Consolas",
            linespacing=1.5
        )

        plt.axis(False)
        plt.tight_layout()
        fig.gca().callbacks.connect("xlim_changed", recapture_bg)
        fig.gca().callbacks.connect("ylim_changed", recapture_bg)
        fig.canvas.mpl_connect("resize_event", recapture_bg)
        fig.canvas.mpl_connect("button_press_event", on_click)
        fig.canvas.mpl_connect("motion_notify_event", on_move)
        plt.show()


class GameMenuT(GameMenu):
    """
    :ivar label_scale: Inflation of the active timer, used for animation. Resets to 0 at the beginning of each turn.
    :ivar time: How much time each player still has: index 1 is X's; index 2 is O's.
    """

    def __init__(self, root: tk.Tk, settings: Settings):
        self.is_countdown: bool = True
        self.label_scale: int = 0

        super().__init__(root, settings)

    def __init_child__(self):
        self.time = [
            None,
            tk.DoubleVar(value=self.settings.INIT_TIME),
            tk.DoubleVar(value=self.settings.INIT_TIME)
        ]
        self.trace1 = self.time[1].trace_add("write", lambda _, __, ___: self.validate(self.time[1]))
        self.trace2 = self.time[2].trace_add("write", lambda _, __, ___: self.validate(self.time[2]))

        # change widget class of turn_labels from Label to LabelFrame
        self.turn_labels[1].destroy()
        self.turn_labels[2].destroy()
        self.turn_labels = [
            None,
            tk.LabelFrame(
                self.board_frame,
                text="X turn",
                **self.settings.TURN_LABEL_CFG
            ),
            tk.LabelFrame(
                self.board_frame,
                text="O turn",
                **self.settings.TURN_LABEL_CFG
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
        self.countdown()

    def unlock_settings(self) -> None:
        super().unlock_settings()

        self.time_entry[1].config(state=tk.NORMAL)
        self.time_entry[2].config(state=tk.NORMAL)
        self.time[1].set(self.settings.INIT_TIME)
        self.time[2].set(self.settings.INIT_TIME)

        # reset time_entry inflation
        self.update_zoom()

    def validate(self, VAR: tk.DoubleVar) -> None:
        try:
            # try to convert the remain time to float
            VAR.get()

        except tk.TclError:
            # if the remain time is not float, show a messagebox and reset the value
            messagebox.askretrycancel("Warning", f"Enter a decimal number!")
            VAR.set(self.settings.INIT_TIME)

    def countdown(self) -> None:
        """Recursively decrement time."""

        # if game ended
        if not self.is_countdown:
            return

        TIME: float = self.time[tt.opp_of(tt.plyr_of(self.board))].get()

        # if player runs out of time, opponent wins
        if TIME <= 0:
            messagebox.showinfo("Result", f"Time's up! Player {tt.char_of(tt.plyr_of(self.board))} won!")
            self.lock_board()
            self.set_end_flags()
            return

        # animate inflate of the current plyr's timer
        # max scale must be odd number for ease-out
        self.label_scale = min(self.label_scale + 2, 5)
        self.time_entry[tt.opp_of(tt.plyr_of(self.board))].config(
            font=("Courier", self.settings.board_zoom.get() * 3 + 2 + self.label_scale, "bold")
        )

        # if X has under 5 secs left
        if TIME < 5.0:
            # flash the timer
            if TIME % 1 < 0.4:
                self.time_entry[tt.opp_of(tt.plyr_of(self.board))].config(
                    relief=tk.SUNKEN,
                    disabledbackground="white",
                )
            else:
                self.time_entry[tt.opp_of(tt.plyr_of(self.board))].config(
                    relief=tk.GROOVE,
                    disabledbackground="yellow"
                )
        self.root.update_idletasks()

        # decrease the time value by 0.1 every 100ms and display only 1 decimal point using round().
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
        # reset inflate animation
        self.label_scale = 0

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

        if self.moved:
            # current plyr gets bonus time
            self.time[tt.plyr_of(self.board)].set(self.time[tt.plyr_of(self.board)].get() + 1)

    def to_submenu(self) -> None:
        if super().to_submenu():
            self.time[1].trace_remove("write", self.trace1)
            self.time[2].trace_remove("write", self.trace2)


class GameMenuV(GameMenu):
    """
    :ivar settings.queue_len: how many turns into the future will an X/O last.
    :ivar settings.show_qfront: show/hide the moves about to pop in the next turns.
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
            **self.settings.SETTINGS_SLIDER_CFG
        )
        self.show_qfront_checkbox = tk.Checkbutton(
            self.settings_frame,
            text="Show queue front",
            variable=self.settings.show_qfront,
            command=self.update_qfront_highlight,
            **self.settings.SETTINGS_CHECKBOX_CFG
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

    def update_qfront_highlight(self) -> None:

        # queue_len is # moves allowed for each player
        # FULL_QUEUE_LEN is for both players
        FULL_QUEUE_LEN: int = 2 * self.settings.queue_len.get()

        # highlight move to pop this and next turn
        if len(self.moved) >= FULL_QUEUE_LEN:
            COL: str = self.settings.colors[0]["queue_front" if self.settings.show_qfront.get() else "board_button"]

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
            self.insert_log(
                f"Pop move: {POP_MOVE}\n" +
                f"Queue:\n{self.moved}"
            )

        self.update_qfront_highlight()

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

    def __init__(self, root: tk.Tk, settings: Settings):
        super().__init__(root, settings)

        # X always win if board_len is < 4. The slider automatically call update_len() to update cross-file vars.
        self.board_len_slider.config(from_=4)
        self.update_len()
        self.settings.ai_type.set(RECUR_SNAKE_AI)
        self.update_ai_type()

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


# === Help Pop-ups ===
FOR_MORE_DETAILS: str = "For more details, read the ⍰ of the Traditional mode."


def default_help() -> None:
    messagebox.showinfo("Help",
                        "Just like the good ol\' one you played in kindergarten...\n\nYou can select a board length between 2 and... infinity? Boards larger than 3x3 only needs 4 in a row to win!\n\nThe starting player is always X, and the other is O. No friends? No worries! You can play with one of four unique AIs designed by me and my friend.")


def time_help() -> None:
    messagebox.showinfo("Help",
                        f"Each player has a certain amount of time to complete the game. At the start, you can set the time.\n\nAfter each move, you earn 1 extra second!\n\nThe AIs don't know there's a time limit, but they might get faster after a few games.\n\n{FOR_MORE_DETAILS}")


def vanish_help() -> None:
    messagebox.showinfo("Help",
                        f"After a certain number of moves, your oldest move will vanish!\n\nPoor memory? Enable 'Show queue front' to highlight your oldest move in yellow.\n\nThe number of moves you can have on the board at any time is determined by 'Queue length'. What is a queue you asked? Go study computer science!\n\nBefore you go, here's a tip: the AIs don't know that moves vanish!\n\n{FOR_MORE_DETAILS}")


def snake_help() -> None:
    messagebox.showinfo("Help",
                        f"For your first move, you can place wherever you want.\n\nAfterwards, you can only place around your last move ( your snake's head ). Watch where your snake is going, as turning around can take some time.\n\nBesides winning traditionally, you can also win by trapping your opponent in a corner! I recommend playing on a 7x7 or larger board.\n\n{FOR_MORE_DETAILS}")


def changelog() -> None:
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
    VER: str = "Tic Tac Toe v18"

    root = tk.Tk()
    MainMenu(root, Settings())
    root.mainloop()
