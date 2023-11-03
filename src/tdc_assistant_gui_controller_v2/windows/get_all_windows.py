from typing import Optional
from pywinauto import Desktop  # type: ignore

from .enums import WindowTitle


def get_all_windows(window_title: Optional[WindowTitle] = None):
    windows = Desktop(backend="uia").windows()

    if window_title is None:
        return windows

    return [w for w in windows if window_title.value in w.window_text()]
