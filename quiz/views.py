from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import QUIZ
from .serializers import QuizSerializer
import random

# Create your views here.

@api_view(['GET'])
def helloAPI(request):
    return Response('Hello, world!')

    
@api_view(['GET'])
def randomQuiz(request, id):
    totlaQuizs = QUIZ.objects.all()
    randomQuizs = random.sample(list(totlaQuizs), id)
    serializers = QuizSerializer(randomQuizs, many=True)
    return Response(serializers.data)