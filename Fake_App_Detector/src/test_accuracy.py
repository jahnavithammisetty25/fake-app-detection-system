import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline import analyze_all
import os, json

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

apps = json.load(open(os.path.join(DATA_DIR, "apps.json")))
official = json.load(open(os.path.join(DATA_DIR, "official.json")))

results = analyze_all(
    os.path.join(DATA_DIR, "apps.json"),
    os.path.join(DATA_DIR, "official.json")
)

correct = 0
total = len(results)

for app, res in zip(apps, results):
    predicted_fake = (res["risk_level"] == "high")
    actual_fake = (app["label"] == "fake")

    if predicted_fake == actual_fake:
        correct += 1

print("Accuracy:", correct / total * 100, "%")
