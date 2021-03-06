from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterForm, RegisterPostForm, \
    UploadImageForm, UserInfoForm, ChangePwdForm, UpadateMobileForm
import redis
from MxOnline.settings import REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.operations.models import UserCourse, UserFavorite
from apps.organizations.models import CourseOrg, Teacher
from apps.courses.models import Course


# Create your views here.
class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwarg):
        current_page = "myfav_teacher"
        teacher_list = []

        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        # for fav_teacher in fav_teachers:
        #     teacher = Teacher.objects.filter(id=fav_teacher.fav_id)
        #     teacher_list.append(teacher)
        #####
        # what is the difference with  get and  filter ?
        #####
        for fav_teacher in fav_teachers:
            org = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(org)

        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,
            "current_page": current_page
        })

    # def get(self, request, *args, **kwargs):
    #     current_page = "myfav_teacher"
    #     teacher_list = []
    #     fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
    #     for fav_teacher in fav_teachers:
    #         org = Teacher.objects.get(id=fav_teacher.fav_id)
    #         teacher_list.append(org)
    #     return render(request, "usercenter-fav-teacher.html", {
    #         "teacher_list": teacher_list,
    #         "current_page": current_page
    #     })


class MyFavCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwarg):
        current_page = "myfav_course"
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)

        for fav_course in fav_courses:
            course = Course.objects.get(id=fav_course.fav_id)
            course_list.append(course)
        return render(request, "usercenter-fav-course.html", {
            "course_list": course_list,
            "current_page": current_page
        })


class MyFavView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwarg):
        current_page = "myfavorg"
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
            "current_page": current_page
        })


class MycourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwarg):
        # my_courses = UserCourse.objects.filter(user=request.user)
        current_page = "mycourse"
        user = request.user
        # 反向取
        my_courses = user.usercourse_set.all()
        return render(request, "usercenter-mycourse.html", {
            "my_courses": my_courses,
            "current_page": current_page,
        })


class ChangeMobileView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, *args, **kwarg):
        mobile_form = UpadateMobileForm(request.POST)
        if mobile_form.is_valid():
            mobile = mobile_form.data.get('mobile')
            if request.user.mobile == mobile:
                return JsonResponse({

                })
            if UserProfile.objects.filter(mobile=mobile):
                return JsonResponse({
                    "mobile": "is return"
                })
            user = request.user
            user.mobile = mobile
            user.username = mobile
            user.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(mobile_form.errors)


class ChangePwdView(View):
    def post(self, request, *args, **kwarg):
        change_pwd_form = ChangePwdForm(request.POST)
        if change_pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            user = request.user
            user.set_password(pwd1)
            user.save()
            login(request, user)
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(change_pwd_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    login_url = "/login/"

    #
    # def save_file(self, file):

    def post(self, request, *args, **kwarg):
        files = request.FILES["image"]
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwarg):
        login_url = "/login/"
        captcha_form = RegisterForm()
        current_page = "info"
        return render(request, "usercenter-info.html", {
            "captcha_form": captcha_form,
            "current_page": current_page
        })

    # def post(self, request, *args, **kwarg):
    #     user_info_form = UserInfoForm(request.POST, instance=request.user)
    #     if user_info_form.is_valid():
    #         user_info_form.save()
    #         return JsonResponse({
    #             "status": "success"
    #         })
    #     else:
    #         return JsonResponse(user_info_form.errors)
    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(user_info_form.errors)


class RegisterView(View):
    def get(self, request, *args, **kwarg):
        register_get_form = RegisterForm()
        return render(request, "register.html", {"register_get_form": register_get_form})

    def post(self, request, *args, **kwarg):
        register_post_form = RegisterPostForm(request.POST)
        # dynamic_login = True
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            register_get_form = RegisterForm()
            return render(request, "register.html", {
                "register_get_form": register_get_form
                , "register_post_form": register_post_form})


class DynamicView(View):

    def get(self, request, *args, **kwarg):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        next = request.GET.get("next", "")

        login_form = DynamicLoginForm()
        return render(request, "login.html", {
            "login_form": login_form,
            "next": next,

        })

    def post(self, request, *args, **kwarg):
        login_form = DynamicLoginPostForm(request.POST)
        dynamic_login = True
        if login_form.is_valid():
            mobile = login_form.cleaned_data["mobile"]
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                user = UserProfile(username=mobile)
                user.set_password("1234")
                user.mobile = mobile
                user.save()
            login(request, user)
            next = request.GET.get("next", "")
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse("index"))
        else:
            d_form = DynamicLoginForm()
            return render(request, "login.html",
                          {"login_form": login_form, "dynamic_login": dynamic_login, "d_form": d_form})


class SendSmsView(View):

    def post(self, request, *args, **kwarg):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]
            code = 1234
            re_dict["status"] = "success"
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf-8", decode_responses=True)
            r.set(str(mobile), code)
            r.expire(str(mobile), 60 * 5)

            # 手机验证码登陆
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]
        return JsonResponse(re_dict)


class LogoutView(View):
    def get(selfs, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


class LoginView(View):

    def get(self, request, *args, **kwarg):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        next = request.GET.get("next", "")

        login_form = DynamicLoginForm()
        return render(request, "login.html", {
            "login_form": login_form,
            "next": next,

        })

    def post(self, request, *args, **kwarg):
        login_form = LoginForm(request.POST)
        # user_name = request.POST.get("username", "")
        # password = request.POST.get("password", "")

        # if not user_name:
        #     return render(request, "login.html", {"msg": "用户名或密码错误"})
        #
        # if not password:
        #     return render(request, "login.html", {"msg": "パスワードを入力してください"})

        # ユーザーの検証

        if login_form.is_valid():
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=password)

            if user is not None:
                login(request, user)
                next = request.GET.get("next", "")
                if next:
                    return HttpResponseRedirect(next)
                #     return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})

        # if user is not None:
        #     login(request, user)
        #     # return render(request, "index.html")  # 慕课网 9.2 18.01
        #
        #     return HttpResponseRedirect(reverse("index"))
        # else:
        #     # return render(request, "login.html", {"msg", "ユーザーまたはパスワードを入力してください"})
        #     # return render(request, "login.html", {"msg", "ユーザーまたはパスワードを入力してください"})
        #     return render(request, "login.html", {"msg": "用户名或密码错误"})
