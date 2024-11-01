# comments/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from questions.models import Question
from answers.models import Answer
from .models import Comment
from .forms import CommentForm


class WriteCommentView(View):
    def get(self, request, model_type, model_id):
        if model_type == 'question':
            parent_object = get_object_or_404(Question, id=model_id)
            title = f"Comment on Question: {parent_object.title}"
        elif model_type == 'answer':
            parent_object = get_object_or_404(Answer, id=model_id)
            title = f"Comment on Answer to: {parent_object.question.title}"
        else:
            return redirect('question_list')  # Geçersiz model_type için

        form = CommentForm()
        return render(request, 'comments/write_comment.html', {
            'form': form,
            'parent_object': parent_object,
            'model_type': model_type,
            'title': title
        })

    def post(self, request, model_type, model_id):
        if model_type == 'question':
            parent_object = get_object_or_404(Question, id=model_id)
        elif model_type == 'answer':
            parent_object = get_object_or_404(Answer, id=model_id)
        else:
            return redirect('question_list')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user

            if model_type == 'question':
                comment.question = parent_object
            elif model_type == 'answer':
                comment.answer = parent_object

            comment.save()
            if model_type == 'question':
                return redirect('question_detail', slug=parent_object.slug)
            else:
                return redirect('question_detail', slug=parent_object.question.slug)

        return render(request, 'comments/write_comment.html', {
            'form': form,
            'parent_object': parent_object,
            'model_type': model_type
        })
