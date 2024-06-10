from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import DESCENDING
from .serializers import LeaderboardSerializer

class LeaderboardAPIView(APIView):
    def get(self, request, quiz_id):
        collection = settings.MONGO_COLLECTION
        leaderboard_data = list(collection.find({'quiz_id': quiz_id}).sort([
            ('grade', DESCENDING),
            ('timestamp', DESCENDING)
        ]))

        for entry in leaderboard_data:
            entry['_id'] = str(entry['_id'])  # Convert ObjectId to string

        serializer = LeaderboardSerializer(leaderboard_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
