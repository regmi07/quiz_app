from rest_framework import serializers

from .models import Option, Question, QuestionAttempt, QuizAttempt


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option', 'isCorrect']
        required = ['option', 'isCorrect']


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


class QuestionAttemptSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = QuestionAttempt
        fields = ['id', 'question', 'isCorrect']


class QuizAttemptSerializer(serializers.ModelSerializer):
    questions_attempt = QuestionAttemptSerializer(many=True, read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ['id', 'attempted_date', 'questions_attempt', 'total_score']

    def create(self, validated_data):
        user = self.context['request'].user
        quiz_attempt = QuizAttempt.objects.create(user=user)

        questions = list(Question.objects.all().order_by('?')[:20])

        for question in questions:
            QuestionAttempt.objects.create(
                question=question, attempt=quiz_attempt)

        return quiz_attempt


class AnswerSerializer(serializers.Serializer):
    question_attempt_id = serializers.IntegerField()
    selected_option_id = serializers.IntegerField()


class QuizSubmissionSerializer(serializers.Serializer):
    quiz_attempt_id = serializers.IntegerField()
    answers = AnswerSerializer(many=True)

    def update(self, instance, validated_data):
        """
            updates the instance of Quiz Attempt
        """
        answers = validated_data.get('answers')
        total_score = 0
        for answer in answers:
            question_attempt_id = answer.get('question_attempt_id')
            selected_option_id = answer.get('selected_option_id')
            try:
                questionAttempt = QuestionAttempt.objects.get(
                    id=question_attempt_id)
            except QuestionAttempt.DoesNotExist:
                continue
            selectedOption = Option.objects.get(id=selected_option_id)
            # update selected option of question attempt model
            questionAttempt.selectedOption = selectedOption
            # update isCorrect option of question attempt model
            questionAttempt.isCorrect = selectedOption.isCorrect
            # save changes to databse
            questionAttempt.save()

            # check if user selected correct option
            if selectedOption.isCorrect:
                total_score += 1

        # update total_score in quiz attempt
        instance.total_score = total_score
        instance.save()
        return {'score': total_score}
