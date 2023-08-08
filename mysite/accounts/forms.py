from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm, ImageField
from django.contrib.auth.models import Group, User

from .models import Profile
from django import forms


class UserInfoForm(ModelForm):
    class Meta:
        model = Profile
        fields = "user", "bio", "agreement_accepted", "avatar"


class UserUpdateForm(forms.ModelForm):
    """
    Форма обновления данных пользователя
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

        widgets = {
            'avatar': forms.FileInput(),
        }



