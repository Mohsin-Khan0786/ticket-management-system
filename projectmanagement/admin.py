from django.contrib import admin
from .models import ProjectModel


# Register your models here.
class ProjectModelAdmin(admin.ModelAdmin):
    list_display=['title','start_date','end_date']
    filter_horizontal=['team_members']




admin.site.register(ProjectModel,ProjectModelAdmin)
