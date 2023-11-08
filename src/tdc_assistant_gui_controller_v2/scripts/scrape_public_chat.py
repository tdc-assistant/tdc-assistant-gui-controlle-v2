from typing import Final

import sys

import os
from os.path import join

import time

import json

from ..public_chat.scrape_public_chat import scrape_public_chat

DIR_NAME_LOGS: Final[str] = "logs"
DIR_NAME_COMMAND: Final[str] = "scrape_public_chat"
FILENAME = f"{int(time.time())}_scrape_public_chat.json"


def main():
    if len(sys.argv) != 3:
        print("Usage: scrape_public_chat first_name last_initial")
        return

    os.makedirs(join(DIR_NAME_LOGS, DIR_NAME_COMMAND), exist_ok=True)

    _, first_name, last_initial = sys.argv

    with open(join(DIR_NAME_LOGS, DIR_NAME_COMMAND, FILENAME), "w") as f:
        public_chat = scrape_public_chat(first_name, last_initial)
        f.write(json.dumps(public_chat, indent=4))
