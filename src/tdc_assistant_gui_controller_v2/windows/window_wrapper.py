from typing import Any

from .window_exception import WindowException


class WindowWrapper:
    _window: Any

    def __init__(self, window: Any):
        self._window = window

    def window_text(self) -> str:
        try:
            return self._window.window_text()
        except:
            raise WindowException()

    def set_focus(self) -> None:
        try:
            return self._window.set_focus()
        except:
            raise WindowException()

    def maximize(self) -> str:
        try:
            return self._window.maximize()
        except:
            raise WindowException()

    def capture_as_image(self) -> Any:
        try:
            return self._window.capture_as_image()
        except:
            raise WindowException()

    def get_properties(self) -> Any:
        try:
            return self._window.get_properties()
        except:
            raise WindowException()

    def descendants(self) -> Any:
        try:
            return self._window.descendants()
        except:
            raise WindowException()
