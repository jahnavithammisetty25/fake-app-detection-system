# src/utils.py
import json
import os
from PIL import Image
import imagehash

def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def load_icon(path):
    if not os.path.isabs(path):
        # path relative to project data/icons
        base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "icons")
        path = os.path.join(base, path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Icon not found: {path}")
    return Image.open(path).convert("RGB")

def phash_score(icon_path_a, icon_path_b):
    """Return similarity score in [0,100] for two icon paths using phash."""
    try:
        img_a = load_icon(icon_path_a)
        img_b = load_icon(icon_path_b)
        h1 = imagehash.phash(img_a)
        h2 = imagehash.phash(img_b)
        # hash difference (Hamming); convert to percentage similarity
        # max distance depends on hash size (default 64-bit => max distance 64)
        max_bits = max(h1.hash.size, h2.hash.size)
        dist = (h1 - h2)
        similarity = max(0.0, 100.0 * (1 - (dist / max_bits)))
        return round(similarity, 2)
    except Exception as e:
        # if anything fails, return 0 similarity
        return 0.0
