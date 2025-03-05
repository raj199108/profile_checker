import asyncio
from typing import List, Tuple, Dict, Any
from fastapi import UploadFile, status, HTTPException

from core.text_extractor import TextExtractor
from core.criteria_extractor import CriteriaExtractor
from core.resume_ranker import ResumeRanker
from core.utils.csv_utils import CSVUtils

class DashboardViews:
    """
    Views for the endpoints /extract-criteria and /score-resumes.
    Handles the logic for criteria extraction from job descriptions and resume scoring.
    """
    def __init__(self):
        """
        Initialize the DashboardViews with required service components.
        """
        self.text_extractor = TextExtractor()
        self.criteria_extractor = CriteriaExtractor()
        self.resume_ranker = ResumeRanker()
        self.csv_utils = CSVUtils()


    async def extract_criteria(self, file: UploadFile) -> Tuple[int, Dict[str, Any]]:
        """
        Extract job criteria from an uploaded job description document.
        
        Args:
            file (UploadFile): The job description document (PDF or DOCX format)
            
        Returns:
            Tuple[int, Dict[str, Any]]: A tuple containing:
                - HTTP status code
                - Response dictionary with extracted criteria or error details
        """
        try:
            print("Extracting criteria")
            # Extract text content from the uploaded file
            text = await self.text_extractor.extract_text(file)
            
            # Process the extracted text to identify job criteria
            criteria = await self.criteria_extractor.extract_criteria(job_description=text)
            print("Criteria", criteria)
            
            # Return success response with extracted criteria
            return status.HTTP_200_OK, {
                "data": criteria,
                "message": "Criteria extracted successfully",
                "error": None
            }
        except Exception as e:
            # Return error response if any exception occurs
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    async def score_resumes(self, criteria: dict, files: List[UploadFile]) -> Tuple[int, str]:
        """
        Score and rank multiple resumes against specified job criteria.
        
        Args:
            criteria (dict): Dictionary containing job criteria (required skills, preferred skills, etc.)
            files (List[UploadFile]): List of resume documents to evaluate
            
        Returns:
            Tuple[int, str]: A tuple containing:
                - HTTP status code
                - Path to the generated CSV file containing resume rankings
            
        Raises:
            Exception: If any error occurs during processing, returns error response tuple
        """
        try:
            # Extract text from all resume files in parallel for efficiency
            extraction_tasks = [self.text_extractor.extract_text(file) for file in files]
            resume_texts = await asyncio.gather(*extraction_tasks)
            
            # Process each resume against the criteria in parallel
            ranking_tasks = [self.resume_ranker.rank_resume(resume_text, criteria) for resume_text in resume_texts]
            ranking_results = await asyncio.gather(*ranking_tasks)
            
            print("Ranking results", ranking_results)
            
            # Generate CSV file with ranking results
            csv_path = self.csv_utils.create_csv(ranking_results)
            
            return csv_path
        except Exception as e:
            # Return error response if any exception occurs
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))