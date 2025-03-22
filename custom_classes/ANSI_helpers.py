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