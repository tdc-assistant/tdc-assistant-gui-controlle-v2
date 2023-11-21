from typing import Final
from pywinauto import Desktop  # type: ignore

from .enums import WindowTitle


default_window_titles: Final[list[WindowTitle]] = [
    WindowTitle.CLASSROOM,
    WindowTitle.PUBLIC_CHAT,
    WindowTitle.EDITOR,
    WindowTitle.SERVER_CONNECTION_ERROR,
    WindowTitle.WHITEBOARD,
    WindowTitle.GRAPHING_CALCULATOR,
    WindowTitle.WORD_PROCESSOR,
    WindowTitle.C_LIKE_EDITOR,
    WindowTitle.CSS_EDITOR,
    WindowTitle.GO_EDITOR,
    WindowTitle.HTML_EDITOR,
    WindowTitle.JAVA_EDITOR,
    WindowTitle.JAVASCRIPT_EDITOR,
    WindowTitle.MATHEMATICA_EDITOR,
    WindowTitle.PHP_EDITOR,
    WindowTitle.PYTHON_EDITOR,
    WindowTitle.R_EDITOR,
    WindowTitle.RUBY_EDITOR,
    WindowTitle.SQL_EDITOR,
    WindowTitle.XML_EDITOR,
]


def get_all_windows(window_titles: list[WindowTitle] = default_window_titles):
    windows = Desktop(backend="uia").windows()

    result = []

    for w in windows:
        for t in window_titles:
            if t.value.lower() in w.window_text().lower():
                result.append(w)
                break

    return result
