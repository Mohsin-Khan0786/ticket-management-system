from django.db import models
from projectmanagement.models import ProjectModel, TaskModel
from userprofile.models import CustomUser
# Create your models here.
class Documents(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=30)
    file = models.FileField(upload_to='documents/')
    version = models.CharField(max_length=15, default='1.0')
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Comments(models.Model):
    text = models.TextField(max_length=300)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE, related_name='comments')
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"
    
    class Meta:
        ordering = ['-created_at']
      