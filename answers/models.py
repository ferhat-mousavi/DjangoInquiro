from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Answer(models.Model):
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, related_name='answers')  # The question being answered
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')  # The user who wrote the answer
    content = models.TextField()  # Markdown content of the answer

    up_votes = models.IntegerField(default=0)  # Number of UP votes
    down_votes = models.IntegerField(default=0)  # Number of DOWN votes
    score = models.IntegerField(default=0)  # Net score of the answer
    reports = models.IntegerField(default=0)  # Number of times the answer has been reported

    created_at = models.DateTimeField(default=timezone.now)  # Timestamp for when the answer was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the answer was last updated

    def __str__(self):
        return f"Answer to '{self.question.title}' by {self.user.username}"

    def up_vote(self):
        """Increase the up_vote count by 1"""
        self.up_votes += 1
        self.score = self.up_votes - self.down_votes
        self.save()

    def down_vote(self):
        """Increase the down_vote count by 1"""
        self.down_votes += 1
        self.score = self.up_votes - self.down_votes
        self.save()

    def report(self):
        """Increase the report count by 1"""
        self.reports += 1
        self.save()
