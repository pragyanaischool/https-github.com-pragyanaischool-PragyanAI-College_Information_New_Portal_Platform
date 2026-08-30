import plotly.express as px
import pandas as pd
from sqlalchemy.orm import Session
from database.models import College, Student, HiringCompany, CollegePlacementRecord

class AnalyticsService:
    @staticmethod
    def get_placement_trend_chart(session: Session):
        """
        Generates an interactive grouped bar chart comparing average 
        and highest CTC across premier institutions.
        """
        placements = (
            session.query(CollegePlacementRecord, College.name)
            .join(College, CollegePlacementRecord.college_id == College.id)
            .limit(15)
            .all()
        )
        
        data = [{
            "College": name,
            "Average CTC (LPA)": p.average_ctc,
            "Highest CTC (LPA)": p.highest_ctc,
            "Placement %": p.placement_percentage
        } for p, name in placements]
        
        df = pd.DataFrame(data)
        if df.empty:
            return px.scatter(title="No Placement Telemetry Available")
            
        fig = px.bar(
            df, 
            x="College", 
            y=["Average CTC (LPA)", "Highest CTC (LPA)"],
            barmode="group", 
            title="Institutional CTC Benchmarking (LPA)",
            template="plotly_white", 
            color_discrete_sequence=["#2563eb", "#10b981"]
        )
        fig.update_layout(
            xaxis_tickangle=-45, 
            margin=dict(t=50, b=100),
            legend_title="Compensation Metric"
        )
        return fig

    @staticmethod
    def get_student_cgpa_distribution(session: Session):
        """
        Generates an interactive histogram illustrating student 
        CGPA distribution across engineering branches.
        """
        students = session.query(Student.cgpa, Student.branch).all()
        df = pd.DataFrame(students, columns=["CGPA", "Branch"])
        
        if df.empty:
            return px.scatter(title="No Student Data Available")
            
        fig = px.histogram(
            df, 
            x="CGPA", 
            color="Branch",  # Fixed case-sensitivity to match column name "Branch"
            nbins=20,
            title="Graduate Talent Pool CGPA Distribution by Branch",
            template="plotly_white", 
            barmode="overlay"
        )
        fig.update_layout(margin=dict(t=50, b=50))
        return fig

    @staticmethod
    def get_company_sector_breakdown(session: Session):
        """
        Generates an interactive donut pie chart breaking down 
        recruiting partners by industry sector.
        """
        companies = session.query(HiringCompany.industry_sector).all()
        df = pd.DataFrame(companies, columns=["Sector"])
        
        if df.empty:
            return px.scatter(title="No Hiring Company Data Available")
            
        sector_counts = df["Sector"].value_counts().reset_index()
        sector_counts.columns = ["Sector", "Count"]
        
        fig = px.pie(
            sector_counts, 
            names="Sector", 
            values="Count",
            title="Recruiting Partner Distribution by Industry Sector",
            template="plotly_white", 
            hole=0.4
        )
        fig.update_layout(margin=dict(t=50, b=50))
        return fig
