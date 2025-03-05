import ast
from typing import List
from pydantic import BaseModel, Field
from core.utils.llm_handler import LLMHandler
from configuration.config import (
    RESUME_RANKER_SYSTEM_PROMPT,
    RESUME_RANKER_USER_PROMPT,
    RESUME_RANKER_MODEL,
    RESUME_RANKER_TEMPERATURE
)

class ScoreModel(BaseModel):
    criteria: str = Field(description="The criteria being rated")
    score: int = Field(description="Score of the given criteria")

class ResumeRankerOutput(BaseModel):
    candidate_name: str = Field(description="The name of the candidate")
    scores: List[ScoreModel]

class ResumeRanker:
    def __init__(self):
        self.llm_handler = LLMHandler()

    async def rank_resume(self, resume: str, criteria: dict):
        print("Extracting criteria")
        # Use JSON mode instead of passing the Pydantic model directly
        response = await self.llm_handler.call_llm(
            system_prompt=RESUME_RANKER_SYSTEM_PROMPT,
            user_prompt=RESUME_RANKER_USER_PROMPT.format(resume=resume, criteria=criteria),
            model=RESUME_RANKER_MODEL,
            response_format=ResumeRankerOutput,
            temperature=RESUME_RANKER_TEMPERATURE
        )
        final_response = ast.literal_eval(response)
        print(final_response)
        # print(CriteriaExtractorOutput.model_validate(response))
        # Parse the JSON response and convert to the Pydantic model
        return final_response

