import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import UploadFile

from core.text_extractor import TextExtractor


class TestTextExtractor:
    @pytest.fixture
    def text_extractor(self):
        return TextExtractor()
        
    @patch('pymupdf.open')
    @pytest.mark.asyncio
    async def test_extract_from_pdf(self, mock_pymupdf_open, text_extractor):
        # Setup mock PDF document
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Sample PDF text"
        mock_doc.load_page.return_value = mock_page
        mock_doc.page_count = 2
        mock_pymupdf_open.return_value = mock_doc
        
        # Create mock PDF file
        mock_file = MagicMock(spec=UploadFile)
        mock_file.content_type = "application/pdf"
        mock_file.read = AsyncMock(return_value=b"mock pdf content")
        
        # Test extraction
        result = await text_extractor.extract_text(mock_file)
        
        # Assertions
        assert result == "Sample PDF text\nSample PDF text\n"
        mock_pymupdf_open.assert_called_once_with("pdf", b"mock pdf content")
        
    @patch('docx.Document')
    @pytest.mark.asyncio
    async def test_extract_from_docx(self, mock_docx, text_extractor):
        # Setup mock DOCX document
        mock_doc = MagicMock()
        mock_paragraph1 = MagicMock()
        mock_paragraph1.text = "Sample DOCX text line 1"
        mock_paragraph2 = MagicMock()
        mock_paragraph2.text = "Sample DOCX text line 2"
        mock_doc.paragraphs = [mock_paragraph1, mock_paragraph2]
        mock_docx.return_value = mock_doc
        
        # Create mock DOCX file
        mock_file = MagicMock(spec=UploadFile)
        mock_file.content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        mock_file.read = AsyncMock(return_value=b"mock docx content")
        
        # Test extraction
        result = await text_extractor.extract_text(mock_file)
        
        # Assertions
        assert result == "Sample DOCX text line 1\nSample DOCX text line 2\n"
        mock_docx.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_unsupported_file_format(self, text_extractor):
        # Create mock file with unsupported format
        mock_file = MagicMock(spec=UploadFile)
        mock_file.content_type = "text/plain"
        mock_file.read = AsyncMock(return_value=b"mock text content")
        
        # Test extraction with unsupported format
        with pytest.raises(ValueError) as excinfo:
            await text_extractor.extract_text(mock_file)
        
        assert "Unsupported file format" in str(excinfo.value)