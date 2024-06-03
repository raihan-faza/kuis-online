from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from .models import *

def index(request):
    quizzes = [
        {'name': 'Quiz 1', 'description': 'This is quiz 1', 'createdBy': 'User 1'},
        {'name': 'Quiz 2', 'description': 'This is quiz 2', 'createdBy': 'User 2'},
    #     # Add more quizzes as needed
    ]

    context = {
        'segment': 'index',
        'quizzes': quizzes,
        #'products' : Product.objects.all()
    }
    return render(request, "pages/index.html", context)

def tables(request):
  context = {
    'segment': 'tables'
  }
  return render(request, "pages/dynamic-tables.html", context)
