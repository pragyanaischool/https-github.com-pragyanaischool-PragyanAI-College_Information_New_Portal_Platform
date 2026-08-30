import streamlit as st

def render_metric_card(label: str, value: str, delta: str = None):
    """
    Renders a clean, enterprise-styled metric display card with a subtle box-shadow and border.
    
    Args:
        label (str): The descriptive title or metric label.
        value (str): The primary numerical or textual metric value.
        delta (str, optional): Secondary growth or benchmark indicator (e.g., '+14% this week').
    """
    delta_html = f"<span style='color: #10b981; font-size: 0.85rem; font-weight: 600;'>{delta}</span>" if delta else ""
    st.markdown(f"""
        <div style="background-color: #ffffff; padding: 18px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.03); border: 1px solid #e2e8f0; margin-bottom: 10px;">
            <p style="color: #64748b; font-size: 0.75rem; text-transform: uppercase; font-weight: 700; margin-bottom: 4px;">{label}</p>
            <h3 style="color: #0f172a; font-size: 1.5rem; font-weight: 800; margin: 0;">{value}</h3>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def render_status_badge(status_text: str, status_type: str = "success"):
    """
    Renders a color-coded status indicator badge for leads, requests, or verification states.
    
    Args:
        status_text (str): The label displayed inside the badge.
        status_type (str): The semantic type ('success' for green, 'info' for executive blue).
    """
    color = "#10b981" if status_type == "success" else "#2563eb"
    st.markdown(f"""
        <span style="background-color: {color}15; color: {color}; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;">
            ● {status_text}
        </span>
    """, unsafe_allow_html=True)
