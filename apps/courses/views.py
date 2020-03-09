from pure_pagination import Paginator, PageNotAnInteger
from django.shortcuts import render
from django.views.generic.base import View
from apps.courses.models import Course, CourseTag, CourseResource, Video
from apps.operations.models import UserFavorite, UserCourse, CourseComments
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class VideoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, video_id, *args, **kwarg):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # lessons = course.lesson_set.all()
        # for lesson in lessons:
        #     for video in lesson.video_set.all():
        #         time = video.learn_time

        video = Video.objects.filter(id=int(video_id))
        users_course = UserCourse.objects.filter(user=request.user, course=course)

        if not users_course:
            users_course = UserCourse(user=request.user, course=course)
            users_course.save()

            course.students += 1
            course.save()

        # すべてコースに参加したユーザーを取得
        user_courses = UserCourse.objects.filter(course=course)
        # 取得したユーザーのidを取得
        user_ids = [user_course.user.id for user_course in user_courses]
        # idからコースを取得
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # 関連するコースを取得
        # related_courses = [user_course.course
        #                    for user_course in all_courses
        #                    if users_courses.id != course.id
        #                    ]

        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course.resources = CourseResource.objects.filter(course=course)

        return render(request, "course-play.html", {
            "course": course,
            "course_resources": course.resources,
            "related_courses": related_courses,
            "video": video,
        })


class CourseCommentView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwarg):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()

        comments = CourseComments.objects.filter(course=course)
        # lessons = course.lesson_set.all()
        # for lesson in lessons:
        #     for video in lesson.video_set.all():
        #         time = video.learn_time

        users_course = UserCourse.objects.filter(user=request.user, course=course)

        if not users_course:
            users_course = UserCourse(user=request.user, course=course)
            users_course.save()

            course.students += 1
            course.save()

        # すべてコースに参加したユーザーを取得
        user_courses = UserCourse.objects.filter(course=course)
        # 取得したユーザーのidを取得
        user_ids = [user_course.user.id for user_course in user_courses]
        # idからコースを取得
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # 関連するコースを取得
        # related_courses = [user_course.course
        #                    for user_course in all_courses
        #                    if users_courses.id != course.id
        #                    ]

        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course.resources = CourseResource.objects.filter(course=course)

        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": course.resources,
            "related_courses": related_courses,
            "comments": comments,
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwarg):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()

        # lessons = course.lesson_set.all()
        # for lesson in lessons:
        #     for video in lesson.video_set.all():
        #         time = video.learn_time

        users_course = UserCourse.objects.filter(user=request.user, course=course)

        if not users_course:
            users_course = UserCourse(user=request.user, course=course)
            users_course.save()

            course.students += 1
            course.save()

        # すべてコースに参加したユーザーを取得
        user_courses = UserCourse.objects.filter(course=course)
        # 取得したユーザーのidを取得
        user_ids = [user_course.user.id for user_course in user_courses]
        # idからコースを取得
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # 関連するコースを取得
        # related_courses = [user_course.course
        #                    for user_course in all_courses
        #                    if users_courses.id != course.id
        #                    ]

        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course.resources = CourseResource.objects.filter(course=course)

        return render(request, "course-video.html", {
            "course": course,
            "course_resources": course.resources,
            "related_courses": related_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwarg):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # おすすめ
        # tag = course.tag
        # related_course = []
        # if tag:
        #     related_course = Course.objects.filter(tag=tag).exclude(id__in=[course_id])[:3]

        tags = course.coursetag_set.all()
        # tag_list = []
        #
        # for tag in tags:
        #     tag_list.append(tag.tag)

        tag_list = [tag.tag for tag in tags]

        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course_id)
        related_couse = []

        for course_tag in course_tags:
            related_couse.append(course_tag)

        return render(request, "course-detail.html", {
            "course": course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            # "related_couse": related_course,
            "related_couse": related_couse,
        })


class CourseListView(View):
    def get(self, request, *args, **kwarg):
        all_courses = Course.objects.order_by("-add_time")
        hot_courses = Course.objects.order_by("-click_nums")[:3]

        sort = request.GET.get("sort", "")

        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, per_page=5, request=request)

        all_courses = p.page(page)

        return render(request, "course-list.html"
                      , {
                          "all_courses": all_courses,
                          "sort": sort,
                          "hot_courses": hot_courses,

                      })
