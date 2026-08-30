import fitz  # PyMuPDF

class OCRService:
    @staticmethod
    def extract_text_from_pdf(uploaded_file) -> str:
        """
        Extracts raw text content from uploaded PDF scorecards, entrance exam rank cards, 
        admission brochures, or candidate resumes using PyMuPDF.
        
        Args:
            uploaded_file: Streamlit UploadedFile object (PDF)
            
        Returns:
            str: Consolidated text extracted across all pages of the document.
        """
        try:
            # Read bytes from the Streamlit uploaded file buffer
            pdf_bytes = uploaded_file.read()
            
            # Open document stream with PyMuPDF
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            extracted_text = ""
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                extracted_text += f"\--- Page {page_num + 1} ---\n"
                extracted_text += page.get_text() + "\n"
                
            return extracted_text.strip()
            
        except Exception as e:
            return f"Error processing PDF document through OCR engine: {str(e)}"
