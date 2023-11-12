from typing import TypedDict

from .public_chat import scrape_public_chat, PublicChat
from .types import Coordinate
from .send_message import Message, send_message


class TutorProfile(TypedDict):
    first_name: str
    last_initial: str


class ComponentCoordinates(TypedDict):
    public_chat_text_area: Coordinate
    public_chat_pop_out: Coordinate


class ControllerOptions(TypedDict):
    tutor_profile: TutorProfile
    coords: ComponentCoordinates


class TdcAssistantGuiControllerV2:
    _options: ControllerOptions

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
        )

    def send_message(self, message: Message):
        send_message(message, self._options["coords"]["public_chat_text_area"])
