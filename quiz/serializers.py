from rest_framework import serializers

from .models import Option, Question


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option', 'isCorrect', 'questioId']
        required = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'category', 'level', 'options']
        required = ['question', 'category', 'level', 'options']

    def create(self, validated_data):
        options = validated_data.pop('options')
        question = Question.objects.create(**validated_data)

        for option in options:
            Option.objects.create(questionId=question, **option)

        return question
