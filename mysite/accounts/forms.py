from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm, ImageField
from django.contrib.auth.models import Group, User

from .models import Profile
from django import forms


class UserInfoForm(ModelForm):
    class Meta:
        model = Profile
        fields = "user", "bio", "agreement_accepted", "avatar"


# class UserUpdateForm(forms.ModelForm):
#     """
#     Форма обновления данных пользователя
#     """
#     username = forms.CharField(max_length=100,
#                                required=True,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
#     # email = forms.EmailField(required=True,
#     #                          widget=forms.TextInput(attrs={'class': 'form-control'}))
#
#
#     class Meta:
#         model = User
#         fields = ('username',)
#
#
# class ProfileUpdateForm(forms.ModelForm):
#     avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
#     bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
#
#     class Meta:
#         model = Profile
#         fields = ['avatar', 'bio']
#         #fields = '__all__'
#
#
#
#
#
