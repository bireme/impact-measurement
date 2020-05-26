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
    list_display = ('question', 'get_pages', 'context', 'type',)
    list_filter = ('site', 'context', 'type',)
    search_fields = ['question', 'page',]

    def get_pages(self, obj):
        if obj.page:
            pages = ast.literal_eval(obj.page)
            labels = [dict(PAGES)[page] for page in pages]
            return labels
        else:
            return 'lango'
    get_pages.short_description = _("Pages")

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
    search_fields = ['page',]

    def label_from_instance(self, obj):
        return "%s" % (obj.question)
    label_from_instance.short_description = "%s" % (_("Question"))


# models = [Questions, Answers, QuestionContextList, WebsiteList, QuestionTypeList]

# admin.site.register(models)
