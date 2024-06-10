

from rest_framework import serializers

class LeaderboardSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    quiz_id = serializers.IntegerField()
    grade = serializers.FloatField()
    timestamp = serializers.DateTimeField()
    correct = serializers.IntegerField()
    false = serializers.IntegerField()
