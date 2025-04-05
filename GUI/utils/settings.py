import os
import json
from utils.gui_helpers import (
    MIN_WIDTH,
    MIN_HEIGHT,
    MAX_WIDTH,
    MAX_HEIGHT,
)

# ===== GLOBALS =====
MAIN_ICON = "icon.png"
CUR_DIR = os.path.dirname(__file__)
DEFAULT_MODEL = "BART"
SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "..", "conf", "settings.json")
DEFAULT_SETTINGS = {
    "Customization": {"theme": "dark"},
    "Options": {"model": "BART", "output_on": False, "width": MIN_WIDTH, "height": MIN_HEIGHT}
}
with open("configs/model_registry.json", "r", encoding="utf-8") as f:
    MODEL_REGISTRY = json.load(f)
    MODEL_CHOICES = list(MODEL_REGISTRY.keys())

# ===== FUNCTIONS =====
def load_settings() -> dict[str, any]:
    """
    Load and validate the SummarAIze project settings.

    ***
    Reads from the JSON config at SETTINGS_PATH (default: GUI/conf/settings.json),
    validates model choice and dimensions, and returns the final settings dict.
    ***

    Returns:
        (dict[str, any]): A dictionary containing validated settings.
    """

    if os.path.exists(SETTINGS_PATH):
        
        # Read settings file
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            settings = json.load(f)
        
        # Get dimensions and values
        width = settings["Options"].get("width", MIN_WIDTH)
        height = settings["Options"].get("height", MIN_HEIGHT)
        output_on = settings["Options"].get("output_on", False)
        model = settings["Options"].get("model", DEFAULT_MODEL)

        # Validate dimensions
        width, height = validate_dimensions(width, height)

        # Validate model
        if model not in MODEL_CHOICES:
            model = DEFAULT_MODEL

        # Update validated values
        settings["Options"]["width"] = width
        settings["Options"]["height"] = height
        settings["Options"]["model"] = model

        return settings
    else:
        # Create settings file if it does not exist
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
        
        # Return default values [set at the global level]
        return DEFAULT_SETTINGS.copy()

def save_settings(theme: str, model: str, output_on: bool, width: int, height: int) -> None:
    """
    Save the current SummarAIze settings to the settings.json file.

    ***
    Updates the JSON config located at SETTINGS_PATH with the provided theme,
    model selection, output toggle state, and window dimensions.
    This ensures the user’s preferences persist across application sessions.
    ***

    Args:
        theme (str): The selected theme ("light" or "dark").
        model (str): The selected summarization model name.
        output_on (bool): Whether output-to-file mode is enabled.
        width (int): Current width of the main window.
        height (int): Current height of the main window.
    """

    settings = {
        "Customization": {"theme": theme},
        "Options": {"model": model, "output_on": output_on, "width": width, "height": height}
    }
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

def validate_dimensions(width: int, height: int) -> tuple[int, int]:
    """
    Validate and clamp the given window dimensions within predefined limits.

    ***
    Ensures the provided width and height fall within the acceptable bounds
    defined by MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, and MAX_HEIGHT constants.
    Returns the corrected dimensions as a tuple.
    ***

    Args:
        width (int): The requested width of the application window.
        height (int): The requested height of the application window.

    Returns:
        (tuple[int, int]): A validated (width, height) pair within allowed range.
    """
    
    height = max(height, MIN_HEIGHT) # if lower than min limit, set to predefined min
    width = max(width, MIN_WIDTH)
    
    width = min(width, MAX_WIDTH) # if higher than max limit, set to predefined max
    height = min(height, MAX_HEIGHT)

    return width, height
