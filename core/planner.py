# core/planner.py

from typing import Dict, Any, List


def create_project_plan(
    project_id: str, name: str, description: str, compliances: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Attach default status fields to each compliance."""
    enriched = []
    for c in compliances:
        c = dict(c)  # copy
        c.setdefault("stage", "pre_construction")
        c.setdefault("time_bound", "as_applicable")
        c.setdefault("document_required", "")
        c.setdefault("source_hint", "")
        c["status"] = "Not Completed"
        enriched.append(c)

    return {
        "id": project_id,
        "name": name,
        "description": description,
        "location": "Mumbai",
        "compliances": enriched,
    }


def human_time_bound(tb: str) -> str:
    mapping = {
        "before_start": "Must be completed before starting construction.",
        "during_construction": "Must be followed during the entire construction phase.",
        "monthly": "Requires monthly compliance during construction.",
        "before_occupancy": "Must be completed before applying for Occupation Certificate.",
        "as_applicable": "Timing depends on project-specific approvals.",
    }
    return mapping.get(tb, "Timing depends on relevant authority / rule.")


def summarize_progress(project: Dict[str, Any]):
    completed = []
    pending = []
    in_progress = []

    for c in project.get("compliances", []):
        s = c.get("status", "Not Completed")
        if s == "Completed":
            completed.append(c["name"])
        elif s == "In Progress":
            in_progress.append(c["name"])
        else:
            pending.append(c["name"])

    return {
        "completed": completed,
        "pending": pending,
        "in_progress": in_progress,
    }
