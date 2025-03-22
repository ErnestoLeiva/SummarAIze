import time
from custom_classes.ANSI_helpers import Symbols as symb, Colors as col

class Timer:
    """Use to time a block of code.\n
    **Example usage**:
        with Timer("Task"):
            run_something()\n
    **Output**:
        - "[Task] completed in X.XXs" *if gui_mode is False.*\n
        - **None** *if gui_mode is True.*\n
    """
    def __init__(self, task_name: str = "Task", gui_mode: bool = False, no_ansi: bool = False) -> None:
        self.task_name = task_name
        self.gui_mode = gui_mode
        self.no_ansi = no_ansi
    
    def __enter__(self) -> 'Timer':
        self.start_time = time.time()
        return self
    
    def __exit__(self,  exc_type, exc_value, traceback) -> bool:
        elapsed = time.time() - self.start_time
        if not self.gui_mode and not self.no_ansi:
            print(f"{symb.WARNING}[{self.task_name}] completed in {col.YELLOW}{elapsed:.2f}s{col.RESET}\n")
        elif not self.gui_mode and self.no_ansi:
            print(f"[{self.task_name}] completed in {elapsed:.2f}s\n")
        else:
            pass  # placeholder for GUI mode
        return False # do not suppress exceptions