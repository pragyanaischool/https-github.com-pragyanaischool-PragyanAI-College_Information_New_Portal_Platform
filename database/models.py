from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # 'aspirant', 'college_management', 'recruiter', 'school_partner', 'admin'
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class College(Base):
    __tablename__ = "colleges"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    location = Column(String(100), nullable=False)
    tier = Column(String(50), default="Tier-1")
    nirf_rank = Column(Integer, nullable=True)
    established_year = Column(Integer, nullable=True)
    
    # Relationships with cascade delete
    cutoffs = relationship("Cutoff", back_populates="college", cascade="all, delete-orphan")
    placements = relationship("CollegePlacementRecord", back_populates="college", cascade="all, delete-orphan")
    students = relationship("Student", back_populates="college", cascade="all, delete-orphan")


class Cutoff(Base):
    __tablename__ = "cutoffs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False)
    branch_code = Column(String(50), nullable=False)
    branch_name = Column(String(255), nullable=False)
    category = Column(String(50), default="GM")
    round_number = Column(Integer, default=2)
    cutoff_rank = Column(Integer, nullable=False)
    year = Column(Integer, default=2026)
    
    college = relationship("College", back_populates="cutoffs")


class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False)
    branch = Column(String(100), nullable=False)
    cgpa = Column(Float, nullable=False)
    tech_stack = Column(String(255), nullable=False)  # e.g., Python, PyTorch, LangChain
    graduation_year = Column(Integer, default=2026)
    
    college = relationship("College", back_populates="students")


class HiringCompany(Base):
    __tablename__ = "hiring_companies"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False, unique=True)
    industry_sector = Column(String(100), nullable=False)
    hr_contact_email = Column(String(150), nullable=False)
    average_offered_ctc = Column(Float, nullable=False)  # in LPA
    tier_preference = Column(String(50), default="Tier-1")
    created_at = Column(DateTime, default=datetime.utcnow)


class CollegePlacementRecord(Base):
    __tablename__ = "college_placement_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False)
    academic_year = Column(String(20), nullable=False)
    average_ctc = Column(Float, nullable=False)
    highest_ctc = Column(Float, nullable=False)
    placement_percentage = Column(Float, nullable=False)
    
    college = relationship("College", back_populates="placements")


class AdmissionLead(Base):
    __tablename__ = "admission_leads"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(50), nullable=False)
    target_branch = Column(String(100))
    entrance_exam = Column(String(50))
    score_rank = Column(Integer)
    intent_score = Column(Float, default=50.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class SchoolOutreachRequest(Base):
    __tablename__ = "school_outreach_requests"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    school_name = Column(String(255), nullable=False)
    contact_person = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    workshop_topic = Column(String(255), nullable=False)
    preferred_date = Column(String(50), nullable=False)
    status = Column(String(50), default="Pending Approval")
    created_at = Column(DateTime, default=datetime.utcnow)


class RecruiterCampusDriveEOI(Base):
    __tablename__ = "recruiter_campus_drive_eois"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False)
    hr_contact = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    target_branches = Column(String(255), nullable=False)
    offered_ctc_lpa = Column(Float, nullable=False)
    status = Column(String(50), default="Reviewing")
    created_at = Column(DateTime, default=datetime.utcnow)
