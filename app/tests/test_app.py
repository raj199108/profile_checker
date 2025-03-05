import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import UploadFile

from views.dashboard_views import DashboardViews
from fastapi import status


class TestDashboardViews:
    @pytest.fixture
    def dashboard_views(self):
        return DashboardViews()
        
    @patch('views.dashboard_views.TextExtractor')
    @patch('views.dashboard_views.CriteriaExtractor')
    @pytest.mark.asyncio
    async def test_extract_criteria_success(self, mock_criteria_extractor_class, mock_text_extractor_class, dashboard_views):
        # Setup mocks
        mock_text_extractor = MagicMock()
        mock_text_extractor.extract_text = AsyncMock(return_value="Sample job description")
        mock_text_extractor_class.return_value = mock_text_extractor
        
        mock_criteria_extractor = MagicMock()
        mock_criteria = {
            "required_skills": ["Python", "FastAPI"],
            "preferred_skills": ["Docker", "AWS"]
        }
        mock_criteria_extractor.extract_criteria = AsyncMock(return_value=mock_criteria)
        mock_criteria_extractor_class.return_value = mock_criteria_extractor
        
        # Create mock file
        mock_file = MagicMock(spec=UploadFile)
        
        # Override the instance attributes
        dashboard_views.text_extractor = mock_text_extractor
        dashboard_views.criteria_extractor = mock_criteria_extractor
        
        # Test criteria extraction
        status_code, response = await dashboard_views.extract_criteria(mock_file)
        
        # Assertions
        assert status_code == status.HTTP_200_OK
        assert response["data"] == mock_criteria
        assert response["message"] == "Criteria extracted successfully"
        assert response["error"] is None
        mock_text_extractor.extract_text.assert_called_once_with(mock_file)
        mock_criteria_extractor.extract_criteria.assert_called_once_with(job_description="Sample job description")
        
    @patch('views.dashboard_views.TextExtractor')
    @patch('views.dashboard_views.CriteriaExtractor')
    @pytest.mark.asyncio
    async def test_extract_criteria_error(self, mock_criteria_extractor_class, mock_text_extractor_class, dashboard_views):
        # Setup mocks with error
        mock_text_extractor = MagicMock()
        mock_text_extractor.extract_text = AsyncMock(side_effect=Exception("Test error"))
        mock_text_extractor_class.return_value = mock_text_extractor
        
        # Create mock file
        mock_file = MagicMock(spec=UploadFile)
        
        # Override the instance attributes
        dashboard_views.text_extractor = mock_text_extractor
        
        # Test criteria extraction with error
        status_code, response = await dashboard_views.extract_criteria(mock_file)
        
        # Assertions
        assert status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response["data"] == {}
        assert response["message"] == "Error extracting criteria"
        assert response["error"] == "Test error"
        
    @patch('views.dashboard_views.TextExtractor')
    @patch('views.dashboard_views.ResumeRanker')
    @patch('views.dashboard_views.CSVUtils')
    @pytest.mark.asyncio
    async def test_score_resumes_success(self, mock_csv_utils_class, mock_resume_ranker_class, mock_text_extractor_class, dashboard_views):
        # Setup mocks
        mock_text_extractor = MagicMock()
        mock_text_extractor.extract_text = AsyncMock(side_effect=["Resume 1", "Resume 2"])
        mock_text_extractor_class.return_value = mock_text_extractor
        
        mock_resume_ranker = MagicMock()
        mock_ranking_results = [
            {
                "candidate_name": "John Doe",
                "scores": [{"criteria": "required_skills", "score": 4}]
            },
            {
                "candidate_name": "Jane Smith",
                "scores": [{"criteria": "required_skills", "score": 3}]
            }
        ]
        mock_resume_ranker.rank_resume = AsyncMock(side_effect=mock_ranking_results)
        mock_resume_ranker_class.return_value = mock_resume_ranker
        
        mock_csv_utils = MagicMock()
        mock_csv_utils.create_csv = MagicMock(return_value="path/to/csv")
        mock_csv_utils_class.return_value = mock_csv_utils
        
        # Create mock files and criteria
        mock_file1 = MagicMock(spec=UploadFile)
        mock_file2 = MagicMock(spec=UploadFile)
        mock_criteria = {"required_skills": ["Python"]}
        
        # Override the instance attributes
        dashboard_views.text_extractor = mock_text_extractor
        dashboard_views.resume_ranker = mock_resume_ranker
        dashboard_views.csv_utils = mock_csv_utils
        
        # Test resume scoring
        result = await dashboard_views.score_resumes(mock_criteria, [mock_file1, mock_file2])
        
        # Assertions
        assert result == "path/to/csv"
        assert mock_text_extractor.extract_text.call_count == 2
        assert mock_resume_ranker.rank_resume.call_count == 2
        mock_csv_utils.create_csv.assert_called_once_with(mock_ranking_results)
        
    @patch('views.dashboard_views.TextExtractor')
    @pytest.mark.asyncio
    async def test_score_resumes_error(self, mock_text_extractor_class, dashboard_views):
        # Setup mocks with error
        mock_text_extractor = MagicMock()
        mock_text_extractor.extract_text = AsyncMock(side_effect=Exception("Test error"))
        mock_text_extractor_class.return_value = mock_text_extractor
        
        # Create mock files and criteria
        mock_file = MagicMock(spec=UploadFile)
        mock_criteria = {"required_skills": ["Python"]}
        
        # Override the instance attributes
        dashboard_views.text_extractor = mock_text_extractor
        
        # Test resume scoring with error
        status_code, response = await dashboard_views.score_resumes(mock_criteria, [mock_file])
        
        # Assertions
        assert status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response["data"] == {}
        assert response["message"] == "Error scoring resumes"
        assert response["error"] == "Test error"

