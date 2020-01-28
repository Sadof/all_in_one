from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Page, Test, Question, Result
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .forms import TestCreateForm, PageCreateForm, QuestionFormSet, PageEditForm
from django.http import JsonResponse, HttpResponse
from blog.decorators import ajax_required
from django.views.decorators.http import require_POST
import json
from django import forms
from django.contrib import messages




class TestCreateView(LoginRequiredMixin,TemplateResponseMixin, View):
    template_name = 'tests/createtest.html'

    def get(self, request):
        form = TestCreateForm()
        return self.render_to_response({'form': form})

    def post(self, request):
        form = TestCreateForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.author = request.user
            test.save()
            return redirect('tests:edit_test', test.id)
        else:
            form = TestCreateForm(request.POST)
            return self.render_to_response({'form': form})


class PageCreateView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'tests/testview.html'

    def dispatch(self, request, test_id):
        self.test = Test.objects.get(id=test_id, author=request.user)
        return super(PageCreateView, self).dispatch(request, test_id)

    def get(self, request, test_id):
        form = PageCreateForm
        return self.render_to_response({'test': self.test, 'form': form,'pagec':'1'})

    def post(self, request, test_id):
        form = PageCreateForm(data=request.POST,
                              files=request.FILES)
        if form.is_valid():
            page = form.save(commit=False)
            page.test = self.test
            page.save()
            self.test.len += 1
            self.test.save()
            return redirect('tests:edit_page', test_id, page.order)


