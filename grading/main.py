from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models import req_model, result_model
from config import grade_collection, simulate_collection, real_grade
from datetime import datetime
import json
import httpx

app = FastAPI()

# Exception Handler
@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

# End Point
# head = get
@app.get("/")
async def root():
    return {"message": "This is the root"}

# patch = post
@app.post("/grade-test")
async def grade_test(info: req_model):
    questions = info.questions
    answers = info.user_answers
    keys = info.options
    points = info.points

    grade = 0
    correct = 0
    false = 0

    for i in range(len(keys)):
        if answers[i] == keys[i]:
            grade += points
            correct += 1
            break
        else:
            false += 1
            break
    
    doc = {
        "user_id": info.user_id,
        "quiz_id": info.quiz_id,
        "grade": float("{:.2f}".format(grade / len(questions))),
        "correct": correct,
        "false": false,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    
    temp = grade_collection.insert_one(doc)

    return {
        "message": "Testing Succeed",
    }

@app.post("/simulation")
async def simulate(info: req_model):
    questions = list(eval(info.questions))
    answers = list(eval(info.user_answers))
    options = list(eval(info.options))
    points = info.points

    grade = 0
    correct = 0
    false = 0

    for question in questions:
        # correct_ans = options[f'{question['correctID']}']
        for option in options:
            if option['id'] == question['correct_id']:
                correct_ans = option['text']
                break

        for answer in answers:
            if answer['q_id'] == question['id'] and answer['answer'] == correct_ans:
                grade += points
                correct += 1
                break
            else:
                false += 1
                break
    
    doc = {
        "user_id": info.user_id,
        "quiz_id": info.quiz_id,
        "grade": float("{:.2f}".format(grade / len(questions))),
        "correct": correct,
        "false": false,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    
    temp = simulate_collection.insert_one(doc)

    return {
        "message": "Simulation Succeed"
    }

@app.post("/grade")
async def get_grade(info: req_model):

    answers = info.user_answers

    quiz_id = info.quiz_id

    questions, options = [], []

    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://your-friends-quiz-service.com/api/quizzes/{quiz_id}/answer/")
        response.raise_for_status()
        questions = response.json()

    points = info.points

    grade = 0
    correct = 0
    false = 0

    for question in questions:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://your-friends-quiz-service.com/api/quizzes/{question["Id"]}/option/")
            response.raise_for_status()
            options = response.json()

        for option in options:
            if option['Id'] == question['CorrectOptionId']:
                correct_answer = option['Text']
                break
        
        for answer in answers:
            if answer['question_id'] == question['Id'] and answer["answer"] == correct_answer:
                grade += points
                correct += 1
                break
            else:
                false += 1
                break

    doc = {
        "user_id": info.user_id,
        "quiz_id": info.quiz_id,
        "grade": float("{:.2f}".format(grade / len(questions))),
        "correct": correct,
        "false": false,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    temp = real_grade.insert_one(doc)

    return {
        "message": "Succeed"
    }