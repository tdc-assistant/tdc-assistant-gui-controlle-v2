from typing import TypedDict

from .public_chat import scrape_public_chat, PublicChat
from .types import Coordinate
from .send_message import Message, send_message
from .insert_code_editor import insert_code_editor
from .scrape_editors import ScrapeEditorConfig
from .scrape_editors import scrape_editors, EditorCache


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
    scraped_editor_config: ScrapeEditorConfig


class TdcAssistantGuiControllerV2:
    _options: ControllerOptions
    _editor_cache: EditorCache

    def __init__(self, options: ControllerOptions):
        self._options = options

    def scrape_public_chat(self) -> PublicChat:
        tutor_profile = self._options["tutor_profile"]
        return scrape_public_chat(
            tutor_first_name=tutor_profile["first_name"],
            tutor_last_initial=tutor_profile["last_initial"],
            chat_log_pop_out_button_coords=self._options["coords"][
                "public_chat_pop_out"
            ],
            public_chat_button_coords=self._options["coords"][
                "public_chat_button_coords"
            ],
        )

    def send_message(self, message: Message):
        send_message(message, self._options["coords"]["public_chat_text_area"])

    def insert_code_editor(self):
        insert_code_editor(self._options["coords"]["insert_code_editor_coord_path"])

    def scrape_editor(self) -> EditorCache:
        scrape_editors(self._options["scraped_editor_config"], self._editor_cache)
        return self._editor_cache
