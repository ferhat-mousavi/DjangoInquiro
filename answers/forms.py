# answers/forms.py
from django import forms
from .models import Answer


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']  # Only content field for the answer
        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Type your answer here...'}),
        }
        labels = {
            'content': 'Your Answer',
        }