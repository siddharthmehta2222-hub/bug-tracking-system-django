from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Bug


# ==================================================
# USER SIGNUP FORM
# ==================================================
class UserSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
# ==================================================
# BUG FORM
# ==================================================
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