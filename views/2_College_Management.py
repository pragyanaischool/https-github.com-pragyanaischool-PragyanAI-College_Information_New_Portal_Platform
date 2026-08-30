import streamlit as st
from sqlalchemy.orm import Session
from database.session import SessionLocal
from database.models import College, CollegePlacementRecord, AdmissionLead, SchoolOutreachRequest, RecruiterCampusDriveEOI
from ui.shared_modules import render_universal_analytics_section, render_universal_rag_chat_section

def render_college_management_view():
    # 1. Executive Portal Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 12px; color: white; margin-bottom: 20px;">
        <h2 style="margin: 0; font-weight: 800;">🏛️ Engineering College Management & Governance Portal</h2>
        <p style="margin: 5px 0 0 0; font-size: 0.95rem; opacity: 0.9;">
            Manage institutional telemetry, update master database records, publish placement records, and track incoming student leads, school outreach requests, and recruiter EOIs.
        </p>
    </div>
    """, unsafe_allow_html=True)

    session = SessionLocal()

    # Management Navigation Tabs
    tabs = [
        "1. Master College Data Management",
        "2. Placement Publishing & Benchmarks",
        "3. Student Admission Inquiries",
        "4. High School Outreach Requests",
        "5. Recruiter Campus Drive EOIs"
    ]
    active_tab = st.selectbox("Select Management Workflow", tabs)
    st.markdown("---")

    if "Master College Data Management" in active_tab:
        st.subheader(" Admin Portal: College Master Data Management")
        st.markdown("Add new engineering colleges, update intake capacities, modify fee structures (CET, COMEDK, Management), and adjust median CTC packages.")

        with st.form("college_master_form"):
            st.markdown("###  Add / Update College Master Record")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                college_code = st.text_input("College Code (Unique) *", value="E101")
                full_name = st.text_input("Full Institution Name *", value="PragyanAI Institute of Technology")
                short_name = st.text_input("Short Name", value="PIT")
                state = st.text_input("State", value="Karnataka")
            with c2:
                district = st.text_input("District", value="Bengaluru Urban")
                city = st.text_input("City *", value="Bengaluru")
                est_year = st.number_input("Established Year", min_value=1900, max_value=2026, value=2012)
                is_autonomous = st.checkbox("Is Autonomous?", value=True)
            with c3:
                total_intake = st.number_input("Total Intake Seats", min_value=60, max_value=5000, value=1200)
                median_ctc = st.number_input("Median CTC (LPA)", min_value=1.0, max_value=100.0, value=12.5)
                highest_ctc = st.number_input("Highest CTC (LPA)", min_value=1.0, max_value=150.0, value=45.0)
                nirf_rank = st.number_input("NIRF Rank", min_value=1, max_value=500, value=42)

            st.markdown("### Fee Structures & Governance")
            f1, f2, f3 = st.columns(3)
            with f1:
                govt_fee = st.number_input("Govt CET Fee (Lakhs/Yr)", min_value=0.1, max_value=10.0, value=1.12)
            with f2:
                comedk_fee = st.number_input("COMEDK Fee (Lakhs/Yr)", min_value=0.5, max_value=25.0, value=2.65)
            with f3:
                mgmt_fee = st.number_input("Management Fee (Lakhs/Yr)", min_value=1.0, max_value=50.0, value=10.0)

            vision_text = st.text_area("Institutional Vision", value="To pioneer deep-tech education, AI research integration, and industry-aligned experiential learning.")
            website_url = st.text_input("Official Website URL", value="https://pragyanai.com")

            submitted = st.form_submit_button("Save College Master Record")
            if submitted:
                # Check if college exists, else create
                existing = session.query(College).filter_by(name=full_name).first()
                if existing:
                    existing.location = city
                    existing.tier = "Autonomous" if is_autonomous else "Affiliated"
                    existing.nirf_rank = nirf_rank
                    existing.established_year = est_year
                    session.commit()
                    st.success(f"College record for '{full_name}' updated successfully!")
                else:
                    new_college = College(
                        name=full_name,
                        location=city,
                        tier="Autonomous" if is_autonomous else "Affiliated",
                        nirf_rank=nirf_rank,
                        established_year=est_year
                    )
                    session.add(new_college)
                    session.commit()
                    st.success(f"New institution '{full_name}' registered into master database successfully!")

    elif "Placement Publishing" in active_tab:
        st.subheader(" Institutional Placement Publishing & Benchmarks")
        st.markdown("Publish and manage department-wise placement statistics, average offers, and peak recruiter compensation packages.")
        
        colleges = session.query(College).all()
        college_map = {c.name: c.id for c in colleges}
        
        with st.form("placement_publish_form"):
            selected_college = st.selectbox("Select Institution", list(college_map.keys()))
            ac_year = st.selectbox("Academic Year", ["2025-26", "2024-25", "2023-24"])
            avg_pkg = st.number_input("Average CTC (LPA)", min_value=2.0, max_value=50.0, value=11.5)
            high_pkg = st.number_input("Highest CTC (LPA)", min_value=5.0, max_value=100.0, value=55.0)
            placement_pct = st.slider("Placement Percentage (%)", 50.0, 100.0, 94.5)
            
            pub_submitted = st.form_submit_button("Publish Placement Telemetry")
            if pub_submitted:
                c_id = college_map[selected_college]
                record = CollegePlacementRecord(
                    college_id=c_id, academic_year=ac_year,
                    average_ctc=avg_pkg, highest_ctc=high_pkg, placement_percentage=placement_pct
                )
                session.add(record)
                session.commit()
                st.success(f"Placement telemetry for {selected_college} published live successfully!")

    elif "Student Admission Inquiries" in active_tab:
        st.subheader(" Live Student Admission Inquiries & Lead Management")
        st.markdown("Review real-time prospective student inquiries, target branches, intent scores, and counselor callback requests.")
        
        leads = session.query(AdmissionLead).order_by(AdmissionLead.created_at.desc()).all()
        if leads:
            for l in leads:
                st.markdown(f"""
                <div style="background: white; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 8px;">
                    <strong> {l.student_name}</strong> ({l.email} | {l.phone})<br>
                    Target Branch: <em>{l.target_branch}</em> | Exam: <strong>{l.entrance_exam}</strong> | Intent Score: <span style="color: #10b981; font-weight: bold;">{l.intent_score}/100</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active student admission leads found in database.")

    elif "High School Outreach" in active_tab:
        st.subheader(" High School / PU Partner Outreach Requests")
        st.markdown("Review and approve workshop bookings, faculty guest lecture requests, and STEM bootcamp schedules.")
        
        outreach_reqs = session.query(SchoolOutreachRequest).all()
        if outreach_reqs:
            for req in outreach_reqs:
                st.write(f"**School:** {req.school_name} | **Topic:** {req.workshop_topic} | **Status:** {req.status}")
        else:
            st.info("No school outreach requests pending.")

    elif "Recruiter Campus Drive" in active_tab:
        st.subheader(" Corporate Recruiter Campus Drive EOIs")
        st.markdown("Manage corporate expressions of interest for upcoming placement drives, NVIDIA H100 CoE access, and tech stack requirements.")
        
        eois = session.query(RecruiterCampusDriveEOI).all()
        if eois:
            for e in eois:
                st.write(f"**Company:** {e.company_name} | **Target Branches:** {e.target_branches} | **Offered CTC:** {e.offered_ctc_lpa} LPA")
        else:
            st.info("No recruiter campus drive EOIs currently registered.")

    # Universal Analytics & RAG Chat Integration across the view
    render_universal_analytics_section(session, "College Management Portal")
    render_universal_rag_chat_section(session, "college_mgmt_view", "College Management Portal")
    
    session.close()

if __name__ == "__main__":
    render_college_management_view()
