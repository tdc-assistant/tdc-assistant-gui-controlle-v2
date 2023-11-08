from typing import Final

from enum import Enum


# Root logging directory
DIR_NAME_LOGS: Final[str] = "logs"


class Command(Enum):
    SCRAPE_PUBLIC_CHAT = "scrape_public_chat"
    PARSE_RAW_TEXT_FROM_PUBLIC_CHAT_LOG = "parse_raw_text_from_public_chat_log"
