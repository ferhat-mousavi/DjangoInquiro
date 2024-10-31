from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.views.decorators.http import require_POST


def question_detail(request, slug):
    # Get the specific question by ID or return 404 if not found
    question = get_object_or_404(Question, slug=slug)

    # Pass the question object to the template
    return render(request, 'questions/question_detail.html', {'question': question})


@require_POST
def question_vote(request, id, vote_type):
    question = get_object_or_404(Question, id=id)

    if vote_type == 'up':
        question.up_vote()
    elif vote_type == 'down':
        question.down_vote()

    question.save()
    return redirect('question_detail', slug=question.slug)