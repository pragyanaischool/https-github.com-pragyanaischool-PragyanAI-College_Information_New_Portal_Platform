import streamlit as st
from sqlalchemy.orm import Session
from database.session import SessionLocal
from database.models import SchoolOutreachRequest, College, Cutoff
from ui.shared_modules import render_universal_analytics_section, render_universal_rag_chat_section

def render_school_partner_view():
    # 1. Executive High School Partner Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #059669 0%, #047857 100%); padding: 25px; border-radius: 12px; color: white; margin-bottom: 20px;">
        <h2 style="margin: 0; font-weight: 800;"> High School & Pre-University Partner Portal</h2>
        <p style="margin: 5px 0 0 0; font-size: 0.95rem; opacity: 0.9;">
            Empower your 11th and 12th standard student batches with expert STEM workshops, faculty guest lectures, and predictive engineering admission readiness programs.
        </p>
    </div>
    """, unsafe_allow_html=True)

    session = SessionLocal()

    # School Partner Workflow Tabs
    tabs = [
        "1. Book STEM Workshops & Lectures",
        "2. Student Batch Readiness & Prep",
        "3. Cohort Query & Sentiment Analytics",
        "4. Verified Cutoffs & Counseling Guidance"
    ]
    active_tab = st.selectbox("Select Partner Workflow Module", tabs)
    st.markdown("---")

    if "Book STEM Workshops" in active_tab:
        st.subheader(" Book Faculty Guest Lectures & Hands-On STEM Workshops")
        st.markdown("Request specialized faculty sessions for your school on Artificial Intelligence, Agentic AI architectures, Robotics, and Engineering Entrance Exam Preparation.")

        with st.form("school_outreach_form"):
            st.markdown("###  Schedule Outreach Event")
            
            c1, c2 = st.columns(2)
            with c1:
                school_name = st.text_input("High School / PU College Name *", value="National Public School, Indiranagar")
                contact_person = st.text_input("Principal / Career Counselor Name *", value="Dr. Sunita Sharma")
                email = st.text_input("Official Contact Email *", value="counselor@nps-indiranagar.edu.in")
            with c2:
                workshop_topic = st.selectbox("Workshop / Lecture Topic", [
                    "Introduction to Generative AI & Python for High Schoolers",
                    "Navigating KCET, COMEDK & JEE: A Strategic Roadmap",
                    "Hands-On Robotics & Embedded Systems Demo",
                    "Future of Engineering Careers in Bengaluru Tech Hub"
                ])
                preferred_date = st.text_input("Preferred Date (DD-MM-YYYY)", value="25-09-2026")
                batch_size = st.number_input("Expected Student Batch Size", min_value=20, max_value=500, value=120)

            submitted = st.form_submit_button("Submit Outreach & Workshop Request")
            if submitted:
                new_request = SchoolOutreachRequest(
                    school_name=school_name,
                    contact_person=contact_person,
                    email=email,
                    workshop_topic=workshop_topic,
                    preferred_date=preferred_date,
                    status="Pending Approval"
                )
                session.add(new_request)
                session.commit()
                st.success(f"Workshop request for '{school_name}' submitted successfully! PragyanAI academic outreach team will confirm within 48 hours.")

    elif "Student Batch Readiness" in active_tab:
        st.subheader(" Tracking Student Batch Readiness & Admissions Prep")
        st.markdown("Monitor cohort diagnostic test scores, mock exam distributions, and engineering readiness indexes across your 12th standard student batch.")

        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            st.metric(label="Registered Student Batch", value="142 Students", delta="12th Standard Science")
        with col_b2:
            st.metric(label="Average Mock PCM Score", value="78.4%", delta="+4.2% vs Last Month")
        with col_b3:
            st.metric(label="Admission Readiness Index", value="89.2 / 100", delta="High Readiness Tier")

        st.markdown("###  Batch Performance Breakdown")
        st.markdown("""
        * **Top 25% Aspirants (Rank < 5,000 Expected):** 36 Students (Focused on Tier-1 CS/AI tracks)
        * **Core Engineering Band (Rank 5k - 25,000):** 74 Students (Targeting Autonomous Institutions)
        * **Foundational Track (Support Required):** 32 Students (Enrolled in Remedial Problem-Solving Modules)
        """)

    elif "Cohort Query & Sentiment Analytics" in active_tab:
        st.subheader(" Cohort Query & Sentiment Analytics Dashboard")
        st.markdown("Inspect real-time analytics reflecting student curiosity areas, common admission anxieties, and career path preferences.")

        col_q1, col_q2 = st.columns(2)
        with col_q1:
            st.markdown("####  Top Student Inquiry Topics")
            st.write("1. **AI & Machine Learning Branch Scope** (38% of queries)")
            st.write("2. **CET vs COMEDK Counselling Process** (24% of queries)")
            st.write("3. **Hostel & Campus Life in Bengaluru** (18% of queries)")
            st.write("4. **Scholarships & Tuition Waivers (TFW)** (20% of queries)")
        with col_q2:
            st.markdown("#### Cohort Sentiment Index")
            st.success(" **Positive & Confident:** 84% (High motivation for competitive engineering entrances)")
            st.info(" **Neutral / Exploring:** 12% (Evaluating multiple career streams)")
            st.warning(" **Anxious / Needs Counseling:** 4% (Managing exam stress and score expectations)")

    elif "Verified Cutoffs & Counseling Guidance" in active_tab:
        st.subheader(" Verified Cutoffs & Career Counseling Guidance")
        st.markdown("Quick reference lookup of historical Round-2 cutoffs to guide high school students during parent-teacher career counselling sessions.")

        sample_cutoffs = session.query(Cutoff, College.name).join(College, Cutoff.college_id == College.id).limit(8).all()
        if sample_cutoffs:
            for cut, c_name in sample_cutoffs:
                st.markdown(f"""
                <div style="background: white; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 8px;">
                    <strong>{c_name}</strong> — Branch: <em>{cut.branch_name} ({cut.branch_code})</em><br>
                    Round-2 Cutoff Rank: <strong style="color: #059669;">{cut.cutoff_rank}</strong> (Category: {cut.category})
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No cutoff records found.")

    # Universal Analytics & RAG Chat Integration across the view
    render_universal_analytics_section(session, "School Partner Portal")
    render_universal_rag_chat_section(session, "school_partner_view", "School Partner Portal")
    
    session.close()

if __name__ == "__main__":
    render_school_partner_view()
