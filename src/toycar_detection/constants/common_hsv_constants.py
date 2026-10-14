"""
Common HSV color range constants for OpenCV-based color detection.

HSV ranges (8-bit OpenCV):
    Hue (H):        0–179
    Saturation (S): 0–255
    Value (V):      0–255

Each color is defined as a tuple of one or more HSV ranges.
Each range contains a lower and an upper HSV bound.

The predefined ranges are approximate thresholds and may require
calibration depending on lighting conditions and camera settings.

Reference:
    docs/common-hsv-color-ranges.md
"""


# =============================================================================
# Chromatic Colors
# =============================================================================

# Red
HSV_RED = (
    ((0, 100, 100), (10, 255, 255)),
    ((170, 100, 100), (179, 255, 255)),
)

# Orange
HSV_ORANGE = (
    ((11, 100, 100), (20, 255, 255)),
)

# Yellow
HSV_YELLOW = (
    ((21, 100, 100), (35, 255, 255)),
)

# Green
HSV_GREEN = (
    ((36, 80, 80), (85, 255, 255)),
)

# Cyan
HSV_CYAN = (
    ((86, 80, 80), (99, 255, 255)),
)

# Blue
HSV_BLUE = (
    ((100, 80, 80), (130, 255, 255)),
)

# Purple
HSV_PURPLE = (
    ((131, 80, 80), (155, 255, 255)),
)

# Pink / Magenta
HSV_PINK = (
    ((156, 80, 80), (169, 255, 255)),
)


# =============================================================================
# Achromatic Colors
# =============================================================================

# White
HSV_WHITE = (
    ((0, 0, 200), (179, 40, 255)),
)

# Black
HSV_BLACK = (
    ((0, 0, 0), (179, 255, 50)),
)

# Gray
HSV_GRAY = (
    ((0, 0, 50), (179, 40, 200)),
)
