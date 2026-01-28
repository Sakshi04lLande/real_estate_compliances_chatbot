import uuid
import streamlit as st

from core.storage import load_projects, save_projects
from core.extractor import extract_compliances
from core.planner import create_project_plan, summarize_progress


# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(
    page_title="Mumbai Compliance Assistant",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -----------------------------------------------------------
# GLOBAL CSS (dark theme + compact sidebar + white cards)
# -----------------------------------------------------------
st.markdown("""
<style>

html, body {
    background-color: #0F172A !important;
}
.main {
    background-color: #0F172A !important;
}

/* GLOBAL TEXT */
h1, h2, h3, h4 {
    color: #F1F5F9 !important;
    font-family: 'Inter', sans-serif;
}
p, label, span, div {
    font-family: 'Inter', sans-serif;
    color: #F1F5F9 !important;
}

/* ---------------- WHITE CARDS ---------------- */
.card {
    background: #FFFFFF !important;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #E2E8F0 !important;
    margin-bottom: 25px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.1);
}
.compact-card {
    background: #FFFFFF !important;
    padding: 10px 16px !important;
    border-radius: 10px !important;
    border: 1px solid #E2E8F0 !important;
    margin-bottom: 10px !important;
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.08);
}
.card *, .compact-card * {
    color: #111 !important;
    -webkit-text-fill-color: #111 !important;
}
.section-title {
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 6px;
    color: #111 !important;
}

/* ---------------- BADGES ---------------- */
.badge {
    padding: 3px 8px;
    font-size: 11px;
    border-radius: 8px;
    font-weight: 600;
    color: white !important;
    margin-right: 6px;
    display: inline-block;
}
.badge-blue   { background: #2563EB; }
.badge-green  { background: #059669; }
.badge-yellow { background: #D97706; }
.badge-gray   { background: #6B7280; }

/* ---------------- METRIC CARDS ---------------- */
.metric-card {
    background: #FFFFFF !important;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    text-align: center;
    box-shadow: 0 3px 8px rgba(15, 23, 42, 0.1);
}
.metric-value {
    font-size: 30px;
    font-weight: 700;
    color: #111 !important;
}
.metric-label {
    font-size: 13px;
    color: #374151 !important;
}
.metric-red {
    border-color: #ef4444 !important;
    background: #fee2e2 !important;
}
.metric-yellow {
    border-color: #f59e0b !important;
    background: #fef3c7 !important;
}
.metric-green {
    border-color: #10b981 !important;
    background: #d1fae5 !important;
}

/* RADIO INLINE */
.stRadio > div { flex-direction: row !important; }

/* --------------- SIDEBAR (compact & neat) --------------- */
section[data-testid="stSidebar"] {
    background-color: #1F2933 !important;
    padding-top: 16px;
}

.sidebar-title {
    color: #CBD5F5 !important;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 6px;
}

/* All sidebar buttons (secondary kind) */
section[data-testid="stSidebar"] button[kind="secondary"] {
    background-color: #2D3138 !important;
    color: #E5E7EB !important;
    border-radius: 8px !important;
    border: 1px solid #3F3F46 !important;
    padding: 4px 8px !important;
    font-size: 13px !important;
    margin-bottom: 4px !important;
}

/* Hover for project buttons */
section[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background-color: #3B3F47 !important;
}

/* Make delete buttons look like plain icons */
section[data-testid="stSidebar"] button[kind="secondary"] span:contains("🗑️") {
    padding: 0 !important;
}

/* Add New Project button */
section[data-testid="stSidebar"] button[kind="secondary"]:last-of-type {
    margin-top: 10px !important;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------
# SESSION LOAD
# -----------------------------------------------------------
if "projects" not in st.session_state:
    st.session_state.projects = load_projects()

if "current_project_id" not in st.session_state:
    st.session_state.current_project_id = None

projects = st.session_state.projects


# -----------------------------------------------------------
# SIDEBAR – functional & compact
# -----------------------------------------------------------
st.sidebar.markdown("<span class='sidebar-title'>Projects</span>", unsafe_allow_html=True)

if projects:
    for pid, proj in projects.items():
        col1, col2 = st.sidebar.columns([6, 1])

        # open project
        if col1.button(f"📁 {proj['name']}", key=f"open_{pid}"):
            st.session_state.current_project_id = pid
            st.rerun()

        # delete project
        if col2.button("🗑️", key=f"delete_{pid}"):
            del projects[pid]
            save_projects(projects)
            st.session_state.current_project_id = None
            st.rerun()
else:
    st.sidebar.write("No projects yet.")

st.sidebar.markdown("---")
if st.sidebar.button("➕ Add New Project"):
    st.session_state.current_project_id = None


# -----------------------------------------------------------
# MAIN HEADER
# -----------------------------------------------------------
st.title("🏗️ Mumbai Construction Compliance Assistant")
st.write(
    "<span style='color:#CBD5E1;'>AI system powered by DCPR 2034, Fire Act, NBC, MPCB, and BMC circulars.</span>",
    unsafe_allow_html=True
)


# -----------------------------------------------------------
# NEW PROJECT FORM
# -----------------------------------------------------------
if st.session_state.current_project_id is None:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">New Project Details</div>', unsafe_allow_html=True)

    project_name = st.text_input(
        "Project Name", 
        placeholder="e.g. Borivali Heights Residential Project"
    )
    description = st.text_area(
        "Project Description",
        placeholder="Describe building type, floors, plot area, location, usage, etc.",
        height=150
    )

    if st.button("🚀 Generate Compliance Checklist", use_container_width=True):
        if not project_name.strip():
            st.error("Please enter a project name.")
        elif not description.strip():
            st.error("Please enter a project description.")
        else:
            with st.spinner("Analyzing Mumbai regulations..."):
                compliances = extract_compliances(description)

            if not compliances:
                st.warning("AI could not extract compliances. Try adding more details.")
            else:
                pid = str(uuid.uuid4())
                project = create_project_plan(pid, project_name, description, compliances)
                projects[pid] = project
                save_projects(projects)
                st.session_state.current_project_id = pid
                st.success("Project created!")

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------
# EXISTING PROJECT VIEW
# -----------------------------------------------------------
else:
    project = projects[st.session_state.current_project_id]

    st.markdown(f"""
    <div class="card">
        <div class="section-title">{project['name']}</div>
        <p><b>📍 Location:</b> Mumbai</p>
        <p><b>📝 Description:</b> {project['description']}</p>
    </div>
    """, unsafe_allow_html=True)

    # metrics
    summary = summarize_progress(project)
    total = len(project["compliances"])
    completed = len(summary["completed"])
    in_progress = len(summary["in_progress"])
    pending = len(summary["pending"])

    values = {"completed": completed, "in_progress": in_progress, "pending": pending}
    sorted_vals = sorted(values.items(), key=lambda x: x[1], reverse=True)
    colors = {
        sorted_vals[0][0]: "metric-red",
        sorted_vals[1][0]: "metric-yellow",
        sorted_vals[2][0]: "metric-green"
    }

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(
        f"<div class='metric-card'><div class='metric-value'>{total}</div><div class='metric-label'>Total Compliances</div></div>",
        unsafe_allow_html=True
    )
    c2.markdown(
        f"<div class='metric-card {colors['completed']}'><div class='metric-value'>{completed}</div><div class='metric-label'>Completed</div></div>",
        unsafe_allow_html=True
    )
    c3.markdown(
        f"<div class='metric-card {colors['in_progress']}'><div class='metric-value'>{in_progress}</div><div class='metric-label'>In Progress</div></div>",
        unsafe_allow_html=True
    )
    c4.markdown(
        f"<div class='metric-card {colors['pending']}'><div class='metric-value'>{pending}</div><div class='metric-label'>Pending</div></div>",
        unsafe_allow_html=True
    )

    st.progress(completed / total if total else 0)

    # compliance list
    st.subheader("📄 Compliance Checklist (AI Generated)")

    stages = {
        "pre_construction": "Pre-Construction Approvals",
        "during_construction": "During Construction Requirements",
        "post_construction": "Post-Construction / Before Occupancy",
    }

    updated = []

    for stage, stage_label in stages.items():
        items = [c for c in project["compliances"] if c.get("stage") == stage]
        if not items:
            continue

        st.markdown(f"### {stage_label}")

        for idx, cdata in enumerate(items):
            st.markdown('<div class="compact-card">', unsafe_allow_html=True)

            st.markdown(f"<div class='section-title'>{cdata['name']}</div>", unsafe_allow_html=True)
            st.write(cdata.get("description", ""))

            st.markdown(f"""
                <span class="badge badge-blue">{cdata.get("stage")}</span>
                <span class="badge badge-yellow">{cdata.get("time_bound")}</span>
                <span class="badge badge-green">{cdata.get("document_required","")}</span>
                <span class="badge badge-gray">{cdata.get("source_hint","")}</span>
            """, unsafe_allow_html=True)

            status_key = f"{project['id']}_{stage}_{idx}"
            new_status = st.radio(
                "Status",
                ["Not Completed", "In Progress", "Completed"],
                index=["Not Completed", "In Progress", "Completed"].index(
                    cdata.get("status", "Not Completed")
                ),
                key=status_key,
                horizontal=True
            )

            cdata["status"] = new_status
            updated.append(cdata)

            st.markdown("</div>", unsafe_allow_html=True)

    project["compliances"] = updated
    projects[project["id"]] = project

    if st.button("💾 Save Progress"):
        save_projects(projects)
        st.success("Changes saved.")
