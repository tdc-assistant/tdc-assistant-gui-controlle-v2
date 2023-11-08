import sys
from os import path

import json

from ..public_chat import parse_public_chat, PublicChat

from .constants import DIR_NAME_LOGS, Command
from .utils import log


@log(
    Command.PARSE_RAW_TEXT_FROM_PUBLIC_CHAT_LOG.value,
    ["first_name", "last_initial", "filename"],
)
def main():
    if not path.exists(path.join(DIR_NAME_LOGS, Command.SCRAPE_PUBLIC_CHAT.value)):
        print("Logs cannot be found")
        return

    _, first_name, last_initial, filename = sys.argv

    filepath = path.join(DIR_NAME_LOGS, Command.SCRAPE_PUBLIC_CHAT.value, filename)

    with open(filepath, "r") as f:
        public_chat: PublicChat = json.loads(f.read())
        return parse_public_chat(public_chat["raw_text"], first_name, last_initial)
