"""
Geometric shape detection module for OpenCV.

Detects triangles, squares, circles, and ovals using
contour approximation and geometric properties.

Supports both Canny edge detection and HSV binary masks.
"""

import cv2
import numpy as np
from numpy.typing import NDArray


class ShapeDetector:
    """Detect and classify geometric shapes in an image."""

    def __init__(
        self,
        min_contour_area: float = 500,
        approximation_factor: float = 0.02,
        circularity_threshold: float = 0.85,
        square_aspect_tolerance: float = 0.10,
        solidity_threshold: float = 0.90,
        ellipse_similarity_threshold: float = 0.85,
        ellipse_error_threshold: float = 0.10,
        bounding_box_color: tuple[int, int, int] = (255, 0, 0),
        bounding_box_thickness: int = 2,
    ) -> None:
        self.min_contour_area = min_contour_area
        self.approximation_factor = approximation_factor
        self.circularity_threshold = circularity_threshold
        self.square_aspect_tolerance = square_aspect_tolerance
        self.solidity_threshold = solidity_threshold
        self.ellipse_similarity_threshold = ellipse_similarity_threshold
        self.ellipse_error_threshold = ellipse_error_threshold
        self.bounding_box_color = bounding_box_color
        self.bounding_box_thickness = bounding_box_thickness

    def preprocess(
        self,
        frame: NDArray[np.uint8],
    ) -> NDArray[np.uint8]:
        """Convert a BGR image to a binary edge map."""

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        return cv2.Canny(blurred, 50, 150)

    def find_contours(
        self,
        binary_image: NDArray[np.uint8],
    ) -> list[NDArray[np.int32]]:
        """Find external contours above the minimum area."""

        contours, _ = cv2.findContours(
            binary_image,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        return [
            contour
            for contour in contours
            if cv2.contourArea(contour) >= self.min_contour_area
        ]

    @staticmethod
    def ellipse_fit_error(
        contour: NDArray[np.int32],
        ellipse: tuple,
    ) -> float:
        """Calculate the mean normalized ellipse fitting error."""

        (cx, cy), (width, height), angle = ellipse

        if width <= 0 or height <= 0:
            return float("inf")

        points = contour.reshape(-1, 2).astype(np.float64)

        theta = np.deg2rad(angle)

        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)

        dx = points[:, 0] - cx
        dy = points[:, 1] - cy

        x_rot = dx * cos_theta + dy * sin_theta
        y_rot = -dx * sin_theta + dy * cos_theta

        normalized_distance = np.sqrt(
            (x_rot / (width / 2)) ** 2
            + (y_rot / (height / 2)) ** 2
        )

        return float(np.mean(np.abs(normalized_distance - 1)))

    def classify_shape(
        self,
        contour: NDArray[np.int32],
    ) -> str:
        """Classify a contour using geometric properties."""

        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        if area <= 0 or perimeter <= 0:
            return "Unknown"

        approximation = cv2.approxPolyDP(
            contour,
            self.approximation_factor * perimeter,
            True,
        )

        vertices = len(approximation)

        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)

        if hull_area <= 0:
            return "Unknown"

        solidity = area / hull_area

        # Triangle
        if vertices == 3:
            if (
                cv2.isContourConvex(approximation)
                and solidity >= self.solidity_threshold
            ):
                return "Triangle"

            return "Unknown"

        # Square
        if vertices == 4:
            if not cv2.isContourConvex(approximation):
                return "Unknown"

            if solidity < self.solidity_threshold:
                return "Unknown"

            rect = cv2.minAreaRect(contour)
            width, height = rect[1]

            if min(width, height) <= 0:
                return "Unknown"

            aspect_ratio = min(width, height) / max(width, height)

            if aspect_ratio >= 1 - self.square_aspect_tolerance:
                return "Square"

            return "Unknown"

        # Reject strongly concave shapes
        if solidity < self.solidity_threshold:
            return "Unknown"

        # Circle
        circularity = (4 * np.pi * area) / (perimeter ** 2)

        if circularity >= self.circularity_threshold:
            rect = cv2.minAreaRect(contour)
            width, height = rect[1]

            if min(width, height) > 0:
                aspect_ratio = min(width, height) / max(width, height)

                if aspect_ratio >= 0.90:
                    return "Circle"

        # Oval
        if len(contour) >= 5 and vertices >= 5:
            ellipse = cv2.fitEllipse(contour)

            major_axis = max(ellipse[1])
            minor_axis = min(ellipse[1])

            if major_axis <= 0:
                return "Unknown"

            axis_ratio = minor_axis / major_axis

            ellipse_area = (
                np.pi * (major_axis / 2) * (minor_axis / 2)
            )

            area_similarity = min(area, ellipse_area) / max(
                area, ellipse_area
            )

            fit_error = self.ellipse_fit_error(contour, ellipse)

            if (
                0.3 <= axis_ratio < 0.9
                and area_similarity >= self.ellipse_similarity_threshold
                and fit_error <= self.ellipse_error_threshold
            ):
                return "Oval"

        return "Unknown"

    def draw_shapes(
        self,
        frame: NDArray[np.uint8],
        contours: list[NDArray[np.int32]],
    ) -> NDArray[np.uint8]:
        """Draw bounding boxes and labels for detected shapes."""

        result = frame.copy()

        for contour in contours:
            shape = self.classify_shape(contour)

            if shape == "Unknown":
                continue

            x, y, w, h = cv2.boundingRect(contour)

            cv2.rectangle(
                result,
                (x, y),
                (x + w, y + h),
                self.bounding_box_color,
                self.bounding_box_thickness,
            )

            cv2.putText(
                result,
                shape,
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                self.bounding_box_color,
                2,
            )

        return result

    def detect(
        self,
        frame: NDArray[np.uint8],
        mask: NDArray[np.uint8] | None = None,
    ) -> tuple[NDArray[np.uint8], NDArray[np.uint8]]:
        """
        Detect geometric shapes in an image.

        If a binary mask is provided, contours are extracted
        directly from the mask. Otherwise, Canny edges are used.

        Returns:
            Annotated image and binary image used for detection.
        """

        if mask is None:
            binary_image = self.preprocess(frame)
        else:
            if mask.ndim != 2 or mask.shape != frame.shape[:2]:
                raise ValueError(
                    "Mask must be a single-channel image "
                    "matching the frame dimensions"
                )

            binary_image = mask.copy()

        contours = self.find_contours(binary_image)

        result = self.draw_shapes(frame, contours)

        return result, binary_image
