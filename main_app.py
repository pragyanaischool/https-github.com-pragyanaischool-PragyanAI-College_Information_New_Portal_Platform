import importlib
import os
import streamlit as st
from config.settings import ensure_directories
from config.styles import load_custom_css
from database.session import SessionLocal, init_db
from services.auth_seed_service import seed_users_and_demo_data
from ui.auth_sidebar import render_auth_sidebar

# Dynamically import view modules to safely handle numeric and emoji filenames
aspirant_desk = importlib.import_module("views.1_Aspirant_Desk")
college_management = importlib.import_module("views.2_College_Management")
recruiter_hub = importlib.import_module("views.3_Recruiter_Hub")
school_partner = importlib.import_module("views.4_School_Partner")
admin_governance = importlib.import_module("views.5_Admin_Governance")
data_ingestion = importlib.import_module("views.6_Data_Ingestion")

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

# 3. Boot Automatic DB Seeding (Users, Colleges, Students, Companies & Telemetry)
session = SessionLocal()
try:
    seed_users_and_demo_data(session)
finally:
    session.close()

# 4. Load Custom Enterprise CSS Styles & High-Contrast Typography
load_custom_css()

# 5. Global PragyanAI Logo Integration in Sidebar
logo_path = "assets/PragyanAI_Transperent.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.title(" PragyanAI Hub")

st.sidebar.markdown("---")

# 6. Render Authentication Sidebar & Retrieve Active Role & Username
session = SessionLocal()
active_role, username = render_auth_sidebar(session)
session.close()

# 7. Main Navigation & Workspace Enforcement Based on Logged-in User Role
st.sidebar.markdown("---")
st.sidebar.markdown("###  Role-Based Workspace")

if not active_role:
    st.markdown("""
        ##  Welcome to the PragyanAI College Intelligence Platform
        
        **Grow with Gyan** — Empowering educational institutions, students, recruiters, and academic partners with advanced **Groq, LangGraph, and ChromaDB Agentic RAG** technology.
        
        👉 **Please log in or create an account using the sidebar to unlock your customized workspace:**
        -  **Student / Parent (Aspirant) Desk:** Explore cutoff ranks, placement metrics, and ask the AI Assistant.
        -  **Engineering College Management:** Manage intake, add students, and track deep analytics.
        -  **Corporate Recruiter Hub:** Benchmark campuses, review verified talent stacks, and post drives.
        -  **High School / Partner Portal:** Request K-12 AI/Robotics workshops and view articulation programs.
        -  **System Administrator:** Oversee complete multi-tenant governance and database entities.
    """)
    st.stop()

# Build navigation options filtered strictly by user role permissions
allowed_views = []
if active_role == "aspirant":
    allowed_views = ["1. Aspirant & Parent Desk"]
elif active_role == "college_management":
    allowed_views = ["2. College Management", "6. Data Ingestion Portal"]
elif active_role == "recruiter":
    allowed_views = ["3. Recruiter Hub", "6. Data Ingestion Portal"]
elif active_role == "school_partner":
    allowed_views = ["4. School Partner"]
elif active_role == "admin":
    allowed_views = [
        "1. Aspirant & Parent Desk",
        "2. College Management",
        "3. Recruiter Hub",
        "4. School Partner",
        "5. Admin & Governance",
        "6. Data Ingestion Portal"
    ]

navigation_choice = st.sidebar.radio("Select Authorized Workspace", allowed_views)

st.sidebar.markdown("---")
st.sidebar.markdown("###  PragyanAI Ecosystem")
st.sidebar.caption("v4.5.0 Enterprise | Powered by Groq, LangGraph & ChromaDB")

# 8. Route to Respective View Module Based on Authorized Selection
session = SessionLocal()
try:
    if "1. Aspirant" in navigation_choice:
        aspirant_desk.render_aspirant_desk()
    elif "2. College Management" in navigation_choice:
        college_management.render_college_management_view()
    elif "3. Recruiter Hub" in navigation_choice:
        recruiter_hub.render_recruiter_hub()
    elif "4. School Partner" in navigation_choice:
        school_partner.render_school_partner_view()
    elif "5. Admin & Governance" in navigation_choice:
        admin_governance.render_admin_governance_view()
    elif "6. Data Ingestion" in navigation_choice:
        data_ingestion.render_data_ingestion_view()
finally:
    session.close()
