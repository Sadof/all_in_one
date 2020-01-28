from django.forms import ModelForm, TextInput, Textarea, SelectMultiple, DateInput, FileInput, PasswordInput, EmailInput, DateTimeInput
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _


class PostAddForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title","slug","text","tag"]
        labels={
            "slug": _("Slug (Человекопонятный url для поста. Необязательный для заполнения. При отсутствии автоматически генерируется )")
        }
        widgets = {
            'title': TextInput(attrs={"class":"form-control"}),
            'slug': TextInput(attrs={"class":"form-control"} ),
            "text": Textarea(attrs={"class": "form-control"}),
            "tag": SelectMultiple(attrs={"class":"form-control"})
        }


    def clean_slug(self):
        new_slug = self.cleaned_data["slug"].lower()
        if Post.objects.filter(slug__iexact=new_slug).count() and self.instance.slug == Post.objects.filter(slug__iexact=new_slug):
            raise ValidationError("This slug already exist!")
        return new_slug




class TagAddForm(ModelForm):
    class Meta:
        model = Tag
        fields = ["title","slug"]
        widgets = {
            "title": TextInput(attrs={"class":"form-control"}),
            "slug": TextInput(attrs={"class":"form-control"}),
        }


    def clean_slug(self):
        new_title = self.cleaned_data['title'].lower()
        new_slug = self.cleaned_data['slug'].lower()
        print(self.instance.slug)
        if new_title == "add":
            raise ValidationError("You can't create Tag with this title!")
        if new_slug == "add" :
            raise ValidationError("You can't create Tag with this slug!")
        if Tag.objects.filter(title__iexact=new_title).count() and self.instance.title == Tag.objects.filter(title__iexact=new_title):
            raise ValidationError("Tag with this title already exist!")
        if Tag.objects.filter(slug__iexact=new_slug).count() and  self.instance.slug == Tag.objects.filter(slug__iexact=new_slug):
            raise ValidationError("Tag with this slug already exist!")
        return new_slug




class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": TextInput(attrs={"class":"form-control"})
        }




#temporarily account stuff here -_-
# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ["first_name","last_name","email"]
#         widgets = {
#             "first_name": TextInput(attrs={"class": "form-control"}),
#             "last_name": TextInput(attrs={"class": "form-control"}),
#             "email": EmailInput(attrs={"class": "form-control"}),
#         }
#
#
#
#
# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ["bio","birth_date","pic"]
#         widgets = {
#             "bio": TextInput(attrs={"class": "form-control"}),
#             "birth_date": DateInput(format=('%m-%d-%Y'),attrs={"class": "form-control","placeholder":"month/day/year. I'm too lazy to set datepicker"}),
#             "pic": FileInput(attrs={"class": "form-control-file"}),
#         }
#
#
#
# #default UserCreationForm with custom forms classes
# class CustomUserCreationForm(UserCreationForm):
#     username = forms.CharField(widget=TextInput(attrs={"class": "form-control"}))
#     password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
#         attrs={'class': 'form-control'}), label=_("Password"))
#     password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
#         attrs={'class': 'form-control'}),label=_("Confirm password"))
#
#
#
#
#
# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.CharField(widget=TextInput(attrs={"class": "form-control"}))
#     password = forms.CharField(max_length=16, widget=forms.PasswordInput(
#         attrs={'class': 'form-control'}), label=_("Password"))
