from typing import Any

from time import sleep


from pywinauto import mouse, keyboard  # type: ignore

from .window_wrapper import WindowWrapper
from .win32_window_manager import Win32WindowManager

from ..public_chat import PublicChat
from ..public_chat.scrape_public_chat import scrape_public_chat
from ..logger import Logger
from ..send_message import send_message

originals_and_replacements = {
    "`": "",
    "\n": "{VK_RETURN}",
}


def _transform_text(text: str):
    transformed_text = ""
    for ch in text:
        if ch in "{}()":
            transformed_text += "{" + ch + "}"
        else:
            transformed_text += ch

    for original, replacement in originals_and_replacements.items():
        transformed_text = transformed_text.replace(original, replacement)

    return "{VK_SPACE}".join(transformed_text.split()) + "{VK_RETURN}"


class PublicChatWindowController:
    _window: WindowWrapper
    _tutor_first_name: str
    _tutor_last_initial: str
    _logger: Logger

    def __init__(self, window: Any, tutor_first_name: str, tutor_last_initial: str):
        self._window = WindowWrapper(window)
        self._tutor_first_name = tutor_first_name
        self._tutor_last_initial = tutor_last_initial
        self._logger = Logger(self)

    def scrape(self) -> PublicChat:
        start = self._logger.log("Started scraping public chat")

        w = Win32WindowManager()
        w.find_window_wildcard(f".*{self._window.window_text()}.*")
        w.set_foreground()
        sleep(2)

        self._window.set_focus()
        sleep(2)

        result = scrape_public_chat(
            self._window, self._tutor_first_name, self._tutor_last_initial
        )
        end = self._logger.log("Finished scraping public chat")
        self._logger.log_elapsed_time(start, end)
        return result

    def get_window_title(self) -> str:
        return self._window.window_text()

    def send_message(self, message: str, coords=[int, int]) -> None:
        w = Win32WindowManager()
        w.find_window_wildcard(f".*{self._window.window_text()}.*")
        w.set_foreground()
        sleep(2)
        self._window.set_focus()
        sleep(2)
        self._window.maximize()
        mouse.move(coords=coords)
        sleep(0.5)
        mouse.click(coords=coords)
        sleep(0.5)
        keyboard.send_keys(_transform_text(message))

    def maximize_window(self):
        self._window.maximize()
