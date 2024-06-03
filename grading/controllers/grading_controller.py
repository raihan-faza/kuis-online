from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.request_models import QuizSubmission
from models.db_models import GradingResultModel
from db.database import SessionLocal
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class GradingResult(BaseModel):
    user_id: str
    correct: int
    false: int
    grade: int
    timestamp: datetime

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/grade", response_model=GradingResult)
async def grade_submission(submission: QuizSubmission, db: AsyncSession = Depends(get_db)):
    grade = 0
    correct = 0
    false = 0

    # Process each answer in the submission
    for answer in submission.answers:
        if answer.user_answer == answer.correct_answer:
            grade += 10  # Increment grade by a certain amount, e.g., 10 points
            correct += 1
        else:
            false += 1

    timestamp = datetime.utcnow()

    # Create the grading result
    grading_result = GradingResultModel(
        user_id=submission.user_id,
        correct=correct,
        false=false,
        grade=grade,
        timestamp=timestamp
    )

    # Save the grading result to the database
    db.add(grading_result)
    await db.commit()

    # Return the result
    result = GradingResult(
        user_id=submission.user_id,
        correct=correct,
        false=false,
        grade=grade,
        timestamp=timestamp
    )

    return result
