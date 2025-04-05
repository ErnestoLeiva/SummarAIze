import sys
import os

def should_disable_ansi() -> bool:
    """
    Check if ANSI escape codes should be disabled. \n
    This is typically the case on Windows systems without ANSICON support.
    """
    return (
        os.name == "nt" and
        not os.environ.get("ANSICON") and # ANSICON is not set
        not os.environ.get("WT_SESSION") and # Windows Terminal
        not os.environ.get("TERM_PROGRAM") # VSCode terminal and other terminals that support ANSI codes
    )

class Colors:
    """ANSI escape codes for colors."""
    RED = "\033[91m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    RESET = "\033[0m"

class Symbols:
    """ANSI escape codes for symbols."""
    ERROR = f"{Colors.RED}✗ {Colors.RESET}"
    RESULT = f"{Colors.CYAN}▶▶ {Colors.RESET}"
    SUCCESS = f"{Colors.GREEN}✓ {Colors.RESET}"
    WARNING = f"{Colors.YELLOW}⚠ {Colors.RESET}"
    TIMER = f"{Colors.MAGENTA}⧗ {Colors.RESET}"
    INFO = f"{Colors.BLUE}ℹ {Colors.RESET}"

    @staticmethod
    def disable() -> None:
        """disable ANSI escape color coded symbols (set to empty string)"""
        Symbols.SUCCESS = ""
        Symbols.ERROR = ""
        Symbols.INFO = ""
        Symbols.TIMER = ""
        Symbols.WARNING = ""

class Printer:
    """Printer class to print specific types of messages."""
    
    def __init__(self, no_ansi: bool = False, gui_mode: bool = False, gui_callback: callable = None) -> None:
        """
        Initialize the printer with ANSI color codes. \n
        Used to print messages with specific ANSI color codes and preceding symbols. \n
        *** \n
        :param no_ansi: If True, disable ANSI color codes. \n
        :param gui_mode: If True, disable all messages. \n
        :param gui_callback: Used for progressbar in GUI app.
        """
        self.no_ansi = no_ansi
        self.gui_mode = gui_mode
        self.gui_callback = gui_callback
        if self.no_ansi or should_disable_ansi():
            Symbols.disable()

    def _output(self, message: str, prefix: str = ""):
        print(f"{prefix}{message}")

    def normal(self, message: str): self._output(message)
    def success(self, message: str): self._output(message, Symbols.SUCCESS)
    def error(self, message: str, exit_code: int = 1):
        if self.gui_mode or self.gui_callback:
            print(f"{Symbols.ERROR}{message}")
            raise Exception(message)
        else:
            print(f"{Symbols.ERROR}{message}")
            sys.exit(exit_code)
    def info(self, message: str): self._output(message, Symbols.INFO)
    def timer(self, message: str): self._output(message, Symbols.TIMER)
    def warning(self, message: str): self._output(message, Symbols.WARNING)
    def result(self, message: str): self._output(message, Symbols.RESULT)