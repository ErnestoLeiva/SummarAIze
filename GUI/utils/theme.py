import os
from utils.settings import save_settings
from typing import TYPE_CHECKING # used for NameError runtime exception 
if TYPE_CHECKING:
    import tkinter as tk
    from tkinter import ttk

def get_current_theme(settings: dict) -> str:
    """
    Retrieve the current UI theme from the loaded settings.

    ***
    Returns the user's saved theme ("dark" or "light") from the settings dictionary.
    If no theme is found, the default value "dark" is returned.
    ***

    Args:
        settings (dict): The loaded settings dictionary from settings.json.

    Returns:
        str: The name of the active theme, either "dark" or "light".
    """

    return settings.get("Customization", {}).get("theme", "dark")

def get_theme_from_bool(is_dark: bool) -> str:
    """Short boolean checker only used within the scope of this module"""
    return "dark" if is_dark else "light"

def apply_theme(window: "tk.Tk", theme_name: str) -> None:
    """
    Apply the Azure theme to the given Tkinter window.

    ***
    Loads and applies the Azure ttk theme from the local filesystem.
    The theme is applied via Tcl calls and updates the styling of all ttk widgets
    within the provided Tk window.
    ***

    Args:
        window (tk.Tk): The root Tkinter window to apply the theme to.
        theme_name (str): The name of the theme to apply ("dark" or "light").
    """

    cur_dir = os.path.dirname(__file__)
    theme_path = os.path.normpath(os.path.join(cur_dir, "..", "themes", "azure-ttk-theme", "azure.tcl"))
    window.tk.call("source", theme_path)
    window.tk.call("set_theme", theme_name)

def toggle_theme_util(window: "tk.Tk", is_dark_var: "tk.BooleanVar", model: str, output_on: bool, toggle_btn: "tk.Checkbutton", output_box: "tk.Widget") -> None:
    """
    Toggle between light and dark themes and update the application state.

    ***
    Applies the selected theme to the main window using `set_theme`, updates the
    toggle button icon based on the current theme, refreshes the output box styling,
    and saves the updated UI state (including theme, model, and dimensions) to settings.json.
    ***

    Args:
        window (tk.Tk): The main application window.
        is_dark_var (tk.BooleanVar): BooleanVar tracking whether dark mode is enabled.
        model (str): The currently selected summarization model.
        output_on (bool): Whether output-to-file is currently enabled.
        toggle_btn (tk.Checkbutton): The checkbutton widget used for toggling theme.
        output_box (tk.Widget): The output display widget with optional `refresh_theme()` support.
    """

    theme = get_theme_from_bool(is_dark_var.get())

    # Apply the theme to the app
    window.tk.call("set_theme", theme)

    # Update icon
    toggle_btn.config(text="🌙" if theme == "dark" else "🌞")

    # Update widget theming
    if hasattr(output_box, "refresh_theme"):
        output_box.refresh_theme()

    # Save settings each toggle
    save_settings(theme, model, output_on, window.winfo_width(), window.winfo_height())