class TestPagesEditView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = "tests/testview.html"


    def dispatch(self, request, test_id, page_order=None, create=False):
        self.test = get_object_or_404(Test, id=test_id, author=request.user, status=False)
        if page_order:
            self.page = get_object_or_404(Page, order=page_order, test=self.test)
        return super(TestPagesEditView, self).dispatch(request, test_id, page_order, create)

    def get(self, request, test_id, page_order=None, create=False):
        if not page_order:
            if not create:
                form = TestCreateForm(instance=self.test)
            else:
                form = PageCreateForm()
        else:
            PageEditForm.base_fields['right_answer'] = forms.ModelChoiceField(queryset=self.page.question.all(),
                                                                              required=False,)
            form = PageEditForm(instance=self.page)
            formset = QuestionFormSet(instance=self.page)
            return self.render_to_response({'test': self.test, 'form': form,'page': self.page,'formset': formset})
        return self.render_to_response({'test': self.test, 'form': form})

    def post(self, request, test_id, page_order=None, create=False):
        if not page_order:
            if not create:
                form = TestCreateForm(instance=self.test,
                                      data=request.POST)
            else:
                form = PageCreateForm(data=request.POST,
                                      files=request.FILES)
        else:
            form = PageEditForm(instance=self.page,
                                  data=request.POST,
                                  files=request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.right_answer = request.POST.get('right_answer', '0')
            print(request.POST.get('right_answer', 0), new_form.right_answer)
            new_form.save()
            if page_order:
                return redirect('tests:edit_page', test_id, page_order)
            return redirect('tests:edit_test', test_id)
        else:
            print(form.errors)
            return self.render_to_response({'test': self.test, 'form': form})


def question_save(request):
    print(request.POST)
    test_id = request.POST['test_id']
    page_order = request.POST['page_order']
    page = get_object_or_404(Page, order=page_order, test=test_id)
    formset = QuestionFormSet(instance=page,
                              data=request.POST)
    if formset.is_valid():
        formset.save()
        print("saved")
    else:
        print(formset.errors)
        print('error')
    return redirect('tests:edit_page', test_id, page_order)


@ajax_required
@require_POST
def PageDelete(request):
    test_id = request.POST['test_id']
    page_id = request.POST['page_id']
    test = get_object_or_404(Test,id=test_id, author=request.user)
    page = get_object_or_404(Page, id=page_id, test__author=request.user)
    page.delete()
    test.len -= 1
    test.save()
    return redirect("tests:edit_test",test_id)


class TestDeleteView(LoginRequiredMixin, View):
    def dispatch(self, request, test_id):
        self.test = get_object_or_404(Test, id=test_id, author=request.user)
        return super(TestDeleteView, self).dispatch(request, test_id)

    def get(self, request,test_id):
        return render(request,'tests/delete_test.html',{'test': self.test})

    def post(self, request, test_id):
        self.test.delete()
        return redirect('accounts:my_test_list')


@ajax_required
def delete_test_ajax(request):
    test_id = json.loads(request.body)
    test = get_object_or_404(Test, id=test_id, author=request.user)
    test.delete()
    print('deleted')
    return JsonResponse({"deleted":"OK"})


@ajax_required
def PageOrder(request):
    json_data = json.loads(request.body)
    for id, order in json_data.items():
        Page.objects.filter(id=id,test__author=request.user).update(order=order)
    return JsonResponse({'saved': 'OK'})



@ajax_required
def QuestionOrder(request):
    json_data = json.loads(request.body)
    print(json_data)
    offset = 0
    for id, order in json_data.items():
        print(offset, id, order)
        if id:
            order -= offset
            Question.objects.filter(id=id,page__test__author=request.user).update(order=order)
        else:
            offset += 1
    return JsonResponse({'saved': 'OK'})

# @ajax_required
# def check_answers(request):
#     json_data = json.loads(request.body)
#     print(json_data)
#     answer = {}
#     for key, item in json_data.items():
#         answer[key] =
#     return JsonResponse({'Ok':'Ok'})


@require_POST
def page_delete(request, page_id):
    page = get_object_or_404(Page, id=page_id, test__author=request.user)
    page.delete()
    delete_reorder(page.test.page.all())
    return redirect('tests:edit_test', page.test.id)


def delete_reorder(obj_list):
    for i, child in enumerate(obj_list):
       child.order = i + 1
       child.save()



class TestPreview(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'tests/testpreview.html'

    def dispatch(self, request, test_id):
        self.test = get_object_or_404(Test, author=request.user, id=test_id, status=False)
        return super(TestPreview, self).dispatch(request, test_id)

    def get(self, request, test_id):
        return self.render_to_response({'test': self.test})




class TestCompletion(TemplateResponseMixin, View):
    template_name = 'tests/test.html'

    def dispatch(self, request, test_slug):
        self.test = get_object_or_404(Test, slug=test_slug, status=True)
        self.results = Result.objects.filter(user=request.user, test=self.test)[:3]
        for result in self.results:
            print(result.result)
        return super(TestCompletion, self).dispatch(request, test_slug)

    def get(self, request, test_id):
        return self.render_to_response({'test': self.test,'results': self.results})





def check_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, author=request.user, status=False)
    errors = 0
    errors = 0
    if len(test.page.all())<5:
        errors += 1
        messages.error(request, 'Test must have at least 5 questions.')
    for page in test.page.all():
        if len(page.question.all()) < 2 :
            errors += 1
            messages.error(request, 'Page %s have less then 2 answers, you should have at least 2 question.'% page.order )
        if not page.right_answer:
            errors += 1
            messages.error(request,
                           "Page %s don't have right answer." % page.order)
    if errors:
        return redirect('tests:edit_test', test_id)
    test.status = True
    test.save()
    return redirect('accounts:home_page')



class TestList(ListView):
    template_name = 'tests/tests_list.html'

    def get_queryset(self):
        username = self.kwargs.get('username','')
        if username:
            queryset = Test.objects.filter(status=True, author__username__icontains=username)
        else:
            queryset = Test.objects.filter(status=True)

        return queryset



class MyTestList(LoginRequiredMixin,View):
    def get(self,request):
        test_list = Test.objects.filter(author=request.user)
        return render(request, 'tests/my_test_list.html',{'tests': test_list})


@ajax_required
@require_POST
def test_complete(request):
    data = json.loads(request.body)
    test_id = data.get('test_id')
    result = data.get('result')
    test = get_object_or_404(Test,id=test_id)
    test.completed += 1
    if request.user.is_authenticated:
        Result.objects.create(user=request.user, test=test, result=result)
    test.save()
    return JsonResponse({"1":'1'})



@ajax_required
@require_POST
def test_like(request):
    data = json.loads(request.body)
    action = data.get('action')
    test_id = data.get('test_id')
    if action and test_id:
        try:
            test = Test.objects.get(id=test_id)
        except ObjectDoesNotExist:
            return JsonResponse({'answer': 'Something went wrong!'})
        if action == 'like':
            test.users_like.add(request.user)
            test.users_dislike.remove(request.user)
            print('like')
        elif action == 'dislike':
            test.users_dislike.add(request.user)
            test.users_like.remove(request.user)
            print('dislike')
        else:
            return JsonResponse({'answer': 'Something went wrong!'})
    return JsonResponse({"1": '1'})
