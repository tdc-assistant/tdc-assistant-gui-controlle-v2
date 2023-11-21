from typing import Any

from time import sleep

from ..public_chat import PublicChat
from ..public_chat.scrape_public_chat import scrape_public_chat
from ..logger import Logger


class PublicChatWindowController:
    _window: Any
    _tutor_first_name: str
    _tutor_last_initial: str
    _logger: Logger

    def __init__(self, window: Any, tutor_first_name: str, tutor_last_initial: str):
        self._window = window
        self._tutor_first_name = tutor_first_name
        self._tutor_last_initial = tutor_last_initial
        self._logger = Logger(self)

    def scrape(self) -> PublicChat:
        start = self._logger.log("Started scraping public chat")
        self._window.set_focus()
        sleep(0.5)
        result = scrape_public_chat(
            self._window, self._tutor_first_name, self._tutor_last_initial
        )
        end = self._logger.log("Finished scraping public chat")
        self._logger.log_elapsed_time(start, end)
        return result

    def get_window_title(self) -> str:
        return self._window.window_text()
