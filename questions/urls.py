from django.urls import path
from .views import QuestionDetailView, QuestionVoteView

urlpatterns = [
    path('<str:slug>/', QuestionDetailView.as_view(), name='question_detail'),
    path('<int:id>/vote/<str:vote_type>/', QuestionVoteView.as_view(), name='question_vote'),
]