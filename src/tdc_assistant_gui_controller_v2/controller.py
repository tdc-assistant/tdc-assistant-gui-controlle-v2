from typing import Optional, TypedDict

from .public_chat import PublicChat
from .types import Coordinate
from .send_message import Message, send_message
from .insert_code_editor import insert_code_editor
from .windows import WindowManager
from .code_editor import CodeEditor
from .types import AWSCredentials, Screenshare
from .word_processor import WordProcessor


class TutorProfile(TypedDict):
    first_name: str
    last_initial: str


class ComponentCoordinates(TypedDict):
    public_chat_text_area: Coordinate
    public_chat_pop_out: Coordinate
    insert_code_editor_coord_path: tuple[Coordinate, Coordinate, Coordinate, Coordinate]
    public_chat_button_coords: Coordinate


class ControllerOptions(TypedDict):
    tutor_profile: TutorProfile
    coords: ComponentCoordinates
    aws_credentials: AWSCredentials


class TdcAssistantGuiControllerV2:
    _options: ControllerOptions
    _window_manager: WindowManager

    def __init__(self, options: ControllerOptions):
        self._options = options
        self._window_manager = WindowManager(
            right_pop_out_button_coords=self._options["coords"]["public_chat_pop_out"],
            public_chat_text_box_coords=self._options["coords"][
                "public_chat_text_area"
            ],
            tutor_first_name=self._options["tutor_profile"]["first_name"],
            tutor_last_initial=self._options["tutor_profile"]["last_initial"],
            aws_credentials=self._options["aws_credentials"],
        )

    def scrape_public_chat(self) -> PublicChat:
        return self._window_manager.scrape_public_chat()

    def send_message(self, message: str):
        self._window_manager.send_message(message)

    def insert_code_editor(self):
        insert_code_editor(self._options["coords"]["insert_code_editor_coord_path"])

    def scrape_editor(self) -> list[CodeEditor]:
        return self._window_manager.scrape_code_editors()

    def scrape_screenshare(self) -> Optional[Screenshare]:
        return self._window_manager.scrape_screenshare()

    def is_screenshare_window_open(self) -> bool:
        return self._window_manager.is_screenshare_window_open()

    def send_text_to_code_editor(
        self, editor_language: str, editor_number: int, text: str
    ):
        self._window_manager.send_text_to_code_editor(
            editor_language, editor_number, text
        )

    def scrape_word_processors(self) -> list[WordProcessor]:
        return self._window_manager.scrape_word_processors()
