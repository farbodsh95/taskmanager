from .models import Task
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }
