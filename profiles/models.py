from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from questions.models import Question
from answers.models import Answer
from comments.models import Comment


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Additional fields, if needed (e.g., bio, avatar, etc.)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    @property
    def questions(self):
        """Return all questions posted by the user."""
        return Question.objects.filter(user=self.user)

    @property
    def answers(self):
        """Return all answers posted by the user."""
        return Answer.objects.filter(user=self.user)

    @property
    def comments(self):
        """Return all comments posted by the user."""
        return Comment.objects.filter(user=self.user)

    @property
    def score(self):
        """Calculate the total score of the user based on their questions, answers, and accepted answers."""
        # Sum of scores from user's questions
        question_score = self.questions.aggregate(score=Sum('score'))['score'] or 0

        # Sum of scores from user's answers
        answer_score = self.answers.aggregate(score=Sum('score'))['score'] or 0

        # Bonus for accepted answers
        accepted_answer_bonus = self.answers.filter(question__accepted_answer=models.F('id')).count() * 10

        # Total score
        total_score = question_score + answer_score + accepted_answer_bonus
        return total_score
