from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile



class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email']



class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['photo','date_of_birth']