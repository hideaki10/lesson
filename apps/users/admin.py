from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.


from apps.users.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass


# admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(UserProfile, UserAdmin)
