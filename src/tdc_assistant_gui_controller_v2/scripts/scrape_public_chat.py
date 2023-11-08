import sys

from ..public_chat.scrape_public_chat import scrape_public_chat


def main():
    if len(sys.argv) != 3:
        print("Usage: scrape_public_chat first_name last_initial")
        return

    _, first_name, last_initial = sys.argv
    print(scrape_public_chat(first_name, last_initial))
