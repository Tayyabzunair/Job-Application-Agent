"""
Application Tracker.
Logs approved applications to a local JSON file so data persists
across server restarts. Simple and dependency-free (Phase 1 MVP).
"""
import json
import os
from datetime import datetime

TRACKER_FILE = "data/applications.json"


def _load_all() -> list[dict]:
    """Reads all logged applications from the JSON file."""
    if not os.path.exists(TRACKER_FILE):
        return []
    try:
        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        # File is empty or corrupted -> start fresh
        return []


def _save_all(applications: list[dict]) -> None:
    """Writes all applications back to the JSON file."""
    os.makedirs(os.path.dirname(TRACKER_FILE), exist_ok=True)
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(applications, f, indent=2, ensure_ascii=False)


def log_application(result: dict) -> dict:
    """
    Saves an approved application to the tracker.
    Stores a compact summary (not the full text) for quick tracking.
    """
    applications = _load_all()

    entry = {
        "result_id": result["result_id"],
        "role": result["role"],
        "seniority": result["seniority"],
        "match_score": result["match_score"],
        "ats_score": result["ats_score"],
        "status": "Applied",
        "applied_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    # Avoid duplicate entries for the same result_id
    applications = [a for a in applications if a["result_id"] != entry["result_id"]]
    applications.append(entry)

    _save_all(applications)
    return entry


def get_all_applications() -> list[dict]:
    """Returns all tracked applications."""
    return _load_all()
