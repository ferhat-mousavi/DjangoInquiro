from django.urls import path
from .views import ProfileView, EditProfileView

urlpatterns = [
    path('edit/', EditProfileView.as_view(), name='edit_profile'),
    path('<str:username>/', ProfileView.as_view(), name='profile'),
]
