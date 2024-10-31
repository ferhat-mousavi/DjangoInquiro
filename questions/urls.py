from django.urls import path
from . import views

urlpatterns = [
    path('<str:slug>/', views.question_detail, name='question_detail'),
    path('<int:id>/vote/<str:vote_type>/', views.question_vote, name='question_vote'),
]