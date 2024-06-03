from fastapi import FastAPI
from core.initializers import init_routers, init_db

app = FastAPI()

# Initialize routers
init_routers(app)

# Initialize database
@app.on_event("startup")
async def on_startup():
    await init_db()

# To run the app, use the following command:
# uvicorn app.main:app --reload
