import os
import json
from utils.gui_helpers import (
    MIN_WIDTH,
    MIN_HEIGHT,
    MAX_WIDTH,
    MAX_HEIGHT,
)

# ----- GLOBALS -----
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

# ----- FUNCTIONS -----
def load_settings() -> dict[str, any]:
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
        width, height = validate_dimensions(width, height, output_on)

        # Validate model
        if model not in MODEL_CHOICES:
            model = DEFAULT_MODEL

        # Update validated values
        settings["Options"]["width"] = width
        settings["Options"]["height"] = height
        settings["Options"]["model"] = model

        return settings
    else:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
        return DEFAULT_SETTINGS.copy()

def save_settings(theme: str, model: str, output_on: bool, width: int, height: int) -> None:
    settings = {
        "Customization": {"theme": theme},
        "Options": {"model": model, "output_on": output_on, "width": width, "height": height}
    }
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

def validate_dimensions(width: int, height: int, output_on: bool) -> tuple[int, int]:
    height = max(height, MIN_HEIGHT) # if lower than min set to min
    width = max(width, MIN_WIDTH) # if lower than min set to min
    
    width = min(width, MAX_WIDTH) # if higher than max set to max
    height = min(height, MAX_HEIGHT) # if higher than max set max

    return width, height
