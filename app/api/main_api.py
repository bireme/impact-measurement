from django.conf import settings
from django.urls import path, re_path, include

from django.contrib.contenttypes.models import ContentType

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.serializers import Serializer
from tastypie.utils import trailing_slash
from tastypie.exceptions import BadRequest
from tastypie import fields

from main.models import *

import requests
import urllib


class MainResource(ModelResource):
    class Meta:
        queryset = WebsiteList.objects.all()
        allowed_methods = ['get']
        serializer = Serializer(formats=['json', 'xml'])
        resource_name = 'main'
        include_resource_uri = False
        filtering = {
            'code': 'exact',
        }

    def build_filters(self, filters=None):
        if 'code' not in filters:
            raise BadRequest("missing code param")
        return super(MainResource, self).build_filters(filters)

    def dehydrate(self, bundle):
        questions = Questions.objects.filter(site=bundle.obj.id)

        if questions:
            bundle.data['questions'] = []

            for q in questions:
                # _q = model_to_dict(q)
                _q = {}
                _q['id'] = q.id
                _q['context'] = q.context
                _q['type'] = q.type.slug
                _q['question'] = {q.language: q.question}

                translations = QuestionsLocal.objects.filter(question=q.id)

                if translations:
                    for t in translations:
                        _t = {t.language: t.label}
                        _q['question'].update(_t)
                
                bundle.data['questions'].append(_q)

        return bundle
