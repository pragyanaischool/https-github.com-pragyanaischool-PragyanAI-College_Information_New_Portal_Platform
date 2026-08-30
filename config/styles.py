import streamlit as st

def load_custom_css():
    """
    Injects custom enterprise CSS styling into the Streamlit app session 
    to refine typography, component shadows, sidebar themes, and card layouts.
    """
    st.markdown("""
        <style>
        /* Global app background and font settings */
        .stApp {
            background-color: #f8fafc;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #0f172a;
        }
        
        /* Custom metric cards styling */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            padding: 18px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
            transition: all 0.2s ease-in-out;
        }
        
        div[data-testid="stMetric"]:hover {
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            border-color: #cbd5e1;
        }
        
        /* Sidebar custom appearance */
        section[data-testid="stSidebar"] {
            background-color: #0f172a;
            color: #ffffff;
        }
        
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stSelectbox p {
            color: #f1f5f9 !important;
        }
        
        /* Expander styling */
        div.streamlit-expanderHeader {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            font-weight: 600;
            color: #1e293b;
        }
        
        /* Button primary styling tweaks */
        div.stButton > button:first-child {
            background-color: #2563eb;
            color: white;
            font-weight: 600;
            border-radius: 6px;
            border: none;
            padding: 0.5rem 1rem;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        }
        
        div.stButton > button:first-child:hover {
            background-color: #1d4ed8;
        }
        </style>
    """, unsafe_allow_html=True)
