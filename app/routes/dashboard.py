import json
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse, FileResponse


from views.dashboard_views import DashboardViews
from models.dashboard_models import ExtractCriteriaResponse, validate_file_type

view_obj = DashboardViews()

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/extract-criteria", 
    response_model=ExtractCriteriaResponse,
    summary="Extract criteria from a job description document",
    description="Upload a job description document (PDF or DOCX) to extract required skills, preferred skills, certifications, experience, qualifications, and soft skills.",
    responses={
        200: {
            "description": "Criteria successfully extracted",
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "required_skills": ["Python", "FastAPI"],
                            "preferred_skills": ["Docker", "AWS"],
                            "certifications": ["AWS Certified Developer"],
                            "experience": ["3+ years in backend development"],
                            "qualifications": ["Bachelor's in Computer Science"],
                            "soft_skills": ["Communication", "Teamwork"]
                        },
                        "message": "Criteria extracted successfully",
                        "error": None
                    }
                }
            }
        },
        400: {
            "description": "Invalid file format",
            "content": {
                "application/json": {
                    "example": {
                        "data": {},
                        "message": "Invalid file format. Only PDF and DOCX files are accepted.",
                        "error": "Unsupported file type"
                    }
                }
            }
        },
        500: {
            "description": "Server error",
            "content": {
                "application/json": {
                    "example": {
                        "data": {},
                        "message": "Error extracting criteria",
                        "error": "Internal server error"
                    }
                }
            }
        }
    }
)
async def extract_criteria(file: UploadFile = Depends(validate_file_type)):
    """
    Extract job criteria from an uploaded job description document.
    
    Args:
        file (UploadFile): The job description document (PDF or DOCX format)
        
    Returns:
        JSONResponse: A response containing the extracted criteria or error details
        
    Raises:
        ValueError: If the file format is invalid
        Exception: For any other processing errors
    """
    try:
        # Extract criteria from the uploaded file
        status_code, response = await view_obj.extract_criteria(file)

        # Return the response
        return JSONResponse(
            status_code=status_code,
            content=response
        )
    
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ExtractCriteriaResponse(
                data={},
                message="Invalid file format. Only PDF and DOCX files are accepted.",
                error=str(e)
            ).model_dump()
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ExtractCriteriaResponse(
                data={},
                message="Error extracting criteria",
                error=str(e)
            ).model_dump()
        )


@router.post(
    "/score-resumes",
    summary="Score and rank resumes against job criteria",
    description="Upload multiple resumes (PDF or DOCX) and job criteria to score and rank candidates. Returns a CSV file with rankings.",
    responses={
        200: {
            "description": "Resumes successfully scored and ranked",
            "content": {
                "text/csv": {
                    "example": "File download (resume_scores.csv)"
                }
            }
        },
        400: {
            "description": "Invalid file format or criteria",
            "content": {
                "application/json": {
                    "example": {
                        "data": {},
                        "message": "Invalid file format or criteria format",
                        "error": "Validation error"
                    }
                }
            }
        },
        500: {
            "description": "Server error",
            "content": {
                "application/json": {
                    "example": {
                        "data": {},
                        "message": "Error scoring resumes",
                        "error": "Internal server error"
                    }
                }
            }
        }
    }
)
async def score_resumes(criteria: str = Form(...), files: List[UploadFile] = File(...)):
    """
    Score and rank multiple resumes against specified job criteria.
    
    Args:
        criteria (str): JSON string containing job criteria (required skills, preferred skills, etc.)
        files (List[UploadFile]): List of resume documents to evaluate (PDF or DOCX format)
        
    Returns:
        FileResponse: A CSV file containing the ranked results of all resumes
        JSONResponse: Error details if processing fails
        
    Raises:
        ValueError: If file formats are invalid or criteria cannot be parsed
        Exception: For any other processing errors
    """
    try:
        # Parse the criteria from the JSON string
        criteria = json.loads(criteria)

        # Validate the files
        validated_files = [validate_file_type(file) for file in files]
        
        # Score and rank the resumes
        csv_path = await view_obj.score_resumes(criteria, validated_files)

        # Return the CSV file
        return FileResponse(
            path=csv_path,
            filename="resume_scores.csv",
            media_type="text/csv"
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ExtractCriteriaResponse(
                data={},
                message="Error scoring resumes",
                error=str(e)
            ).model_dump()
        )

