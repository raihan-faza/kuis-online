from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index,  name='index'),
    path('tables/', views.tables, name='tables'),
    path('quiz/attempt', views.attempt_quiz, name='attempt_quiz'),
    path('quiz/create/<str:Id>', views.create_quiz, name='create_quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('auth/', views.auth, name='auth'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leaderboard/<int:quiz_id>/', views.leaderboard_view, name='leaderboard'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('google/', views.google, name='google'),
]
