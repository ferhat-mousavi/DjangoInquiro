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
        elif model_type == 'answer':
            parent_object = get_object_or_404(Answer, id=model_id)
        else:
            return redirect('question_list')  # Geçersiz model_type için

        form = CommentForm()
        return render(request, 'comments/write_comment.html', {
            'form': form,
            'parent_object': parent_object,
            'model_type': model_type
        })

    def post(self, request, model_type, model_id):
        print(model_type, model_id)
        if model_type == 'question':
            parent_object = get_object_or_404(Question, id=model_id)
        elif model_type == 'answer':
            parent_object = get_object_or_404(Answer, id=model_id)
        else:
            return redirect('question_list')

        print(parent_object)

        form = CommentForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print("1")
            comment = form.save(commit=False)
            print("2")
            comment.user = request.user

            if model_type == 'question':
                comment.question = parent_object
            elif model_type == 'answer':
                comment.answer = parent_object

            print(comment.question, comment.answer)
            comment.save()
            if model_type == 'question':
                return redirect('question_detail', slug=parent_object.slug)
            else:
                return redirect('question_detail', slug=parent_object.question.slug)

        print("Form errors:", form.errors)

        return render(request, 'comments/write_comment.html', {
            'form': form,
            'parent_object': parent_object,
            'model_type': model_type
        })
