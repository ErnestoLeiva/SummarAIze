from tkinter import ttk
import tkinter as tk

class ThemedScrolledText(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        
        self.text = tk.Text(self, **kwargs, relief='flat', bd=0, highlightthickness=0)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self.scrollbar.set)
        
        style = ttk.Style()
        theme_bg = style.lookup('TFrame', 'background')
        
        if theme_bg:
            rgb_bg = self.hex_to_rgb(theme_bg)
            adjusted_rgb = self.adjust_brightness(rgb_bg, 1.1)
            adjusted_bg = self.rgb_to_hex(adjusted_rgb)
            self.text.configure(bg=adjusted_bg, fg='white', insertbackground='white')
    
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def adjust_brightness(self, rgb_color, factor):
        return tuple(min(255, int(c * factor)) for c in rgb_color)

    def rgb_to_hex(self, rgb_color):
        return '#{:02x}{:02x}{:02x}'.format(*rgb_color)