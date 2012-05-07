from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User
from filizver.contrib.passages.models import Passage
from filizver.models import Topic

class PassageForm(forms.ModelForm):
    user            = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    topic          = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.HiddenInput())
    body            = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'textarea markup', 'rows': 8, 'required': 'required'}))
#    footnote        = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'textarea', 'rows': 2}))

    class Meta:
        model       = Passage
        exclude     = ['date_created', 'footnote']
        
class PassageUpdateForm(forms.ModelForm):
    body            = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'textarea', 'rows': 8}))
    footnote        = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'textarea', 'rows': 2}))

    class Meta:
        model       = Passage
        exclude     = ['date_created', 'footnote']
