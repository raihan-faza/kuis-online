from motor.motor_asyncio import AsyncIOMotorClient
import os


MONGO_URL = os.getenv("MONGO_URL")

# Create the MongoDB client
client = AsyncIOMotorClient(MONGO_URL)
database = client['quiz_db']
grading_results_collection = database['grade_list']
