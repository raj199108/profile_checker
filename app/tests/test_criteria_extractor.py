import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from core.criteria_extractor import CriteriaExtractor, CriteriaExtractorOutput


class TestCriteriaExtractor:
    @pytest.fixture
    def criteria_extractor(self):
        return CriteriaExtractor()
        
    @patch('core.criteria_extractor.LLMHandler')
    @pytest.mark.asyncio
    async def test_extract_criteria(self, mock_llm_handler_class, criteria_extractor):
        # Setup mock LLM handler
        mock_llm_handler = MagicMock()
        mock_llm_handler.call_llm = AsyncMock()
        mock_llm_handler_class.return_value = mock_llm_handler
        
        # Mock response from LLM
        mock_response = {
            "required_skills": ["Python", "FastAPI"],
            "preferred_skills": ["Docker", "AWS"],
            "certifications": ["AWS Certified Developer"],
            "experience": ["3+ years in backend development"],
            "qualifications": ["Bachelor's in Computer Science"],
            "soft_skills": ["Communication", "Teamwork"]
        }
        mock_llm_handler.call_llm.return_value = str(mock_response)
        
        job_description = "Python Developer with 3+ years of experience in backend development and FastAPI and AWS certifications and Bachelor's in Computer Science and Communication and Teamwork"
        # Test criteria extraction
        result = await criteria_extractor.extract_criteria(job_description)
        
        
        # Validate that all expected keys from the CriteriaExtractorOutput model are present
        expected_keys = CriteriaExtractorOutput.__annotations__.keys()
        for key in expected_keys:
            assert key in result, f"Expected key '{key}' not found in response"
            
        # Validate that there are no unexpected keys in the response
        for key in result:
            assert key in expected_keys, f"Unexpected key '{key}' found in response"