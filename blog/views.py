from django.shortcuts import render, reverse, get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.views import View
from .utils import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
import json
from .decorators import post_author,ajax_required



# paginate var(query_set) by amount of var(range) and return context
def paginatoring(request,query_set, range):
    paginator = Paginator(query_set, range)
    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)
    is_paginator = page.has_other_pages
    if page.has_next():
        next_url = "?page={}".format(page.next_page_number())
    else:
        next_url = ""

    if page.has_previous():
        prev_url = "?page={}".format(page.previous_page_number())
    else:
        prev_url = ""
    context = {
        "page": page,
        "is_paginator": is_paginator,
        "next_url": next_url,
        "prev_url": prev_url
    }
    return context


def PostListView(request):
    # search_query = request.GET.get("search","")
    # if search_query:
    #      posts = Post.objects.filter(Q(title__icontains=search_query) | Q(text__icontains=search_query))
    # else:
    posts = Post.objects.all()
    context = paginatoring(request, posts, 5)

    return render(request,"blog/posts_list.html", context=context)




def TagListView(request):
    tags = Tag.objects.all()
    return render(request,"blog/tags_list.html", context={"tags":tags})




class PostView(PostDetailMixin,View):
    model = Post
    template = "blog/post_detail.html"
    form_comment = CommentForm



class TagView(ObjectDetailMixin,View):
    model = Tag
    template = "blog/tag_detail.html"




class PostAddView(ObjectAddMixin,View):
   template = "blog/post_add.html"
   form = PostAddForm




class TagAddView(ObjectAddMixin,View):
    template = "blog/tag_add.html"
    form = TagAddForm
    raise_exception = True




class PostDeleteView(ObjectDeleteMixin,View):
    model = Post
    template = "blog/post_delete.html"
    redirect_url = "posts_list_url"




class TagDeleteView(ObjectDeleteMixin,View):
    model = Tag
    template =  "blog/tag_delete.html"
    redirect_url = "tags_list_url"




class PostEditView(ObjectEditMixim, View):
    model = Post
    template = "blog/post_edit.html"
    form = PostAddForm




class TagEditView(ObjectEditMixim, View):
    model = Tag
    template = "blog/tag_edit.html"
    form = TagAddForm



class RegistrationView(View):
    def get(self,request):
        registration_form = CustomUserCreationForm
        return render(request,'registration/registration.html',context={"form":registration_form})
    def post(self,request):
        bound_form = CustomUserCreationForm(request.POST)
        if bound_form.is_valid():
            new_form = bound_form.save()
            user = authenticate(request, username=request.POST['username'], password=request.POST["password1"])
            login(request,user)
            return redirect("update_profile_url")
        else:
            return render(request,'registration/registration.html',context={"form":bound_form})


class UpdateProfileView(LoginRequiredMixin,View):
    def get(self,request):
        user = User.objects.get(username=request.user.username)
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
        print(user_form)
        return render(request,"profile/update_profile.html",context={"form":[user_form,profile_form]})
    def post(self,request):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile_url", request.user.username)
        else:
            messages.error(request, ('Пожалуйста, исправьте ошибки.'))
            return render(request,"profile/update_profile.html",context={"form":[user_form,profile_form]})



class ProfileView(View):
    def get(self,request,slug):
        user = get_object_or_404(User,username=slug)
        print(user.email)
        post_list = Post.objects.filter(author=user)
        return render(request,"profile/base_profile.html",context={"form":user,"post_list":post_list})



# Default LoginView with replaced form by CustonAuthenticatedForm with custom field classes
# class CustomLoginView(LoginView):
#     authentication_form = CustomAuthenticationForm

# Delete comment by pk from post with given slug, if it's not reply to a comment, then responce pk to delete reply button with the same pk
@ajax_required
def CommentDeleteView(request):
    if request.method == "POST":
        comment = get_object_or_404(Comment,pk=request.POST['comment_id'])
        data = {}
        if not comment.parent:
            data['result'] = request.POST['comment_id']
        comment.delete()
        return HttpResponse(json.dumps(data), content_type="application/json")


@ajax_required
def CommentEditView(request):
    if request.method == "POST":
        comment = get_object_or_404(Comment,pk=request.POST['comment_id'])
        comment.text = request.POST['text']
        comment.save()
        data = 'Ok'
        return HttpResponse(json.dumps(data), content_type="application/json")




def SearchList(request, search=None):
    if request.method == "GET":
        if not search:
            search_query = request.GET.get("search","")
            if not search_query:
                return redirect("posts_list_url")
            else:
                users = User.objects.filter(username__icontains=search_query)
                posts = Post.objects.filter(Q(title__icontains=search_query)|Q(text__icontains=search_query)|Q(author__username__icontains=search_query)) #
                tags = Tag.objects.filter(title__icontains=search_query)
                context={
                    "users":users,
                    "posts": posts,
                    "tags": tags,
                    'search_query': search_query,
                }
        else:
            posts = Post.objects.filter(author__username=search)
            context = {'posts': posts, 'search_query': search_query,}
        return render(request,"blog/search_list.html",context=context)

