# src/features.py
from rapidfuzz import fuzz
from .utils import phash_score

def name_similarity(app_name, official_name):
    """
    Return similarity [0,100] using token_set_ratio then fallback to simple ratio.
    """
    if not app_name or not official_name:
        return 0.0
    try:
        score = fuzz.token_set_ratio(app_name, official_name)
        return float(score)
    except Exception:
        return float(fuzz.ratio(app_name, official_name))

def package_similarity(pkg_a, pkg_b):
    """
    Package names are usually reverse domain strings.
    We'll use a token-based ratio: if equal → 100.
    """
    if not pkg_a or not pkg_b:
        return 0.0
    try:
        return float(fuzz.ratio(pkg_a, pkg_b))
    except Exception:
        return 0.0

def publisher_mismatch(developer_name, official_developer_name):
    """
    Simple check:
     - returns 100 if exact mismatch (suspicious),
     - returns 0 if match,
     - intermediate values if similar.
    """
    if not developer_name or not official_developer_name:
        return 50.0  # unknown -> suspicious-ish
    try:
        sim = fuzz.token_set_ratio(developer_name, official_developer_name)
        # invert similarity into mismatch score: higher => more mismatch
        mismatch = max(0.0, 100.0 - float(sim))
        return round(mismatch, 2)
    except Exception:
        return 100.0
