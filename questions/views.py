from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from .forms import QuestionForm
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
        context['answers'] = Answer.objects.filter(question=self.object).order_by('created_at')
        # Get all comments related to the question
        context['comments'] = Comment.objects.filter(question=self.object).order_by('created_at')

        # Set the title based on the question's title
        context['title'] = f"DjangoInquiro - {self.object.title}"

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


class AskQuestionView(View):
    def get(self, request):
        # Initialize an empty form for the GET request
        form = QuestionForm()
        return render(request, 'questions/ask_question.html', {'form': form, 'title': 'Ask a Question'})

    def post(self, request):
        # Populate the form with POST data
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Create a new question without saving to the database yet
            question = form.save(commit=False)
            question.user = request.user  # Set the user who asked the question
            question.save()  # Save the question to the database
            form.save_m2m()  # Save any tags or many-to-many relationships

            return redirect('question_detail', slug=question.slug)  # Redirect to the question's detail page

        # If the form is invalid, render the form with errors
        return render(request, 'questions/ask_question.html', {'form': form, 'title': 'Ask a Question'})
