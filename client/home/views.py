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
        access_token = request.headers.get('Access-Token')
        if access_token is None:
            return redirect('auth')
        request.session['access_token'] = access_token
        request.session['refresh_token'] = request.headers.get('Refresh-Token')
    quizzes = [
        {'name': 'Quiz 1', 'description': 'This is quiz 1', 'createdBy': 'User 1'},
        {'name': 'Quiz 2', 'description': 'This is quiz 2', 'createdBy': 'User 2'},
        #     # Add more quizzes as needed
    ]
    context = {
        'segment': 'dashboard',
        'quizzes': quizzes,
    }
    return render(request, "pages/dashboard.html", context)


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
def submit_create_quiz(request):
    quiz_name = request.POST.get('quiz_name')
    questions = request.POST.getlist('question[]')
    options = request.POST.getlist('option[]')
    correct_options = request.POST.getlist('correct_option')
    try:
        quiz_response = post(url="http://localhost:8080/Quiz", json={"Name": f"{quiz_name}", "Description": "test desc",
                                                                     "DurationMinute": "20", "OpenTime": "2024-09-02T13:13:13.866Z", "CloseTime": "2024-10-02T13:13:13.866Z"})
        quiz_id = quiz_response.json()['Id']
    except:
        return JsonResponse(data={"message": "failed to create quiz"})

    for i, question_text in enumerate(questions):
        question_response = post(
            url=f"http://localhost:8080/Quiz/{quiz_id}/question", json={"Prompt": f"{question_text}", "CorrectOptionId": None})
        question_id = question_response.json()['Id']
        for i, option_text in enumerate(options):
            options_response = post(
                url=f"http://localhost:8080/Quiz/{question_id}/option", json={"Text": f"{option_text}"})
        post(
            url=f"http://localhost:8080/{quiz_id}/question/{question_id}", json={"Prompt": f"{question_response.json()["Prompt"]}", "CorrectOptions": f"{correct_options[i]}"})
    '''
        question_dict = {
            'question_text': question_text,
            'options': options[i*4:i*4+4],
            'correct_option': correct_options[i]
        }
        quiz_data['questions'].append(question_dict)

    json_data = json.dumps(quiz_data)
       '''

    return redirect('dashboard')


'''
     try:
        post(url="http://localhost:5000", data=json_data)
    except:
        return JsonResponse({"Message": "failed to create quiz"}, safe=False)
'''

'''
@require_POST
def submit_add_question(request, id):
    questions = request.POST.getlist('question[]')
    options = request.POST.getlist('option[]')
    correct_options = request.POST.getlist('correct_option')
    return

'''
