from typing import Optional

from .get_all_windows import get_all_windows

from .enums import WindowTitle


def get_first_window(window_title: Optional[WindowTitle] = None):
    windows = get_all_windows(window_title)

    if len(windows) == 0:
        return None

    return windows[0]