"""
Image-based color and geometric shape detection.

Detects blue and yellow objects using HSV segmentation
and classifies triangles, squares, circles, and ovals.
"""

import cv2

from toycar_detection.camera import Camera


def main() -> None:
    try:
        with Camera() as camera:
            while camera.is_opened():
                frame = camera.read()

                cv2.imshow("Original", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
