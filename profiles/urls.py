from django.urls import path
from .views import ProfileView, EditProfileView, LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Login URL
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout URL
    path('edit/', EditProfileView.as_view(), name='edit_profile'),
    path('<str:username>/', ProfileView.as_view(), name='profile'),
]
