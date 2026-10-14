"""
Image-based color and geometric shape detection.

Detects blue and yellow objects using HSV segmentation
and classifies triangles, squares, circles, and ovals.
"""

import cv2

from toycar_detection.image import load_image
from toycar_detection.detection import ObjectDetector
from toycar_detection.shape_detection import ShapeDetector
from toycar_detection.constants import HSV_BLUE, HSV_YELLOW


def main() -> None:
    frame = load_image("images/S__5980164.jpg")

    # Combine blue and yellow HSV ranges
    hsv_ranges = HSV_BLUE + HSV_YELLOW

    object_detector = ObjectDetector(
        hsv_ranges=hsv_ranges,
        min_contour_area=500,
    )

    shape_detector = ShapeDetector(
        min_contour_area=500,
        approximation_factor=0.04,
        circularity_threshold=0.80,
        solidity_threshold=0.75,
        ellipse_similarity_threshold=0.80,
        ellipse_error_threshold=0.15,
    )

    # HSV color detection
    result, mask, edges = object_detector.detect(frame)

    # Shape detection using combined HSV mask
    shape_result, shape_mask = shape_detector.detect(
        frame,
        mask=mask,
    )

    try:
        cv2.imshow("Original Image", frame)
        cv2.imshow("Object Detection", result)
        cv2.imshow("HSV Mask", mask)
        cv2.imshow("Canny Edges", edges)
        cv2.imshow("Shape Detection", shape_result)

        cv2.waitKey(0)

    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
