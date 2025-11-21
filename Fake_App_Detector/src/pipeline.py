# src/pipeline.py
import os
import argparse
from .utils import read_json
from .features import name_similarity, package_similarity, publisher_mismatch
from .utils import phash_score
from .constants import (
    WEIGHT_NAME,
    WEIGHT_ICON,
    WEIGHT_PACKAGE,
    WEIGHT_PUBLISHER,
    DATA_DIR,
    THRESHOLD_HIGH,
    THRESHOLD_MEDIUM,
)



def compute_risk_for_app(app, official_record):
    """
    app: dict with keys: name, package, developer, icon
    official_record: dict for target brand: name, package, developer, icon
    returns: dict { risk, breakdown }
    """
    name_sim = name_similarity(app.get("name", ""), official_record.get("name", ""))
    pkg_sim = package_similarity(app.get("package", ""), official_record.get("package", ""))
    icon_sim = phash_score(app.get("icon", ""), official_record.get("icon", ""))
    pub_mismatch = publisher_mismatch(app.get("developer", ""), official_record.get("developer", ""))

    # normalize publisher mismatch to 0..100 (we already produce 0..100)
    # Compose risk: higher similarity of name/icon increases risk, publisher mismatch increases risk
    # Note: name/icon similarity are positive indicators; publisher_mismatch is already inverted (higher -> worse)
    score = (
        WEIGHT_NAME * name_sim +
        WEIGHT_ICON * icon_sim +
        WEIGHT_PACKAGE * (100 - pkg_sim) +  # if package is similar → less suspicious, so invert
        WEIGHT_PUBLISHER * pub_mismatch
    )
    # clamp
    score = max(0.0, min(100.0, score))
    breakdown = {
        "name_similarity": round(name_sim, 2),
        "icon_similarity": round(icon_sim, 2),
        "package_similarity": round(pkg_sim, 2),
        "publisher_mismatch": round(pub_mismatch, 2),
    }
    return {"risk": round(score, 2), "breakdown": breakdown}

def risk_level(score):
    if score >= THRESHOLD_HIGH:
        return "high"
    if score >= THRESHOLD_MEDIUM:
        return "medium"
    return "low"

def analyze_all(apps_path, official_path, target_brand=None):
    apps = read_json(apps_path)
    official = read_json(official_path)

    results = []
    for app in apps:
        # choose which official brand to compare against:
        brand_key = target_brand or app.get("brand") or app.get("target_brand")
        if brand_key and brand_key in official:
            off = official[brand_key]
        else:
            # fallback: try to find closest official brand by name
            # simple heuristic: compare app name to all official names and pick highest
            best_brand = None
            best_score = -1
            for k, v in official.items():
                s = name_similarity(app.get("name", ""), v.get("name", ""))
                if s > best_score:
                    best_score = s
                    best_brand = k
            off = official[best_brand] if best_brand else list(official.values())[0]

        res = compute_risk_for_app(app, off)
        res_record = {
            "app_name": app.get("name"),
            "package": app.get("package"),
            "developer": app.get("developer"),
            "brand_checked": off.get("name"),
            "risk": res["risk"],
            "risk_level": risk_level(res["risk"]),
            "breakdown": res["breakdown"],
        }
        # add human-readable reasons
        reasons = []
        b = res["breakdown"]
        # -------- Enhanced Human-Readable Explanation -------- #

# Name Similarity
        if b["name_similarity"] >= 75:
            reasons.append(f"High name similarity ({b['name_similarity']}%). The app name closely matches the official one.")
        elif b["name_similarity"] >= 40:
            reasons.append(f"Moderate name similarity ({b['name_similarity']}%). The names share some common patterns.")
        else:
            reasons.append(f"Low name similarity ({b['name_similarity']}%). The name does not resemble the official brand.")

# Icon Similarity
        if b["icon_similarity"] >= 70:
            reasons.append(f"High icon similarity ({b['icon_similarity']}%). The icon visually resembles the official app icon.")
        elif b["icon_similarity"] >= 40:
            reasons.append(f"Moderate icon similarity ({b['icon_similarity']}%). Some visual resemblance detected.")
        else:
            reasons.append(f"Low icon similarity ({b['icon_similarity']}%). The icon does not match the official branding.")

# Package Similarity
        if b["package_similarity"] >= 85:
            reasons.append(f"Package name very similar ({b['package_similarity']}%). The reverse-domain package pattern is close to the official one.")
        elif b["package_similarity"] >= 40:
            reasons.append(f"Package name moderately similar ({b['package_similarity']}%). Some components match the official package.")
        else:
            reasons.append(f"Package name different ({b['package_similarity']}%). The package format does not match the official structure.")

# Publisher Mismatch
        if b["publisher_mismatch"] >= 80:
            reasons.append(f"Publisher completely different ({b['publisher_mismatch']}%). Strong indication the app is not official.")
        elif b["publisher_mismatch"] >= 50:
            reasons.append(f"Publisher mismatch ({b['publisher_mismatch']}%). Developer does not match the official publisher.")
        else:
            reasons.append("Publisher matches the official developer.")

# Final interpretation (based on risk_level)
        if res_record["risk_level"] == "high":
            reasons.append("⚠️ High Risk: Strong resemblance + publisher mismatch increases suspicion.")
        elif res_record["risk_level"] == "medium":
            reasons.append("ℹ️ Medium Risk: Some similarity detected, but not enough to classify as highly suspicious.")
        else:
            reasons.append("✔️ Low Risk: App does not resemble the official brand closely.")

        res_record["reasons"] = reasons
        results.append(res_record)
    return results

def run_detection(brand):
    """
    Simplified wrapper for Streamlit UI.
    Loads apps.json and official.json and returns analysis results ONLY for the given brand.
    """
    apps_path = os.path.join(DATA_DIR, "apps.json")
    official_path = os.path.join(DATA_DIR, "official.json")

    all_results = analyze_all(apps_path, official_path, target_brand=brand)

    # Filter results: only apps that belong to this brand or target brand
    filtered = [r for r in all_results if r.get("brand_checked", "").lower() == brand.lower()]

    # If no filtered apps match, return everything (just in case)
    return filtered if filtered else all_results

def main():
    parser = argparse.ArgumentParser(description="Fake App Detection Pipeline")
    parser.add_argument("--apps", default=os.path.join(DATA_DIR, "apps.json"), help="path to apps.json")
    parser.add_argument("--official", default=os.path.join(DATA_DIR, "official.json"), help="path to official.json")
    parser.add_argument("--brand", default=None, help="(optional) force brand to check against (key from official.json)")
    args = parser.parse_args()

    results = analyze_all(args.apps, args.official, target_brand=args.brand)
    import json, sys
    json.dump(results, sys.stdout, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
