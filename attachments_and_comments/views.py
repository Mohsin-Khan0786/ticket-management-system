from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from projectmanagement.models import ProjectModel, TaskModel
from .models import Documents, Comments
from .forms import DocumentForm
from django.views import View

# Create your views here.

class DocumentUploadView(LoginRequiredMixin, View):
    def get(self, request, project_id):
        project = get_object_or_404(ProjectModel, pk=project_id)
        form = DocumentForm()
        return render(
            request,
            'attachments_and_comments/upload_document.html',
            {
                'form': form,
                'project': project,
            },
        )
    def post(self, request, project_id):
        project = get_object_or_404(ProjectModel, pk=project_id)
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.project = project
            document.save()
            return redirect('project_detail', project_id=project_id)
        return render(request, 'attachments_and_comments/upload_document.html', {
            'form': form,
            'project': project
        })
class DocumentListView(LoginRequiredMixin, View):
    def get(self, request, project_id):
        project = get_object_or_404(ProjectModel, pk=project_id)
        documents = Documents.objects.filter(project=project)
        return render(
            request,
            'attachments_and_comments/document_list.html',
            {
                'project': project,
                'documents': documents,
            },
        )
          
