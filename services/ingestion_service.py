import pandas as pd
from sqlalchemy.orm import Session
from database.models import Student, HiringCompany

class IngestionService:
    @staticmethod
    def process_excel_or_csv(uploaded_file, entity_type: str, session: Session) -> int:
        """
        Bulk imports student or hiring company records into the database 
        from uploaded CSV or Excel (.xlsx) files.
        
        Args:
            uploaded_file: Streamlit UploadedFile object (CSV or Excel)
            entity_type (str): Target entity table ("students" or "companies")
            session (Session): Active SQLAlchemy database session
            
        Returns:
            int: Number of successfully imported records.
        """
        # Load dataframe based on file extension
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        imported_count = 0
        
        if entity_type == "students":
            for _, row in df.iterrows():
                student = Student(
                    name=row['name'],
                    email=row['email'],
                    college_id=int(row['college_id']),
                    branch=row['branch'],
                    cgpa=float(row['cgpa']),
                    tech_stack=row['tech_stack'],
                    graduation_year=int(row.get('graduation_year', 2026))
                )
                session.add(student)
                imported_count += 1
                
        elif entity_type == "companies":
            for _, row in df.iterrows():
                company = HiringCompany(
                    company_name=row['company_name'],
                    industry_sector=row['industry_sector'],
                    hr_contact_email=row['hr_contact_email'],
                    average_offered_ctc=float(row['average_offered_ctc']),
                    tier_preference=row.get('tier_preference', 'Tier-1')
                )
                session.add(company)
                imported_count += 1
                
        session.commit()
        return imported_count
