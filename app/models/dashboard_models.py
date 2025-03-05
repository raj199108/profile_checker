from pydantic import BaseModel
from fastapi import UploadFile, File
from typing import List, Optional
        
def validate_file_type(file: UploadFile = File(...)):
    """
    Validate that the uploaded file is either a PDF or DOCX format.
    
    Args:
        file (UploadFile): The file uploaded by the user
        
    Returns:
        UploadFile: The validated file object
        
    Raises:
        ValueError: If the file is not a PDF or DOCX format
    """
    # Define the content types that are acceptable
    valid_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    
    # Check if the file's content type is in our list of valid types
    if file.content_type not in valid_types:
        raise ValueError("Only PDF and DOCX files are accepted")
    
    # Log validation success
    print("File type is valid")
    return file
    
class Criteria(BaseModel):
    """
    Pydantic model representing a list of criteria extracted from a job description.
    
    Attributes:
        criteria (List[str]): A list of criteria strings extracted from the document
    """
    criteria: List[str]

class ExtractCriteriaResponse(BaseModel):
    """
    Pydantic model representing the response format for criteria extraction.
    
    Attributes:
        data (Criteria): The extracted criteria data
        message (str): A message describing the result of the operation
        error (Optional[str]): An optional error message if something went wrong
    """
    data: Criteria
    message: str
    error: Optional[str] = None
