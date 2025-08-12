from django.db import models
from userprofile.models import CustomUser
# Create your models here.


class ProjectStatus(models.TextChoices):
    PLANNING = 'planning', 'Planning'
    ACTIVE = 'active', 'Active'
    ON_HOLD = 'on_hold', 'On Hold'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'

class ProjectModel(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.PLANNING
    )
    team_members = models.ManyToManyField(CustomUser, related_name='projects')

    def __str__(self):
        return self.title

class TaskStatus(models.TextChoices):
      OPEN = 'open', 'Open'
      WORKING = 'working', 'Working'
      REVIEW = 'review', 'Review'
      WAITING_QA = 'waiting_qa', 'Waiting QA'
      AWAITING_RELEASE = 'awaiting_release', 'Awaiting Release'
      CLOSED = 'closed', 'Closed'

class TaskModel(models.Model):
      title = models.CharField(max_length=25)
      description = models.TextField()
      status = models.CharField(
          max_length=30,
          choices=TaskStatus.choices,
          default=TaskStatus.OPEN,
      )
      project = models.ForeignKey(
          ProjectModel,
          on_delete=models.CASCADE,
          related_name='tasks'
      )
      assignee = models.ForeignKey(
          CustomUser,
          on_delete=models.SET_NULL,
          null=True,
          blank=True,
          related_name='tasks'
      )

      def __str__(self):
          return self.title