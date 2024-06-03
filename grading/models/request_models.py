from pydantic import BaseModel
from typing import List

class Answer(BaseModel):
    user_answer: str
    correct_answer: str

class QuizSubmission(BaseModel):
    user_id: str
    answers: List[Answer]
