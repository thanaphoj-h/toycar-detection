"""
Image loading utilities for OpenCV.

Provides functions for loading images from files
and retrieving basic image information.
"""

from pathlib import Path

import cv2
import numpy as np
from numpy.typing import NDArray


def load_image(
    path: str | Path,
    flags: int = cv2.IMREAD_COLOR,
) -> NDArray[np.uint8]:
    """Load an image from a file."""

    image_path = Path(path)

    if not image_path.is_file():
        raise FileNotFoundError(
            f"Image file not found: {image_path}"
        )

    frame = cv2.imread(str(image_path), flags)

    if frame is None:
        raise ValueError(
            f"Unable to read image: {image_path}"
        )

    return frame


def get_image_size(
    frame: NDArray[np.uint8],
) -> tuple[int, int]:
    """Return image dimensions as (width, height)."""

    height, width = frame.shape[:2]

    return width, height


def resize_image(
    frame: NDArray[np.uint8],
    width: int,
    height: int,
) -> NDArray[np.uint8]:
    """Resize an image to the specified dimensions."""

    if width <= 0 or height <= 0:
        raise ValueError(
            "Image width and height must be positive"
        )

    return cv2.resize(
        frame,
        (width, height),
        interpolation=cv2.INTER_AREA,
    )
