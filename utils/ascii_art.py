from utils.version_helper import get_version

class ASCII_art:
    """ASCII art class to store ASCII art strings."""
    
    # Fixed values
    total_width = 84
    left_content = "║ Summarize legal documents using AI. - "
    version = f"v{get_version()}"
    right_marker = "└─────────────────╢"

    # Calculate the spacing needed
    dynamic_padding = total_width - len(left_content) - len(version) - len(right_marker)
    padded_line = f"{left_content}{version}{' ' * dynamic_padding}{right_marker}"

    
    splash_title = f"""\
╔══════════════════════════════════════════════════════════════════════════════════╗
║███████╗██╗   ██╗███╗   ███╗███╗   ███╗ █████╗ ██████╗  █████╗ ██╗███████╗███████╗║
║██╔════╝██║   ██║████╗ ████║████╗ ████║██╔══██╗██╔══██╗██╔══██╗██║╚══███╔╝██╔════╝║
║███████╗██║   ██║██╔████╔██║██╔████╔██║███████║██████╔╝███████║██║  ███╔╝ █████╗  ║
║╚════██║██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██╔══██╗██╔══██║██║ ███╔╝  ██╔══╝  ║
║███████║╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██║██║███████╗███████╗║
║╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝║
╟────────────────────────────────────────────────────────────────┐ est. 2025 ┆ FIU ║
{padded_line}
╚══════════════════════════════════════════════════════════════════════════════════╝\
"""