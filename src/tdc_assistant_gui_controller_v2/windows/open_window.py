from time import sleep

from pywinauto import mouse  # type: ignore

from ..types import Coordinate


def open_window(right_pop_out_button_coords: Coordinate):
    coords = (right_pop_out_button_coords["x"], right_pop_out_button_coords["y"])
    mouse.move(coords=coords)
    sleep(0.5)
    mouse.click(coords=coords)
    sleep(0.5)
