from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from apps.organizations.models import CourseOrg
from apps.organizations.models import City, Teacher
from apps.organizations.forms import AddAskForm
from pure_pagination import Paginator, PageNotAnInteger
from django.http import JsonResponse
from apps.operations.models import UserFavorite


class TeacherDetailView(View):
    def get(self, request, teacher_id, *args, **kwarg):
        # teacher = Teacher.objects.get(id=teacher_id)
        #
        # return render(request, "teacher-detail.html",
        #               {"teacher": teacher})

        teacher = Teacher.objects.get(id=int(teacher_id))

        teacher_fav = False
        org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                org_fav = True

        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "teacher_fav": teacher_fav,
            "org_fav": org_fav,
            "hot_teachers": hot_teachers
        })


class TeacherListView(View):
    def get(self, request, *args, **kwarg):
        teachers = Teacher.objects.all()

        teacher_nums = teachers.count()

        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        sort = request.GET.get("sort", "")
        if sort == "hot":
            teachers = teachers.order_by("-click_nums")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(teachers, per_page=3, request=request)

        teachers = p.page(page)

        return render(request, "teachers-list.html",
                      {"teachers": teachers,
                       "teacher_nums": teacher_nums,
                       "sort": sort,
                       "hot_teachers": hot_teachers, })


class OrgDescView(View):
    def get(self, request, org_id, *args, **kwarg):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        return render(request, "org-detail-desc.html"
                      , {
                          "course_org": course_org,
                          "current_page": current_page,
                          "has_fav": has_fav,
                      })


class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwarg):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        all_courses = course_org.course_set.all()

        # ページング
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, per_page=5, request=request)

        orgs = p.page(page)

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        return render(request, "org-detail-course.html"
                      , {
                          "all_course": all_courses,
                          "course_org": course_org,
                          "current_page": current_page,
                          "has_fav": has_fav,
                      })


class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwarg):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        all_teacher = course_org.teacher_set.all()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        return render(request, "org-detail-teachers.html"
                      , {
                          "all_teacher": all_teacher,
                          "course_org": course_org,
                          "current_page": current_page,
                          "has_fav": has_fav,
                      })


class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwarg):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        # course_org = course_org[0]
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]

        return render(request, "org-detail-homepage.html"
                      , {"all_courses": all_courses,
                         "all_teacher": all_teacher,
                         "course_org": course_org,
                         "current_page": current_page,
                         "has_fav": has_fav,
                         })


class AddAskView(View):
    def post(self, request, *args, **kwarg):
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():
            userask_form = userask_form.save(commit=True)
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "エラー"
            })


class OrgView(View):
    def get(self, request, *args, **kwarg):
        all_orgs = CourseOrg.objects.all()
        all_citys = City.objects.all()

        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        city_id = request.GET.get("city", "")

        if city_id:
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))

        sort = request.GET.get("sort", "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, per_page=5, request=request)

        orgs = p.page(page)

        return render(request, "org-list.html",
                      {"all_orgs": orgs,
                       "org_nums": org_nums,
                       "all_citys": all_citys,
                       "category": category,
                       "city_id": city_id,
                       "sort": sort})
