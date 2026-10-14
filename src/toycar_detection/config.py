# src/toycar_detection/config.py

"""
Configuration module for Toy Car Detection
"""

import os
from dotenv import load_dotenv

load_dotenv()

CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", "0"))
FRAME_WIDTH = int(os.getenv("FRAME_WIDTH", "640"))
FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT", "360"))
FPS = int(os.getenv("FPS", "24"))
