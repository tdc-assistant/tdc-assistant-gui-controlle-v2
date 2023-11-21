from typing import Any, Union, Optional

from tdc_assistant_gui_controller_v2.code_editor.types.code_editor import CodeEditor

from ..logger import Logger
from ..types import Coordinate
from ..public_chat import PublicChat

from .open_all_windows import open_all_windows
from .public_chat_window_controller import PublicChatWindowController
from .code_editor_window_controller import CodeEditorWindowController


from .enums import WindowTitle

WindowController = Union[PublicChatWindowController, CodeEditorWindowController]

code_editor_window_titles = [
    WindowTitle.C_LIKE_EDITOR,
    WindowTitle.CSS_EDITOR,
    WindowTitle.GO_EDITOR,
    WindowTitle.HTML_EDITOR,
    WindowTitle.JAVA_EDITOR,
    WindowTitle.JAVASCRIPT_EDITOR,
    WindowTitle.MATHEMATICA_EDITOR,
    WindowTitle.PHP_EDITOR,
    WindowTitle.PYTHON_EDITOR,
    WindowTitle.R_EDITOR,
    WindowTitle.RUBY_EDITOR,
    WindowTitle.SCREENSHARE,
    WindowTitle.SQL_EDITOR,
    WindowTitle.XML_EDITOR,
]


class WindowManager:
    _right_pop_out_button_coords: Coordinate
    _tutor_first_name: str
    _tutor_last_initial: str
    _window_controllers: list[WindowController]
    _logger: Logger

    def __init__(
        self,
        right_pop_out_button_coords: Coordinate,
        tutor_first_name: str,
        tutor_last_initial: str,
    ):
        self._right_pop_out_button_coords = right_pop_out_button_coords
        self._tutor_first_name = tutor_first_name
        self._tutor_last_initial = tutor_last_initial
        self._window_controllers = []
        self._logger = Logger(self)

    def open_all_windows(self):
        open_all_windows_start = self._logger.log("Started opening all windows")
        for window in open_all_windows(self._right_pop_out_button_coords):
            controller = self._map_window_to_controller(window)

            if controller is not None:
                for existing_controller in self._window_controllers:
                    if (
                        existing_controller.get_window_title()
                        == controller.get_window_title()
                    ):
                        break
                else:
                    self._window_controllers.append(controller)
            else:
                print(f"No controller exists for Window: '{window.window_text()}'")

        open_all_windows_end = self._logger.log("Finished opening all windows")
        self._logger.log_elapsed_time(open_all_windows_start, open_all_windows_end)

    def _parse_programming_language_and_editor_number(
        self, window_title: str
    ) -> tuple[str, int]:
        editor_index = window_title.index("Editor")
        programming_language = window_title[:editor_index]
        editor_number = int(
            window_title[editor_index + len("Editor") :].split()[0].strip()
        )
        return programming_language, editor_number

    def _map_window_to_controller(self, window: Any) -> Optional[WindowController]:
        window_text = window.window_text().lower()
        if WindowTitle.PUBLIC_CHAT.value.lower() in window_text:
            return PublicChatWindowController(
                window, self._tutor_first_name, self._tutor_last_initial
            )
        for code_editor_window_title in code_editor_window_titles:
            if code_editor_window_title.value.lower() in window_text:
                (
                    programming_language,
                    editor_number,
                ) = self._parse_programming_language_and_editor_number(window_text)
                return CodeEditorWindowController(
                    window, programming_language, editor_number
                )

        return None

    def scrape_public_chat(self) -> PublicChat:
        self.open_all_windows()

        for controller in self._window_controllers:
            if isinstance(controller, PublicChatWindowController):
                return controller.scrape()

        raise Exception(f"Cannot find {WindowTitle.PUBLIC_CHAT.value} window")

    def scrape_code_editors(self) -> list[CodeEditor]:
        self.open_all_windows()

        code_editors: list[CodeEditor] = []

        for controller in self._window_controllers:
            if isinstance(controller, CodeEditorWindowController):
                code_editors.append(controller.scrape())

        return code_editors
