from fastapi import APIRouter
from core.db_utils import get_leaderboard_data, get_quiz_ids

router = APIRouter()

@router.get("/leaderboard/{quiz_id}")
async def read_leaderboard(quiz_id: str):
    data = await get_leaderboard_data(quiz_id)
    return data

@router.get("/quiz-ids")
async def read_quiz_ids():
    quiz_ids = await get_quiz_ids()
    return quiz_ids
