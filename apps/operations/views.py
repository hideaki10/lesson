from django.views.generic.base import View

from apps.operations.models import UserFavorite, CourseComments
from apps.operations.form import UserFavForm, CommentForm
from django.http import JsonResponse
from apps.courses.models import Course
from apps.organizations.models import Teacher, CourseOrg


# Create your views here.


class CommentView(View):
    def post(self, request, *args, **kwarg):
        # ユーザーがログインできているかどうか確認
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录",
            })
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            course= comment_form.cleaned_data["course"]
            comments = comment_form.cleaned_data["comments"]

            # ブックマークしてたかどうか確認
            course_comment = CourseComments()

            course_comment.user = request.user
            course_comment.course = course
            course_comment.comments = comments
            course_comment.save()

            return JsonResponse({
                "status": "success",
                "msg": "已收藏",
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误",
            })


class AddFavView(View):
    def post(self, request, *args, **kwarg):

        # ユーザーがログインできているかどうか確認
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录",
            })
        user_fav_form = UserFavForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data["fav_id"]
            fav_type = user_fav_form.cleaned_data["fav_type"]

            # ブックマークしてたかどうか確認
            exitsted_recode = UserFavorite.objects.filter(user=request.user,
                                                          fav_id=fav_id,
                                                          fav_type=fav_type)

            if exitsted_recode:
                exitsted_recode.delete()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 2:
                    course = CourseOrg.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 3:
                    course = Teacher.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                return JsonResponse({
                    "status": "success",
                    "msg": "收藏",
                })
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()
                return JsonResponse({
                    "status": "success",
                    "msg": "已收藏",
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误",
            })
