from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/leaderboard/<int:quiz_id>/', views.LeaderboardAPIView.as_view(), name='leaderboard_api'),
    path('admin/', admin.site.urls),
]