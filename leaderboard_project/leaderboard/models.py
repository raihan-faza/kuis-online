from django.db import models

# Create your models here.
# leaderboard/models.py

from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Leaderboard(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quiz', 'user')
        ordering = ['-score', 'timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"
