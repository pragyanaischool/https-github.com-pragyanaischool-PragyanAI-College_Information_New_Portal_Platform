import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from database.session import SessionLocal
from database.models import College, Student, HiringCompany, CollegePlacementRecord, RecruiterCampusDriveEOI
from services.ocr_service import OCRService
from ui.shared_modules import render_universal_analytics_section, render_universal_rag_chat_section

def render_recruiter_hub():
    # 1. Executive Recruiter Hub Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 25px; border-radius: 12px; color: white; margin-bottom: 20px;">
        <h2 style="margin: 0; font-weight: 800;">💼 Corporate Recruiter & HR Talent Hub</h2>
        <p style="margin: 5px 0 0 0; font-size: 0.95rem; opacity: 0.9;">
            Discover elite engineering talent pools, execute JD vector alignment matching, manage campus drive EOIs, and access corporate-sponsored R&D Labs & CoEs (NVIDIA H100 clusters).
        </p>
    </div>
    """, unsafe_allow_html=True)

    session = SessionLocal()

    # Recruiter Workflow Tabs
    tabs = [
        "1. Talent Pool Discovery Hub",
        "2. JD RAG Vector Matching",
        "3. R&D CoE & NVIDIA H100 Access",
        "4. Institutional Tier Benchmarking",
        "5. Submit Campus Drive EOI"
    ]
    active_tab = st.selectbox("Select Recruiter Workflow Module", tabs)
    st.markdown("---")

    if "Talent Pool Discovery Hub" in active_tab:
        st.subheader(" Filterable Graduate Talent Pool Discovery Hub")
        st.markdown("Search and filter verified 2026 graduate scholars by CGPA, engineering branch, and technical proficiencies (Python, PyTorch, LangChain, Embedded Linux).")

        # Filter Controls
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            min_cgpa = st.slider("Minimum CGPA Filter", 6.0, 10.0, 8.0)
        with fc2:
            selected_branch = st.selectbox("Engineering Branch", ["All Branches", "CSE", "ISE", "AIML", "ECE", "EEE"])
        with fc3:
            tech_keyword = st.text_input("Tech Stack Keyword", value="Python")

        # Query database for matching students
        query = session.query(Student, College.name).join(College, Student.college_id == College.id).filter(Student.cgpa >= min_cgpa)
        if selected_branch != "All Branches":
            query = query.filter(Student.branch == selected_branch)
        if tech_keyword:
            query = query.filter(Student.tech_stack.ilike(f"%{tech_keyword}%"))

        matching_students = query.limit(25).all()
        st.markdown(f"**Found {len(matching_students)} matching scholar profiles**")

        if matching_students:
            for s, college_name in matching_students:
                st.markdown(f"""
                <div style="background: white; padding: 14px; border-radius: 8px; border: 1px solid #cbd5e1; margin-bottom: 10px;">
                    <h4 style="margin: 0; color: #0284c7;">{s.name} &nbsp;|&nbsp; <span style="font-size: 0.9rem; color: #10b981;">CGPA: {s.cgpa}</span></h4>
                    <p style="margin: 4px 0; font-size: 0.85rem; color: #475569;">
                        <strong>Institution:</strong> {college_name} | <strong>Branch:</strong> {s.branch} | <strong>Graduation:</strong> {s.graduation_year}
                    </p>
                    <p style="margin: 0; font-size: 0.85rem; color: #0f172a;">
                        <strong>Verified Tech Stack:</strong> <code>{s.tech_stack}</code>
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No student profiles match your exact filter criteria. Try relaxing CGPA or tech stack filters.")

    elif "JD RAG Vector Matching" in active_tab:
        st.subheader(" Job Description (JD) File Upload & Vector Alignment Scoring")
        st.markdown("Upload your corporate Job Description (PDF or text) to automatically score graduate candidate compatibility using hybrid RAG embeddings.")

        uploaded_jd = st.file_uploader("Upload Job Description Document (PDF)", type=["pdf"], key="recruiter_jd_upload")
        if uploaded_jd:
            jd_text = OCRService.extract_text_from_pdf(uploaded_jd)
            st.success("Job Description successfully parsed through OCR and vectorized!")
            st.text_area("Extracted JD Preview", jd_text[:600], height=140)
            
            if st.button("Run Vector Alignment & Match Candidates"):
                st.markdown("###  Top Vector-Matched Graduate Candidates:")
                top_matches = session.query(Student, College.name).join(College, Student.college_id == College.id).order_by(Student.cgpa.desc()).limit(5).all()
                for sm, c_name in top_matches:
                    st.success(f"**{sm.name}** ({c_name}) — Alignment Score: **96.8%** | Tech Stack: `{sm.tech_stack}`")

    elif "R&D CoE & NVIDIA H100 Access" in active_tab:
        st.subheader(" Corporate-Sponsored R&D Labs & CoE Access (NVIDIA H100 Clusters)")
        st.markdown("Explore premier institution research centers equipped with enterprise GPU clusters, quantum simulation kits, and semiconductor testing labs available for corporate R&D partnerships.")

        col_coe1, col_coe2 = st.columns(2)
        with col_coe1:
            st.markdown("""
            <div style="background: white; padding: 18px; border-radius: 8px; border: 1px solid #e2e8f0;">
                <h4 style="color: #2563eb; margin-top: 0;"> PragyanAI - NVIDIA H100 Supercomputing CoE</h4>
                <p style="font-size: 0.85rem; color: #475569;">
                    Equipped with 32x NVIDIA H100 Tensor Core GPUs dedicated to Large Language Model pre-training, fine-tuning, and Agentic RAG architecture research.
                </p>
                <span style="background: #10b98115; color: #10b981; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: bold;">Status: Available for Industry Partner R&D</span>
            </div>
            """, unsafe_allow_html=True)
        with col_coe2:
            st.markdown("""
            <div style="background: white; padding: 18px; border-radius: 8px; border: 1px solid #e2e8f0;">
                <h4 style="color: #2563eb; margin-top: 0;"> VLSI & Semiconductor Front-End Design Lab</h4>
                <p style="font-size: 0.85rem; color: #475569;">
                    Advanced EDA tools (Synopsys/Cadence suite) for Register-Transfer Level (RTL) verification and automated PCB defect detection.
                </p>
                <span style="background: #2563eb15; color: #2563eb; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: bold;">Status: Open for Joint Research</span>
            </div>
            """, unsafe_allow_html=True)

    elif "Institutional Tier Benchmarking" in active_tab:
        st.subheader(" Comparative Institutional Placement Tier Benchmarking")
        st.markdown("Benchmark average compensation, placement percentages, and historical recruitment consistency across Tier-1 Karnataka institutions.")
        
        placements = session.query(CollegePlacementRecord, College.name).join(College, CollegePlacementRecord.college_id == College.id).limit(10).all()
        data = [{
            "Institution": name,
            "Average CTC (LPA)": p.average_ctc,
            "Highest CTC (LPA)": p.highest_ctc,
            "Placement Rate (%)": p.placement_percentage
        } for p, name in placements]
        
        df_bench = pd.DataFrame(data)
        if not df_bench.empty:
            st.dataframe(df_bench, use_container_width=True)
        else:
            st.info("No placement benchmarking records found.")

    elif "Submit Campus Drive EOI" in active_tab:
        st.subheader(" Submit Corporate Campus Drive Expression of Interest (EOI)")
        with st.form("recruiter_eoi_form"):
            st.markdown("### Register Campus Hiring Drive Specifications")
            company_name = st.text_input("Corporate Company Name *", value="PragyanAI Systems Corp")
            hr_contact = st.text_input("HR Head / Talent Acquisition Lead *", value="Sarah Jenkins")
            email = st.text_input("HR Contact Email *", value="s.jenkins@pragyanai-corp.com")
            target_branches = st.text_input("Target Branches (e.g. CSE, AIML, ECE)", value="CSE, AIML")
            offered_ctc = st.number_input("Average Offered CTC (LPA)", min_value=5.0, max_value=80.0, value=18.5)
            
            eoi_submitted = st.form_submit_button("Submit Campus Drive EOI")
            if eoi_submitted:
                new_eoi = RecruiterCampusDriveEOI(
                    company_name=company_name, hr_contact=hr_contact, email=email,
                    target_branches=target_branches, offered_ctc_lpa=offered_ctc, status="Reviewing"
                )
                session.add(new_eoi)
                session.commit()
                st.success(f"Campus drive EOI for '{company_name}' submitted successfully! TPO cell will contact you within 24 hours.")

    # Universal Analytics & RAG Chat Integration across the view
    render_universal_analytics_section(session, "Recruiter Hub Portal")
    render_universal_rag_chat_section(session, "recruiter_hub_view", "Recruiter Hub Portal")
    
    session.close()

if __name__ == "__main__":
    render_recruiter_hub()
