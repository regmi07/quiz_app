from django.urls import path
from .views import create_question, getQuestions, createQuizAttempt, submitQuiz

urlpatterns = [
    path('question/create/', create_question, name='create-question'),
    path('attempt/create/', createQuizAttempt, name='create-quiz-attempt'),
    path('attempt/submit/', submitQuiz, name='submit-quiz-attempt'),
]
