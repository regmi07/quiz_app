from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .serializers import QuestionSerializer
from django.http import JsonResponse, HttpResponseNotFound


# Create your views here.
@api_view(['POST'])
def create_question(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Question created successfully!", "status": HTTP_201_CREATED})
    return JsonResponse(serializer.data, status=HTTP_400_BAD_REQUEST)
