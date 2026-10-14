"""
Object detection module for OpenCV.

Provides an ObjectDetector class for HSV color segmentation,
Canny edge detection, contour extraction, and bounding boxes.
"""

import cv2
import numpy as np
from numpy.typing import NDArray

from toycar_detection.constants import HSV_BLUE
from toycar_detection.filter import gaussian_blur


type HSVRange = tuple[tuple[int, int, int], tuple[int, int, int]]
type HSVRanges = tuple[HSVRange, ...]


class ObjectDetector:
    """Detect colored objects using HSV segmentation and contours."""

    def __init__(
        self,
        hsv_ranges: HSVRanges = HSV_BLUE,
        min_contour_area: float = 500,
        canny_threshold_low: int = 50,
        canny_threshold_high: int = 150,
        bounding_box_color: tuple[int, int, int] = (255, 0, 0),
        bounding_box_thickness: int = 2,
    ) -> None:
        self.hsv_ranges = hsv_ranges
        self.min_contour_area = min_contour_area
        self.canny_threshold_low = canny_threshold_low
        self.canny_threshold_high = canny_threshold_high
        self.bounding_box_color = bounding_box_color
        self.bounding_box_thickness = bounding_box_thickness

    def create_mask(
        self,
        frame: NDArray[np.uint8],
    ) -> NDArray[np.uint8]:
        """Create a binary mask using predefined HSV color ranges."""

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

        for lower, upper in self.hsv_ranges:
            lower_bound = np.array(lower, dtype=np.uint8)
            upper_bound = np.array(upper, dtype=np.uint8)

            color_mask = cv2.inRange(
                hsv,
                lower_bound,
                upper_bound,
            )

            mask = cv2.bitwise_or(mask, color_mask)

        return mask

    def detect_edges(
        self,
        mask: NDArray[np.uint8],
    ) -> NDArray[np.uint8]:
        """Detect object edges using the Canny algorithm."""

        return cv2.Canny(
            mask,
            self.canny_threshold_low,
            self.canny_threshold_high,
        )

    def find_contours(
        self,
        mask: NDArray[np.uint8],
    ) -> list[NDArray[np.int32]]:
        """Find contours that satisfy the minimum area threshold."""

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        return [
            contour
            for contour in contours
            if cv2.contourArea(contour) >= self.min_contour_area
        ]

    def draw_bounding_boxes(
        self,
        frame: NDArray[np.uint8],
        contours: list[NDArray[np.int32]],
    ) -> NDArray[np.uint8]:
        """Draw bounding boxes around detected objects."""

        result = frame.copy()

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            cv2.rectangle(
                result,
                (x, y),
                (x + w, y + h),
                self.bounding_box_color,
                self.bounding_box_thickness,
            )

        return result

    def detect(
        self,
        frame: NDArray[np.uint8],
    ) -> tuple[
        NDArray[np.uint8],
        NDArray[np.uint8],
        NDArray[np.uint8],
    ]:
        """Detect colored objects and return result, mask, and edges."""

        blurred = gaussian_blur(
            frame,
            kernel_size=(5, 5),
        )

        mask = self.create_mask(blurred)

        edges = self.detect_edges(mask)

        contours = self.find_contours(mask)

        result = self.draw_bounding_boxes(frame, contours)

        return result, mask, edges
