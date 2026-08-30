import hashlib
import streamlit as st
from sqlalchemy.orm import Session
from database.models import User

def render_auth_sidebar(session: Session) -> tuple:
    """
    Renders secure authentication sidebar supporting user login and account signup,
    persisting credentials and roles securely in the SQLite database and displaying 
    convenient test credentials for immediate evaluation.
    
    Args:
        session (Session): Active SQLAlchemy database session
        
    Returns:
        tuple: (active_role, logged_in_username)
    """
    
    # 1. Initialize Authentication Session State variables if absent
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.full_name = None

    # 2. Render Login or User Session Status
    if not st.session_state.authenticated:
        st.sidebar.markdown("### 🔐 PragyanAI Authentication Hub")
        
        # Display Visible Test Credentials for Quick Testing
        with st.sidebar.expander("📌 Quick Test Credentials", expanded=True):
            st.markdown("""
                **Student/Aspirant:** `aspirant1` / `password123`  
                **College Admin:** `college_admin` / `password123`  
                **Recruiter:** `recruiter_hr` / `password123`  
                **School Partner:** `school_principal` / `password123`  
                **Admin:** `admin` / `admin123`
            """)

        auth_tab1, auth_tab2 = st.sidebar.tabs(["🔑 Login", "📝 Create Account"])

        with auth_tab1:
            with st.form("login_form"):
                username_input = st.text_input("Username")
                password_input = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Secure Login", use_container_width=True)

                if submit_login:
                    if not username_input or not password_input:
                        st.error("Please enter both username and password.")
                    else:
                        hashed_pwd = hashlib.sha256(password_input.encode()).hexdigest()
                        user = session.query(User).filter_by(username=username_input, password_hash=hashed_pwd).first()
                        
                        if user:
                            st.session_state.authenticated = True
                            st.session_state.username = user.username
                            st.session_state.role = user.role
                            st.session_state.full_name = user.full_name
                            st.success(f"Welcome back, {user.full_name}!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")

        with auth_tab2:
            with st.form("signup_form"):
                st.markdown("##### Register New Account")
                new_user = st.text_input("Choose Username")
                new_name = st.text_input("Full Name")
                new_email = st.text_input("Email Address")
                new_pwd = st.text_input("Choose Password", type="password")
                
                role_selection = st.selectbox(
                    "Select Stakeholder Role",
                    [
                        ("Student / Parent (Aspirant)", "aspirant"),
                        ("Engineering College Management", "college_management"),
                        ("Corporate Recruiter / HR", "recruiter"),
                        ("High School / PU Partner", "school_partner"),
                        ("System Administrator", "admin")
                    ],
                    format_func=lambda x: x[0]
                )
                
                submit_signup = st.form_submit_button("Create Account & Store", use_container_width=True)

                if submit_signup:
                    existing_user = session.query(User).filter(
                        (User.username == new_user) | (User.email == new_email)
                    ).first()
                    
                    if existing_user:
                        st.error("Username or email already exists in database.")
                    elif not new_user or not new_pwd or not new_name or not new_email:
                        st.error("All mandatory fields must be filled.")
                    else:
                        hashed = hashlib.sha256(new_pwd.encode()).hexdigest()
                        new_account = User(
                            username=new_user,
                            password_hash=hashed,
                            role=role_selection[1],
                            full_name=new_name,
                            email=new_email
                        )
                        session.add(new_account)
                        session.commit()
                        st.success("Account created successfully! Switch to the Login tab to sign in.")
        
        return None, None
    else:
        # User is authenticated: Display profile details and Logout button
        st.sidebar.markdown("### 👤 Active User Session")
        st.sidebar.success(f"**{st.session_state.full_name}**")
        st.sidebar.caption(f"Role: `{st.session_state.role.upper()}`")
        st.sidebar.caption(f"Username: @{st.session_state.username}")
        
        if st.sidebar.button("🚪 Terminate Session (Logout)", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.role = None
            st.session_state.full_name = None
            st.rerun()
            
        return st.session_state.role, st.session_state.username
