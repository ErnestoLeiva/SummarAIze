import re

class Colors:
    """ANSI escape codes for colors."""
    RED = "\033[91m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    RESET = "\033[0m"

ANSI_COLOR_MAP = {
    '\033[91m': 'red',
    '\033[92m': 'green',
    '\033[93m': 'yellow',
    '\033[94m': 'blue',
    '\033[95m': 'magenta',
    '\033[96m': 'cyan',
    '\033[0m': 'reset',
}

ANSI_PATTERN = re.compile(r'(\033\[\d+m)')

