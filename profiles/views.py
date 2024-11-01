from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.models import User
from .forms import ProfileEditForm, LoginForm, UserRegistrationForm
from .models import Profile


class ProfileView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)  # Fetch Profile using the user

        context = {
            'profile': profile,
            'questions': profile.questions,
            'answers': profile.answers,
            'comments': profile.comments,
            'score': profile.score,
            'title': f"DjangoInquiro - {user.username}'s Profile"
        }
        return render(request, 'profiles/profile.html', context)


@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    def get(self, request):
        # Retrieve the user's profile
        profile = get_object_or_404(Profile, user=request.user)

        # Populate the form with the profile data
        form = ProfileEditForm(instance=profile, user=request.user)

        return render(request, 'profiles/edit_profile.html', {'form': form, 'title': f'Edit Profile: {request.user}'})

    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)  # Redirect to the profile page

        return render(request, 'profiles/edit_profile.html', {'form': form, 'title': 'Edit Profile'})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'profiles/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('question_list')  # Redirect to the question list or another page after login
            else:
                form.add_error(None, "Invalid username or password")
        return render(request, 'profiles/login.html', {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('question_list')  # Redirect to the main question list or home page after logout


class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'profiles/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('question_list')  # Redirect to the main question list
        return render(request, 'profiles/register.html', {'form': form})