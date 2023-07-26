from django.forms import ModelForm, ImageField
from django.contrib.auth.models import Group

from .models import Profile
from django import forms


class UserInfoForm(ModelForm):
    class Meta:
        model = Profile
        fields = "user", "bio", "agreement_accepted", "avatar"


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = "bio", "avatar"


class UserProfileUpdateForm(ProfileUpdateForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta(ProfileUpdateForm.Meta):
        fields = ProfileUpdateForm.Meta.fields + ('first_name', 'last_name')
