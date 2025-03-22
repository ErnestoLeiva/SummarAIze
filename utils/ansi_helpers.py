import sys

class Colors:
    """ANSI escape codes for colors."""
    RED = "\033[91m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

class Symbols:
    """ANSI escape codes for symbols."""
    ERROR = f"{Colors.RED}✗ {Colors.RESET}"
    INFO = f"{Colors.CYAN}▶▶ {Colors.RESET}"
    SUCCESS = f"{Colors.GREEN}√ {Colors.RESET}"
    WARNING = f"{Colors.YELLOW}⚠ {Colors.RESET}"

    @staticmethod
    def disable() -> None:
        """disable ANSI escape color coded symbols (set to empty string)"""
        Symbols.SUCCESS = ""
        Symbols.ERROR = ""
        Symbols.INFO = ""
        Symbols.WARNING = ""

class Printer:
    """Printer class to print specific types of messages."""
    def __init__(self, no_ansi: bool = False) -> None:
        """Initialize the printer with ANSI color codes."""
        self.no_ansi = no_ansi
        if self.no_ansi:
            Symbols.disable()

    def success(self, message: str) -> None:
        """Print a success message."""
        print(f"{Symbols.SUCCESS}{message}")

    def error(self, message: str, exit_code: int = 1) -> None:
        """Print an error message. \n
        **Note**: This will exit the program with a status code of 1."""
        print(f"{Symbols.ERROR}{message}")
        sys.exit(exit_code)

    def info(self, message: str) -> None:
        """Print an info message."""
        print(f"{Symbols.INFO}{message}")
    
    def warning(self, message: str) -> None:
        """Print a warning message."""
        print(f"{Symbols.WARNING}{message}")