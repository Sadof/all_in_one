from .models import Test, Page, Question
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django import forms
from django.utils.translation import ugettext_lazy as _




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
            'title': 'Title( optional)',
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


