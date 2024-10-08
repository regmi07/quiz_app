from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from .serializers import QuestionSerializer, QuizAttemptSerializer, QuizSubmissionSerializer
from django.http import Http404, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .models import Question, QuizAttempt

# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_question(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Question created successfully!", "status": HTTP_201_CREATED})
    return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getQuestions(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(data=questions)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createQuizAttempt(request):
    serializer = QuizAttemptSerializer(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submitQuiz(request):
    serializer = QuizSubmissionSerializer(data=request.data)
    if serializer.is_valid():
        quiz_attempt_id = serializer.validated_data['quiz_attempt_id']
        try:
            quizAttempt = QuizAttempt.objects.get(
                id=quiz_attempt_id, user=request.user)

            score = serializer.update(quizAttempt, serializer.validated_data)
            return Response(score, status=HTTP_201_CREATED)

        except QuizAttempt.DoesNotExist:
            return JsonResponse({'message': 'attempt does not exists!'}, status=HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
