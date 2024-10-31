from django.urls import path
from .views import QuestionDetailView, QuestionVoteView, AskQuestionView

urlpatterns = [
    path('ask/', AskQuestionView.as_view(), name='ask_question'),
    path('<str:slug>/', QuestionDetailView.as_view(), name='question_detail'),
    path('<int:id>/vote/<str:vote_type>/', QuestionVoteView.as_view(), name='question_vote'),
]