from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from main.models import *


class QuestionsLocalAdmin(admin.TabularInline):
    model = QuestionsLocal
    extra = 0

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    inlines = [QuestionsLocalAdmin,]
    list_display = ('question', 'context', 'type',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(QuestionsAdmin, self).get_form(request, obj, **kwargs)
        # form.base_fields['type'].label_from_instance = lambda obj: "{} {}".format(obj.id, obj.name)
        # form.base_fields['context'].label_from_instance = lambda obj: "{} {}".format(obj.id, obj.name)
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


# models = [Questions, Answers, QuestionContextList, QuestionTypeList, WebsiteList]

# admin.site.register(models)
