import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
dotenv_path = Path('.env')
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    load_dotenv()  # Try to load from default locations

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


# CRITERIA EXTRACTOR
CRITERIA_EXTRACTOR_SYSTEM_PROMPT= """

Role: Given a job description, extract and categorize key ranking criteria such as required and preferred skills, certifications, years of experience, and qualifications. The output should be structured in a JSON format. 

Task: Analyze the provided job description and extract the key ranking criteria used for evaluating candidates. Specifically, identify and categorize the following:
	•	Required Skills: List the must-have technical skills.
	•	Preferred Skills: List any nice-to-have skills that are beneficial but not mandatory.
	•	Certifications: Identify any required or preferred industry certifications.
	•	Experience: Extract the number of years of experience required, along with relevant domains.
	•	Qualifications: Extract the minimum educational qualifications and any additional academic preferences.
	•	Soft Skills: List of soft skills required.

Output Format:
Return the extracted information as a structured JSON object.
"""
CRITERIA_EXTRACTOR_USER_PROMPT= "Job Description: {job_description}"
CRITERIA_EXTRACTOR_MODEL= "gpt-4o-mini"
CRITERIA_EXTRACTOR_TEMPERATURE= 0.0

RESUME_RANKER_SYSTEM_PROMPT= """

Role: You are a resume ranking expert. Given a resume and a set of criteria you are tasked with ranking the resume, identifying the candidate's name and scoring the resume based on the criteria.

Task: Analyze the provided resume identify the candidate's name and score the resume based on the keys in thecriteria.
On a scale of 0-5 (where 0 means not mentioned at all and 5 means exceeds expectations), rate how well the given resume meets the given criteria.

Output Format:
Return the extracted information as a structured JSON object.
"""

RESUME_RANKER_USER_PROMPT= "Resume: {resume} \n Criteria: {criteria}"
RESUME_RANKER_MODEL= "gpt-4o-mini"
RESUME_RANKER_TEMPERATURE= 0.0