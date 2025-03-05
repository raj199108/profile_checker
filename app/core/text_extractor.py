import io
import pymupdf
import docx
from fastapi import UploadFile


class TextExtractor:
    """
    A utility class for extracting text content from different document formats.
    
    This class provides methods to extract plain text from PDF and DOCX files,
    which can then be processed by other components of the application.
    """
    
    async def extract_text(self, file: UploadFile) -> str:
        """
        Extract text content from an uploaded file.
        
        Args:
            file (UploadFile): The uploaded file object from FastAPI
            
        Returns:
            str: The extracted text content from the document
            
        Raises:
            ValueError: If the file format is not supported
        """
        # Read the file content into memory
        content = await file.read()
        text = ""
        
        # Process the file based on its content type
        if file.content_type == "application/pdf":
            text = self._extract_from_pdf(content)
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = self._extract_from_docx(content)
        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX files are supported.")
        
        # Return the extracted text
        return text
    
    def _extract_from_pdf(self, content: bytes) -> str:
        """
        Extract text from PDF file content.
        
        Args:
            content (bytes): The binary content of the PDF file
            
        Returns:
            str: The extracted text from all pages of the PDF
        """
        # Open the PDF document from memory
        doc = pymupdf.open("pdf", content)
        text = ""
        
        # Iterate through each page and extract text
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text() + "\n"
        
        # Close the document to free resources
        doc.close()
        return text
    
    def _extract_from_docx(self, content: bytes) -> str:
        """
        Extract text from DOCX file content.
        
        Args:
            content (bytes): The binary content of the DOCX file
            
        Returns:
            str: The extracted text from all paragraphs of the document
        """
        # Create a document object from the binary content
        doc = docx.Document(io.BytesIO(content))
        text = ""
        
        # Extract text from each paragraph in the document
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text
