import streamlit as st
from config.settings import ensure_directories
from config.styles import load_custom_css
from database.session import SessionLocal, init_db
from services.seed_service import run_database_seed
from ui.auth_sidebar import render_auth_sidebar

# Import view modules
from views import (
    "1_Aspirant_Desk",
    "2_College_Management",
    "3_Recruiter_Hub",
    "4_School_Partner",
    "5_Admin_Governance",
    "6_Data_Ingestion"
)

# 1. Page Configuration
st.set_page_config(
    page_title="PragyanAI College Intelligence Portal",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Initialize Runtime Directories & Database Schema
ensure_directories()
init_db()

# 3. Boot Automatic Synthetic Database Seeding on First Launch
session = SessionLocal()
try:
    run_database_seed(session)
finally:
    session.close()

# 4. Load Custom Enterprise CSS Styles
load_custom_css()

# 5. Render RBAC Authentication Sidebar & Retrieve Active Role
active_role = render_auth_sidebar()

# 6. Main View Routing Engine
st.sidebar.markdown("---")
st.sidebar.markdown("### Workspace Navigation")

# Role-based default mapping or manual selection
view_options = {
    "Student / Parent (Aspirant)": "1. Aspirant Desk",
    "Engineering College Management": "2. College Management",
    "Corporate Recruiter / HR": "3. Recruiter Hub",
    "High School / PU Partner": "4. School Partner",
    "Administrator / Leadership": "5. Admin Governance"
}

navigation_choice = st.sidebar.radio(
    "Select Portal View",
    [
        "1. Aspirant & Parent Desk",
        "2. College Management",
        "3. Recruiter Hub",
        "4. School Partner",
        "5. Admin & Governance",
        "6. Data Ingestion Portal"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### PragyanAI Ecosystem")
st.sidebar.caption("v4.2.0 Enterprise | Powered by SQLite & ChromaDB RAG Engine")

# Route to respective view module based on user selection
if "1. Aspirant" in navigation_choice:
    "1_Aspirant_Desk".render_aspirant_desk()

elif "2. College Management" in navigation_choice:
    # Enforce role check for administrative/management views
    if active_role not in ["college_management", "admin"]:
        st.warning(" **Restricted Access:** Please switch your session role in the sidebar to 'Engineering College Management' or 'Administrator' to unlock this workspace.")
    else:
        "2_College_Management".render_college_management_view()

elif "3. Recruiter Hub" in navigation_choice:
    if active_role not in ["recruiter", "admin"]:
        st.warning(" **Restricted Access:** Please switch your session role in the sidebar to 'Corporate Recruiter / HR' to unlock this workspace.")
    else:
        "3_Recruiter_Hub".render_recruiter_hub()

elif "4. School Partner" in navigation_choice:
    if active_role not in ["school_partner", "admin"]:
        st.warning(" **Restricted Access:** Please switch your session role in the sidebar to 'High School / PU Partner' to unlock this workspace.")
    else:
        "4_School_Partner".render_school_partner_view()

elif "5. Admin & Governance" in navigation_choice:
    if active_role != "admin":
        st.error(" **Access Denied:** Administrator credentials required to access system governance and master CRUD controls.")
    else:
        "5_Admin_Governance".render_admin_governance_view()

elif "6. Data Ingestion" in navigation_choice:
    "6_Data_Ingestion".render_data_ingestion_view()
