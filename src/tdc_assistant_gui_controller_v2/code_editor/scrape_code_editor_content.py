from typing import Any

from time import sleep

from pywinauto import mouse, keyboard, clipboard  # type: ignore

from .types import CodeEditor


def scrape_code_editor_content(window: Any) -> str:
    window.set_focus()
    sleep(0.5)
    # window.maximize()
    # sleep(0.5)

    mouse.move(coords=(750, 750))
    sleep(0.5)
    mouse.click(coords=(750, 750))
    sleep(0.5)

    clipboard.EmptyClipboard()
    keyboard.send_keys("^a^c")
    try:
        content = clipboard.GetData(clipboard.win32clipboard.CF_UNICODETEXT)  # type: ignore
    except:
        content = ""

    return content
