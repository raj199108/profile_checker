# Profile Checker

A FastAPI-based application designed to analyse job descriptions, extract the criteria and rank resumes/profiles based on the criteria in the job description.

## Project Structure

```
app/
├── __init__.py
├── app.py                 # Main FastAPI application entry point
├── requirements.txt       # Project dependencies
├── configuration/        # Configuration files and settings
├── core/                # Core business logic
├── models/              # Data models and schemas
├── routes/              # API route definitions
├── views/               # View-related logic
├── tests/              # Test files
└── output_files/       # Generated output files
```

## Prerequisites

- Python 3.8 or higher
- Docker (optional)
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd profile_checker
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r app/requirements.txt
```

## Running the Application

### Using Uvicorn

To run the application locally using Uvicorn:

```bash
cd app
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000/apis/v1`

### Using Docker

1. Build the Docker image:
```bash
docker build -t profile-checker .
```

2. Run the container:
```bash
docker run -d -p 8000:8000 --env-file .env profile-checker
```

## API Documentation

Once the application is running, you can access the interactive API documentation:

- Swagger UI: `http://localhost:8000/apis/v1/docs`
- ReDoc: `http://localhost:8000/apis/v1/redoc`

## Running Tests

To run the test suite:

```bash
cd app
pytest
```

For verbose output:
```bash
pytest -v
```

To run specific test files:
```bash
pytest tests/test_specific_file.py
```

## Demo Video

```

https://www.loom.com/share/a6d510fb37924d86aa44fc6d44301d24?sid=2e7d7b97-3646-44f2-af16-d3b454df1089
  
```

A demonstration video showcasing the application's features and usage will be added here.

## Environment Variables

Create a `.env` file in the root directory with the following variables:
```

# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here


```

The `OPENAI_API_KEY` is required for the AI-powered analysis features. You can obtain an API key by signing up at [OpenAI's platform](https://platform.openai.com/).



