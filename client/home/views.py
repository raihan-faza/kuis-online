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

# kuis-online/client/views.py
from django.shortcuts import render
from django.conf import settings
from pymongo import DESCENDING

def leaderboard_view(request, quiz_id):
    collection = settings.MONGO_COLLECTION
    leaderboard_data = collection.find({'quiz_id': quiz_id}).sort([
        ('grade', DESCENDING),
        ('timestamp', DESCENDING)
    ])

    context = {
        'leaderboard_data': leaderboard_data,
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
        #     {'name': 'Quiz 1', 'description': 'This is quiz 1', 'createdBy': 'User 1'},
        #     {'name': 'Quiz 2', 'description': 'This is quiz 2', 'createdBy': 'User 2'},
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


def attempt_quiz(request):
    context = {
        'questions': [
            {
                'number': '1',
                'question': 'test_question',
                'choices': {
                    'a': 'apa',
                    'b': 'bbbb',
                    'c': 'ccc',
                }
            },
            {
                'number': '2',
                'question': 'test_question_2',
                'choices': {
                    'a': 'apa',
                    'b': 'bbbb',
                    'c': 'ccc',
                }
            },
        ]
    }
    return render(request, "/home/lahh/projects/scalable/client/templates/quiz/show_question.html", context)


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


def create_quiz(request):
    return render(request=request, template_name="quiz/create_quiz.html")


def leaderboard(request):
    return render(request=request, template_name="pages/Leaderboard.html")


@require_POST
def submit_quiz(request):
    quiz_name = request.POST.get('quiz_name')
    questions = request.POST.getlist('question[]')
    options = request.POST.getlist('option[]')
    correct_options = request.POST.getlist('correct_option')

    quiz_data = {
        'quiz_name': quiz_name,
        'questions': []
    }
    try:
        response = post(url="http://localhost:8081/quiz", data={"Id": "1", "Name": f"{quiz_name}", "Description": "test desc",
                                                                "DurationMinute": "20", "OpenTime": "2024-09-02T13:13:13.866Z", "CloseTime": "2024-10-02T13:13:13.866Z"})
        return response.json()
    except:
        return JsonResponse(data={"message": "failed to create quiz"})

    for i, question_text in enumerate(questions):
        question_dict = {
            'question_text': question_text,
            'options': options[i*4:i*4+4],
            'correct_option': correct_options[i]
        }
        quiz_data['questions'].append(question_dict)

    json_data = json.dumps(quiz_data)
    return JsonResponse(json_data, safe=False)


'''
     try:
        post(url="http://localhost:5000", data=json_data)
    except:
        return JsonResponse({"Message": "failed to create quiz"}, safe=False)
'''
