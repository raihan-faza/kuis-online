# leaderboard/urls.py

from django.urls import path
from .views import QuizListCreateView, LeaderboardListCreateView, LeaderboardByQuizView

urlpatterns = [
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('leaderboards/', LeaderboardListCreateView.as_view(), name='leaderboard-list-create'),
    path('leaderboards/<int:quiz_id>/', LeaderboardByQuizView.as_view(), name='leaderboard-by-quiz'),
]
