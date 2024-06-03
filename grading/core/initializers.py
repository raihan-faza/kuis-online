from fastapi import FastAPI
from controllers import grading_controller
from db.database import database, engine, Base
import models.db_models  # Import to ensure models are created

def init_routers(app: FastAPI):
    app.include_router(grading_controller.router)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await database.connect()
