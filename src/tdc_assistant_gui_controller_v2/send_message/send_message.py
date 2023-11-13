from pywinauto import mouse, keyboard  # type: ignore

from .types import Message
from ..types import Coordinate

originals_and_replacements = {
    "`": "",
    "\n": "{VK_RETURN}",
}


def _transform_text(text: str):
    transformed_text = ""
    for ch in text:
        if ch in "{}()":
            transformed_text += "{" + ch + "}"
        else:
            transformed_text += ch

    for original, replacement in originals_and_replacements.items():
        transformed_text = transformed_text.replace(original, replacement)

    return "{VK_SPACE}".join(transformed_text.split()) + "{VK_RETURN}"


def send_message(message: Message, public_chat_coords: Coordinate):
    mouse.click(coords=(public_chat_coords["x"], public_chat_coords["y"]))
    keyboard.send_keys(_transform_text(message["content"]))
