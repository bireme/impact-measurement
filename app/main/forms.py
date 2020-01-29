from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django import forms

from main.models import Answers


class AnswersForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = '__all__'
