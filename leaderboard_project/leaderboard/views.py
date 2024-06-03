from django.shortcuts import render

# Create your views here.
# leaderboard/views.py

from rest_framework import generics
from .models import Quiz, Leaderboard
from .serializers import QuizSerializer, LeaderboardSerializer

class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class LeaderboardListCreateView(generics.ListCreateAPIView):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

class LeaderboardByQuizView(generics.ListAPIView):
    serializer_class = LeaderboardSerializer

    def get_queryset(self):
        quiz_id = self.kwargs['quiz_id']
        return Leaderboard.objects.filter(quiz_id=quiz_id)
