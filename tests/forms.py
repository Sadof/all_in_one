from .models import Test, Page, Question
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
import re






class TestCreateForm(ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'slug', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 10, 'class': 'form-control'}),
        }
        labels = {
            'slug': _('Humanlike url(optional).')
        }
        # validators ={
        #     'title': [validate_slug]
        # }


    def clean(self):
        print(self.cleaned_data)
        cleaned_data = self.cleaned_data
        title = cleaned_data['title']
        slug = cleaned_data['slug']
        if re.match("[a-zA-Z0-9]+", title) == None and not slug:
            raise forms.ValidationError("The title is not sluggable. Change title to valide one or give slug.")
        if slug.isspace():
            raise forms.ValidationError('Slug contains only spaces.')
        return cleaned_data
    
    # def save(self, commit=True):
    #     instance = super(TestCreateForm, self).save(commit=False)
    #     if commit:
    #         try:
    #             instance.save()
    #         except IntegrityError:
    #             raise forms.ValidationError('This slug already exist!')
    #     return instance
    
class PageCreateForm(ModelForm):
    class Meta:
        model = Page
        fields = ['title','image', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'image':forms.FileInput(attrs={'class':'custom-file-label'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-control'}),
            'question_commentory': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'image': 'Image( optional)',
            'text': 'Question text',
        }



class PageEditForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     self.page_id = kwargs.pop('page_id')
    #     super(PageEditForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Page
        fields = ['title','image', 'text', 'right_answer','question_commentory']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'image':forms.FileInput(attrs={'class':'custom-file-label'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-control'}),
            # 'right_answer': forms.ModelChoiceField(queryset=Page.objects.filter(id=page_id).question.all()),
            'question_commentory': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-control'}),
        }
        labels = {
            'text': _('Question text.'),
            'question_commentory': _("This text will show up if user quessed wrong answer and tell him right one and why it is.")

        }



QuestionFormSet = inlineformset_factory(Page,
                                        Question,
                                        fields=['order','text'],
                                        extra=1,
                                        can_delete=True,
                                        widgets={'order': forms.HiddenInput(),
                                                 'text': forms.TextInput(attrs={'class': 'form-control'})},
                                        labels={'text': ('Answer text'),
                                                'order': ('Answer order'),}

                                        )


