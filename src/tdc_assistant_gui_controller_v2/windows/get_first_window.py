from typing import Optional

from .get_all_windows import get_all_windows

from ..types import WindowTitle


def get_first_window(window_title: Optional[WindowTitle] = None):
    windows = get_all_windows([] if window_title is None else [window_title])

    if len(windows) == 0:
        return None

    return windows[0]
