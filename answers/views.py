# answers/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from questions.models import Question
from .models import Answer
from .forms import AnswerForm


class WriteAnswerView(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        form = AnswerForm()
        return render(request, 'answers/write_answer.html', {'question': question, 'form': form})

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.user  # Logged in user
            answer.save()
            return redirect('question_detail', slug=question.slug)
        return render(request, 'answers/write_answer.html', {'question': question, 'form': form})


@method_decorator(require_POST, name='dispatch')
class AnswerVoteView(View):
    def post(self, request, id, vote_type):
        answer = get_object_or_404(Answer, id=id)

        if vote_type == 'up':
            answer.up_vote()
        elif vote_type == 'down':
            answer.down_vote()

        answer.save()
        # Redirect to the question detail page where the answer is displayed
        return redirect('question_detail', slug=answer.question.slug)