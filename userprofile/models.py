from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
# Create your models here.

class RoleChoice(models.TextChoices):
      MANAGER='manager','Manager'
      DEVELOPER='developer','Developer'
      QA='qa','Qa'
      DESIGNER='designer','Designer'

class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  
    objects = CustomUserManager()

    def __str__(self):
        return self.email 
       
class Profile(models.Model):
    user= models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg',upload_to='profile_pics/')
    phone=models.CharField(max_length=20)
    role=models.CharField(max_length=20, choices=RoleChoice.choices, default=RoleChoice.MANAGER)

    def __str__(self):
        return f"{self.user} - {self.role}"


     