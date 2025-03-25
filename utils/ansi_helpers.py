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
    SUCCESS = f"{Colors.GREEN}√ {Colors.RESET}"
    WARNING = f"{Colors.YELLOW}⚠ {Colors.RESET}"
    INFO = f"{Colors.BLUE}ℹ {Colors.RESET}"

    @staticmethod
    def disable() -> None:
        """disable ANSI escape color coded symbols (set to empty string)"""
        Symbols.SUCCESS = ""
        Symbols.ERROR = ""
        Symbols.INFO = ""
        Symbols.WARNING = ""

class Printer:
    """Printer class to print specific types of messages."""
    
    def __init__(self, no_ansi: bool = False, gui_mode: bool = False) -> None:
        """
        Initialize the printer with ANSI color codes. \n
        Used to print messages with specific ANSI color codes and preceding symbols. \n
        :param no_ansi: If True, disable ANSI color codes. \n
        :param gui_mode: If True, disable all messages. \n
        """
        self.no_ansi = no_ansi
        self.gui_mode = gui_mode
        if self.no_ansi or should_disable_ansi():
            Symbols.disable()

    def success(self, message: str) -> None:
        """
        Print a success message. \n
        Ignores the message if in *GUI mode*.
        """
        if self.gui_mode:
            return
        print(f"{Symbols.SUCCESS}{message}")

    def error(self, message: str, exit_code: int = 1) -> None:
        """
        Print an error message. \n
        **Note**: This will exit the program with a status code of 1.\n
        Ignores the message if in *GUI mode*.
        """
        if not self.gui_mode:
            print(f"{Symbols.ERROR}{message}")
        sys.exit(exit_code)

    def info(self, message: str) -> None:
        """
        Print an info message.\n
        Ignores the message if in *GUI mode*.
        """
        if self.gui_mode:
            return
        print(f"{Symbols.INFO}{message}")
    
    def warning(self, message: str) -> None:
        """
        Print a warning message.\n
        Ignores the message if in *GUI mode*.
        """
        if self.gui_mode:
            return
        print(f"{Symbols.WARNING}{message}")

    def result(self, message: str) -> None:
        """
        Print a result message.\n
        Ignores the message if in *GUI mode*.
        """
        if self.gui_mode:
            return
        print(f"{Symbols.RESULT}{message}")