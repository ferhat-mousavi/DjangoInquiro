from django.shortcuts import render
from django.views.generic import ListView
from questions.models import Question


class QuestionListView(ListView):
    model = Question
    template_name = 'home/question_list.html'  # Template file path
    context_object_name = 'questions'  # Context variable name for the template
    ordering = ['-created_at']  # Order questions by creation date (newest first)
    paginate_by = 10  # Number of questions per page

    def get_context_data(self, **kwargs):
        # Get the base context data from the parent class
        context = super().get_context_data(**kwargs)

        # Determine the page number
        page_number = self.request.GET.get('page', 1)

        # Set the title based on the page number
        if int(page_number) > 1:
            context['title'] = f"DjangoInquiro Page {page_number}"
        else:
            context['title'] = "DjangoInquiro"

        return context