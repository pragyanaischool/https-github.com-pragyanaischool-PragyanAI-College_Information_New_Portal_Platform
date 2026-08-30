import streamlit as st
from sqlalchemy.orm import Session
from database.session import SessionLocal
from database.models import College, Student, HiringCompany
from services.ocr_service import OCRService
from services.ingestion_service import IngestionService
from ui.shared_modules import render_universal_analytics_section, render_universal_rag_chat_section

def render_data_ingestion_view():
    # 1. Executive Ingestion Portal Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%); padding: 25px; border-radius: 12px; color: white; margin-bottom: 20px;">
        <h2 style="margin: 0; font-weight: 800;">📥 Enterprise Data Ingestion Portal</h2>
        <p style="margin: 5px 0 0 0; font-size: 0.95rem; opacity: 0.9;">
            Scale institutional database telemetry seamlessly by uploading PDF scorecards/brochures, bulk importing CSV/Excel student and company datasets, or registering records via manual forms.
        </p>
    </div>
    """, unsafe_allow_html=True)

    session = SessionLocal()

    # Ingestion Workflow Tabs
    tabs = [
        "1. PDF Ingestion & OCR Extraction",
        "2. Bulk Excel/CSV Dataset Import",
        "3. Manual Entity Registration"
    ]
    active_tab = st.selectbox("Select Ingestion Method", tabs)
    st.markdown("---")

    if "PDF Ingestion & OCR Extraction" in active_tab:
        st.subheader(" Automated PDF Scorecard & Brochure Text Extraction")
        st.markdown("Upload entrance exam scorecards, institutional brochures, or candidate resumes to extract text instantly using the PyMuPDF OCR engine.")

        uploaded_pdf = st.file_uploader("Upload Document (PDF)", type=["pdf"], key="ingestion_pdf_upload")
        if uploaded_pdf:
            if st.button("Extract Content via OCR Engine"):
                extracted_text = OCRService.extract_text_from_pdf(uploaded_pdf)
                st.success("PDF document successfully parsed and extracted!")
                st.text_area("Extracted Document Content Preview", extracted_text[:1500], height=300)

    elif "Bulk Excel/CSV Dataset Import" in active_tab:
        st.subheader(" Bulk Import Students or Hiring Companies")
        st.markdown("Upload structured `.csv` or `.xlsx` files to instantly populate thousands of student records or hiring partners into the SQLite database.")

        entity_choice = st.selectbox("Select Target Database Schema", ["students", "companies"])
        
        st.info(f" **Expected Columns for `{entity_choice}`:** " + 
                ("`name`, `email`, `college_id`, `branch`, `cgpa`, `tech_stack`" if entity_choice == "students" 
                 else "`company_name`, `industry_sector`, `hr_contact_email`, `average_offered_ctc`"))

        uploaded_file = st.file_uploader(f"Upload {entity_choice} Dataset", type=["csv", "xlsx"], key="bulk_dataset_upload")
        
        if uploaded_file and st.button("Execute Bulk Database Import"):
            try:
                imported_count = IngestionService.process_excel_or_csv(uploaded_file, entity_choice, session)
                st.success(f"Successfully imported **{imported_count}** new records into the `{entity_choice}` table!")
            except Exception as e:
                st.error(f"Bulk import failed due to structural validation error: {str(e)}")

    elif "Manual Entity Registration" in active_tab:
        st.subheader(" Manual Entity Registration Form")
        st.markdown("Register individual records directly into the operational database with live form validation.")

        manual_type = st.selectbox("Choose Entity Type", ["Student Scholar", "Hiring Company", "Engineering College"])

        if manual_type == "Student Scholar":
            with st.form("manual_student_form"):
                s_name = st.text_input("Full Name *", value="Rohan Patil")
                s_email = st.text_input("Email Address *", value="rohan.patil@pragyanai.edu")
                
                colleges = session.query(College).all()
                college_map = {c.name: c.id for c in colleges} if colleges else {"Default Institute": 1}
                s_college = st.selectbox("Affiliated Institution", list(college_map.keys()))
                
                s_branch = st.selectbox("Engineering Branch", ["CSE", "ISE", "AIML", "ECE", "EEE"])
                s_cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=8.9)
                s_tech = st.text_input("Tech Stack (comma separated)", value="Python, PyTorch, LangChain, FastApi")
                
                submitted = st.form_submit_button("Register Student Record")
                if submitted:
                    new_student = Student(
                        name=s_name,
                        email=s_email,
                        college_id=college_map[s_college],
                        branch=s_branch,
                        cgpa=s_cgpa,
                        tech_stack=s_tech,
                        graduation_year=2026
                    )
                    session.add(new_student)
                    session.commit()
                    st.success(f"Student scholar '{s_name}' successfully registered into database!")

        elif manual_type == "Hiring Company":
            with st.form("manual_company_form"):
                c_name = st.text_input("Company Name *", value="NeuralSynth Technologies")
                c_sector = st.selectbox("Industry Sector", ["Artificial Intelligence", "Enterprise Software", "Semiconductors & Embedded", "Fintech & Banking"])
                c_email = st.text_input("HR Contact Email *", value="recruitment@neuralsynth.com")
                c_ctc = st.number_input("Average Offered CTC (LPA)", min_value=3.0, max_value=75.0, value=22.5)
                
                c_submitted = st.form_submit_button("Register Hiring Company")
                if c_submitted:
                    new_comp = HiringCompany(
                        company_name=c_name,
                        industry_sector=c_sector,
                        hr_contact_email=c_email,
                        average_offered_ctc=c_ctc,
                        tier_preference="Tier-1"
                    )
                    session.add(new_comp)
                    session.commit()
                    st.success(f"Hiring partner '{c_name}' successfully registered into database!")

        elif manual_type == "Engineering College":
            with st.form("manual_college_form"):
                col_name = st.text_input("Institution Name *", value="Karnataka Institute of Advanced Technology")
                col_loc = st.text_input("City Location *", value="Bengaluru")
                col_tier = st.selectbox("Tier Classification", ["Tier-1", "Tier-2"])
                col_nirf = st.number_input("NIRF Rank", min_value=1, max_value=200, value=28)
                
                col_submitted = st.form_submit_button("Register Institution")
                if col_submitted:
                    new_col = College(
                        name=col_name,
                        location=col_loc,
                        tier=col_tier,
                        nirf_rank=col_nirf,
                        established_year=2005
                    )
                    session.add(new_col)
                    session.commit()
                    st.success(f"Institution '{col_name}' successfully added to master directory!")

    # Universal Analytics & RAG Chat Integration across the view
    render_universal_analytics_section(session, "Data Ingestion Portal")
    render_universal_rag_chat_section(session, "data_ingestion_view", "Data Ingestion Portal")
    
    session.close()

if __name__ == "__main__":
    render_data_ingestion_view()
