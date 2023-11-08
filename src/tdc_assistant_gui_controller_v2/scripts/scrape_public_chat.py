import sys

from ..public_chat import scrape_public_chat

from .constants import Command
from .utils import log


@log(Command.SCRAPE_PUBLIC_CHAT.value, ["first_name", "last_initial"])
def main():
    _, first_name, last_initial = sys.argv
    return scrape_public_chat(first_name, last_initial)
