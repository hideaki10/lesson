import xadmin

from apps.operations.models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse


class UseAskAdmin(object):
    list_display = ["name", "mobile", "course_name", "add_time"]
    search_filed = ["name", "mobile", "course_name", "add_time"]
    list_filter = ["name", "mobile", "course_name", "add_time"]


class CourseCommentsAdmin(object):
    list_display = ["user", "course", "comments", "add_time"]
    search_filed = ["user", "course", "comments"]
    list_filter = ["user", "course", "comments", "add_time"]


class UserFavoriteAdmin(object):
    list_display = ["user", "fav_id", "fav_type", "add_time"]
    search_filed = ["user", "fav_id", "fav_type"]
    list_filter = ["user", "fav_id", "fav_type", "add_time"]


class UserMessageAdmin(object):
    list_display = ["user", "message", "has_read", "add_time"]
    search_filed = ["user", "message", "has_read"]
    list_filter = ["user", "message", "has_read", "add_time"]


class UserCourseAdmin(object):
    list_display = ["user", "course", "add_time"]
    search_filed = ["user", "course"]
    list_filter = ["user", "course", "add_time"]


xadmin.site.register(UserAsk, UseAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
