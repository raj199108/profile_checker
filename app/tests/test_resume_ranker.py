import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from core.resume_ranker import ResumeRanker

class TestResumeRanker:
    @pytest.fixture
    def resume_ranker(self):
        return ResumeRanker()
        
    @patch('core.resume_ranker.LLMHandler')
    @pytest.mark.asyncio
    async def test_rank_resume(self, mock_llm_handler_class, resume_ranker):
        # Setup mock LLM handler
        mock_llm_handler = MagicMock()
        mock_llm_handler.call_llm = AsyncMock()
        mock_llm_handler_class.return_value = mock_llm_handler
        
        # Mock criteria and resume
        criteria = {
            "required_skills": ["Python", "FastAPI"],
            "preferred_skills": ["Docker", "AWS"],
            "certifications": ["AWS Certified Developer"],
            "experience": ["3+ years in backend development"],
            "qualifications": ["Bachelor's in Computer Science"],
            "soft_skills": ["Communication", "Teamwork"]
        }
        resume_text = "Rajat is a good candidate with Python experience and AWS certifications and Bachelor's in Computer Science and Communication and Teamwork"
        
        # Mock response from LLM
        mock_response = {
            "candidate_name": "Rajat",
            "scores": [
                {"criteria": "required_skills", "score": 5},
                {"criteria": "preferred_skills", "score": 4},
                {"criteria": "certifications", "score": 2},
                {"criteria": "experience", "score": 1},
                {"criteria": "qualifications", "score": 3},
                {"criteria": "soft_skills", "score": 2}
            ]
        }
        mock_llm_handler.call_llm.return_value = str(mock_response)
        
        # Test resume ranking
        result = await resume_ranker.rank_resume(resume_text, criteria)
        print("result", result)
        # Assertions
        assert "candidate_name" in result
        assert "scores" in result
        assert result["candidate_name"] == "Rajat"
        assert len(result["scores"]) == 6
        # Check if all required criteria keys exist
        criteria_keys = [score["criteria"] for score in result["scores"]]
        assert "required_skills" in criteria_keys
        assert "preferred_skills" in criteria_keys
        assert "certifications" in criteria_keys
        assert "experience" in criteria_keys
        assert "qualifications" in criteria_keys
        assert "soft_skills" in criteria_keys
