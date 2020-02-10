from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView, RedirectView
from django.views.debug import default_urlconf
from django.conf import settings

from api.main_api import MainResource

from main import views as main_views


main_resource = MainResource()

urlpatterns = [
    # path('', default_urlconf),
    # path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    path('', admin.site.login),
    path('admin/', admin.site.urls),

    # Login/Logout
    path('login/', LoginView.as_view(template_name="authentication/login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # Main
    # path('', main_views.dashboard, name="dashboard"),

    # Feedback
    path('send-feedback/', main_views.get_feedback),

    # API
    path('api/', include(main_resource.urls)),
]

# messages translation
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls')),
    ]