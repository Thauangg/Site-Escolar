from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Professor

class ProfessorRegistrationForm(UserCreationForm):
    class Meta:
        model = Professor
        fields = ('username', 'email', 'password1', 'password2')
