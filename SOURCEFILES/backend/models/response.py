from pydantic import BaseModel
from typing import List

class EvaluationSchema(BaseModel):
    semanticSimilarity: int
    difficultyLevel: str
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    missingIdeas: List[str]
    wrongStatements: List[str]
    suggestions: List[str]
    learningAdvice: str
    coveredKeywords: List[str]
    missedKeywords: List[str]
