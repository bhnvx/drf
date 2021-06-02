from django.db.models import fields
from rest_framework import serializers
from .models import QUIZ

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = QUIZ
        fields = ('title', 'body', 'answer')