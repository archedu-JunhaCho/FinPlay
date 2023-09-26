from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.widgets import NumberInput, TextInput
from django import forms
from .models import *


class updateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'name', 'email', 'first_name', 'last_name')
