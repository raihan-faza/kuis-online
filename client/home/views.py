from django.shortcuts import (
    render,
    redirect
)
from django.http import HttpResponse
from admin_datta.forms import (
    RegistrationForm,
    LoginForm,
    UserPasswordChangeForm,
    UserPasswordResetForm,
    UserSetPasswordForm
)
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView
)

from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from .models import *

from httpx import (
    post,
    get
)

from django.views.decorators.http import require_POST

import json

from django.http.response import JsonResponse
from django.shortcuts import render
from django.conf import settings
from pymongo import DESCENDING


def leaderboard_view(request, quiz_id):
    context = {
        'quiz_id': quiz_id
    }
    return render(request, 'leaderboard.html', context)


def index(request):
    quizzes = [
        {'name': 'Quiz 1', 'description': 'This is quiz 1', 'createdBy': 'User 1'},
        {'name': 'Quiz 2', 'description': 'This is quiz 2', 'createdBy': 'User 2'},
        #     # Add more quizzes as needed
    ]

    context = {
        'segment': 'index',
        'quizzes': quizzes,
        # 'products' : Product.objects.all()
    }
    return render(request, "pages/index.html", context)
    # 'products' : Product.objects.all()


def dashboard(request):
    if 'access_token' not in request.session:
        return redirect('auth')

    try:
        response = get('http://localhost:5000/api/Quiz')
        quizzes = response.json()
        
        # quizzes = [
        #     {'Id':'Capek1','Name': 'Quiz 1', 'Description': 'This is quiz 1', 'CreatedBy': 'User 1'},
        #     {'Id':'Capek2','Name': 'Quiz 2', 'Description': 'This is quiz 2', 'CreatedBy': 'User 2'},
        #     #     # Add more quizzes as needed
        # ]
        context = {
            'segment': 'dashboard',
            'quizzes': quizzes,
        }
        return render(request, "pages/dashboard.html", context)
    except Exception as e:
        print(e)
        return redirect('index')


def tables(request):
    context = {
        'segment': 'tables'
    }
    return render(request, "pages/dynamic-tables.html", context)


def attempt_quiz(request, quiz_id):
    question_response = get(
        url=f"http://localhost:8080/Quiz/{quiz_id}/question")
    question_data = question_response.json()
    questions = [{"id": question['Id'], "text": question['Prompt']}
                 for question in question_data]
    context = {}
    for question in questions:
        question_id = question['id']
        question_text = question['text']
        option_response = get(
            f"http://localhost:8080/Quiz/{question_id}/option")
        option_data = option_response.json()
        # return JsonResponse(data=option_data, safe=False)
        options = [option['Text'] for option in option_data]
        context[question_id] = {
            "text": question_text,
            "options": options
        }
    # return JsonResponse(data=context, safe=False)
    return render(request, "/home/lahh/projects/scalable/client/templates/quiz/show_question.html", context={"questions": context})


def auth(request):
    context = {
        'segment': 'login'
    }
    return render(request, "pages/login.html", context)


def google(request):
    if request.method == 'GET':
        try:
            response = get('http://localhost:3000/users/auth/google')
            if response.status_code == 200:
                data = response.json()
                print(data)
                request.session['access_token'] = data['access_token']
                request.session['refresh_token'] = data['refresh_token']
                return redirect('dashboard')
            else:
                data = response.json()
                print(data)
                return redirect('auth')
        except Exception as e:
            print(e)
            return redirect('auth')


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        try:
            response = post('http://localhost:3000/users/login',
                            json={'email': email, 'password': password})
            if response.status_code == 200:
                data = response.json()
                print(data)
                request.session['access_token'] = data['access_token']
                request.session['refresh_token'] = data['refresh_token']
                return redirect('dashboard')
            else:
                data = response.json()
                print(data)
                return redirect('auth')
        except:
            return redirect('auth')


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        try:
            response = post('http://localhost:3000/users/signup', json={
                            'email': email, 'password': password, 'name': name, 'gender': 'Male', 'phone': '08123456789'})
            if response.status_code == 200:
                data = response.json()
                print(data)
                request.session['access_token'] = data['access_token']
                request.session['refresh_token'] = data['refresh_token']
                return redirect('dashboard')
            else:
                data = response.json()
                print(data)
                return redirect('auth')
        except:
            return redirect('auth')


def create_quiz(request, Id):
    context = {
        'quiz_id': Id
    }
    return render(request=request, template_name="quiz/create_quiz.html", context=context)


def leaderboard(request):
    return render(request=request, template_name="pages/Leaderboard.html")


@require_POST
def submit_create_quiz(request):
    quiz_name = request.POST.get('quiz_name')
    desc = request.POST.get('description')
    duration = request.POST.get('duration')
    open_time = request.POST.get('open_time')
    close_time = request.POST.get('close_time')
    questions = request.POST.getlist('question[]')
    options = request.POST.getlist('option[]')
    correct_options = request.POST.getlist('correct_option')
    try:
        quiz_response = post(url="http://localhost:8080/Quiz", json={"Name": f"{quiz_name}", "Description": f"{desc}",
                                                                     "DurationMinute": f"{duration}", "OpenTime": f"{open_time}", "CloseTime": f"{close_time}"})
        quiz_id = quiz_response.json()['Id']
    except:
        return JsonResponse(data={"message": "failed to create quiz"})

    for i, question_text in enumerate(questions):
        question_response = post(
            url=f"http://localhost:8080/Quiz/{quiz_id}/question", json={"Prompt": f"{question_text}", "CorrectOptionId": None})
        question_id = question_response.json()['Id']
        for _, option_text in enumerate(options[i*4:i*4+4]):
            options_response = post(
                url=f"http://localhost:8080/Quiz/{question_id}/option", json={"Text": f"{option_text}"})
        post(url=f"http://localhost:8080/{quiz_id}/question/{question_id}", json={"Prompt": f"{
             question_response.json()["Prompt"]}", "CorrectOptions": f"{correct_options[i]}"})
    '''
        question_dict = {
            'question_text': question_text,
            'options': options[i*4:i*4+4],
            'correct_option': correct_options[i]
        }
        quiz_data['questions'].append(question_dict)

    json_data = json.dumps(quiz_data)
       '''
    response = get(url=f"http://localhost:8080/Quiz/{quiz_id}/question")
    return JsonResponse(data=response.json(), safe=False)


'''
     try:
        post(url="http://localhost:5000", data=json_data)
    except:
        return JsonResponse({"Message": "failed to create quiz"}, safe=False)
'''


@require_POST
def submit_attempt_quiz(request):
    questions = request.POST.getlist('question[]')
    options = request.POST.getlist('option[]')
    correct_options = request.POST.getlist('correct_option')
    user_responses = {}
    for question_id, user_answer in request.POST.items():
        if question_id.startswith('question'):
            question_id = question_id.replace(
                'question', '')  # Remove 'question' prefix
            user_responses[question_id] = user_answer
    return JsonResponse(data=user_responses, safe=False)
