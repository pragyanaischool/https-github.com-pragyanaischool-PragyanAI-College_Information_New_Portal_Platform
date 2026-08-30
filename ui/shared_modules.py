import streamlit as st
from sqlalchemy.orm import Session
from services.analytics_service import AnalyticsService
from services.rag_service import RAGService

def render_universal_analytics_section(session: Session, persona_title: str):
    """
    Renders comprehensive interactive Plotly charts and metrics 
    for any stakeholder view in the portal.
    
    Args:
        session (Session): Active SQLAlchemy database session
        persona_title (str): Title describing the active stakeholder view
    """
    st.markdown("---")
    st.subheader(f"📊 Deep-Dive Analytics & Metrics: {persona_title}")
    
    col1, col2 = st.columns(2)
    with col1:
        fig_placement = AnalyticsService.get_placement_trend_chart(session)
        st.plotly_chart(fig_placement, use_container_width=True)
        
    with col2:
        fig_cgpa = AnalyticsService.get_student_cgpa_distribution(session)
        st.plotly_chart(fig_cgpa, use_container_width=True)
        
    col3, col4 = st.columns(2)
    with col3:
        fig_sector = AnalyticsService.get_company_sector_breakdown(session)
        st.plotly_chart(fig_sector, use_container_width=True)
    with col4:
        st.info(
            "💡 **Live Telemetry Insight:** All charts update dynamically in real time "
            "as new students, colleges, or placement records are ingested via CSV, PDF OCR, or manual forms."
        )


def render_universal_rag_chat_section(session: Session, unique_key: str, persona_title: str):
    """
    Renders a universal RAG conversational chat box with scoped keys 
    for deep stakeholder questions and relational database queries.
    
    Args:
        session (Session): Active SQLAlchemy database session
        unique_key (str): Unique scope identifier string to prevent ID collisions
        persona_title (str): Active persona title for context-aware responses
    """
    st.markdown("---")
    st.subheader(f"🤖 PragyanAI RAG Intelligence Assistant ({persona_title})")
    
    chat_key = f"messages_univ_{unique_key}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = [
            {
                "role": "assistant", 
                "content": f"Hello! I am your AI decision advisor tailored for the **{persona_title}** role. Ask me anything about institutional data, cutoffs, placements, or RAG insights."
            }
        ]
        
    for msg in st.session_state[chat_key]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    user_input = st.chat_input("Ask a deep question or query database telemetry...", key=f"input_univ_{unique_key}")
    
    if user_input:
        st.session_state[chat_key].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        # Retrieve context-aware intelligence response via RAG service
        response_text = RAGService.query_knowledge_base(session, user_input, persona_title)
        
        st.session_state[chat_key].append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)
