from typing import Any, Union, Optional

from tdc_assistant_gui_controller_v2.code_editor.types.code_editor import CodeEditor

from ..logger import Logger
from ..types import Coordinate, AWSCredentials, Screenshare
from ..public_chat import PublicChat

from .open_all_windows import open_all_windows
from .public_chat_window_controller import PublicChatWindowController
from .code_editor_window_controller import CodeEditorWindowController
from .screenshare_window_controller import ScreenshareWindowController


from ..types import WindowTitle

WindowController = Union[
    PublicChatWindowController, CodeEditorWindowController, ScreenshareWindowController
]

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
    WindowTitle.SQL_EDITOR,
    WindowTitle.XML_EDITOR,
]


class WindowManager:
    _right_pop_out_button_coords: Coordinate
    _public_chat_text_box_coords: Coordinate
    _tutor_first_name: str
    _tutor_last_initial: str
    _aws_credentials: AWSCredentials
    _window_controllers: list[WindowController]
    _logger: Logger

    def __init__(
        self,
        aws_credentials: AWSCredentials,
        right_pop_out_button_coords: Coordinate,
        public_chat_text_box_coords: Coordinate,
        tutor_first_name: str,
        tutor_last_initial: str,
    ):
        self._aws_credentials = aws_credentials
        self._right_pop_out_button_coords = right_pop_out_button_coords
        self._public_chat_text_box_coords = public_chat_text_box_coords
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
                self._logger.log_warning(
                    f"No controller exists for Window: '{window.window_text()}'"
                )

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
        window_text = window.window_text()
        if WindowTitle.PUBLIC_CHAT.value.lower() in window_text.lower():
            return PublicChatWindowController(
                window, self._tutor_first_name, self._tutor_last_initial
            )
        for code_editor_window_title in code_editor_window_titles:
            if code_editor_window_title.value.lower() in window_text.lower():
                (
                    programming_language,
                    editor_number,
                ) = self._parse_programming_language_and_editor_number(window_text)
                return CodeEditorWindowController(
                    window, programming_language, editor_number
                )
        if WindowTitle.SCREENSHARE.value.lower() in window_text.lower():
            return ScreenshareWindowController(window, self._aws_credentials)
        return None

    def find_public_chat_window_controller(
        self,
    ) -> Optional[PublicChatWindowController]:
        self.open_all_windows()

        for controller in self._window_controllers:
            if isinstance(controller, PublicChatWindowController):
                return controller

        return None

    def find_screenshare_window_controller(
        self,
    ) -> Optional[ScreenshareWindowController]:
        self.open_all_windows()

        for controller in self._window_controllers:
            if isinstance(controller, ScreenshareWindowController):
                return controller

        return None

    def scrape_public_chat(self) -> PublicChat:
        controller = self.find_public_chat_window_controller()

        if controller is None:
            raise Exception(f"Cannot find {WindowTitle.PUBLIC_CHAT.value} window")

        return controller.scrape()

    def scrape_code_editors(self) -> list[CodeEditor]:
        self.open_all_windows()

        code_editors: list[CodeEditor] = []

        for controller in self._window_controllers:
            if isinstance(controller, CodeEditorWindowController):
                code_editors.append(controller.scrape())

        return code_editors

    def send_message(self, message: str):
        controller = self.find_public_chat_window_controller()

        if controller is None:
            raise Exception(f"Cannot find {WindowTitle.PUBLIC_CHAT.value} window")

        controller.send_message(
            message,
            (
                self._public_chat_text_box_coords["x"],
                self._public_chat_text_box_coords["y"],
            ),
        )

    def scrape_screenshare(self) -> Optional[Screenshare]:
        controller = self.find_screenshare_window_controller()

        if controller is None:
            print("cannot find screenshare window")
            return None

        return controller.scrape()

    def is_screenshare_window_open(self) -> bool:
        return self.find_screenshare_window_controller() is not None
