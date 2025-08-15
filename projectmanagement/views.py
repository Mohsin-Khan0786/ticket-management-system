from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Count, Q
from .models import TaskModel, ProjectModel, ProjectStatus, TaskStatus
from userprofile.models import CustomUser
from attachments_and_comments.models import Comments
from attachments_and_comments.forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()  

class TaskListView(View):
    def get(self, request):
        tasks = TaskModel.objects.all()
        status_filter = request.GET.get('status')
        assignee_filter = request.GET.get('assignee')

        if status_filter:
            tasks = tasks.filter(status=status_filter)

        if assignee_filter:
            tasks = tasks.filter(assignee_id=assignee_filter)

        context = {
            'tasks': tasks,
            'status_choices': TaskStatus.choices,
            'users': User.objects.all(),
            'projects': ProjectModel.objects.all(),
            'all_statuses': TaskStatus.choices,
        }
        return render(request, 'tasks/task_list.html', context)


class TaskCreateView(View):
    def get(self, request, project_id):
        context = {
            'project_id': project_id,
            'status_choices': TaskStatus.choices,
            'users': User.objects.all(),
        }
        return render(request, 'tasks/task_create.html', context)

    def post(self, request, project_id):
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')  
        assignee_id = request.POST.get('assignee')

        project = get_object_or_404(ProjectModel, id=project_id)
        assignee = get_object_or_404(User, id=assignee_id)

        TaskModel.objects.create(
            title=title,
            description=description,
            status=status,
            project=project,
            assignee=assignee
        )
        return redirect(reverse('task_list'))


class TaskDetailView(View):
    def get(self, request, task_id):
        task = get_object_or_404(TaskModel, id=task_id)
        form = CommentForm()
        return render(request, 'tasks/task_detail.html', {
            'task': task,
            'comment_form': form,
            'all_statuses': TaskStatus.choices,
        })


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, task_id):
        task = get_object_or_404(TaskModel, id=task_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            Comments.objects.create(
                text=form.cleaned_data['text'],
                author=request.user,
                task=task,
                project=task.project,
            )
        return redirect(reverse('task_detail', kwargs={'task_id': task.id}))


class TaskChangeStatusView(View):
    def post(self, request, task_id):
        task = get_object_or_404(TaskModel, id=task_id)
        new_status = request.POST.get('new_status')
        valid_values = [value for value, _ in TaskStatus.choices]
        if new_status in valid_values:
            task.status = new_status
            task.save(update_fields=['status'])
    
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
        if next_url:
            return redirect(next_url)
        return redirect(reverse('task_detail', kwargs={'task_id': task.id}))


class TaskUpdateView(View):
    def get(self, request, task_id):
        task = get_object_or_404(TaskModel, id=task_id)
        context = {
            'task': task,
            'users': User.objects.all(),
        }
        return render(request, 'tasks/task_update.html', context)

    def post(self, request, task_id):
        task = get_object_or_404(TaskModel, id=task_id)
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')

        assignee_id = request.POST.get('assignee')
        task.assignee = get_object_or_404(User, id=assignee_id)

        task.save()
        return redirect(reverse('task_list'))


class TaskDeleteView(View):
    def get(self, request, task_id):
        task = get_object_or_404(TaskModel, id=task_id)
        return render(request, 'tasks/task_delete.html', {'task': task})

    def post(self, request, task_id):
        task = get_object_or_404(TaskModel, id=task_id)
        task.delete()
        return redirect(reverse('task_list'))


class ProjectDetailView(View):
    def get(self, request, project_id):
        try:
            project = ProjectModel.objects.get(id=project_id)
        except ProjectModel.DoesNotExist:
            return HttpResponseNotFound("Project not found")
        return render(request, 'tasks/project_detail.html', {'project': project})


class ProjectUpdateView(View):
    def get(self, request, project_id):
        project = get_object_or_404(ProjectModel, id=project_id)
        return render(request, 'tasks/project_update.html', {
            'project': project,
            'users': CustomUser.objects.all()
        })

    def post(self, request, project_id):
        project = get_object_or_404(ProjectModel, id=project_id)
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')

        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date:
            project.start_date = start_date
        if end_date:
            project.end_date = end_date

        members = request.POST.getlist('team_members')
        project.team_members.set(members)

        project.save()
        return redirect(reverse('project_detail', kwargs={'project_id': project.id}))


class ProjectDeleteView(View):
    def get(self, request, project_id):
        project = get_object_or_404(ProjectModel, id=project_id)
        return render(request, 'tasks/project_delete.html', {'project': project})

    def post(self, request, project_id):
        project = get_object_or_404(ProjectModel, id=project_id)
        project.delete()
        return redirect(reverse('project_list'))


class ProjectListView(View):
    def get(self, request):
        projects = (
            ProjectModel.objects.all()
            .annotate(
                open_tasks=Count('tasks', filter=Q(tasks__status=TaskStatus.OPEN))
            )
        )
        return render(request, 'tasks/project_list.html', {'projects': projects})


class ProjectCreateView(View):
    def get(self, request):
        return render(request, 'tasks/project_create.html')

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        project = ProjectModel.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date or None,
        )

        if request.user.is_authenticated:
            project.team_members.add(request.user)
        members = request.POST.getlist('team_members')
        if members:
            project.team_members.set(members)
        return redirect(reverse('project_detail', kwargs={'project_id': project.id}))
