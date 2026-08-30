import streamlit as st

def load_custom_css():
    """
    Injects custom enterprise CSS styling into the Streamlit app session 
    to guarantee high-contrast visible typography and polished card backgrounds.
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
        
        /* Custom metric cards styling */
        div[data-testid="stMetric"] {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0;
            padding: 18px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        }
        
        div[data-testid="stMetric"] label {
            color: #64748b !important; /* Muted label */
        }

        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #0f172a !important; /* Bold value */
            font-weight: 700 !important;
        }
        
        /* Sidebar custom appearance */
        section[data-testid="stSidebar"] {
            background-color: #0f172a !important;
            color: #ffffff !important;
        }
        
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stSelectbox p,
        section[data-testid="stSidebar"] span {
            color: #f1f5f9 !important;
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
