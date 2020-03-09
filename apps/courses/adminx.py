import xadmin
from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag


class GlobalSetting(object):
    site_title = "サイト"
    site_footer = "僕のサイト"
    # menu_style = "accordion"


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class CourseAdmin(object):
    list_display = ["name", "desc", "detail", "degree", "learn_times", "students", "teacher"]
    search_fields = ["name", "desc", "detail", "degree", "students"]
    list_filter = ["name", "desc", "detail", "degree", "learn_times", "students", "teacher__name"]
    list_editable = ["degree", "desc"]


class LessonAdmin(object):
    list_display = ["name", "course", "add_time"]
    search_fields = ["name", "course"]
    list_filter = ["name", "course__name", "add_time"]  # couse__name 加上外健的字段一起过滤


class VideoAdmin(object):
    list_display = ["lesson", "name", "add_time"]
    search_fields = ["lesson", "name"]
    list_filter = ["lesson", "name", "add_time"]


class CourseResourceAdmin(object):
    list_display = ["name", "course", "file", "add_time"]
    search_fields = ["name", "course", "file"]
    list_filter = ["name", "course", "file", "add_time"]


class CourseTagAdmin(object):
    list_display = ["course", "tag", "add_time"]
    search_fields = ["course", "tag", ]
    list_filter = ["course", "tag", "add_time"]


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseTag, CourseTagAdmin)


xadmin.site.register(xadmin.views.CommAdminView, GlobalSetting)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)
