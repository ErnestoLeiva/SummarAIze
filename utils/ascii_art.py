from utils.version_helper import get_version

class ASCII_art:
    """ASCII art class to store ASCII art strings."""
    # I dont apply strict typing here because it is genuinely not needed.
    
    def dynamic_padding_splash() -> str:
        """Dynamically calculate padding for the ASCII splash title art."""
        
        # Fixed values (other than version which can change ofc)
        total_width = 84
        left_content = "║ Summarize legal documents using AI. - "
        
        version = f"v{get_version()}" # no longer than 25 characters
        if len(version) > 25:
            version = version[:22] + "..." # this is really like saying from index 0 to 21 since 22 is not included in string slicing
        
        right_marker = "└─────────────────╢"

        # Calculate the spacing needed (to make sure the version changing does not ever mess up the ascii art)
        dynamic_padding = total_width - len(left_content) - len(version) - len(right_marker)
        padded_line = f"{left_content}{version}{' ' * dynamic_padding}{right_marker}"

        return padded_line
    
    splash_title = f"""\
╔══════════════════════════════════════════════════════════════════════════════════╗
║███████╗██╗   ██╗███╗   ███╗███╗   ███╗ █████╗ ██████╗  █████╗ ██╗███████╗███████╗║
║██╔════╝██║   ██║████╗ ████║████╗ ████║██╔══██╗██╔══██╗██╔══██╗██║╚══███╔╝██╔════╝║
║███████╗██║   ██║██╔████╔██║██╔████╔██║███████║██████╔╝███████║██║  ███╔╝ █████╗  ║
║╚════██║██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██╔══██╗██╔══██║██║ ███╔╝  ██╔══╝  ║
║███████║╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██║██║███████╗███████╗║
║╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝║
╟────────────────────────────────────────────────────────────────┐ est. 2025 ┆ FIU ║
{dynamic_padding_splash()}
╚══════════════════════════════════════════════════════════════════════════════════╝\
"""