from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from .models import *


def index(request):

    context = {
        'segment': 'index',
        # 'products' : Product.objects.all()
    }
    return render(request, "pages/index.html", context)


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
    return render(request, "/home/lahh/projects/scalable/client/templates/quiz/question.html", context)


def submit_quiz(request):
    return
