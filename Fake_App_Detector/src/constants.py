# src/constants.py
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT, "data")
ICONS_DIR = os.path.join(DATA_DIR, "icons")

# scoring weights (adjustable)
WEIGHT_NAME = 0.4
WEIGHT_ICON = 0.35
WEIGHT_PACKAGE = 0.15
WEIGHT_PUBLISHER = 0.10

# risk thresholds
THRESHOLD_HIGH = 80
THRESHOLD_MEDIUM = 60
