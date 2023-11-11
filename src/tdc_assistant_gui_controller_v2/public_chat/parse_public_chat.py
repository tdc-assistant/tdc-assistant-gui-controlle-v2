from os import name
import re
from tdc_assistant_gui_controller_v2.public_chat.types.participant import Participant

from tdc_assistant_gui_controller_v2.public_chat.types.participant_type import (
    ParticipantType,
)

from .types import PublicChatMessage

pattern_timestamp = re.compile(r"\d+:\d\d:\d\d")
pattern = re.compile(r"(\w+|\(\w*\))\s+(\d+:\d\d:\d\d)")


texts_to_remove = ["has entered the room.", "is typing", "Classroo"]

REGEX_ASCII = r"[^\x00-\x7F]"
REGEX_DISPLAY_TIME = re.compile(r"\d:\d\d:\d\d")
REGEX_STUDENT_HAS_ENTERED = re.compile(r"(\w+)\shas\sentered\sthe\sroom.")
REGEX_HAS_ENTERED_ROOM = re.compile(r"has\s*entered\s*the\s*room\.")


def _process_message(message, customer_name, tutor_first_name, tutor_last_initial):
    for text_to_remove in texts_to_remove + [
        f"{tutor_first_name} {tutor_last_initial} (Tutor)"
    ]:
        message = message.replace(text_to_remove, "")

    message = message.replace(
        customer_name[0] if len(customer_name) > 0 else "" + " " + tutor_first_name[0],
        "",
    )

    if len(customer_name) > 0:
        message = message.replace(
            customer_name[0] if len(customer_name) > 0 else "" + " " + customer_name, ""
        )

    message = message.strip()

    return message


def _parse_customer_name(raw_text):
    m = re.search(REGEX_STUDENT_HAS_ENTERED, raw_text)

    if m is None:
        return None

    (customer_name,) = m.groups()

    return customer_name


def parse_public_chat(
    raw_text, tutor_first_name, tutor_last_initial
) -> list[PublicChatMessage]:
    raw_text_clean = re.sub(REGEX_ASCII, " ", raw_text)
    tutor_name = f"{tutor_first_name} {tutor_last_initial}"
    student_name = _parse_customer_name(raw_text_clean)

    # TODO Change tutor name to "\w+\s+\w" because could be any tutor not just me
    tutor_or_student_name_regex = re.compile(
        rf"({tutor_name}\s\(Tutor\)|{student_name}|Classroom)"
    )

    trailing_initials_regex = re.compile(
        rf"\s*({tutor_name[0]}\s+{student_name[0] if student_name else ''}?|C)\s*$"
    )

    m = tutor_or_student_name_regex.split(raw_text_clean)

    messages: list[PublicChatMessage] = []
    curr_message_content = ""
    for s in reversed(m):
        content = re.sub(REGEX_DISPLAY_TIME, " ", s).strip()
        content = re.sub(trailing_initials_regex, "", content).strip()
        content = re.sub(r"\s{2,}A", "", content).strip()
        if tutor_or_student_name_regex.match(content):
            if re.match(REGEX_HAS_ENTERED_ROOM, curr_message_content):
                messages.append(
                    {
                        "participant": {"type": "classroom", "name": None},
                        "content": curr_message_content,
                    }
                )
            else:
                participant: Participant
                if content == student_name:
                    participant = {"type": "student", "name": student_name}
                elif content == "Classroom":
                    participant = {"type": "classroom", "name": None}
                else:
                    participant = {"type": "tutor", "name": tutor_first_name}

                messages.append(
                    {
                        "participant": participant,
                        "content": curr_message_content,
                    }
                )
            curr_message_content = ""
        else:
            curr_message_content += content

    return messages
