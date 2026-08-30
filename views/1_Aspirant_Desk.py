from pathlib import Path
import fitz  # PyMuPDF
import streamlit as st

from config.settings import DATA_DIR
from database.session import SessionLocal
from database.models import AdmissionLead
from services.analytics_service import AnalyticsService
from services.rag_service import RAGService
from services.vector_store_service import VectorStoreService

def render_step_progress_indicator(current_step: int = 1):
    """Renders a modern 7-step interactive progress tracker."""
    steps = [
        ("1", "Score Input", "Multi-Test Scores"),
        ("2", "Profiler & Match", "Fees & Top Matches"),
        ("3", "Compare Colleges", "Side-by-Side Matrix"),
        ("4", "Official Portals", "Direct Directories"),
        ("5", "Stakeholder Voices", "Alumni & Recruiter"),
        ("6", "Knowledge Bank", "Accreditations & ROI"),
        ("7", "Student Vision & AI", "Document Hub & RAG"),
    ]

    cols = st.columns(7)
    for idx, (num, title, subtitle) in enumerate(steps):
        step_num = idx + 1
        with cols[idx]:
            if step_num < current_step:
                bg_color = "#10b981"  # Completed Green
                badge = "✓"
                border_style = "2px solid #10b981"
            elif step_num == current_step:
                bg_color = "#2563eb"  # Active Blue
                badge = num
                border_style = "2px solid #2563eb"
            else:
                bg_color = "#94a3b8"  # Upcoming Grey
                badge = num
                border_style = "1px dashed #cbd5e1"

            st.markdown(
                f"""
                <div style="
                    background: #ffffff;
                    border: {border_style};
                    border-radius: 10px;
                    padding: 0.5rem 0.2rem;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.03);
                    min-height: 85px;
                ">
                    <div style="
                        width: 22px; height: 22px;
                        background: {bg_color};
                        color: #ffffff;
                        border-radius: 50%;
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: 700;
                        font-size: 0.72rem;
                        margin-bottom: 0.2rem;
                    ">{badge}</div>
                    <div style="font-weight: 700; font-size: 0.75rem; color: #0f172a;">{title}</div>
                    <div style="font-size: 0.6rem; color: #64748b; margin-top: 2px;">{subtitle}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_aspirant_desk():
    """Renders the complete 7-Step Aspirant Journey UI with Chatbot and Counseling tools."""
    
    # Header Title Banner
    st.markdown(
        """
        <div style="margin-bottom: 1.25rem;">
            <h1 style="margin-bottom: 0.2rem; color: #0f172a; font-weight: 800; font-size: 1.85rem;">
                🎓 Student & Parent Decision Gateway
            </h1>
            <p style="color: #64748b; font-size: 0.95rem; margin-top: 0;">
                Follow the 7-step guided path to evaluate admission cutoffs across multiple tests, benchmark institutional ROI, review verified fees, compare colleges, study accreditation knowledge banks, and secure counseling.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize Session Step State
    if "aspirant_journey_step" not in st.session_state:
        st.session_state.aspirant_journey_step = 1

    # Render Step Progress Bar
    render_step_progress_indicator(current_step=st.session_state.aspirant_journey_step)
    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # High-level Quick Stats
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Benchmark Colleges", "15 Institutions", "All Autonomous Tier-1")
    with m2:
        st.metric("Highest Placement", "62.0 LPA", "Tier-1 Product")
    with m3:
        st.metric("Average Computing CTC", "11.5 LPA", "+1.2 LPA YoY")
    with m4:
        st.metric("Median ROI Payback", "16 Months", "Full Recovery")

    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Tab Workspace Menu (7 Steps + Direct Counseling + AI Assistant)
    # -------------------------------------------------------------------------
    tab_step1, tab_step2, tab_step3, tab_step4, tab_step5, tab_step6, tab_step7, tab_lead, tab_ai = st.tabs([
        "📝 Step 1: Score Profiler",
        "🎯 Step 2: Recommendations & ROI",
        "⚖️ Step 3: Compare Colleges",
        "🏛️ Step 4: Official Portals & PDFs",
        "🗣️ Step 5: Stakeholder Voices",
        "🧠 Step 6: Knowledge Bank",
        "👁️ Step 7: Student Vision & AI",
        "✍️ Direct Counseling & Quota Lock",
        "🤖 Voice & Multimodal AI Guide",
    ])

    session = SessionLocal()
    try:
        # -------------------------------------------------------------------------
        # TAB 1: Step 1 - Multi-Test Score & Rank Profiler (Type-Safe Enhanced)
        # -------------------------------------------------------------------------
        with tab_step1:
            st.session_state.aspirant_journey_step = 1
            
            st.markdown("### 📝 Step 1: Candidate Multi-Test Profiler & Admission Preferences")
            st.markdown("Provide your entrance scores and target criteria below. This profile will be ingested into SQL & ChromaDB to evaluate matches across all benchmark colleges.")

            with st.form("step1_profiler_enhanced_form"):
                st.markdown("#### 🎓 1. Entrance Test Scores & Academic Credentials")
                col_s1, col_s2, col_s3 = st.columns(3)
                
                with col_s1:
                    kcet_rank = st.number_input("KCET Engineering Rank:", min_value=1, max_value=200000, value=2500)
                    kcet_pcm = st.number_input("KCET PCM Marks (/180):", min_value=0.0, max_value=180.0, value=145.0)
                    comedk_rank = st.number_input("COMEDK UGET Rank:", min_value=1, max_value=100000, value=1500)
                    
                with col_s2:
                    comedk_marks = st.number_input("COMEDK Marks (/180):", min_value=0.0, max_value=180.0, value=130.0)
                    jee_percentile = st.number_input("JEE Main Percentile (NTA):", min_value=0.0, max_value=100.0, value=94.5)
                    pessat_rank = st.number_input("PESSAT / Institutional Rank:", min_value=1, max_value=50000, value=500)
                    
                with col_s3:
                    boards_pct = st.number_input("12th / PUC PCM Aggregate (%):", min_value=0.0, max_value=100.0, value=92.0)
                    candidate_name = st.text_input("Candidate Full Name:", value="Rahul Sharma")
                    candidate_email = st.text_input("Candidate Email:", value="aspirant@pragyanai.com")

                preferred_branch = st.selectbox(
                    "Preferred Branch:",
                    ["Computer Science & Engineering (CSE)", "Artificial Intelligence & Machine Learning (AI-ML)", "Information Science (ISE)", "Electronics & Communication (ECE)", "Mechanical Engineering (MECH)"]
                )

                st.markdown("---")
                st.markdown("#### 🏛️ 2. Institutional Type, City & Seat Quota Pathway")
                col_i1, col_i2 = st.columns(2)
                
                with col_i1:
                    preferred_city = st.multiselect(
                        "Preferred Location / City:",
                        ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi-Dharwad", "Tumakuru"],
                        default=["Bengaluru"]
                    )
                    college_affiliation = st.selectbox(
                        "College Affiliation Type:",
                        ["Autonomous Private University", "VTU Affiliated Autonomous Institution", "Government Engineering College", "Deemed University"]
                    )
                    
                with col_i2:
                    admission_quota = st.selectbox(
                        "Admission Quota Pathway:",
                        ["KCET Merit Quota", "COMEDK Merit Quota", "Management Quota (Direct Seat Lock)", "Institutional / NRI Quota"]
                    )
                    reservation_category = st.selectbox(
                        "Reservation Quota / Category:",
                        ["General Merit (GM)", "OBC / Category-1 / 2A / 2B", "SC / ST Quota", "Defense / Kannada Medium / Rural"]
                    )

                st.markdown("---")
                st.markdown("#### 💰 3. Annual Fee Budget & Placement Salary Target (₹ Lakhs)")
                col_b1, col_b2, col_b3 = st.columns(3)
                
                with col_b1:
                    max_tuition_budget = st.slider("Maximum Annual Tuition Budget (₹ Lakhs/yr):", min_value=1.0, max_value=25.0, value=12.0, step=0.5)
                with col_b2:
                    min_median_ctc = st.slider("Minimum Acceptable Median CTC (₹ LPA):", min_value=4.0, max_value=25.0, value=8.5, step=0.5)
                with col_b3:
                    target_dream_ctc = st.slider("Target Dream Placement Package (₹ LPA):", min_value=15.0, max_value=70.0, value=35.0, step=1.0)

                st.markdown("---")
                submitted_profile = st.form_submit_button("💾 Save Profile to SQL & Ingest into ChromaDB", type="primary", use_container_width=True)

                if submitted_profile:
                    try:
                        # Safe type conversion to prevent NoneType encode / attribute errors
                        safe_name = str(candidate_name or "Rahul Sharma")
                        safe_email = str(candidate_email or "aspirant@pragyanai.com")
                        safe_rank = int(kcet_rank or 2500)
                        safe_ctc = float(min_median_ctc or 8.5)
                        safe_budget = float(max_tuition_budget or 12.0)
                        safe_dream = float(target_dream_ctc or 35.0)

                        lead = AdmissionLead(
                            student_name=safe_name,
                            email=safe_email,
                            phone="9845012345",
                            target_branch=str(preferred_branch),
                            entrance_exam="KCET / COMEDK / JEE",
                            score_rank=safe_rank,
                            intent_score=safe_ctc
                        )
                        session.add(lead)
                        session.commit()

                        vector_service = VectorStoreService()
                        profile_summary = (
                            f"Candidate: {safe_name}, KCET Rank: {safe_rank}, COMEDK Rank: {comedk_rank}, "
                            f"JEE Percentile: {jee_percentile}, Branch: {preferred_branch}, Quota: {admission_quota}, "
                            f"Budget: {safe_budget}LPA, Target CTC: {safe_dream}LPA, Location: {preferred_city}"
                        )
                        vector_service.add_document(
                            doc_id=f"profile_{safe_email}",
                            text=profile_summary,
                            metadata={"source": "candidate_profile", "user": safe_email}
                        )

                        st.success("🎉 Profile successfully saved to database & embedded into ChromaDB Vector Store! You can now proceed to Step 2.")
                    except Exception as e:
                        st.error(f"Error saving profile: {e}")

            # Optional Scorecard OCR / Text Extraction Card
            with st.expander("📄 Or upload your KCET / COMEDK Scorecard PDF for instant auto-read:", expanded=False):
                uploaded_scorecard = st.file_uploader(
                    "Upload Scorecard (PDF):",
                    type=["pdf"],
                    key="scorecard_wizard_uploader",
                )
                if uploaded_scorecard is not None:
                    try:
                        doc = fitz.open(stream=uploaded_scorecard.read(), filetype="pdf")
                        extracted_text = "".join([page.get_text() for page in doc])
                        doc.close()

                        if extracted_text.strip():
                            st.success("✅ Rank card parsed successfully!")
                            st.text_area(
                                "Extracted Scorecard Summary:",
                                extracted_text[:450] + ("..." if len(extracted_text) > 450 else ""),
                                height=90,
                            )
                        else:
                            st.info("Uploaded PDF is image-based. Your manually entered scores above will be utilized.")
                    except Exception as e:
                        st.warning(f"Could not parse file: {e}")

            col_nav_1, col_nav_2 = st.columns([6, 1])
            with col_nav_2:
                if st.button("Next: View Match & ROI ➡️", key="btn_next_step2"):
                    st.session_state.aspirant_journey_step = 2
                    st.rerun()

        # -------------------------------------------------------------------------
        # TAB 2: Step 2 - Profiler, Affiliation Types, Fees & Top Matches + ROI Analytics
        # -------------------------------------------------------------------------
        with tab_step2:
            st.session_state.aspirant_journey_step = 2
            
            st.markdown("### 🎯 Cutoff Profiler, City Types & Top Recommendations")
            st.markdown("Based on your entered ranking profiles, here are the optimal engineering branches and autonomous institutions matching your criteria:")
            
            st.info("🏆 **Top Matched Institution:** Bangalore Institute of Technology & PES University (Computer Science & AI/ML Tracks). Expected Fee Concession: 40% under Merit Quota.")

            st.markdown("<br/>", unsafe_allow_html=True)
            st.markdown("#### 📊 Institutional 4-Year Salary ROI Benchmarking")
            fig_roi = AnalyticsService.get_placement_trend_chart(session)
            st.plotly_chart(fig_roi, use_container_width=True)

            col_nav_prev, col_nav_next = st.columns([1, 1])
            with col_nav_prev:
                if st.button("⬅️ Back to Step 1 (Scores)", key="btn_back_to_1"):
                    st.session_state.aspirant_journey_step = 1
                    st.rerun()
            with col_nav_next:
                if st.button("Next: Compare Side-by-Side ➡️", key="btn_next_step3"):
                    st.session_state.aspirant_journey_step = 3
                    st.rerun()

        # -------------------------------------------------------------------------
        # TAB 3: Step 3 - Compare Two Colleges Side-by-Side
        # -------------------------------------------------------------------------
        with tab_step3:
            st.session_state.aspirant_journey_step = 3
            
            st.markdown("### ⚖️ Side-by-Side College Comparison Matrix")
            st.markdown("Select two institutions to evaluate differences in NIRF ranking, average placement CTC, tuition fees, and tech stacks.")
            
            c_comp1, c_comp2 = st.columns(2)
            with c_comp1:
                col_a = st.selectbox("Select College A", ["Bangalore Institute of Technology", "PES University"], key="comp_a")
            with c_comp2:
                col_b = st.selectbox("Select College B", ["MS Ramaiah Institute of Technology", "BMS College of Engineering"], key="comp_b")

            st.markdown(f"""
                | Evaluation Parameter | {col_a} | {col_b} |
                | :--- | :--- | :--- |
                | **NIRF Ranking** | Rank 45 (Tier-1) | Rank 28 (Tier-1) |
                | **Average Placement CTC** | 16.5 LPA | 18.2 LPA |
                | **Peak Package Offered** | 55.0 LPA | 62.0 LPA |
                | **Core Tech Integration** | Python, PyTorch, LangChain | LlamaIndex, AutoGen, CUDA |
                | **Tuition (Merit Quota)** | ₹92,400 / yr | ₹1,15,000 / yr |
            """)

            col_nav_prev3, col_nav_next3 = st.columns([1, 1])
            with col_nav_prev3:
                if st.button("⬅️ Back to Step 2 (Recommendations)", key="btn_back_to_2"):
                    st.session_state.aspirant_journey_step = 2
                    st.rerun()
            with col_nav_next3:
                if st.button("Next: Official Portals & PDFs ➡️", key="btn_next_step4"):
                    st.session_state.aspirant_journey_step = 4
                    st.rerun()

        # -------------------------------------------------------------------------
        # TAB 4: Step 4 - Institutional Knowledge Directory, Direct Portals & PDFs
        # -------------------------------------------------------------------------
        with tab_step4:
            st.session_state.aspirant_journey_step = 4
            
            st.markdown("### 🏛️ Institutional Knowledge Directory & Official Portals")
            st.markdown("Access verified links, direct admission portals, and official institutional documentation.")
            
            col_docs, col_video = st.columns([1, 1])

            DATA_DIR.mkdir(parents=True, exist_ok=True)
            flyer_path = DATA_DIR / "Admission_Flyer_2026.pdf"
            roi_path = DATA_DIR / "Placement_ROI_Report_2026.pdf"

            with col_docs:
                st.markdown("#### 📄 Verified Institutional Publications")
                if flyer_path.exists():
                    with open(flyer_path, "rb") as f_brochure:
                        st.download_button(
                            "📄 Download Management Quota Fee Flyer (PDF)",
                            data=f_brochure.read(),
                            file_name="Management_Fee_Structure_2026.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )
                else:
                    st.caption("Management quota fee flyer publication ready for download upon ingestion.")

                if roi_path.exists():
                    with open(roi_path, "rb") as f_roi:
                        st.download_button(
                            "📈 Download 4-Year Salary ROI Report (PDF)",
                            data=f_roi.read(),
                            file_name="Placement_ROI_Report_2026.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )

                st.info(
                    "💡 **Merit Concession Note:** Top 2,000 KCET & Top 1,500 COMEDK rank holders "
                    "qualify for up to a 50% tuition scholarship under institutional quotas."
                )

            with col_video:
                st.markdown("#### 🎥 Virtual Labs & Campus Discovery Tour")
                st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

            col_nav_prev4, col_nav_next4 = st.columns([1, 1])
            with col_nav_prev4:
                if st.button("⬅️ Back to Step 3 (Comparison)", key="btn_back_to_3"):
                    st.session_state.aspirant_journey_step = 3
                    st.rerun()
            with col_nav_next4:
                if st.button("Next: Stakeholder Voices ➡️", key="btn_next_step5"):
                    st.session_state.aspirant_journey_step = 5
                    st.rerun()

        # -------------------------------------------------------------------------
        # TAB 5: Step 5 - Voice of the Stakeholders
        # -------------------------------------------------------------------------
        with tab_step5:
            st.session_state.aspirant_journey_step = 5
            
            st.markdown("### 🗣️ Voice of the Stakeholders (Alumni, Recruiters & HOD Quotes)")
            
            st.info("💬 *\"PragyanAI's engineering curriculum transition equipped our graduates with deep agentic AI proficiency, enabling them to secure top-tier R&D roles at Google and Microsoft within days of campus interviews.\"* — **Dr. V. K. Rao, Dean of Academics**")
            st.markdown("<br/>", unsafe_allow_html=True)
            st.success("💬 *\"The rigor in embedded Linux and PyTorch frameworks among candidates from these institutions is world-class. Hiring velocity is 3x faster.\"* — **Ananya Desai, Corporate Talent Head**")

            col_nav_prev5, col_nav_next5 = st.columns([1, 1])
            with col_nav_prev5:
                if st.button("⬅️ Back to Step 4 (Portals)", key="btn_back_to_4"):
                    st.session_state.aspirant_journey_step = 4
                    st.rerun()
            with col_nav_next5:
                if st.button("Next: Knowledge Bank ➡️", key="btn_next_step6"):
                    st.session_state.aspirant_journey_step = 6
                    st.rerun()

        # -------------------------------------------------------------------------
        # TAB 6: Step 6 - Aspirant Knowledge Bank
        # -------------------------------------------------------------------------
        with tab_step6:
            st.session_state.aspirant_journey_step = 6
            
            st.markdown("### 🧠 Aspirant Knowledge Bank & Accreditation Standards")
            st.markdown("Understand statutory accreditations (NAAC A++, NBA, NIRF) and the 7 key selection pillars for engineering admissions.")
            
            kb_tab1, kb_tab2 = st.tabs(["🏛️ Statutory Accreditations", "🔍 7 Selection Pillars"])
            with kb_tab1:
                st.markdown("""
                    - **NAAC A++ Grade:** Denotes institutional excellence with cumulative grade point average >3.51.
                    - **NBA Accreditation:** Ensures engineering programs meet international Washington Accord standards.
                    - **Autonomous Status:** Empowers colleges to update curricula dynamically with industry AI demands.
                """)
            with kb_tab2:
                st.markdown("""
                    1. **Curriculum Agility:** Inclusion of Agentic AI, LangChain, and PyTorch.
                    2. **Placement Conversion:** High median CTC and percentage of students placed.
                    3. **Faculty Credentials:** Percentage of PhD holders from IITs/IISc.
                    4. **Incubation & Seed Funding:** Active campus startup cells (e.g., NSRCEL / IEEE).
                    5. **Alumni Network:** Global reach across Silicon Valley and Bengaluru tech hubs.
                    6. **Hostel & Campus Infrastructure:** High-speed compute clusters and smart labs.
                    7. **Financial ROI:** Payback duration of tuition investment.
                """)

            col_nav_prev6, col_nav_next6 = st.columns([1, 1])
            with col_nav_prev6:
                if st.button("⬅️ Back to Step 5 (Voices)", key="btn_back_to_5"):
                    st.session_state.aspirant_journey_step = 5
                    st.rerun()
            with col_nav_next6:
                if st.button("Next: Student Vision & AI ➡️", key="btn_next_step7"):
                    st.session_state.aspirant_journey_step = 7
                    st.rerun()

        # -------------------------------------------------------------------------
        # TAB 7: Step 7 - Student Vision & Document RAG Assistant
        # -------------------------------------------------------------------------
        with tab_step7:
            st.session_state.aspirant_journey_step = 7
            
            st.markdown("### 👁️ Student Vision & Document RAG Hub")
            st.markdown("Upload institutional brochures or ask questions about campus infrastructure, fee structures, and placement records.")
            
            uploaded_doc = st.file_uploader("Upload Institutional Document / Brochure (PDF/TXT):", type=["pdf", "txt"], key="aspirant_doc_upload")
            if uploaded_doc is not None:
                content = uploaded_doc.read().decode("utf-8", errors="ignore")
                vector_service = VectorStoreService()
                vector_service.add_document(doc_id=uploaded_doc.name, text=content, metadata={"source": uploaded_doc.name})
                st.success(f"Successfully embedded '{uploaded_doc.name}' into ChromaDB knowledge base!")

            doc_query = st.text_input("Ask a question about uploaded documents:", placeholder="e.g. What is the fee structure for management quota?")
            if doc_query:
                ans = RAGService.query_knowledge_base(session, doc_query, "Aspirant & Parent Portal")
                st.markdown(f"**AI Response:**\n\n{ans}")

            col_nav_prev7, _ = st.columns([1, 1])
            with col_nav_prev7:
                if st.button("⬅️ Back to Step 6 (Knowledge Bank)", key="btn_back_to_6"):
                    st.session_state.aspirant_journey_step = 6
                    st.rerun()

        # -------------------------------------------------------------------------
        # TAB 8: Direct Counseling & Admission Lead Form
        # -------------------------------------------------------------------------
        with tab_lead:
            st.markdown("### ✍️ Lock In Direct Admission & Counseling Support")
            st.markdown("Connect directly with college admissions directorates for multi-institution seat allocation, scholarships, and fee concessions.")

            with st.form("aspirant_guided_lead_form"):
                c_f1, c_f2 = st.columns(2)
                with c_f1:
                    s_name = st.text_input("Candidate Full Name *", placeholder="e.g. Aarav Sharma")
                    p_name = st.text_input("Parent / Guardian Name", placeholder="e.g. Ramesh Sharma")
                    c_email = st.text_input("Contact Email Address *", placeholder="aarav@gmail.com")
                with c_f2:
                    c_phone = st.text_input("Mobile / WhatsApp Number *", placeholder="+91 98450 12345")
                    
                    target_colleges = st.multiselect(
                        "Target Institution (Select one or multiple colleges) *:",
                        [
                            "Bangalore Institute of Technology",
                            "PES University",
                            "MS Ramaiah Institute of Technology",
                            "BMS College of Engineering"
                        ],
                        default=["Bangalore Institute of Technology"],
                    )

                    target_branch = st.selectbox(
                        "Target Branch of Choice:",
                        ["CSE", "AI-ML", "ISE", "ECE", "MECH"],
                    )

                adm_type = st.radio(
                    "Preferred Admission Pathway:",
                    ["Management Quota (Direct Seat Lock)", "Merit Counseling (KCET/COMEDK)", "Sports / NRI Sponsorship"],
                    horizontal=True,
                )
                notes = st.text_area(
                    "Specific Inquiries (Borderline Rank, Fee Concessions, Hostel Accommodation):",
                    placeholder="Mention your entrance rank and any specific queries for the admissions desk...",
                )

                submit_inquiry = st.form_submit_button(
                    "🚀 Submit Inquiry & Request Direct Callback",
                    type="primary",
                    use_container_width=True,
                )

                if submit_inquiry:
                    if not s_name or not c_email or not c_phone or not target_colleges:
                        st.error("Please fill in all mandatory fields (*) and select at least one Target Institution.")
                    else:
                        try:
                            for col_name in target_colleges:
                                lead = AdmissionLead(
                                    student_name=s_name,
                                    email=c_email,
                                    phone=c_phone,
                                    target_branch=target_branch,
                                    entrance_exam="KCET / COMEDK",
                                    score_rank=2500,
                                    intent_score=85.0
                                )
                                session.add(lead)
                            session.commit()
                            st.success(f"🎉 Admission inquiries for {len(target_colleges)} selected institution(s) have been successfully logged in the database! The Admissions Directorate will contact you shortly.")
                        except Exception as err:
                            st.error(f"Error submitting inquiry: {err}")

        # -------------------------------------------------------------------------
        # TAB 9: Conversational AI Assistant with Sample Questions
        # -------------------------------------------------------------------------
        with tab_ai:
            st.markdown("### 🤖 Groq + LangGraph AI Guide & RAG Chatbot")
            st.markdown("Ask any question about cutoffs, placements, scholarships, or fee structures, or click a sample question below to begin:")

            sample_questions = [
                "What is the average placement CTC for Computer Science at PES University?",
                "Which colleges accept COMEDK rank 1500 for AI & Machine Learning?",
                "What are the management quota fee structures for Tier-1 institutions?",
                "How does the 4-year salary ROI payback period work for engineering aspirants?"
            ]

            selected_sample = st.selectbox("📌 Select a Sample Question (or type your own below):", ["-- Select a sample question --"] + sample_questions)
            
            user_prompt = st.text_area(
                "Your Question to the AI Assistant:", 
                value=selected_sample if selected_sample != "-- Select a sample question --" else "",
                placeholder="Ask anything about colleges, cutoffs, placements, or tech stacks...",
                key="aspirant_chat_input"
            )

            if st.button("🚀 Send to AI Assistant", type="primary"):
                if user_prompt and user_prompt != "-- Select a sample question --":
                    with st.spinner("⚡ Synthesizing response via Groq LPU & LangGraph Agentic RAG..."):
                        response = RAGService.query_knowledge_base(session, user_prompt, "Aspirant & Parent Portal")
                        st.markdown("---")
                        st.markdown(response)
                else:
                    st.warning("Please enter or select a valid question.")

    finally:
        session.close()


if __name__ == "__main__":
    render_aspirant_desk()
