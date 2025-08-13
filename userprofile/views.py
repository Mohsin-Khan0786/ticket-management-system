from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, RoleChoice
from .forms import RegistrationForm, LoginForm, ProfileForm, ProfileTaskForm
from projectmanagement.models import TaskModel, TaskStatus, ProjectModel
from django.utils import timezone

class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')
        return redirect('login')

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
    User = get_user_model()
    def get(self, request):
        login_url = '/login/'
        profile, created = Profile.objects.get_or_create(user=request.user)
        user_tasks = TaskModel.objects.filter(assignee=request.user).select_related('project')
        create_form = ProfileTaskForm()
        update_form = ProfileTaskForm()
        if getattr(request.user, 'profile', None) and request.user.profile.role == RoleChoice.MANAGER:
            available_projects = ProjectModel.objects.all()
        else:
            available_projects = request.user.projects.all()

        return render(request, 'userprofile/profile.html', {
            'profile': profile,
            'tasks': user_tasks,
            'create_form': create_form,
            'update_form': update_form,
            'status_choices': TaskStatus.choices,
            'available_projects': available_projects,
            'all_users': self.User.objects.all(),
        })

    def post(self, request):
        action = request.POST.get('action')
        if action == 'create':

            project = None
            project_id = request.POST.get('project')
            if project_id:
                project = ProjectModel.objects.filter(id=project_id).first()
            title = request.POST.get('title')
            description = request.POST.get('description')
            status = request.POST.get('status') or TaskStatus.OPEN
          
            is_manager = getattr(request.user, 'profile', None) and request.user.profile.role == RoleChoice.MANAGER
            assignee = request.user
            if is_manager:
                assignee_id = request.POST.get('assignee')
                if assignee_id:
                    assignee = self.User.objects.filter(id=assignee_id).first() or request.user

            if project and title:
           
                project.team_members.add(assignee)
                TaskModel.objects.create(
                    title=title,
                    description=description or '',
                    status=status,
                    project=project,
                    assignee=assignee,
                )
            return redirect('profile')
        if action == 'update':
            task_id = request.POST.get('task_id')
            task = TaskModel.objects.filter(id=task_id, assignee=request.user).first()
            if task:
                form = ProfileTaskForm(request.POST, instance=task)
                if form.is_valid():
                    form.save()
            return redirect('profile')
        if action == 'delete':
            task_id = request.POST.get('task_id')
            TaskModel.objects.filter(id=task_id, assignee=request.user).delete()
            return redirect('profile')
        return redirect('profile')


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
