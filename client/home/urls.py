from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index,  name='index'),
    path('tables/', views.tables, name='tables'),
    path('quiz/attempt', views.attempt_quiz, name='attempt_quiz'),
    path('quiz/question/add', views.create_question, name='add_question'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
