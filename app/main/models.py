from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, get_language
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.template.defaultfilters import slugify
from django_userforeignkey.models.fields import UserForeignKey

import uuid


LANGUAGES_CHOICES = (
    ('en', _('English')), # default language
    ('pt-BR', _('Portuguese')),
    ('es', _('Spanish')),
)


class Generic(models.Model):

    class Meta:
        abstract = True

    created_time = models.DateTimeField(_("created at"), auto_now_add=True, editable=False)
    updated_time = models.DateTimeField(_("updated"), auto_now=True, editable=False, null=True, blank=True)
    created_by = UserForeignKey(auto_user_add=True, related_name="+")
    updated_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name="+")

class WebsiteList(Generic):

    class Meta:
        verbose_name = _("Website")
        verbose_name_plural = _("Websites")

    code = models.UUIDField(_('Code'), default=uuid.uuid4, editable=False)
    name = models.CharField(_('Website'), max_length=255, blank=True)
    url = models.URLField(_('URL'), blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class QuestionContextList(Generic):

    class Meta:
        verbose_name = _("Context")
        verbose_name_plural = _("Contexts")

    name = models.CharField(_('Context'), max_length=255, blank=True)
    slug = models.SlugField(_('Slug'), max_length=255, default='', editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(QuestionContextList, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class QuestionTypeList(Generic):

    class Meta:
        verbose_name = _("Type")
        verbose_name_plural = _("Types")

    name = models.CharField(_('Type'), max_length=255, blank=True)
    slug = models.SlugField(_('Slug'), max_length=255, default='', editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(QuestionTypeList, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class QuestionPageTypeList(Generic):

    class Meta:
        verbose_name = _("Page type")
        verbose_name_plural = _("Page types")

    name = models.CharField(_('Page'), max_length=255, blank=True)
    slug = models.SlugField(_('Slug'), max_length=255, default='', editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(QuestionPageTypeList, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Questions(Generic):

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
    
    question = models.CharField(_('Question'), max_length=455)
    site = models.ManyToManyField(WebsiteList, verbose_name=_('Websites'), blank=True)
    page = models.ManyToManyField(QuestionPageTypeList, verbose_name=_('Pages'), blank=True)
    context = models.ForeignKey(QuestionContextList, verbose_name=_("Context"), blank=True, on_delete=models.PROTECT)
    type = models.ForeignKey(QuestionTypeList, verbose_name=_("Type"), blank=True, on_delete=models.PROTECT)
    language = models.CharField(_("Language"), max_length=10, choices=LANGUAGES_CHOICES)

    def get_translations(self):
        translation_list = ["%s|%s" % (self.language, self.question.strip())]
        translation = QuestionsLocal.objects.filter(question_id=self.id)
        if translation:
            other_languages = ["%s|%s" % (trans.language, trans.label.strip()) for trans in translation]
            translation_list.extend(other_languages)

        return translation_list

    def get_all_labels(self):
        label_list = [self.question]
        label_list.extend([local.label for local in QuestionsLocal.objects.filter(question_id=self.id)])

        return label_list

    def __unicode__(self):
        lang_code = get_language()
        translation = QuestionsLocal.objects.filter(question_id=self.id, language=lang_code)
        if translation:
            return "%s | %s" % (translation[0].label, self.context)
        else:
            return "%s | %s" % (self.question, self.context)

    def __str__(self):
        lang_code = get_language()
        translation = QuestionsLocal.objects.filter(question_id=self.id, language=lang_code)
        if translation:
            return "%s | %s" % (translation[0].label, self.context)
        else:
            return "%s | %s" % (self.question, self.context)

class QuestionsOrdering(models.Model):

    class Meta:
        verbose_name = _("Questions ordering")
        verbose_name_plural = _("Questions ordering")
        unique_together = ('page', 'site',)

    site = models.ForeignKey(WebsiteList, verbose_name=_("Website"), on_delete=models.PROTECT)
    page = models.ForeignKey(QuestionPageTypeList, verbose_name=_("Page"), on_delete=models.PROTECT)
    order = models.CharField(_('Order'), max_length=255, blank=False, help_text=_("Comma-separated (e.g. 1,2,3,4,5)"))

    def __unicode__(self):
        return "%s | %s | %s" % (self.site.name, self.page.name, self.order)

    def __str__(self):
        return "%s | %s | %s" % (self.site.name, self.page.name, self.order)


class QuestionsLocal(models.Model):

    class Meta:
        verbose_name = _("Translation")
        verbose_name_plural = _("Translations")

    question = models.ForeignKey(Questions, verbose_name=_("Question"), on_delete=models.PROTECT)
    language = models.CharField(_("Language"), max_length=10, choices=LANGUAGES_CHOICES)
    label = models.CharField(_("Label"), max_length=255)

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.label

class Answers(Generic):

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    question = models.ForeignKey(Questions, verbose_name=_("Question"), help_text=_("Question | Context"), blank=True, on_delete=models.PROTECT)
    rating = models.CharField(_('Rating'), max_length=55, blank=True)
    user = models.CharField(_('User'), max_length=255, blank=True)
    myvhl_user = models.CharField(_('MyVHL user'), max_length=255, blank=True)
    page_type = models.CharField(_('Page type'), max_length=255, blank=True)
    page = models.URLField(_('Page'), blank=True)

    def __unicode__(self):
        return "%s | %s" % (self.question, self.rating)

    def __str__(self):
        return "%s | %s" % (self.question, self.rating)
