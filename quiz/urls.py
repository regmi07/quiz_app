from django.urls import path
from .views import create_question, getQuestions

urlpatterns = [
    path('question/create/', create_question, name='create-question')
]
