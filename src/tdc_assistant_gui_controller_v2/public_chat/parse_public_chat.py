import re

from .types import PublicChatMessage

pattern_timestamp = re.compile(r"\d+:\d\d:\d\d")
pattern = re.compile(r"(\w+|\(\w*\))\s+(\d+:\d\d:\d\d)")


texts_to_remove = ["has entered the room.", "is typing", "Classroo"]


def _parse_customer_name_from_first_message(lines):
    for i, line in enumerate(lines):
        if pattern_timestamp.match(line):
            if i > 0 and lines[i - 1] not in ["(Tutor)", "Classroo"]:
                return lines[i - 1]


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


def parse_public_chat(
    raw_text, tutor_first_name, tutor_last_initial
) -> list[PublicChatMessage]:
    stripped_matches = []
    for match in re.split(pattern, raw_text):
        stripped_matches.append(
            match.strip().rstrip(f"{tutor_first_name} {tutor_last_initial}").strip()
        )

    customer = _parse_customer_name_from_first_message(stripped_matches)
    processed_matches = []
    for sm in stripped_matches:
        processed_matches.append(
            _process_message(sm, customer, tutor_first_name, tutor_last_initial)
        )

    messages: list[PublicChatMessage] = []
    for sm in processed_matches:
        if sm in [customer, "(Tutor)"]:
            is_customer = sm == customer
            messages.append(
                {
                    "participant": {
                        "name": sm if is_customer else tutor_first_name,
                        "type": "student" if is_customer else "tutor",
                    },
                    "content": "",
                }
            )
        elif len(messages) == 0:
            continue
        elif pattern_timestamp.match(sm):
            continue
        else:
            messages[-1]["content"] += (
                " ".join(sm.split())
                .strip(customer[0] if len(customer) > 0 else "")  # type: ignore
                .strip()
                .strip(tutor_first_name[0])
                .strip()
            )

    return messages
