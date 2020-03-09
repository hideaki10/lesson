from django import forms
from apps.operations.models import UserAsk
import re

# class AddAskFrom(forms.Form):
#     name = forms.CharField(required=True, min_length=5, max_length=5)
#     mobile = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=2, max_length=50)


class AddAskForm(forms.ModelForm):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)

    class Meta:
        model = UserAsk
        fields = ["name", "mobile", "course_name"]

    def clean_mobile(self):

        mobile = self.cleaned_data["mobile"]
        regex_mobile = ""
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("",code="")