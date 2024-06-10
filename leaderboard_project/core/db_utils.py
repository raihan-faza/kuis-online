from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import SessionLocal
from models.db_models import GradingResultModel

async def get_leaderboard_data(quiz_id: str):
    async with SessionLocal() as session:
        query = select(GradingResultModel).where(GradingResultModel.quiz_id == quiz_id).order_by(GradingResultModel.grade.desc(), GradingResultModel.timestamp.asc())
        result = await session.execute(query)
        results = result.scalars().all()

        data = [
            {
                "user_id": row.user_id,
                "quiz_id": row.quiz_id,
                "name": row.name,
                "correct": row.correct,
                "false": row.false,
                "grade": row.grade,
                "timestamp": row.timestamp,
            }
            for row in results
        ]
        return data

async def get_quiz_ids():
    async with SessionLocal() as session:
        query = select(GradingResultModel.quiz_id).distinct()
        result = await session.execute(query)
        quiz_ids = result.scalars().all()
        return quiz_ids
