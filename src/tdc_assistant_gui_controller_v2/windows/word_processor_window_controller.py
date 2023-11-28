from typing import Any

from time import sleep

from pywinauto import keyboard  # type: ignore

from ..logger import Logger
from ..code_editor import scrape_code_editor_content
from ..word_processor import WordProcessor
from ..utils import transform_text


class WordProcessorWindowController:
    _window: Any
    _number: int
    _logger: Logger

    def __init__(self, window: Any, number: int):
        self._window = window
        self._number = number
        self._logger = Logger(self)

    def scrape(self) -> WordProcessor:
        start = self._logger.log(f"Started scraping Word Processor '{self._number}'")
        self._window.set_focus()
        sleep(0.5)
        self._window.maximize()
        sleep(0.5)
        content = scrape_code_editor_content(self._window)
        end = self._logger.log(f"Finished scraping Word Processor '{self._number}'")
        self._logger.log_elapsed_time(start, end)
        return {"content": content, "number": self._number}

    def get_window_title(self) -> str:
        return self._window.window_text()

    def send_text(self, text: str):
        self._window.set_focus()
        sleep(0.5)
        self._window.maximize()
        sleep(0.5)

        keyboard.send_keys("{VK_END}")
        keyboard.send_keys(transform_text(text), pause=0.0)

    def maximize_window(self):
        self._window.maximize()
