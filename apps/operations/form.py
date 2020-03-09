from django import forms
from apps.operations.models import UserFavorite, CourseComments
import re


# class AddAskFrom(forms.Form):
#     name = forms.CharField(required=True, min_length=5, max_length=5)
#     mobile = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=2, max_length=50)


class UserFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ["fav_id", "fav_type"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = [ "course", "comments"]
