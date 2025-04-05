from tkinter import ttk
import tkinter as tk

class ThemedScrolledText(ttk.Frame):
    def __init__(self, parent, theme="dark", **kwargs):
        super().__init__(parent)
        self.theme = theme  # default to dark

        self.text = tk.Text(self, **kwargs, relief='flat', bd=0, highlightthickness=0)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self.scrollbar.set)

        self.refresh_theme()

    def refresh_theme(self):
        if self.theme == "light":
            self.text.configure(bg="#ffffff", fg="#000000", insertbackground="#000000")
        else:
            self.text.configure(bg="#333333", fg="#ffffff", insertbackground="#ffffff")

    def update_theme(self, theme):
        """Call this to dynamically change the theme at runtime"""
        self.theme = theme
        self.refresh_theme()

    def is_valid_hex(self, color) -> bool:
        return isinstance(color, str) and color.startswith('#') and len(color) == 7

    def hex_to_rgb(self, hex_color) -> tuple[int, ...]:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def adjust_brightness(self, rgb_color, factor) -> tuple[int, ...]:
        return tuple(min(255, int(c * factor)) for c in rgb_color)

    def rgb_to_hex(self, rgb_color) -> str:
        return '#{:02x}{:02x}{:02x}'.format(*rgb_color)