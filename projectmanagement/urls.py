from django.urls import path
from .views import (
    TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskDetailView, AddCommentView, TaskChangeStatusView,
    ProjectDetailView, ProjectUpdateView, ProjectDeleteView, ProjectListView, ProjectCreateView,
)

urlpatterns = [

    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/create/', ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:project_id>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/update/<int:project_id>/', ProjectUpdateView.as_view(), name='project_update'),
    path('projects/delete/<int:project_id>/', ProjectDeleteView.as_view(), name='project_delete'),
    
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/<int:project_id>/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:task_id>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('tasks/<int:task_id>/status/', TaskChangeStatusView.as_view(), name='task_change_status'),
    path('tasks/update/<int:task_id>/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/delete/<int:task_id>/', TaskDeleteView.as_view(), name='task_delete'),

    

]

