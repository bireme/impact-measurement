from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.html import escape
from django.urls import reverse

from tastypie.exceptions import BadRequest

from itertools import zip_longest

from main.models import *
from main.forms import *

import operator
import base64


# @login_required
class SurveyView(ListView):
    model = Questions
    template_name = "main/survey.html"

    def get_queryset(self):
        param_code = self.request.GET.get('code')
        param_user = self.request.GET.get('user')
        param_page = self.request.GET.get('page')
        param_page_type = self.request.GET.get('page_type')
        param_page_type_slug = self.request.GET.get('page_type_slug')

        if not param_user:
            raise BadRequest("missing user param")

        if not param_code:
            raise BadRequest("missing code param")

        if not param_page:
            raise BadRequest("missing page param")

        if not param_page_type:
            raise BadRequest("missing page_type param")

        if not param_page_type_slug:
            raise BadRequest("missing page_type_slug param")

        object_list = self.model.objects.filter(site__code=param_code, page__slug=param_page_type_slug, level=2).order_by('question')

        try:
            obj_order = SurveyOrdering.objects.get(site__code=param_code, page__slug=param_page_type_slug)
            order = obj_order.order.split(",");
        except SurveyOrdering.DoesNotExist:
            order = None

        if order and len(order) == len(object_list):
            for index, q in enumerate(object_list):
                q.order = int(order[index])

            object_list = sorted(object_list, key=lambda q: q.order, reverse=True)

        return object_list

    def get_context_data(self, **kwargs):
        context = super(SurveyView, self).get_context_data(**kwargs)
        param_myvhl_user = self.request.GET.get('myvhl_user')

        context['code'] = self.request.GET.get('code')
        context['page'] = base64.urlsafe_b64decode(self.request.GET.get('page')).decode('utf-8')
        context['page_type'] = self.request.GET.get('page_type')
        context['im_user'] = self.request.GET.get('user')
        context['myvhl_user'] = param_myvhl_user if param_myvhl_user else ''

        return context

@csrf_exempt
def get_feedback(request, **kwargs):
    response = None
    success = True

    code = escape(request.POST.get('code', None))
    page = escape(request.POST.get('page_type_slug', None))

    try:
        obj = WebsiteList.objects.filter(code=code)

        if obj:
            request.POST = request.POST.copy() # to make it editable
            questions_list = request.POST.getlist('question')
            rating_list = request.POST.getlist('rating')
            zipped = list(zip_longest(questions_list, rating_list, fillvalue=''))

            for q, r in zipped:
                request.POST['question'] = q
                request.POST['rating'] = r

                form = AnswersForm(request.POST)

                if form.is_valid():
                    form.save()
                else:
                    success = False

            if success:
                survey = Questions.objects.filter(site__code=code, page__slug=page, level=2)
                
                if survey:
                    success = 'Survey'
        else:
            success = False
    except Exception as e:
        success = False

    response = HttpResponse(success)  
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST"
    response["Access-Control-Allow-Headers"] = "*" 
    
    return response

def load_questions(request):
    level = request.GET.get('level')
    site_id = request.GET.get('site')
    page_id = request.GET.get('page')
    
    questions = Questions.objects.filter(site=site_id, page=page_id, level=level).order_by('question')
    
    return render(request, 'admin/questions_list.html', {'questions': questions})