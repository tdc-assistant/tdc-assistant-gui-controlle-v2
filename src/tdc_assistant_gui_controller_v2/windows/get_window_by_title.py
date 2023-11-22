from time import sleep

from pywinauto import mouse  # type: ignore

from .get_all_windows import get_all_windows

from ..controls import ControlPropertyKey
from ..types import Coordinate, WindowTitle

from ..constants import (
    GUI_EVENT_DELAY_BASE_IN_SECONDS,
    GUI_EVENT_DELAY_INCREMENT_IN_SECONDS,
)


MAX_RETRY_COUNT = 3


def get_window_by_title(
    window_title: WindowTitle,
    coords: Coordinate,
):
    windows_before_clicks = get_all_windows()

    window = None
    num_tries = 0
    delay = GUI_EVENT_DELAY_BASE_IN_SECONDS

    while window is None and num_tries < MAX_RETRY_COUNT:
        mouse.click(coords=(coords["x"], coords["y"]))
        sleep(delay)

        for w in get_all_windows():
            # TODO Check title to ensure robustness .. another window could open while this is happening
            texts = w.get_properties().get(ControlPropertyKey.TEXTS.value)

            if len(texts) == 0:
                continue

            text = texts[0]

            if w not in windows_before_clicks and window_title.value in text:
                window = w
                break

        delay += GUI_EVENT_DELAY_INCREMENT_IN_SECONDS
        num_tries += 1

    if window is None:
        raise Exception(f"Cannot find window for `WindowTitle`: '{window_title.value}")

    return window
