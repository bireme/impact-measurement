from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView, RedirectView
from django.views.debug import default_urlconf
from django.conf import settings

from api.main_api import MainResource

from main.views import *


main_resource = MainResource()

urlpatterns = [
    path('', admin.site.login),
    path('admin/', admin.site.urls),
    path('ajax/load-questions/', load_questions, name='ajax_load_questions'),

    # Login/Logout
    path('login/', LoginView.as_view(template_name="authentication/login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),

    # Feedback
    path('send-feedback/', get_feedback, name="send_feedback"),

    # API
    path('api/', include(main_resource.urls)),

    # Main
    re_path(r'^survey/?$', SurveyView.as_view(), name='survey'),
]

# messages translation
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls')),
    ]