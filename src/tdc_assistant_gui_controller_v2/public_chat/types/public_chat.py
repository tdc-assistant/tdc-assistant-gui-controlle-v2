from typing import TypedDict

from .public_chat_message import PublicChatMessage


class PublicChat(TypedDict):
    messages: list[PublicChatMessage]
    raw_text: str
