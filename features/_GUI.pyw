import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from ttkthemes import ThemedTk
from custom_classes.ttk_scrollbar import ThemedScrolledText
import subprocess
import sys
import os
import threading

class SummarAIzeApp:
    def __init__(self, root):
        self.root = root
        self.root.title('SummarAIze [ALPHA]')
        self.root.resizable(False, False)

        # Output Text Box (ScrolledText widget)
        self.output_frame = ttk.Frame(self.root)
        self.output_frame.pack(pady=5)
        
        self.output_label = ttk.Label(self.root, text="SummarAIzed Text:")
        self.output_label.pack(anchor=tk.W, pady=5, padx=5)

        self.output_text = ThemedScrolledText(self.root, wrap=tk.WORD, height=15, width=70, font=('Arial', 10))
        self.output_text.pack(pady=10, padx=10)
        
        self.output_text.text.config(state=tk.DISABLED)
        self.output_text.text.tag_config('info', foreground='cyan')
        self.output_text.text.tag_config('error', foreground='red')
        self.output_text.text.tag_config('success', foreground='lightgreen')
        self.output_text.text.tag_config('highlight', foreground='yellow')

        # Input Entry Field
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(pady=5)
        
        self.input_label = ttk.Label(self.input_frame, text="Enter text to summarize:")
        self.input_label.pack(anchor=tk.W, pady=5, padx=5)
        
        self.input_entry = ThemedScrolledText(self.input_frame, wrap=tk.WORD, height=15, width=70, font=('Arial', 10))
        self.input_entry.pack(pady=10, padx=10)

        # SummarAIze Button
        self.summarize_button = ttk.Button(self.root, text='SummarAIze Text', command=self.summarize_text)
        self.summarize_button.pack(pady=10)

    def summarize_text(self):
        # clear output text box before summarizing
        self.output_text.text.config(state=tk.NORMAL)
        self.output_text.text.delete('1.0', tk.END)
        self.output_text.text.config(state=tk.DISABLED)
        
        # get the input text
        input_text = self.input_entry.text.get('1.0', tk.END).strip()
        
        # if input was empty
        if not input_text:
            messagebox.showerror("Error", "EMPTY INPUT", detail="No text was entered and we need that... thanks!")
            return

        # if ai-sum.py file is not found
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ai-sum.py'))
        if not os.path.isfile(script_path):
            messagebox.showerror("Error", "\"ai-sum.py\" NOT FOUND", detail="The \"ai-sum.py\" script was not found. Please make sure it is in the correct location. ")
            return

        # disable the button to prevent multiple clicks
        self.summarize_button.config(state=tk.DISABLED)

        # start the summarization in a new thread to prevent the GUI from freezing - non-blocking
        threading.Thread(target=self.run_summarization, args=(script_path, input_text)).start()

    def run_summarization(self, script_path, input_text):
        try:
            self.display_message("▶▶ ", 'info', newline=False)
            self.display_message("SummarAIzing text...\n", 'highlight')

            # run the ai-sum.py script with subprocess because it is a blocking operation
            # capture_output=True to capture the stdout
            # text=True to decode the stdout as text (and not bytes)
            # check=True to raise an exception if the command fails
            result = subprocess.run(
                [sys.executable, script_path, '--summarize', input_text, '--no-ansi'],
                capture_output=True, text=True, check=True
            )

            summarized_text = result.stdout.strip()

            self.display_message(summarized_text, 'success')
        except subprocess.CalledProcessError as e:
            self.display_message(f"[X] ERROR WHEN SUMMARIZING: {e.stderr.strip()}", 'error')
        except Exception as e:
            self.display_message(f"[X] UNEXPECTED ERROR: {str(e)}", 'error')
        finally:
            # Re-enable the button after the task is complete
            self.summarize_button.config(state=tk.NORMAL)


    # method for displaying messages in the output_text widget in color
    def display_message(self, message, tag=None, newline=True):
        if newline:
            message += '\n'
        self.output_text.text.after(0, self._insert_message, message, tag)
    
    def _insert_message(self, message, tag):
        self.output_text.text.config(state=tk.NORMAL)
        self.output_text.text.insert(tk.END, message, tag)
        self.output_text.text.config(state=tk.DISABLED)
        self.output_text.text.see(tk.END)

if __name__ == '__main__':
    root = ThemedTk(theme='equilux', themebg=True)
    app = SummarAIzeApp(root)
    root.mainloop()
