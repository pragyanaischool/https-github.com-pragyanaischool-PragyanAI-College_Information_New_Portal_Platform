import pandas as pd

def convert_df_to_csv(df: pd.DataFrame) -> bytes:
    """
    Converts a pandas DataFrame to UTF-8 encoded CSV bytes 
    for direct use in Streamlit download buttons.
    
    Args:
        df (pd.DataFrame): The data table to convert.
        
    Returns:
        bytes: Encoded CSV bytes.
    """
    return df.to_csv(index=False).encode('utf-8')

def generate_text_report(title: str, metrics: dict, records: list) -> str:
    """
    Generates a structured plain-text report summarizing matched institutions, 
    cutoffs, or candidate profiles for export.
    
    Args:
        title (str): Title of the report.
        metrics (dict): Key-value summary metrics.
        records (list): List of textual record summaries.
        
    Returns:
        str: Formatted report text.
    """
    report_lines = [
        f"=" * 60,
        f"PRAGYANAI INSTITUTIONAL INTELLIGENCE REPORT",
        f"Title: {title}",
        f"=" * 60,
        "\n--- EXECUTIVE METRICS ---"
    ]
    
    for k, v in metrics.items():
        report_lines.append(f"{k}: {v}")
        
    report_lines.append("\n--- VERIFIED RECORDS ---")
    for idx, rec in enumerate(records, 1):
        report_lines.append(f"{idx}. {rec}")
        
    report_lines.append("\n" + "=" * 60)
    report_lines.append("Generated via PragyanAI Decision Portal — Autonomous Telemetry Engine")
    
    return "\n".join(report_lines)
