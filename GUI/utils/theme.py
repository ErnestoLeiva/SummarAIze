import os
from utils.settings import save_settings

def get_current_theme(settings: dict) -> str:
    """Return the current theme from settings, defaulting to 'dark'."""
    return settings.get("Customization", {}).get("theme", "dark")

def get_theme_from_bool(is_dark: bool) -> str:
    return "dark" if is_dark else "light"

def apply_theme(window, theme_name: str) -> None:
    """Apply Azure theme to the given window with the specified theme."""
    cur_dir = os.path.dirname(__file__)
    theme_path = os.path.normpath(os.path.join(cur_dir, "..", "themes", "azure-ttk-theme", "azure.tcl"))
    window.tk.call("source", theme_path)
    window.tk.call("set_theme", theme_name)

def toggle_theme_util(window, is_dark_var, model, output_on, toggle_btn, output_box) -> None:
    """Handles UI + settings logic for theme switching"""
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

def apply_toggle_style(current_theme, ttk) -> None:
    style = ttk.Style()
    
    style.configure("ThemeToggle.TCheckbutton",
                    background="#2e2e2e" if current_theme == "dark" else "#f7f7f7",
                    borderwidth=1,
                    relief="raised",
                    padding=5)