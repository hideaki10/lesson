"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
import xadmin

from apps.users.views import LoginView, LogoutView, SendSmsView, DynamicView, RegisterView
from apps.organizations.views import OrgView
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin', xadmin.site.urls),
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
    # path('login/',TemplateView.as_view(template_name="login.html"),name="login"),

    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('d_login/', DynamicView.as_view(), name="d_login"),
    path('register/', RegisterView.as_view(), name="register"),
    # url(r'^captcha/', include('captcha.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^send_sms/', csrf_exempt(SendSmsView.as_view()), name="send_sms"),
    url(r'^org_list/', OrgView.as_view(), name="org_list"),
    url(r'^org/', include(('apps.organizations.urls', "organizations"), namespace="org")),

    url(r'^course/', include(('apps.courses.urls', "courses"), namespace="courses")),

    # img upload of url
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    url(r'^op/', include(('apps.operations.urls', "operations"), namespace="op")),

    url(r'^users/', include(('apps.users.urls', "users"), namespace="users")),

]
