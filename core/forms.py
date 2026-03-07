from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Bug


class UserSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'role', 'password1', 'password2']

class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = [
            'title',
            'description',
            'project',
            'assigned_to',
            'priority',
            'status'
        ]


class UserSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email','role','password1','password2']

from .models import Bug

class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = [
            'title',
            'description',
            'project',
            'assigned_to',
            'priority',
            'status'
        ]        

