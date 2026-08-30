import random
from sqlalchemy.orm import Session
from database.models import College, Student, HiringCompany, Cutoff, CollegePlacementRecord

KARNATAKA_CITIES = ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi", "Belagavi", "Tumakuru", "Shivamogga"]
BRANCHES = [
    ("CSE", "Computer Science & Engineering"),
    ("ISE", "Information Science & Engineering"),
    ("AIML", "Artificial Intelligence & Machine Learning"),
    ("ECE", "Electronics & Communication Engineering"),
    ("EEE", "Electrical & Electronics Engineering")
]
TECH_STACKS = [
    "Python, PyTorch, LangChain", 
    "Java, Spring Boot, AWS", 
    "C++, Embedded Linux, RTOS", 
    "React, Node.js, PostgreSQL", 
    "TensorFlow, OpenCV, FastAPI"
]
SECTORS = [
    "Artificial Intelligence", 
    "Enterprise Software", 
    "Semiconductors & Embedded", 
    "Fintech & Banking", 
    "Cloud & Infrastructure"
]

def run_database_seed(session: Session):
    """
    Checks if the database contains at least 100 colleges. 
    If not, seeds the database with synthetic enterprise data:
    - 100+ Colleges (Tier-1 and Tier-2 in Karnataka)
    - Cutoff records for each branch across round numbers
    - College placement statistics (average & highest CTC, placement %)
    - 2,000+ Students with CGPA and tech stack proficiencies
    - 100+ Hiring Companies across technology sectors
    """
    if session.query(College.id).count() >= 100:
        return

    print("🌱 Bootstrapping database with 100+ Colleges, 2000+ Students, and 100+ Companies...")

    # 1. Seed 100+ Colleges
    colleges = []
    for i in range(1, 105):
        c_name = f"Institute of Technology & Engineering - Block {i}" if i > 15 else f"Tier-1 Premier Engineering College {i}"
        college = College(
            name=c_name,
            location=random.choice(KARNATAKA_CITIES),
            tier="Tier-1" if i <= 25 else "Tier-2",
            nirf_rank=i if i <= 80 else None,
            established_year=random.randint(1980, 2020)
        )
        colleges.append(college)
        session.add(college)
    session.commit()

    all_colleges = session.query(College).all()

    # 2. Seed Cutoffs & Placement Records for each College
    for college in all_colleges:
        session.add(CollegePlacementRecord(
            college_id=college.id, 
            academic_year="2025-26",
            average_ctc=round(random.uniform(6.5, 22.5), 2),
            highest_ctc=round(random.uniform(25.0, 68.0), 2),
            placement_percentage=round(random.uniform(85.0, 99.5), 1)
        ))
        for code, name in BRANCHES:
            session.add(Cutoff(
                college_id=college.id, 
                branch_code=code, 
                branch_name=name,
                category="GM", 
                round_number=2, 
                cutoff_rank=random.randint(500, 25000), 
                year=2026
            ))

    # 3. Seed 2,000+ Students across colleges in batches
    students = []
    first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Ananya", "Diya", "Saanvi"]
    last_names = ["Ambesange", "Rao", "Nayak", "Patil", "Reddy", "Gowda", "Deshmukh", "Iyer", "Sharma"]

    for i in range(1, 2100):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"student_{i}_{random.randint(1000,9999)}@pragyanai.edu"
        target_college = random.choice(all_colleges)
        branch_code, _ = random.choice(BRANCHES)
        
        student = Student(
            name=name, 
            email=email, 
            college_id=target_college.id,
            branch=branch_code, 
            cgpa=round(random.uniform(6.5, 10.0), 2),
            tech_stack=random.choice(TECH_STACKS), 
            graduation_year=2026
        )
        students.append(student)
        
        if len(students) >= 500:
            session.bulk_save_objects(students)
            session.commit()
            students = []
            
    if students:
        session.bulk_save_objects(students)
        session.commit()

    # 4. Seed 100+ Hiring Companies in batches
    companies = []
    company_prefixes = ["PragyanAI", "Neural", "Silicon", "Quantum", "Apex", "Vanguard", "Cognitive", "NextGen", "DeepTech", "Synth"]
    company_suffixes = ["Systems", "Labs", "Technologies", "AI", "Global", "Networks", "Cloud", "Solutions", "Semiconductors", "Ventures"]

    for i in range(1, 110):
        c_name = f"{random.choice(company_prefixes)} {random.choice(company_suffixes)} {i}"
        company = HiringCompany(
            company_name=c_name, 
            industry_sector=random.choice(SECTORS),
            hr_contact_email=f"hr_{i}@company-recruitment.com",
            average_offered_ctc=round(random.uniform(8.0, 45.0), 2), 
            tier_preference="Tier-1"
        )
        companies.append(company)
        
        if len(companies) >= 50:
            session.bulk_save_objects(companies)
            session.commit()
            companies = []
            
    if companies:
        session.bulk_save_objects(companies)
        session.commit()
        
    print("✅ Database seeding complete: 100+ Colleges, 2000+ Students, and 100+ Hiring Companies populated successfully!")
