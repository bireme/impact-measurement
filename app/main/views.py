from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.html import escape
from django.urls import reverse

from itertools import zip_longest

from main.models import *
from main.forms import *


# @login_required
def dashboard(request):
    context = {}
    return render(request, 'main/index.html', context)
    # return HttpResponseRedirect(reverse('admin:index'))

@csrf_exempt
def get_feedback(request, **kwargs):
    response = None
    success = True

    code = escape(request.POST.get('code', None))

    try:
        obj = WebsiteList.objects.get(code=code)

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
    site_id = request.GET.get('site')
    page_id = request.GET.get('page')
    questions = Questions.objects.filter(site=site_id, page=page_id).order_by('question')
    return render(request, 'admin/questions_list.html', {'questions': questions})