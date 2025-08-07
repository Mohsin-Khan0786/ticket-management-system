from django import forms
from .models import CustomUser,Profile


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

    class Meta:
        model = Profile
        fields = ['image', 'phone', 'role', 'email']

      