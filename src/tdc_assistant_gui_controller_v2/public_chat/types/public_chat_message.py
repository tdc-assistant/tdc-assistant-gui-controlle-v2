from typing import TypedDict

from .participant import Participant


class PublicChatMessage(TypedDict):
    participant: Participant
    content: str
