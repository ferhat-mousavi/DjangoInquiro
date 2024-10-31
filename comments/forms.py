# answers/forms.py
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Only content field for the comment
        widgets = {
            'content': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Type your comment here...'}),
        }
        labels = {
            'content': 'Your Comment',
        }
