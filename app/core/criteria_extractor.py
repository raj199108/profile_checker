import ast
from pydantic import BaseModel, Field
from typing import Dict, List, Any

from core.utils.llm_handler import LLMHandler
from configuration.config import (
    CRITERIA_EXTRACTOR_SYSTEM_PROMPT,
    CRITERIA_EXTRACTOR_USER_PROMPT,
    CRITERIA_EXTRACTOR_MODEL,
    CRITERIA_EXTRACTOR_TEMPERATURE
)

class CriteriaExtractorOutput(BaseModel):
    """
    Pydantic model defining the structure for job criteria extraction output.
    
    This model specifies all the categories of information that should be
    extracted from a job description document.
    
    Attributes:
        required_skills: Essential technical skills needed for the job
        preferred_skills: Desirable but not mandatory skills
        certifications: Required or preferred professional certifications
        experience: Required work experience and relevant domains
        qualifications: Educational requirements and academic preferences
        soft_skills: Interpersonal and non-technical skills required
    """
    required_skills: list[str] = Field(description="List the must-have technical skills")
    preferred_skills: list[str] = Field(description="List any nice-to-have skills that are beneficial but not mandatory")
    certifications: list[str] = Field(description="List of any required or preferred industry certifications")
    experience: list[str] = Field(description="List of experience required along with relevant domains.")
    qualifications: list[str] = Field(description="List of minimum educational qualifications and any additional academic preferences required.")
    soft_skills: list[str] = Field(description="List of soft skills required.")

class CriteriaExtractor:
    """
    Extracts structured job criteria from unstructured job description text.
    
    This class uses a language model to analyze job descriptions and extract
    key criteria like required skills, experience, and qualifications.
    """
    def __init__(self):
        """Initialize the CriteriaExtractor with an LLM handler."""
        self.llm_handler = LLMHandler()

    async def extract_criteria(self, job_description: str) -> Dict[str, List[str]]:
        """
        Extract structured job criteria from a job description text.
        
        Args:
            job_description (str): The raw text of a job description document
            
        Returns:
            Dict[str, List[str]]: A dictionary containing categorized job criteria
                with keys for required_skills, preferred_skills, certifications,
                experience, qualifications, and soft_skills
        """
        print("Extracting criteria")
        
        # Call the language model with the job description to extract criteria
        # Using JSON mode to ensure structured output format
        response = await self.llm_handler.call_llm(
            system_prompt=CRITERIA_EXTRACTOR_SYSTEM_PROMPT,
            user_prompt=CRITERIA_EXTRACTOR_USER_PROMPT.format(job_description=job_description),
            model=CRITERIA_EXTRACTOR_MODEL,
            response_format=CriteriaExtractorOutput,
            temperature=CRITERIA_EXTRACTOR_TEMPERATURE
        )
        
        # Convert the string response to a Python dictionary
        # ast.literal_eval safely evaluates the string as a Python literal
        final_response = ast.literal_eval(response)
        
        # Log the extracted criteria for debugging
        print(final_response)
        
        # Return the structured criteria dictionary
        return final_response
