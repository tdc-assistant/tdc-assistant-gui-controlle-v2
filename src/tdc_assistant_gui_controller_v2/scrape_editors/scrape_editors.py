from typing import TypedDict

from pywinauto import mouse, keyboard, clipboard  # type: ignore

from time import sleep

from tdc_assistant_gui_controller_v2.windows import get_all_windows, WindowTitle


class Editor(TypedDict):
    name: str
    button_coords: tuple[int, int]
    content: str


class ScrapeEditorConfig(TypedDict):
    coords_left: tuple[int, int]
    coords_right: tuple[int, int]
    coords_pop_out_button: tuple[int, int]
    text_editor_coords: tuple[int, int]


editor_names = [
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

BUTTON_SCAN_STEP_SIZE_HORIZONTAL = 100
BUTTON_SCAN_STEP_SIZE_VERTICAL = 35
NUM_POP_OUT_BUTTON_TRIES = 3
POP_OUT_BUTTON_TRIES_STEP_SIZE = 10
MAX_DUPLICATE = 4


def scrape_editors(
    config: ScrapeEditorConfig, editor_cache: list[Editor]
) -> list[Editor]:
    # Search known buttons first
    for editor in editor_cache:
        mouse.move(coords=editor["button_coords"])
        mouse.click(coords=editor["button_coords"])

        for i in range(NUM_POP_OUT_BUTTON_TRIES):
            x, y = config["coords_pop_out_button"]
            mouse.move(coords=(x + i * POP_OUT_BUTTON_TRIES_STEP_SIZE, y))
            mouse.click(coords=(x + i * POP_OUT_BUTTON_TRIES_STEP_SIZE, y))
            sleep(1)

            windows = get_all_windows(editor_names)
            for window in windows:
                # TODO Scrape content here and update editor here
                window.close()
                sleep(1)

            if len(windows) > 0:
                break

    # Brute-force search after using the cache
    # TODO Continue until it fails to open a window twice (extra check in case it clicks a gap)
    x = config["coords_left"][0]
    y = config["coords_left"][1]

    if len(editor_cache) > 0:
        last_cached_button_coords = editor_cache[-1]["button_coords"]
        x, y = last_cached_button_coords

    is_clicking_editor = False
    should_stop_on_next_missing_window = False
    duplicate_count = 0
    while True:
        mouse.move(coords=(x, y))
        mouse.click(coords=(x, y))
        sleep(1)
        found_window = False
        for i in range(NUM_POP_OUT_BUTTON_TRIES):
            pop_out_button_cord_x, pop_out_button_cord_y = config[
                "coords_pop_out_button"
            ]
            mouse.move(
                coords=(
                    pop_out_button_cord_x + i * POP_OUT_BUTTON_TRIES_STEP_SIZE,
                    pop_out_button_cord_y,
                )
            )
            mouse.click(
                coords=(
                    pop_out_button_cord_x + i * POP_OUT_BUTTON_TRIES_STEP_SIZE,
                    pop_out_button_cord_y,
                )
            )
            sleep(1)

            windows = get_all_windows(editor_names)

            if len(windows) == 0:
                if should_stop_on_next_missing_window:
                    break

            if len(windows) > 1:
                raise Exception(
                    f"Failed to close windows: '{','.join([w.window_text() for w in windows ])}'"
                )
            elif len(windows) == 1:
                window = windows[0]
                editor_name = window.window_text()
                editor_cache_names = [editor["name"] for editor in editor_cache]

                if editor_name not in editor_cache_names:
                    mouse.click(coords=config["text_editor_coords"])
                    clipboard.EmptyClipboard()
                    keyboard.send_keys("^a^c")
                    try:
                        content = clipboard.GetData(clipboard.win32clipboard.CF_UNICODETEXT)  # type: ignore
                    except:
                        content = ""
                    editor_cache.append(
                        {
                            "name": editor_name,
                            "button_coords": (x, y),
                            "content": content,
                        }
                    )
                    duplicate_count = 0
                else:
                    if editor_name != editor_cache_names[-1]:
                        is_clicking_editor = True
                    else:
                        duplicate_count += 1

                window.close()
                sleep(1)
                found_window = True

            if len(windows) > 0:
                break

        if duplicate_count >= MAX_DUPLICATE:
            break

        if is_clicking_editor:
            break

        if found_window:
            should_stop_on_next_missing_window = False
        elif should_stop_on_next_missing_window:
            break
        else:
            should_stop_on_next_missing_window = True

        x += BUTTON_SCAN_STEP_SIZE_HORIZONTAL

        if x > config["coords_right"][0]:
            x = config["coords_left"][0]
            print("incrementing y")
            y += BUTTON_SCAN_STEP_SIZE_VERTICAL

    return editor_cache
