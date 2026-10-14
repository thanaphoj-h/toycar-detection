# Common HSV Color Ranges

This project provides predefined HSV (Hue, Saturation, Value) color ranges
for color-based object detection using OpenCV.

The predefined color constants are located in:

`src/toycar_detection/constants/common_hsv_constants.py`

These ranges serve as initial thresholds for HSV-based color segmentation
and may require calibration depending on environmental conditions.

## 1. HSV Color Definitions

The HSV color model represents colors using three components:

- **Hue (H):** Represents the color type as an angle on the color wheel.
- **Saturation (S):** Represents the intensity or purity of a color.
- **Value (V):** Represents the brightness of a color.

The predefined HSV color ranges are divided into two categories:

1. **Chromatic Colors:** Eight color groups, including red, orange,
   yellow, green, cyan, blue, purple, and pink/magenta.
2. **Achromatic Colors:** Three neutral color groups, including
   white, black, and gray.

The following tables provide approximate HSV ranges in both
standard HSV and OpenCV representations.

### 1.1 Chromatic Colors

Chromatic colors are characterized by their hue, saturation,
and brightness.

**Table 1. HSV Color Ranges for Chromatic Colors**

| Color           | Hue (°)             | Saturation (%) | Value (%) | Hue <br/> (OpenCV) | Saturation <br/> (OpenCV) | Value <br/> (OpenCV) |
|-----------------|---------------------|----------------|-----------|--------------------|---------------------------|----------------------|
| 🔴 Red          | 0–20°<br/>340–360°  | 39.2–100%      | 39.2–100% | 0–10<br/>170–179   | 100–255                   | 100–255              |
| 🟠 Orange       | 22–40°              | 39.2–100%      | 39.2–100% | 11–20              | 100–255                   | 100–255              |
| 🟡 Yellow       | 42–70°              | 39.2–100%      | 39.2–100% | 21–35              | 100–255                   | 100–255              |
| 🟢 Green        | 72–170°             | 31.4–100%      | 31.4–100% | 36–85              | 80–255                    | 80–255               |
| 🩵 Cyan         | 172–198°            | 31.4–100%      | 31.4–100% | 86–99              | 80–255                    | 80–255               |
| 🔵 Blue         | 200–260°            | 31.4–100%      | 31.4–100% | 100–130            | 80–255                    | 80–255               |
| 🟣 Purple       | 262–310°            | 31.4–100%      | 31.4–100% | 131–155            | 80–255                    | 80–255               |
| 🩷 Pink/Magenta | 312–338°            | 31.4–100%      | 31.4–100% | 156–169            | 80–255                    | 80–255               |

**Note:** Red requires two separate hue ranges because hue is circular.
In OpenCV, red appears near both ends of the hue range.

The hue angle of 360° is equivalent to 0°.

### 1.2 Achromatic Colors

Achromatic colors are characterized primarily by saturation
and brightness rather than hue.

White, black, and gray are classified using saturation and
value thresholds.

**Table 2. HSV Color Ranges for Achromatic Colors**

| Color    | Hue (°) | Saturation (%) | Value (%)  | Hue (OpenCV) | Saturation (OpenCV) | Value (OpenCV) |
|----------|---------|----------------|------------|--------------|---------------------|----------------|
| ⚪ White | Any     | 0–15.7%        | 78.4–100%  | 0–179        | 0–40                | 200–255        |
| ⚫ Black | Any     | 0–100%         | 0–19.6%    | 0–179        | 0–255               | 0–50           |
| 🩶 Gray  | Any     | 0–15.7%        | 19.6–78.4% | 0–179        | 0–40                | 50–200         |

**Note:** The term "Any" indicates that hue is not restricted
when detecting achromatic colors.

When saturation is zero, hue becomes undefined because
the resulting color contains no chromatic information.

## 2. HSV Conversion

The standard HSV color model represents hue in degrees (0–360°),
while saturation and value are expressed as percentages (0–100%).

For 8-bit images, OpenCV represents HSV values using the following ranges:

| Component | Standard HSV | OpenCV HSV |
|-----------|--------------|------------|
| Hue (H) | 0–360° | 0–179 |
| Saturation (S) | 0–100% | 0–255 |
| Value (V) | 0–100% | 0–255 |

**Table 3. Comparison of Standard HSV and OpenCV HSV Representations**

### 2.1 Hue Conversion

Hue represents the angular position of a color on the color wheel.

The approximate conversion from standard HSV to OpenCV HSV is:

$$
H_{\text{OpenCV}} \approx \frac{H_{\text{Standard}}}{2}
$$

Where:

- $H_{\text{Standard}}$ is the standard hue angle in degrees.
- $H_{\text{OpenCV}}$ is the OpenCV hue value (0–179).

Since hue is circular, 360° is equivalent to 0°.

### 2.2 Saturation Conversion

Saturation represents the intensity or purity of a color.

The conversion from standard saturation (%) to OpenCV saturation is:

$$
S_{\text{OpenCV}} = \frac{S_{\text{Standard}}}{100} \times 255
$$

Where:

- $S_{\text{Standard}}$ is the standard saturation percentage (0–100%).
- $S_{\text{OpenCV}}$ is the OpenCV saturation value (0–255).

### 2.3 Value Conversion

Value represents the brightness of a color.

The conversion from standard value (%) to OpenCV value is:

$$
V_{\text{OpenCV}} = \frac{V_{\text{Standard}}}{100} \times 255
$$

Where:

- $V_{\text{Standard}}$ is the standard value percentage (0–100%).
- $V_{\text{OpenCV}}$ is the OpenCV value (0–255).

### 2.4 Conversion Example

Consider the following HSV color in the standard representation:

$$
HSV_{\text{Standard}} = (240^\circ, 80\%, 60\%)
$$

The corresponding OpenCV HSV values can be calculated as follows.

**Hue:**

$$
H_{\text{OpenCV}} = \frac{240}{2} = 120
$$

**Saturation:**

$$
S_{\text{OpenCV}} = \frac{80}{100} \times 255 = 204
$$

**Value:**

$$
V_{\text{OpenCV}} = \frac{60}{100} \times 255 = 153
$$

Therefore:

$$
\boxed{HSV_{\text{OpenCV}} = (120, 204, 153)}
$$

**Note:** OpenCV represents HSV values as integers for 8-bit images.
Quantization and rounding may introduce small differences
between standard HSV values and OpenCV HSV values.

## References

- [OpenCV Documentation](https://docs.opencv.org/4.x/)
- [OpenCV Color Conversions](https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html)
- [OpenCV Color Space Conversion](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html)
