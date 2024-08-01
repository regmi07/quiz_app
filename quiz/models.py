from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Question(models.Model):
    question = models.TextField()
    category = models.TextField()
    level = models.TextField()


class Option(models.Model):
    option = models.TextField()
    isCorrect = models.BooleanField()
    questionId = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='options')


class QuizAttempt(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    attempted_date = models.DateTimeField(auto_now_add=True)
    total_score = models.IntegerField(default=0)


class QuestionAttempt(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt, on_delete=models.CASCADE, related_name="questions_attempt")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selectedOption = models.ForeignKey(
        Option, blank=True, null=True, on_delete=models.CASCADE)
    isCorrect = models.BooleanField(default=False)
