from .models import *
from django.shortcuts import  get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied


class PostDetailMixin:
    model = None
    template = None
    form_comment = None
    def get(self,request,slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        comments = obj.comments.filter(parent__isnull=True)
        return render(request, self.template,
                      context={self.model.__name__.lower(): obj, "admin_panel": obj, "comments": comments,
                               "form": self.form_comment})
    def post(self,request,slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        comments = obj.comments.filter(parent__isnull=True)
        bound_form = self.form_comment(request.POST)
        if bound_form.is_valid():
            new_comment = bound_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = obj
            if request.POST.get('parent_id'):
                new_comment.parent = obj.comments.get(pk=request.POST['parent_id'])
            new_comment.save()
            return redirect(self.request.path_info)
        else:
            return render(request,self.template, context={self.model.__name__.lower():obj,"admin_panel": obj,"comments":comments,"form":bound_form})

class ObjectDetailMixin:
    model = None
    template = None
    def get(self,request,slug):
        obj = get_object_or_404(self.model,slug__iexact=slug)
        return render(request,self.template,context={self.model.__name__.lower(): obj , "admin_panel": obj if self.model=="Post" else None })


class ObjectAddMixin:
    template = None
    form = None
    def get(self, request):
        # if not request.user.is_staff:
        if not request.user.is_authenticated:
             raise PermissionDenied
        bound_form = self.form
        return render(request, self.template, context={"form": bound_form})
    def post(self, request):
        bound_form = self.form(request.POST)
        if bound_form.is_valid():
            new_form = bound_form.save(commit=False)
            new_form.author = request.user
            new_form.save()
            return redirect(new_form)
        return render(request, self.template, context={"form": bound_form})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None
    def get(self,request,slug):
        # if not request.user.is_staff:
        #     raise PermissionDenied
        obj = self.model.objects.get(slug__iexact=slug)
        if not request.user.is_staff and not request.user.username == str(obj.author):
            raise PermissionDenied
        return render(request,self.template,context={"content":obj})
    def post(self,request,slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(self.redirect_url)



class ObjectEditMixim:
    model = None
    template = None
    form = None
    def get(self,request,slug):
        # if not request.user.is_staff:
        #     raise PermissionDenied
        obj = self.model.objects.get(slug__iexact=slug)
        if not request.user.username==str(obj.author):
            raise PermissionDenied
        bound_form = self.form(instance=obj)
        return render(request, self.template, context={"form": bound_form, self.model.__name__.lower(): obj})
    def post(self,request,slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.form(request.POST,instance=obj)
        if bound_form.is_valid():
            new_form = bound_form.save()
            return redirect(new_form)
        return render(request,self.template,context={"form":bound_form, self.model.__name__.lower():obj})


