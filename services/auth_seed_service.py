import hashlib
from datetime import datetime
from sqlalchemy.orm import Session
from database.models import (
    User, College, Cutoff, Student, HiringCompany, 
    CollegePlacementRecord, AdmissionLead, SchoolOutreachRequest, RecruiterCampusDriveEOI
)

def seed_users_and_demo_data(session: Session):
    """
    Seeds default user authentication credentials and comprehensive demo data 
    across all stakeholder modules into the SQLite database on initial boot.
    """
    
    # 1. Seed Default Secure Users (Hashing passwords with SHA-256)
    if session.query(User.id).count() == 0:
        default_users = [
            User(
                username="aspirant1", 
                password_hash=hashlib.sha256("password123".encode()).hexdigest(), 
                role="aspirant", 
                full_name="Rahul Sharma (Student/Parent)", 
                email="aspirant@pragyanai.com"
            ),
            User(
                username="college_admin", 
                password_hash=hashlib.sha256("password123".encode()).hexdigest(), 
                role="college_management", 
                full_name="Dr. V. K. Rao (College Dean)", 
                email="dean@college.edu"
            ),
            User(
                username="recruiter_hr", 
                password_hash=hashlib.sha256("password123".encode()).hexdigest(), 
                role="recruiter", 
                full_name="Ananya Desai (Talent Head)", 
                email="hr@techcorp.com"
            ),
            User(
                username="school_principal", 
                password_hash=hashlib.sha256("password123".encode()).hexdigest(), 
                role="school_partner", 
                full_name="Suresh Hebbar (PU Principal)", 
                email="principal@school.edu"
            ),
            User(
                username="admin", 
                password_hash=hashlib.sha256("admin123".encode()).hexdigest(), 
                role="admin", 
                full_name="Sateesh Ambesange (System Admin)", 
                email="admin@pragyanai.com"
            )
        ]
        session.add_all(default_users)
        session.commit()

    # 2. Seed Rich Institutional & College Data
    if session.query(College.id).count() == 0:
        colleges = [
            College(name="Bangalore Institute of Technology", location="Bengaluru", tier="Tier-1", nirf_rank=45, established_year=1979),
            College(name="PES University", location="Bengaluru", tier="Tier-1", nirf_rank=28, established_year=1988),
            College(name="MS Ramaiah Institute of Technology", location="Bengaluru", tier="Tier-1", nirf_rank=35, established_year=1962),
            College(name="BMS College of Engineering", location="Bengaluru", tier="Tier-1", nirf_rank=52, established_year=1946)
        ]
        session.add_all(colleges)
        session.commit()

        # Seed Placement Records & Cutoffs for each college
        for c in colleges:
            session.add(CollegePlacementRecord(
                college_id=c.id, 
                academic_year="2025-2026",
                average_ctc=16.5 if c.tier == "Tier-1" else 11.2,
                highest_ctc=55.0 if c.tier == "Tier-1" else 28.0, 
                placement_percentage=94.5
            ))
            session.add(Cutoff(
                college_id=c.id, 
                branch_code="CSE",
                branch_name="Computer Science & Engineering",
                category="GM",
                round_number=2,
                cutoff_rank=1250,
                year=2026
            ))
            session.add(Cutoff(
                college_id=c.id, 
                branch_code="AIML",
                branch_name="Artificial Intelligence & Machine Learning",
                category="GM",
                round_number=2,
                cutoff_rank=1800,
                year=2026
            ))
        session.commit()

    # 3. Seed Verified Student Talent Pool
    if session.query(Student.id).count() == 0:
        sample_college = session.query(College).first()
        college_id = sample_college.id if sample_college else 1
        
        sample_students = [
            Student(name="Aarav Patel", email="aarav@student.edu", college_id=college_id, branch="CSE", cgpa=9.2, tech_stack="Python, PyTorch, LangChain", graduation_year=2026),
            Student(name="Diya Nair", email="diya@student.edu", college_id=college_id, branch="AI & ML", cgpa=9.5, tech_stack="Python, LlamaIndex, TensorFlow", graduation_year=2026),
            Student(name="Rohan Gupta", email="rohan@student.edu", college_id=college_id, branch="ECE", cgpa=8.4, tech_stack="Embedded C, Linux Kernel, OpenCV", graduation_year=2026),
            Student(name="Sneha Rao", email="sneha@student.edu", college_id=college_id, branch="CSE", cgpa=8.9, tech_stack="Agentic AI, AutoGen, FastAPI", graduation_year=2027)
        ]
        session.add_all(sample_students)
        session.commit()

    # 4. Seed Hiring Partner Ecosystem
    if session.query(HiringCompany.id).count() == 0:
        sample_companies = [
            HiringCompany(company_name="Google India", industry_sector="Deep Tech & Cloud", hr_contact_email="recruiting@google.com", average_offered_ctc=32.0, tier_preference="Tier-1"),
            HiringCompany(company_name="Microsoft", industry_sector="Software & AI", hr_contact_email="hr@microsoft.com", average_offered_ctc=28.5, tier_preference="Tier-1"),
            HiringCompany(company_name="Bosch Global", industry_sector="Automotive & Embedded", hr_contact_email="talent@bosch.com", average_offered_ctc=14.0, tier_preference="Tier-1")
        ]
        session.add_all(sample_companies)
        session.commit()

    # 5. Seed Admission Leads, School Outreach & Recruiter EOIs
    if session.query(AdmissionLead.id).count() == 0:
        session.add(AdmissionLead(student_name="Kiran Kumar", email="kiran@gmail.com", phone="9876543210", target_branch="Computer Science", entrance_exam="KCET", score_rank=2100, intent_score=85.0))
        session.commit()

    if session.query(SchoolOutreachRequest.id).count() == 0:
        session.add(SchoolOutreachRequest(school_name="National Public School", contact_person="Principal Sharma", email="nps@school.edu", workshop_topic="Introduction to Agentic AI & Robotics", preferred_date="2026-04-15", status="Approved"))
        session.commit()

    if session.query(RecruiterCampusDriveEOI.id).count() == 0:
        session.add(RecruiterCampusDriveEOI(company_name="NVIDIA India", hr_contact="Priya Menon", email="pmenon@nvidia.com", target_branches="CSE, AI/ML, ECE", offered_ctc_lpa=36.0, status="Scheduled"))
        session.commit()
