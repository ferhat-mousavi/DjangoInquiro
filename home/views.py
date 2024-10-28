from django.shortcuts import render
from django.views.generic import ListView
from questions.models import Question


class QuestionListView(ListView):
    model = Question
    template_name = 'home/question_list.html'  # Template file path
    context_object_name = 'questions'  # Context variable name for the template
    ordering = ['-created_at']  # Order questions by creation date (newest first)
    paginate_by = 10  # Number of questions per page
