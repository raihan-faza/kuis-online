from pydantic import BaseModel

# Models
class req_model(BaseModel):
    user_id: int | str
    quiz_id: int | str
    questions: list[str] | list[dict] | str
    user_answers: list[str] | list[dict] | str | None
    options: list[str] | list[dict] | str
    points: int = 10

class result_model(BaseModel):
    user_id: int | str
    quiz_id: int | str
    grade: float | int = 0
    correct: int = 0
    false: int = 0