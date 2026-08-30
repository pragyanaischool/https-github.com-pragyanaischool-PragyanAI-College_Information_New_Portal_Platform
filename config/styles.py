import streamlit as st

def load_custom_css():
    """
    Injects custom enterprise CSS styling into the Streamlit app session 
    to guarantee high-contrast visible typography, background styling, 
    and clear sidebar text visibility.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Global app background and font settings */
        .stApp {
            background-color: #f8fafc;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #0f172a !important;
        }

        /* Force visibility on markdown, text blocks, and labels */
        p, span, label, div, h1, h2, h3, h4, h5, h6 {
            color: #0f172a;
            font-family: 'Inter', sans-serif;
        }

        /* Explicitly style file uploader / drop box container & text visibility */
        [data-testid="stFileUploader"] {
            background-color: #0f172a !important;
            border: 2px dashed #eab308 !important;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        [data-testid="stFileUploader"] section {
            background-color: #0f172a !important;
        }

        [data-testid="stFileUploader"] section div,
        [data-testid="stFileUploader"] span,
        [data-testid="stFileUploader"] label,
        [data-testid="stFileUploader"] small {
            color: #facc15 !important;
            font-weight: 600 !important;
        }

        [data-testid="stFileUploader"] button {
            background-color: #ef4444 !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            border: none !important;
        }
        
        /* Sidebar container styling & forcing all internal text visible */
        section[data-testid="stSidebar"] {
            background-color: #0f172a !important;
            color: #ffffff !important;
        }
        
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stRadio div,
        section[data-testid="stSidebar"] .stSelectbox p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] small,
        section[data-testid="stSidebar"] caption {
            color: #f1f5f9 !important;
        }

        /* Sidebar radio item text specifically */
        section[data-testid="stSidebar"] div[role="radiogroup"] label p {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        /* Custom metric cards styling */
        div[data-testid="stMetric"] {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0;
            padding: 18px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        }
        
        div[data-testid="stMetric"] label {
            color: #64748b !important;
        }

        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #0f172a !important;
            font-weight: 700 !important;
        }
        
        /* Expander styling */
        div.streamlit-expanderHeader {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            font-weight: 600;
            color: #1e293b !important;
        }
        
        /* Primary buttons */
        div.stButton > button:first-child {
            background-color: #2563eb;
            color: white !important;
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
