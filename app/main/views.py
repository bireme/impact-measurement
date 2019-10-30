from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    context = {}

    return render(request, 'main/index.html', context)
