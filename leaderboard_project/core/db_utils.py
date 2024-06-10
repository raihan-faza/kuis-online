from db.database import grading_results_collection
from bson import ObjectId

async def get_leaderboard_data(quiz_id: str):
    query = {"quiz_id": quiz_id}
    cursor = grading_results_collection.find(query).sort([("grade", -1), ("timestamp", 1)])
    results = await cursor.to_list(length=100)

    data = [
        {
            "user_id": result["user_id"],
            "quiz_id": result["quiz_id"],
            "name": result.get("name", ""),
            "correct": result["correct"],
            "false": result["false"],
            "grade": result["grade"],
            "timestamp": result["timestamp"],
        }
        for result in results
    ]
    return data

async def get_quiz_ids():
    cursor = grading_results_collection.distinct("quiz_id")
    quiz_ids = await cursor.to_list(length=100)
    return quiz_ids
