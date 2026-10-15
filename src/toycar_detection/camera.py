# src/toycar_detection/camera.py

import cv2
import numpy as np

from numpy.typing import NDArray

from toycar_detection.configs.config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    FPS,
)


class Camera:

    def __init__(self,
                 camera_index: int = CAMERA_INDEX,
                 width: int = FRAME_WIDTH,
                 height: int = FRAME_HEIGHT,
                 fps: int = FPS, ) -> None:
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.fps = fps

        self.cap: cv2.VideoCapture | None = None

    def open(self) -> None:

        if self.is_opened():
            return

        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            self.cap.release()
            self.cap = None

            raise RuntimeError(f"Unable to open camera at index {self.camera_index}")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

    def read(self) -> NDArray[np.uint8]:

        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError("Camera is not opened")

        ret, frame = self.cap.read()

        if not ret or frame is None:
            raise RuntimeError("Failed to capture frame")

        return frame

    def is_opened(self) -> bool:

        b
        if self.cap is not None and


        return self.cap is not None and self.cap.isOpened()

    def release(self) -> None:

        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def __enter__(self) -> "Camera":

        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:

        self.release()
