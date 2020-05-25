from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from main.models import *
from main.forms import *

import ast


PAGES = (
    ('wp-home', 'Home (WP)'),
    ('wp-document', 'Document (WP)'),
    ('wp-search', 'Search (WP)'),
    ('iahx-document', 'Document (iAHx)'),
    ('iahx-search', 'Search (iAHx)'),
    ('iahx-search-skip-true', 'Search skfp=true (iAHx)'),
    ('iahx-search-skip-false', 'Search skfp=false (iAHx)'),
    ('iahx-advanced-search', 'Advanced Search (iAHx)'),
    ('iahx-decs-locator', 'DeCS Locator (iAHx)'),
)


class QuestionsLocalAdmin(admin.TabularInline):
    model = QuestionsLocal
    extra = 0

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    form = QuestionsForm
    inlines = [QuestionsLocalAdmin,]
    list_display = ('question', 'page', 'context', 'type',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(QuestionsAdmin, self).get_form(request, obj, **kwargs)
        # form.base_fields['page'].label_from_instance = lambda obj: "{} {}".format(obj.id, obj.name)
        # form.base_fields['context'].label_from_instance = lambda obj: "{} {}".format(obj.id, obj.name)
        # form.base_fields['type'].label_from_instance = lambda obj: "{} {}".format(obj.id, obj.name)
        return form

@admin.register(QuestionContextList)
class QuestionContextListAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    readonly_fields = ('slug',)

@admin.register(QuestionTypeList)
class QuestionTypeListAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    readonly_fields = ('slug',)

@admin.register(WebsiteList)
class WebsiteListAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'code',)
    readonly_fields = ('code',)

@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'myvhl_user', 'page_type', 'rating',)

    def label_from_instance(self, obj):
        return "%s" % (obj.question)
    label_from_instance.short_description = "%s" % (_("Question"))


# models = [Questions, Answers, QuestionContextList, WebsiteList, QuestionTypeList]

# admin.site.register(models)
