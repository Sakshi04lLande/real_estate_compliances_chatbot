# core/storage.py

import json
import os
from typing import Dict, Any

PROJECTS_FILE = "projects.json"


def load_projects() -> Dict[str, Any]:
    if not os.path.exists(PROJECTS_FILE):
        return {}
    with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_projects(projects: Dict[str, Any]) -> None:
    with open(PROJECTS_FILE, "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)
