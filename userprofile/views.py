from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import RegistrationForm, LoginForm, ProfileForm

class RegistrationView(View):
    def get(self, request):
        return render(request, 'userprofile/register.html', {'form': RegistrationForm()})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            return redirect('login')
        return render(request, 'userprofile/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        return render(request, 'userprofile/login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        user = authenticate(email=form.data['email'], password=form.data['password'])
        if user:
            login(request, user)
            return redirect('profile')
        return render(request, 'userprofile/login.html', {'form': form, 'error': 'Invalid credentials'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        return render(request, 'userprofile/profile.html', {'profile': profile})


class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        form = ProfileForm(instance=profile, initial={'email': request.user.email})
        return render(request, 'userprofile/update.html', {'form': form})

    def post(self, request):
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            request.user.email = form.cleaned_data.get('email')
            request.user.save()
            return redirect('profile')
        return render(request, 'userprofile/update.html', {'form': form})
