from typing import TypedDict

from .public_chat import scrape_public_chat, PublicChat


class TutorProfile(TypedDict):
    first_name: str
    last_initial: str


class ControllerOptions(TypedDict):
    tutor_profile: TutorProfile


class TdcAssistantGuiControllerV2:
    _options: ControllerOptions

    def __init__(self, options: ControllerOptions):
        self._options = options

    def scrape_public_chat(self) -> PublicChat:
        tutor_profile = self._options["tutor_profile"]
        return scrape_public_chat(
            tutor_first_name=tutor_profile["first_name"],
            tutor_last_initial=tutor_profile["last_initial"],
        )
