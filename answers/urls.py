# answers/urls.py
from django.urls import path
from .views import WriteAnswerView, AnswerVoteView

urlpatterns = [
    path('write/<int:question_id>/', WriteAnswerView.as_view(), name='write_answer'),
    path('vote/<int:id>/<str:vote_type>/', AnswerVoteView.as_view(), name='answer_vote'),
]
