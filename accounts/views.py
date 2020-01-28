from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import CreateView, View, ListView
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Profile
from blog.models import Post
from tests.models import Test
from django.urls import reverse_lazy, reverse
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView
#from .forms import CustomAuthenticationForm



# class AccountRegistrationView(View):
#
#     def get(self, request):
#         form = UserRegistrationForm()
#         return render(request, 'registration/registration.html', {'form': form})
#
#     def post(self, request):
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             new_user = form.save(commit=False)
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             new_user.set_password(password)
#             new_user.save()
#             Profile.objects.create(user=new_user)
#             user = authenticate(request, username=username, password=password)
#             login(request, user)
#             return redirect('accounts:home_page')
#         else:
#             form = UserRegistrationForm(request.POST)
#             return render(request, 'registration/registration.html',{'form': form})



class AccountRegistrationView(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/registration.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            print(new_user)
            profile = Profile.objects.create(user=new_user)
            print(profile.user)
            user = authenticate(request, username=new_user.username, password=request.POST.get('password1'))
            login(request, user)
            return redirect('accounts:home_page')
        else:
            form = UserCreationForm(request.POST)
            return render(request, 'registration/registration.html',{'form': form})



class UserPageView(TemplateResponseMixin, View):
    template_name = 'accounts/user_page.html'
    def get(self, request, username=None):
        if username == request.user.username:
            return redirect('accounts:home_page')
        else:
            if not username:
                user = get_object_or_404(User, username=request.user.username)
                tests = Test.objects.filter(author__username=request.user.username)[:5]
                posts = Post.objects.filter(author__username=request.user.username)[:5]
                return self.render_to_response({'profile':user,'posts':posts, 'tests': tests})
            else:
                user = get_object_or_404(User, username=username)
                tests = Test.objects.filter(author__username=username,status=True)[:5]
                posts = Post.objects.filter(author__username=username)[:5]
                return self.render_to_response({'userpage': user, 'posts':posts, 'tests': tests})



class UserEditView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'accounts/edit.html'
    login_url = reverse_lazy('accounts:login')

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return self.render_to_response({'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
        return redirect('accounts:edit_profile')


class AccountListView(ListView):
    model = User
    template_name = 'accounts/account_list.html'


# class CustomLoginView(LoginView):
#     authentication_form = CustomAuthenticationForm
#     login_redirect = "/"
