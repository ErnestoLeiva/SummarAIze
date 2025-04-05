import os
from tkinter import PhotoImage
from typing import TYPE_CHECKING, Union # used for NameError runtime exception 
if TYPE_CHECKING:
    import tkinter as tk

# ---- GLOBALS ----
MIN_WIDTH = 649
MIN_HEIGHT = 725

MAX_WIDTH = 800
MAX_HEIGHT = 900

def set_icon(window, icon_name="icon.png") -> None:
    """Set default icon accross tkinter app"""
    icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", icon_name)
    icon = PhotoImage(file=icon_path)
    window.iconphoto(True, icon)

def set_window_constraints(window, output_not_enabled: bool) -> None:
    """Set min/max size depending on output toggle without resetting geometry."""
    window.minsize(MIN_WIDTH, MIN_HEIGHT)
    window.maxsize(MAX_WIDTH, MAX_HEIGHT)
    #window.resizable(True, False) # was causing stutter so i disabled

def center_window(window: Union["tk.Tk", "tk.Toplevel"]):
    window.update_idletasks()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    win_w = window.winfo_width()
    win_h = window.winfo_height()
    x = (screen_w - win_w) // 2
    y = (screen_h - win_h) // 2
    window.geometry(f"+{x}+{y}")
