from typing import Optional
from pywinauto import Desktop  # type: ignore

from .enums import WindowTitle


def get_all_windows(window_titles: Optional[list[WindowTitle]] = None):
    windows = Desktop(backend="uia").windows()

    if window_titles is None:
        return windows

    result = []

    for w in windows:
        for t in window_titles:
            if t.value in w.window_text():
                result.append(w)
                break

    return result

