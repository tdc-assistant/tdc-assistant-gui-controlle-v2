from typing import Any

from time import sleep

from pywinauto import keyboard  # type: ignore

from ..logger import Logger
from ..code_editor import scrape_code_editor_content, CodeEditor
from ..utils import transform_text


class CodeEditorWindowController:
    _window: Any
    _programming_language: str
    _editor_number: int
    _logger: Logger

    def __init__(self, window: Any, programming_language: str, editor_number: int):
        self._window = window
        self._programming_language = programming_language
        self._editor_number = editor_number
        self._logger = Logger(self)

    def _get_clean_window_title(self):
        return f"{self._programming_language} {self._editor_number}"

    def scrape(self) -> CodeEditor:
        start = self._logger.log(
            f"Started scraping code editor '{self._get_clean_window_title()}'"
        )
        self._window.set_focus()
        sleep(0.5)
        result: CodeEditor = {
            "editor_language": self._programming_language,
            "editor_number": self._editor_number,
            "content": scrape_code_editor_content(self._window),
        }
        end = self._logger.log(
            f"Finished scraping code editor '{self._get_clean_window_title()}'"
        )
        self._logger.log_elapsed_time(start, end)
        return result

    def get_window_title(self) -> str:
        return self._window.window_text()

    def send_text(self, text: str):
        self._window.set_focus()
        sleep(0.5)
        self._window.maximize()
        sleep(0.5)

        keyboard.send_keys("{VK_END}")
        keyboard.send_keys(transform_text(text), pause=0.0)
