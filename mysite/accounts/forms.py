from django.forms import ModelForm, ImageField
from django.contrib.auth.models import Group

from .models import Profile


class UserInfoForm(ModelForm):
    class Meta:
        model = Profile
        fields = "user", "bio", "agreement_accepted", "avatar"
