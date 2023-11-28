from typing import Any

from ..types import Coordinate

from .get_all_windows import get_all_windows
from .get_first_window import get_first_window
from ..types import WindowTitle
from .open_window import open_window

MAX_TRIES = 2


def open_all_windows(right_pop_out_button_coords: Coordinate) -> list[Any]:
    optional_classroom_window = get_first_window(WindowTitle.CLASSROOM)

    if optional_classroom_window is not None:
        optional_classroom_window.set_focus()

    prev_windows = get_all_windows()
    prev_num_windows = len(prev_windows)
    curr_windows = []

    num_tries = 0

    while num_tries < MAX_TRIES:
        open_window(right_pop_out_button_coords)
        curr_windows = get_all_windows()
        curr_num_windows = len(curr_windows)

        if prev_num_windows == curr_num_windows:
            num_tries += 1
        else:
            num_tries = 0

        prev_num_windows = curr_num_windows

    return curr_windows
