from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django import forms

from main.models import *

import ast


PAGES_CHOICES = (
    ('WordPress', (
    	('wp-home', 'Home'),
    	('wp-document', 'Document'),
    	('wp-search', 'Search'),
    )),
    ('iAHx', (
    	('iahx-document', 'Document'),
    	('iahx-search', 'Search'),
        ('iahx-search-skip-true', 'Search skfp=true'),
    	('iahx-search-skip-false', 'Search skfp=false'),
    	('iahx-advanced-search', 'Advanced Search'),
    	('iahx-decs-locator', 'DeCS Locator'),
    )),
)


class AnswersForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = '__all__'

class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(QuestionsForm, self).__init__(*args, **kwargs)

        self.fields['page'] = forms.MultipleChoiceField(choices=PAGES_CHOICES, widget=forms.SelectMultiple(attrs={'size': 11}), required=False)
        self.fields['page'].help_text = _("Leave blank to display this question on all pages")

        if 'instance' in kwargs and kwargs['instance'] is not None:
            self.initial['page'] = ast.literal_eval(kwargs['instance'].page)
