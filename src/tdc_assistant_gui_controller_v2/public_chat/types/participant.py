from typing import TypedDict

from .participant_type import ParticipantType


class Participant(TypedDict):
    type: ParticipantType
    name: str
