# questions/forms.py
from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'category', 'tags']  # Adjust fields as needed
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter question title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your question'}),
            'category': forms.Select(attrs={'class': 'form-control'}),  # Category dropdown
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Question Title',
            'content': 'Question Content',
            'category': 'Select Category',
            'tags': 'Tags (optional)',
        }
