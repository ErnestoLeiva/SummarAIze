import os
from tkinter import PhotoImage
from typing import TYPE_CHECKING, Union # used for NameError runtime exception 
if TYPE_CHECKING:
    import tkinter as tk

# ===== GLOBALS =====
MIN_WIDTH = 649
MIN_HEIGHT = 725

MAX_WIDTH = 800
MAX_HEIGHT = 900

ICON_NAME = "icon.png" # stored in %PROJECTROOT%/GUI/icons/

def set_icon(window: "tk.Tk", icon_name: str = ICON_NAME) -> None:
    """Set default icon accross tkinter app"""
    icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", icon_name)
    icon = PhotoImage(file=icon_path)
    window.iconphoto(True, icon)

def set_window_constraints(window: "tk.Tk") -> None:
    """Set min/max size depending on output toggle without resetting geometry."""
    window.minsize(MIN_WIDTH, MIN_HEIGHT)
    window.maxsize(MAX_WIDTH, MAX_HEIGHT)
    #window.resizable(True, False) # was causing stutter so i disabled

def center_window(window: Union["tk.Tk", "tk.Toplevel"]) -> None:
    """Center tkinter app on the center of user's screen"""
    window.update_idletasks()
    
    # Get screen dimensions
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    
    # Get tkinter window dimensions
    win_w = window.winfo_width()
    win_h = window.winfo_height()

    # Calculate centering
    x = (screen_w - win_w) // 2
    y = (screen_h - win_h) // 2
    
    # Shift position to center (uses '+' to control window position, not dimensions)
    window.geometry(f"+{x}+{y}")
