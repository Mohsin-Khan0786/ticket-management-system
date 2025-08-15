from django.urls import path
from .views import DocumentUploadView, DocumentListView

urlpatterns = [
    path('projects/<int:project_id>/documents/upload/', DocumentUploadView.as_view(), name='upload_document'),
    path('projects/<int:project_id>/documents/', DocumentListView.as_view(), name='document_list'),
]


