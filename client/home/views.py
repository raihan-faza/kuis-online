from django.shortcuts import (
    render,
    redirect
)
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


def create_quiz(request):
    return render(request=request, template_name="quiz/create_quiz.html")


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

    for i, question_text in enumerate(questions):
        question_dict = {
            'question_text': question_text,
            'options': options[i*4:i*4+4],
            'correct_option': correct_options[i]
        }
        quiz_data['questions'].append(question_dict)

    json_data = json.dumps(quiz_data)
    try:
        post(url="urlirfan", data=json_data)
    except:
        return JsonResponse({"Message": "failed to create quiz"}, safe=False)
    return JsonResponse(json_data, safe=False)
