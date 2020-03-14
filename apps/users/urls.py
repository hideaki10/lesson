from django.conf.urls import url
from apps.users.views import UserInfoView, UploadImageView, ChangePwdView, ChangeMobileView, MycourseView, MyFavView,MyFavTeacherView,MyFavCourseView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='info'),
    url(r'^image/upolad/$', UploadImageView.as_view(), name='image'),
    url(r'^update/pwd/$', ChangePwdView.as_view(), name='update_pwd'),
    url(r'^update/mobile/$', ChangeMobileView.as_view(), name='update_mobile'),
    # url(r'^mycourse/$', MycourseView.as_view(), name='my_course'),
    url(r'^mycourse/$',
        login_required(TemplateView.as_view(template_name="usercenter-mycourse.html"), login_url="/login"),
        {"current_page": "mycourse"},
        name='my_course'),
    url(r'^mafavorg/$', MyFavView.as_view(), name='my_fav_org'),
    url(r'^mafavteacher/$', MyFavTeacherView.as_view(), name='my_fav_teacher'),
    url(r'^mafavcourse/$', MyFavCourseView.as_view(), name='my_fav_course'),
]
