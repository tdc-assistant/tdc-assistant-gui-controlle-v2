from typing import Any
from time import sleep

from pywinauto import mouse  # type: ignore

from .parse_public_chat import parse_public_chat
from .types import PublicChat

from ..windows import WindowTitle, get_all_windows
from ..controls import (
    ControlPropertyKey,
    ControlPropertyValue,
    find_control_by_property,
)

from ..constants import (
    CHAT_LOG_POP_OUT_BUTTON_COORDS,
    GUI_EVENT_DELAY_BASE_IN_SECONDS,
    GUI_EVENT_DELAY_INCREMENT_IN_SECONDS,
)


MAX_RETRY_COUNT = 3
ERR_MSG_CONTROL_NOT_FOUND = f"Cannot find control property '{ControlPropertyKey.CLASS_NAME.value}' with value '{ControlPropertyValue.PUBLIC_CHAT.value}' in window '{WindowTitle.PUBLIC_CHAT.value}'"


def scrape_public_chat_raw_text(control: Any) -> str:
    result = find_control_by_property(
        control,
        ControlPropertyKey.CLASS_NAME,
        ControlPropertyValue.PUBLIC_CHAT,
        lambda props: props.get(ControlPropertyKey.TEXTS.value)[0],
    )

    if result is None:
        raise Exception(ERR_MSG_CONTROL_NOT_FOUND)

    return result


def scrape_public_chat(tutor_first_name: str, tutor_last_initial: str) -> PublicChat:
    windows_before_clicks = get_all_windows()

    public_chat_window = None
    num_tries = 0
    delay = GUI_EVENT_DELAY_BASE_IN_SECONDS

    while public_chat_window is None and num_tries < MAX_RETRY_COUNT:
        mouse.click(coords=CHAT_LOG_POP_OUT_BUTTON_COORDS)
        sleep(delay)

        for w in get_all_windows():
            # TODO Check title to ensure robustness .. another window could open while this is happening
            texts = w.get_properties().get(ControlPropertyKey.TEXTS.value)

            if len(texts) == 0:
                continue

            text = texts[0]

            if w not in windows_before_clicks and WindowTitle.PUBLIC_CHAT.value in text:
                public_chat_window = w
                break

        delay += GUI_EVENT_DELAY_INCREMENT_IN_SECONDS
        num_tries += 1

    if public_chat_window is None:
        raise Exception(f"Cannot find window: '{WindowTitle.PUBLIC_CHAT.value}")

    raw_text = scrape_public_chat_raw_text(public_chat_window)

    messages = parse_public_chat(
        raw_text,
        tutor_first_name,
        tutor_last_initial,
    )

    public_chat_window.close()

    return {"messages": messages, "raw_text": raw_text}
