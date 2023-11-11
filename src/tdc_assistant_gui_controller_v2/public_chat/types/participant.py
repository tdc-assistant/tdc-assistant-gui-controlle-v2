from typing import TypedDict, Optional

from .participant_type import ParticipantType


class Participant(TypedDict):
    type: ParticipantType
    name: Optional[str]
