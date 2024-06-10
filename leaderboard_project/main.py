from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from controllers import leaderboard_controller

app = FastAPI()

templates = Jinja2Templates(directory="../client/templates")

app.include_router(leaderboard_controller.router)
app.mount("/static", StaticFiles(directory="../client/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("leaderboard.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
