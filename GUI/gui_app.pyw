import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from themes.others.ttk_scrollbar import ThemedScrolledText
from utils.settings import load_settings, save_settings, MAIN_ICON, DEFAULT_MODEL, MODEL_CHOICES
from utils.gui_helpers import set_icon, set_window_constraints, center_window, MIN_WIDTH, MIN_HEIGHT
from utils.summarize import run_summarizer
from utils.theme import get_current_theme, apply_theme, toggle_theme_util
from utils.version_helper import get_version
from utils.ansi import ANSI_COLOR_MAP, ANSI_PATTERN

class SummarAIzeGUI(tk.Tk):
    """
    The main GUI class for SummarAIze. \n
    Handles all user interaction, file selection, theme toggling, \n
    and real-time subprocess output streaming with ANSI coloring.
    """

    # ===== GUI Setup & Init ====
    def __init__(self) -> None:
        """Initialize the SummarAIze GUI window, load settings, apply theme, center window, and create all widgets."""

        super().__init__()
        
        # ===== Set title & icon =====
        self.title(f"SummarAIze [v{get_version()}]")
        set_icon(self, MAIN_ICON)
        
        # ===== Load settings & set window contraints ===== 
        self.settings = load_settings()
        width = self.settings["Options"].get("width", MIN_WIDTH)
        height = self.settings["Options"].get("height", MIN_HEIGHT)
        self.geometry(f"{width}x{height}")
        set_window_constraints(self)
        
        # ===== Apply Azure theme ===== [dark & light themes]
        apply_theme(self, get_current_theme(self.settings))

        # ===== Initialize the variables =====
        saved_model = self.settings["Options"].get("model", "BART")
        if saved_model not in MODEL_CHOICES:
            saved_model = DEFAULT_MODEL
        self.model_choice = tk.StringVar(value=saved_model)
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.save_to_file = tk.BooleanVar(value=self.settings["Options"].get("output_on", False))

        # ===== Create the widgets/elements of the GUI ===== [e.g. Buttons, dropdowns, etc.]
        self.create_widgets()

        # ===== Bind resizing event to save window dimensions =====
        self.bind("<Configure>", self._on_resize)

        # ===== Always start app at the center of the user's screen =====
        center_window(self)

        # ===== DEBUG FUNCTION =====
        #self.start_debug_resize_watcher()
    def create_widgets(self) -> None:
        """Construct and lay out all GUI widgets, including buttons, input fields, output area, and progress bar."""

        # ===== TOPBAR/TOOLBAR FRAME =====
        topbar = ttk.Frame(self, padding=5)
        topbar.pack(side="top", fill="x")
        ttk.Separator(self, orient="horizontal").pack(fill="x")

        # ===== TITLE LABEL =====
        title_label = ttk.Label(
            topbar,
            text="Summarize Legal Documents - [CAP4630 Group 3]",
            font=("Segoe UI", 12, "bold")
        )
        title_label.pack(side="left", padx=10)

        # ===== THEME TOGGLE BUTTON =====
        self.is_dark_theme = tk.BooleanVar(value=self.settings["Customization"].get("theme", "dark") == "dark")
        self.theme_toggle = ttk.Checkbutton(
            topbar,
            variable=self.is_dark_theme,
            command=self.toggle_theme,
            style="Toggle.TButton",
            text="🌙" if self.is_dark_theme.get() else "🌞"
        )
        self.theme_toggle.pack(side="right")

        # ===== MAIN FRAME =====
        frame = ttk.LabelFrame(self, text="SummarAIze Options", padding=(20, 5))
        frame.pack(padx=20, pady=5, fill="x")

        # ===== MODEL SELECTION =====
        ttk.Label(frame, text="Select Model:").grid(row=0, column=0, sticky="w")
        self.model_choice.set(self.settings["Options"].get("model", "BART"))  # default value of BART
        self.model_menu = ttk.OptionMenu(
            frame,
            self.model_choice,
            self.model_choice.get(),
            *MODEL_CHOICES,
            command=lambda val: save_settings(
                self._current_theme(),
                val,
                self.save_to_file.get(),
                self.winfo_width(),
                self.winfo_height()
            )
        )
        self.model_menu.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # ===== INPUT FILE SELECTION =====
        ttk.Label(frame, text="Select Input File:").grid(row=1, column=0, sticky="w")
        self.input_button = ttk.Button(frame, text="Browse", command=self.select_input_file, style='Accent.TButton')
        self.input_button.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        # INPUT FILE LABEL
        self.input_file_label = ttk.Label(frame, text="", wraplength=300)
        

        # ===== OUTPUT FILE SELECTION & TOGGLE =====
        self.output_toggle_button = ttk.Checkbutton(frame, text="Save output to file", variable=self.save_to_file, command=self.toggle_output, style='Switch.TCheckbutton')
        self.output_toggle_button.grid(row=2, column=0, sticky="w")
        self.output_button = ttk.Button(frame, text="Choose Output File", command=self.select_output_file, style='Accent.TButton')
        self.output_button.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        # OUTPUT FILE LABEL
        self.output_file_label = ttk.Label(frame, text="", wraplength=300)
        
        # ===== OUTPUT/CONTENT FRAME =====
        self.content_frame = ttk.Frame(self, style='Card.TFrame')
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.output_box_frame = ttk.Frame(self.content_frame, style='Card.TFrame')
        self.output_box_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ===== OUTPUT CONTENT BOX ===== [uses the custom scrollbar] 
        self.output_box = ThemedScrolledText(self.output_box_frame, wrap="word", theme=self._current_theme())
        self.output_box.pack(fill="both", expand=True)
        self.output_box.text.config(state="disabled")

        # OUTPUT CONTENT BOX COLOR TAGS 
        self._init_color_tags()

        # ===== SUMMARIZE SUBMIT BUTTON =====
        self.summarize_btn = ttk.Button(self, text="SummarAIze", command=self.summarize, style='Accent.TButton')
        self.summarize_btn.pack(pady=10)


        # ===== PROGRESS BAR ===== [does not show progress, just activity: its indeterminate]
        self.progress = ttk.Progressbar(self, mode='indeterminate')
        self.progress.pack(fill='x', padx=20, pady=(0, 10))
        self.progress.stop()
        self.progress.pack_forget()  # Hide initially


        # ========== DEBUG SECTION ========== 
        #self.start_debug_resize_watcher()
        #self._stream_to_output_box("\033[91mError:\033[0m Something went wrong.")
        #self._stream_to_output_box("\033[92mSuccess:\033[0m Everything worked.")

    # ===== Theme & Styling =====
    def _init_color_tags(self):
        """Define color tags for the output text box to visually differentiate status messages."""

        self.output_box.text.tag_config("red", foreground="#ff5c5c")
        self.output_box.text.tag_config("green", foreground="#4caf50")
        self.output_box.text.tag_config("yellow", foreground="#ffc107")
        self.output_box.text.tag_config("blue", foreground="#42a5f5")
        self.output_box.text.tag_config("magenta", foreground="#d81b60")
        self.output_box.text.tag_config("cyan", foreground="#00acc1")
    def _current_theme(self):
        """Return the currently selected theme as a string: 'dark' or 'light'."""

        return "dark" if self.is_dark_theme.get() else "light"
    def toggle_theme(self):
        """Switch between light and dark themes, update icons and theme styles, and save the selection."""

        toggle_theme_util(
            window=self,
            is_dark_var=self.is_dark_theme,
            model=self.model_choice.get(),
            output_on=self.save_to_file.get(),
            toggle_btn=self.theme_toggle,
            output_box=self.output_box
        )
        self.output_box.update_theme(self._current_theme())

    # ===== Event handling =====
    def _on_resize(self, event):
        """Debounce window resizing and schedule saving updated window dimensions."""

        if event.widget is self:
            if hasattr(self, "_resize_after_id"):
                self.after_cancel(self._resize_after_id)
            self._resize_after_id = self.after(500, self._save_current_window_size)
    def _save_current_window_size(self):
        """Save the current window width and height to the settings configuration."""

        save_settings(
            theme=self._current_theme(),
            model=self.model_choice.get(),
            output_on=self.save_to_file.get(),
            width=self.winfo_width(),
            height=self.winfo_height()
        )
    def toggle_output(self):
        """Apply window constraints and persist output toggle state to settings."""

        self.update_idletasks()

        set_window_constraints(self)
        
        save_settings(
            self._current_theme(), 
            self.model_choice.get(), 
            self.save_to_file.get(),
            self.winfo_width(),
            self.winfo_height()
        )
    def select_input_file(self):
        """Open file dialog to select an input file and display its name in the UI."""

        file_path = filedialog.askopenfilename(title="Input File", filetypes=[("Supported Files", "*.txt *.pdf *.docx")])
        if file_path:
            self.input_file.set(file_path)
            self.input_file_label.grid(row=1, column=2, sticky="w", padx=5)
            self.input_file_label.config(text=os.path.basename(file_path))  # show only filename
    def select_output_file(self):
        """Open file dialog to set output destination and display its name in the UI."""

        file_path = filedialog.asksaveasfilename(title="Output File", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.output_file.set(file_path)
            self.output_file_label.grid(row=2, column=2, sticky="w", padx=5)
            self.output_file_label.config(text=os.path.basename(file_path))  # show only filename

    # ===== Threaded SummarAIzation handling ===== [Threaded &+ SubProcess]
    def summarize(self):
        """Validate input/output paths, clear the output box, and launch threaded summarization process."""

        model = self.model_choice.get()
        input_path = self.input_file.get()
        output_path = self.output_file.get() if self.save_to_file.get() else None

        if not input_path:
            messagebox.showerror("Input Error", "Please select an input file.")
            return

        if self.save_to_file.get() and not output_path:
            messagebox.showerror("Output Error", "Please select an output file.")
            return

        # Clear current output box / label before running
        self.output_box.text.config(state="normal") 
        self.output_box.text.delete("1.0", tk.END)
        self.output_box.text.config(state="disabled") 

        # Disable buttons to prevent repeat clicks
        self.summarize_btn.config(state="disabled")
        self.output_toggle_button.config(state=tk.DISABLED)
        self.output_button.config(state=tk.DISABLED)
        self.input_button.config(state=tk.DISABLED)
        self.model_menu.config(state=tk.DISABLED)

        # Start the background summarization thread
        threading.Thread(
            target=self._run_summarize_thread,
            args=(model, input_path, output_path),
            daemon=True
        ).start()
    def _run_summarize_thread(self, model, input_path, output_path):
        """Run the CLI summarization script in a background thread and stream output line-by-line to the GUI."""

        # show & start the indeterminate bar
        self.after(0, self.progress.pack, {"fill": "x", "padx": 20})
        self.after(0, self.progress.start, 10)

        # ---- THREAD‑SAFE WRAPPER --------------------------------------
        def safe_gui_callback(line: str):
            # hop to the main thread before touching widgets
            self.after(0, self._stream_to_output_box, line)
        # ----------------------------------------------------------------

        # run the CLI in this background thread
        output = run_summarizer(model, input_path, output_path,
                                gui_callback=safe_gui_callback)

        # when finished, schedule the “done” handler on the UI thread
        self.after(0, self._on_summarize_complete, output, output_path)
    def _on_summarize_complete(self, output, output_path):
        """Handle cleanup and UI reset after the summarization process finishes (success or failure)."""

        # RESET PROGRESS BAR
        self.progress.stop()
        self.progress.pack_forget()

        # Re-enable summarize button
        self.summarize_btn.config(state="normal")
        self.output_toggle_button.config(state=tk.NORMAL)
        self.output_button.config(state=tk.NORMAL)
        self.input_button.config(state=tk.NORMAL)
        self.model_menu.config(state=tk.NORMAL)

        # Save latest settings again
        save_settings(
            self._current_theme(),
            self.model_choice.get(),
            self.save_to_file.get(),
            self.winfo_width(),
            self.winfo_height()
        )
    def _stream_to_output_box(self, message):
        """Insert output from the CLI into the output box, preserving color using ANSI tags."""

        self.output_box.text.config(state="normal") # enable editing

        parts = ANSI_PATTERN.split(message)
        current_tag = None

        for part in parts:
            if part in ANSI_COLOR_MAP:
                current_tag = ANSI_COLOR_MAP[part]
            else:
                self.output_box.text.insert("end", part, current_tag)

        self.output_box.text.insert("end", "\n")
        self.output_box.text.see("end")
        self.output_box.text.config(state="disabled") # disable editing

    # ===== DEBUGER HELPERS =====
    def start_debug_resize_watcher(self):
        width = self.winfo_width()
        height = self.winfo_height()

        if hasattr(self, "output_box"):
            self.output_box.text.delete("1.0", tk.END)
            self.output_box.text.insert("1.0", f"Window size: {width} x {height}")

        self.title(f"SummarAIze - Win Size: {width} x {height}")

        # 500 ms refresh
        self.after(500, self.start_debug_resize_watcher)


if __name__ == "__main__":
    app = SummarAIzeGUI()
    app.mainloop()