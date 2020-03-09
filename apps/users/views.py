from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterForm, RegisterPostForm
import redis
from MxOnline.settings import REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile


# Create your views here.

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
