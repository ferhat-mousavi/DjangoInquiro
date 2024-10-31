from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # The user who wrote the comment

    # Nullable ForeignKey fields to either Question or Answer
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    answer = models.ForeignKey('answers.Answer', on_delete=models.CASCADE, null=True, blank=True, related_name='comments')

    content = models.TextField()  # Content of the comment

    created_at = models.DateTimeField(default=timezone.now)  # Timestamp for when the comment was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the comment was last updated

    def __str__(self):
        if self.question:
            return f"Comment by {self.user.username} on Question: {self.question.title}"
        elif self.answer:
            return f"Comment by {self.user.username} on Answer to Question: {self.answer.question.title}"
        return f"Comment by {self.user.username}"

    def save(self, *args, **kwargs):
        # Ensure that the comment is linked to either a Question or an Answer, but not both
        if not (self.question or self.answer):
            raise ValidationError("A comment must be linked to either a question or an answer.")
        if self.question and self.answer:
            raise ValidationError("A comment cannot be linked to both a question and an answer.")

        # Save the comment after validation
        super(Comment, self).save(*args, **kwargs)