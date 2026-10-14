"""
Image filtering and preprocessing utilities for OpenCV.

Provides common image filters for noise reduction,
smoothing, and image enhancement.
"""

import cv2
import numpy as np
from numpy.typing import NDArray


def gaussian_blur(
    frame: NDArray[np.uint8],
    kernel_size: tuple[int, int] = (5, 5),
    sigma: float = 0,
) -> NDArray[np.uint8]:
    """Apply Gaussian blur to reduce image noise."""

    return cv2.GaussianBlur(frame, kernel_size, sigma)


def median_blur(
    frame: NDArray[np.uint8],
    kernel_size: int = 5,
) -> NDArray[np.uint8]:
    """Apply median blur to reduce salt-and-pepper noise."""

    return cv2.medianBlur(frame, kernel_size)


def average_blur(
    frame: NDArray[np.uint8],
    kernel_size: tuple[int, int] = (5, 5),
) -> NDArray[np.uint8]:
    """Apply average blur to smooth an image."""

    return cv2.blur(frame, kernel_size)


def bilateral_filter(
    frame: NDArray[np.uint8],
    diameter: int = 9,
    sigma_color: float = 75,
    sigma_space: float = 75,
) -> NDArray[np.uint8]:
    """Reduce noise while preserving object edges."""

    return cv2.bilateralFilter(
        frame,
        diameter,
        sigma_color,
        sigma_space,
    )


def non_local_means_denoising(
    frame: NDArray[np.uint8],
    strength: float = 10,
    template_window_size: int = 7,
    search_window_size: int = 21,
) -> NDArray[np.uint8]:
    """Reduce noise in a BGR image using non-local means."""

    return cv2.fastNlMeansDenoisingColored(
        frame,
        None,
        strength,
        strength,
        template_window_size,
        search_window_size,
    )
