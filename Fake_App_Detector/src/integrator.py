# src/integrator.py

from src.pipeline import run_detection

def run_for_brand(brand_name):
    """
    Integrator that connects the UI to Person B's pipeline.
    Takes a brand name and returns scored detection results.
    """
    return run_detection(brand_name)
