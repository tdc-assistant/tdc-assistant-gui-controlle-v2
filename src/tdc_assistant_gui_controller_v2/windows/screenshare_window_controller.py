from typing import Any, TypedDict

import os
from os.path import join, dirname

from time import time, sleep

import boto3

from ..logger import Logger
from ..types import AWSCredentials, Screenshare

FILENAME = "image_capture"
FILETYPE = "png"
FILEPATH = join(dirname(__file__), "code-snippet-screenshot.png")


class ScreenshareWindowController:
    _window: Any
    _logger: Logger
    _aws_credentials: AWSCredentials

    def __init__(self, window: Any, aws_credentials: AWSCredentials):
        self._window = window
        self._aws_credentials = aws_credentials
        self._logger = Logger(self)

    def scrape(self) -> Screenshare:
        start = self._logger.log(f"Started screenshare image capture")
        self._window.set_focus()
        sleep(0.5)
        self._window.maximize()
        sleep(0.5)
        self._window.capture_as_image().save(FILEPATH)
        s3 = boto3.client(
            "s3",
            aws_access_key_id=self._aws_credentials["access_key"],
            aws_secret_access_key=self._aws_credentials["secret_key"],
        )
        key = f"{int(time())}_{FILENAME}.{FILETYPE}"
        with open(FILEPATH, "rb") as f:
            s3.put_object(
                Bucket=self._aws_credentials["bucket_name"],
                Body=f.read(),
                Key=key,
            )
        end = self._logger.log(f"Finished screenshare image capture")
        self._logger.log_elapsed_time(start, end)
        return {"image_url": f'{self._aws_credentials["object_url_domain"]}/{key}'}

    def get_window_title(self) -> str:
        return self._window.window_text()
