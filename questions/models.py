from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


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
    tags = models.ManyToManyField(Tag, related_name='questions')
    score = models.IntegerField(default=0)  # To keep track of UP and DOWN votes
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    last_activity = models.DateTimeField(default=timezone.now)
    reports = models.IntegerField(default=0)  # Number of reports from users
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_questions', blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def up_vote(self):
        """Increase the question's score by 1 for an UP vote"""
        self.score += 1
        self.save()

    def down_vote(self):
        """Decrease the question's score by 1 for a DOWN vote"""
        self.score -= 1
        self.save()

    def increment_views(self):
        """Increase the view count by 1 each time the question is viewed"""
        self.views += 1
        self.save()

    def update_last_activity(self):
        """Update the last activity timestamp to the current time"""
        self.last_activity = timezone.now()
        self.save()

    def report(self):
        """Increase the report count by 1 each time a user reports the question"""
        self.reports += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)