from typing import TypedDict

from os import listdir
from os.path import isfile, join

import json

from tdc_assistant_gui_controller_v2.public_chat import parse_public_chat
from tdc_assistant_gui_controller_v2.public_chat.types import public_chat_message
from tdc_assistant_gui_controller_v2.public_chat.types.public_chat_message import (
    PublicChatMessage,
)


class ParsePublicChatTestFixtureEntry(TypedDict):
    raw_text: str
    public_chat_messages: list[PublicChatMessage]


ParsePublicChatTestFixture = list[ParsePublicChatTestFixtureEntry]


def test_parse_public_chat():
    test_fixture = load_test_fixture()

    for entry in test_fixture:
        raw_text = entry["raw_text"]
        messages = entry["public_chat_messages"]

        assert parse_public_chat(raw_text, "Adam", "C") == messages


def load_test_fixture() -> ParsePublicChatTestFixture:
    print("loading test fixture...")
    test_fixture_path = join("test", "fixtures", "parse_public_chat")
    test_fixture = []
    for filepath in listdir(test_fixture_path):
        if isfile(join("test", "fixtures", "parse_public_chat", filepath)):
            with open(
                join("test", "fixtures", "parse_public_chat", filepath), "r"
            ) as f:
                raw_json = json.loads(f.read())
                test_fixture_entry: ParsePublicChatTestFixtureEntry = {
                    "raw_text": raw_json["input"]["raw_text"],
                    "public_chat_messages": raw_json["output"],
                }
                test_fixture.append(test_fixture_entry)

    return test_fixture
