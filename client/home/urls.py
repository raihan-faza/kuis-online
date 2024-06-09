from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index,  name='index'),
    path('tables/', views.tables, name='tables'),
    path('quiz/attempt', views.attempt_quiz, name='attempt_quiz'),
    path('quiz/create', views.create_quiz, name='create_quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard')
]
