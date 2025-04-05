import subprocess, os
from utils import ansi

def run_summarizer(model: str, input_path: str, output_path: str = None, gui_callback: callable = None) -> str | None:
    # Create color object
    color = ansi.Colors
    
    command = [
        "python", "-u",
        "ai-sum.py",
        "--summarize", input_path,
        "--model", model,
        "--gui-mode"
    ]
    if output_path:
        command += ["--output", output_path]

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"   # forces -u (unbuffered) behaviour
    env["PYTHONIOENCODING"] = "utf-8"   # stdout/stderr → UTF‑8
    env["PYTHONUTF8"]       = "1"       # force UTF‑8 mode on Windows ≥ 3.7

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
    
        for line in process.stdout:
            output_lines.append(line)
            if gui_callback:
                gui_callback(line.rstrip(None))

        # Wait for process to finish and get the exit code
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