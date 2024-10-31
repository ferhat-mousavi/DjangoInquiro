# comments/urls.py
from django.urls import path
from .views import WriteCommentView

urlpatterns = [
    path('write/<str:model_type>/<int:model_id>/', WriteCommentView.as_view(), name='write_comment'),
]
