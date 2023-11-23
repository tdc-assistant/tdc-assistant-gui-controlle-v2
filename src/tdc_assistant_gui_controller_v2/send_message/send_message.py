from pywinauto import mouse, keyboard  # type: ignore

from .types import Message
from ..types import Coordinate
from ..utils import transform_text


def send_message(message: Message, public_chat_coords: Coordinate):
    mouse.click(coords=(public_chat_coords["x"], public_chat_coords["y"]))
    keyboard.send_keys(transform_text(message["content"]))
