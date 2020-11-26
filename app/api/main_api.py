from django.conf import settings
from django.urls import path, re_path, include
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.serializers import Serializer
from tastypie.utils import trailing_slash
from tastypie.exceptions import BadRequest
from tastypie import fields

from main.models import *

import requests
import urllib
import operator


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
        filter_page = bundle.request.GET.get('page', False)

        if filter_page:
            questions = Questions.objects.filter(site=bundle.obj.id, page__slug=filter_page, level=1).order_by('question')
        else:
            raise BadRequest("missing page param")

        if questions:
            bundle.data['questions'] = []
            obj_page = QuestionPageTypeList.objects.get(slug=filter_page)
            obj_order = QuestionsOrdering.objects.get(site=bundle.obj.id, page=obj_page.id)
            order = obj_order.order.split(",");

            for index, q in enumerate(questions):
                # _q = model_to_dict(q)
                _q = {}
                _q['id'] = q.id
                _q['page'] = [p.slug for p in q.page.all()]
                _q['context'] = q.context
                _q['type'] = q.type.slug
                _q['question'] = {q.language: q.question}
                _q['order'] = int(order[index]) if order and len(order) == len(questions) else index+1

                translations = QuestionsLocal.objects.filter(question=q.id)

                if translations:
                    for t in translations:
                        _t = {t.language: t.label}
                        _q['question'].update(_t)
                
                bundle.data['questions'].append(_q)

            if bundle.data['questions']:
                obj_sorted = sorted(bundle.data['questions'], key=operator.itemgetter('order'))
                bundle.data['questions'] = obj_sorted

        return bundle
