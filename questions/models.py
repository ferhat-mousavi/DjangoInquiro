from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


class QuestionVote(models.Model):
    VOTE_TYPES = [
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_votes')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='vote_entries')
    vote_type = models.CharField(max_length=4, choices=VOTE_TYPES)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'question')  # Ensures that a user can only vote once per question

    def __str__(self):
        return f"{self.user.username} - {self.vote_type} on {self.question.title}"


class QuestionReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_reports')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='report_entries')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'question')  # Ensures that a user can only report once per question

    def __str__(self):
        return f"{self.user.username} reported {self.question.title}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('answered', 'Answered'),
    ]

    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    content = models.TextField()  # Markdown content will be stored here
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='questions')
    up_votes = models.IntegerField(default=0)  # Number of UP votes
    down_votes = models.IntegerField(default=0)  # Number of DOWN votes
    score = models.IntegerField(default=0)  # Net score of the question
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    last_activity = models.DateTimeField(default=timezone.now)
    reports = models.IntegerField(default=0)  # Number of reports from users
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_questions', blank=True)
    accepted_answer = models.ForeignKey(
        'answers.Answer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_in_question'
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def up_vote(self, user):
        """Increase the up_votes count by 1, only if the user has not already upvoted."""
        if user.is_authenticated and not QuestionVote.objects.filter(user=user, question=self, vote_type='up').exists():
            QuestionVote.objects.create(user=user, question=self, vote_type='up')
            self.up_votes += 1
            self.score = self.up_votes - self.down_votes
            self.save()

    def down_vote(self, user):
        """Increase the down_votes count by 1, only if the user has not already downvoted."""
        if user.is_authenticated and not QuestionVote.objects.filter(user=user, question=self, vote_type='down').exists():
            QuestionVote.objects.create(user=user, question=self, vote_type='down')
            self.down_votes += 1
            self.score = self.up_votes - self.down_votes
            self.save()

    def update_last_activity(self):
        """Update the last activity timestamp to the current time"""
        self.last_activity = timezone.now()
        self.views += 1
        self.save()

    def report(self, user):
        """Increase the report count by 1, only if the user has not already reported."""
        if user.is_authenticated and not QuestionReport.objects.filter(user=user, question=self).exists():
            QuestionReport.objects.create(user=user, question=self)
            self.reports += 1
            self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)