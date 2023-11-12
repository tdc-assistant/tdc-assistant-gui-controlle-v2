from pywinauto import mouse # type: ignore

from time import sleep

from tdc_assistant_gui_controller_v2.types.coordinate import Coordinate  

def insert_code_editor(coord_path: tuple[Coordinate, Coordinate, Coordinate, Coordinate]):
     for coord in coord_path:
        x = coord['x']
        y = coord['y']
        mouse.move(coords=(x, y))
        mouse.click(coords=(x, y))
        sleep(0.1)

