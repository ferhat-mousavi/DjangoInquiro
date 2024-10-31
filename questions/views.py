from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

from .models import Question
from answers.models import Answer
from comments.models import Comment


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'questions/question_detail.html'
    context_object_name = 'question'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We get all the answers according to the question
        context['answers'] = Answer.objects.filter(question=self.object).order_by('-created_at')
        # Get all comments related to the question
        context['comments'] = Comment.objects.filter(question=self.object).order_by('-created_at')
        return context


@method_decorator(require_POST, name='dispatch')
class QuestionVoteView(View):
    def post(self, request, id, vote_type):
        question = get_object_or_404(Question, id=id)

        if vote_type == 'up':
            question.up_vote()
        elif vote_type == 'down':
            question.down_vote()

        question.save()
        return redirect('question_detail', slug=question.slug)
