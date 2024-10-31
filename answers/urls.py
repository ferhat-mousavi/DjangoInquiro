# answers/urls.py
from django.urls import path
from .views import WriteAnswerView

urlpatterns = [
    path('write/<int:question_id>/', WriteAnswerView.as_view(), name='write_answer'),
]
