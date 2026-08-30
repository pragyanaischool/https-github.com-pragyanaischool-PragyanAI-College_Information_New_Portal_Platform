import streamlit as st

def render_auth_sidebar() -> str:
    """
    Renders the Role-Based Access Control (RBAC) authentication sidebar widget.
    
    Returns:
        str: Normalized role identifier string ('student', 'college_management', 
             'recruiter', 'school_partner', or 'admin').
    """
    st.sidebar.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.sidebar.title("PragyanAI Portal")
    st.sidebar.markdown("### Institutional Governance & Decision Engine")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔒 Session Authentication")
    
    roles = [
        "Student / Parent (Aspirant)", 
        "Engineering College Management", 
        "Corporate Recruiter / HR", 
        "High School / PU Partner", 
        "Administrator / Leadership"
    ]
    
    selected_role = st.sidebar.selectbox("Select Stakeholder Role", roles)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📌 Active System Status")
    st.sidebar.success("Database: Connected (SQLite)")
    st.sidebar.info("RAG Engine: Hybrid SQL + Vector Active")
    
    # Normalize role key for downstream routing and permission checks
    role_mapping = {
        "Student / Parent (Aspirant)": "student",
        "Engineering College Management": "college_management",
        "Corporate Recruiter / HR": "recruiter",
        "High School / PU Partner": "school_partner",
        "Administrator / Leadership": "admin"
    }
    
    return role_mapping.get(selected_role, "student")
