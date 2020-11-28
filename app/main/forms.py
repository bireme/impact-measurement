from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django import forms

from main.models import *


PAGES_CHOICES = (
    ('WordPress', (
    	('wp-home', 'Home'),
    	('wp-document', 'Document'),
    	('wp-search', 'Search'),
    )),
    ('WP Plugins', (
        ('wp-plugin-document', 'Document'),
        ('wp-plugin-search', 'Search'),
    )),
    ('iAHx', (
    	('iahx-document', 'Document'),
    	('iahx-search', 'Search'),
        ('iahx-search-skfp-true', 'Search skfp=true'),
    	('iahx-search-skfp-false', 'Search skfp=false'),
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
        widgets = {
            'page': forms.SelectMultiple(attrs={'size': '11'})
        }
        
    def __init__(self, *args, **kwargs):
        super(QuestionsForm, self).__init__(*args, **kwargs)
        # self.fields['page'].help_text = _("Leave blank to display this question on all pages")
