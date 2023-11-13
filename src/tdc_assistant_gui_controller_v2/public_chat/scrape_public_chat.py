from typing import Any

from time import sleep

from pywinauto import mouse  # type: ignore

from .parse_public_chat import parse_public_chat
from .types import PublicChat

from ..windows import get_window_by_title, WindowTitle
from ..controls import (
    ControlPropertyKey,
    ControlPropertyValue,
    find_control_by_property,
)

from ..types import Coordinate


MAX_RETRY_COUNT = 3
ERR_MSG_CONTROL_NOT_FOUND = f"Cannot find control property '{ControlPropertyKey.CLASS_NAME.value}' with value '{ControlPropertyValue.PUBLIC_CHAT.value}' in window '{WindowTitle.PUBLIC_CHAT.value}'"


def scrape_public_chat_raw_text(control: Any) -> str:
    result = find_control_by_property(
        control,
        ControlPropertyKey.CLASS_NAME,
        ControlPropertyValue.PUBLIC_CHAT,
        lambda c: c.get_properties().get(ControlPropertyKey.TEXTS.value)[0],
    )

    if result is None:
        raise Exception(ERR_MSG_CONTROL_NOT_FOUND)

    return result


def scrape_public_chat(
    tutor_first_name: str,
    tutor_last_initial: str,
    chat_log_pop_out_button_coords: Coordinate,
    public_chat_button_coords: Coordinate,
) -> PublicChat:
    mouse.click(coords=(public_chat_button_coords["x"], public_chat_button_coords["y"]))
    sleep(0.5)
    public_chat_window = get_window_by_title(
        WindowTitle.PUBLIC_CHAT, chat_log_pop_out_button_coords
    )

    raw_text = scrape_public_chat_raw_text(public_chat_window)

    messages = parse_public_chat(
        raw_text,
        tutor_first_name,
        tutor_last_initial,
    )

    public_chat_window.close()

    return {"messages": messages, "raw_text": raw_text}
