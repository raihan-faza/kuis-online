from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index,  name='index'),
    path('tables/', views.tables, name='tables'),
    path('quiz/attempt/<str:quiz_id>/', views.attempt_quiz, name='attempt_quiz'),
    path('quiz/create/', views.create_quiz, name='create_quiz'),
    path('submit/quiz/create/', views.submit_create_quiz,
         name='submit_create_quiz'),
    path('auth/', views.auth, name='auth'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leaderboard/<int:quiz_id>/',
         views.leaderboard_view, name='leaderboard'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('google/', views.google, name='google'),
    path('submit/quiz/attempt/<str:quiz_id>/', views.submit_attempt_quiz,
         name='submit_attempt_quiz'),
    path('quiz/submitted', views.done, name='submitted')
]
