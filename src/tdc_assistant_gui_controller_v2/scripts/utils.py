from typing import Callable, Any

import sys

import os
from os.path import join

import time

import json

from .constants import DIR_NAME_LOGS


def log(
    command_name: str, arg_names: list[str]
) -> Callable[[Callable[[], Any]], Callable[[], Any]]:
    def log_outer(command: Callable[[], dict[Any, Any]]):
        def log_inner():
            if len(sys.argv) - 1 != len(arg_names):
                print(f"Command not recognized: {' '.join(sys.argv)}")
                print(f"Usage: {' '.join([command_name] + arg_names)}")
                return

            os.makedirs(join(DIR_NAME_LOGS, command_name), exist_ok=True)

            filename = f"{int(time.time())}_{command_name}.json"

            with open(join(DIR_NAME_LOGS, command_name, filename), "w") as f:
                f.write(json.dumps(command(), indent=4))

        return log_inner

    return log_outer
