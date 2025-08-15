from django import forms
from .models import CustomUser, Profile
from projectmanagement.models import TaskModel
from django.core.validators import RegexValidator

class RegistrationForm(forms.ModelForm):
      password=forms.CharField(widget=forms.PasswordInput)
      username = forms.CharField(required=False)
      class Meta:
            model=CustomUser
            fields=['email','username','password']
 
class LoginForm(forms.ModelForm):
      password=forms.CharField(widget=forms.PasswordInput)

      class Meta:
            model=CustomUser
            fields=['email','password']

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(
    required=True,
    validators=[
    RegexValidator(
            regex='^\d{12}$',
            message='Phone number must be exactly 12 digits.'
            )
        ]
    )

    class Meta:
        model = Profile
        fields = ['image', 'phone', 'role', 'email']

class ProfileTaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ['title', 'description', 'status', 'project']