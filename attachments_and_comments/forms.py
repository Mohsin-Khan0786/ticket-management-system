from django import forms
from .models import Documents, Comments


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['name', 'description', 'file', 'version']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']

