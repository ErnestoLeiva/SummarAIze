import subprocess, os
from utils import ansi

def run_summarizer(model: str, input_path: str, output_path: str = None, gui_callback: callable = None) -> str | None:
    """
    Run the CLI-based SummarAIze process as a subprocess with real-time output streaming.

    ***
    Executes `ai-sum.py` with the specified model and input file path using UTF-8
    encoding and unbuffered I/O. If a GUI callback is provided, output is streamed
    line-by-line to the GUI in real time. This function is designed for integration
    into threaded GUI applications and handles subprocess output safely.
    ***

    Args:
        model (str): The name of the summarization model to use (e.g., "BART").
        input_path (str): Path to the input file to summarize.
        output_path (str, optional): Path to save the summary. If None, output is not written to file.
        gui_callback (callable, optional): Function to stream output lines to the GUI (e.g., inserting into a widget).

    Returns:
        (str | None): The full summarized output as a string, or None if an error occurred.
    """

    # Create color object
    color = ansi.Colors
    
    # Prepare command for ai-sum.py argparser
    command = [
        "python", "-u",
        "ai-sum.py",
        "--summarize", input_path,
        "--model", model,
        "--gui-mode"
    ]
    if output_path:
        command += ["--output", output_path]

    # Set environment variables to force specific modes
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"   # forces -u (unbuffered) behaviour
    env["PYTHONIOENCODING"] = "utf-8"   # stdout/stderr → UTF‑8
    env["PYTHONUTF8"]       = "1"       # force UTF‑8 mode on Windows ≥ 3.7

    # Start subprocess running ai-sum.py 
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            text=True,          # auto‑decodes bytes → str
            encoding="utf-8",   # use UTF‑8 for that decoding
            errors="replace",   # avoid crashes on weird bytes
            env=env             # UTF‑8 environment goes to the child
        )
        output_lines = []

        # Print live output from subprocess stdout to GUI output content widget [uses gui callback]
        for line in process.stdout:
            output_lines.append(line)
            if gui_callback:
                gui_callback(line.rstrip(None))

        # Wait for subprocess to finish and get the exit code
        process.wait()
        if process.returncode != 0:
            error_msg = process.stderr.read().strip()
            if gui_callback:
                gui_callback(f"{color.RED}[✗]{color.RESET} Summarization failed:\n{error_msg}")
            return None

        return "".join(output_lines)

    except Exception as e:
        if gui_callback:
            gui_callback(f"{color.RED}[✗]{color.RESET} Unexpected Error: {e}")
        return None