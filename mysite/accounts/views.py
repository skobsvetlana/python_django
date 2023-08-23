import json
import os

from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from django.views import View
from django.shortcuts import get_object_or_404

# from .forms import UserUpdateForm,
from .forms import UserInfoForm, ProfileUpdateForm
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib import messages

class UserInfoView(TemplateView):
    template_name = "accounts/user-info.html"


class AboutMeView(UpdateView):
    template_name = "accounts/about-me.html"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("accounts:about_me")

    def get_object(self, queryset=None):

        return self.request.user.profile


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:profile_update")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)

        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


#@user_passes_test(lambda u: u.is_superuser)


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    #permission_required = 'accounts.change_avatar'
    template_name = "accounts/profile_update_form.html"
    model = Profile
    fields = "bio",  "avatar",

    def get(self, request, *args, **kwargs):
        update_profile = User.objects.get(pk=self.kwargs["pk"])
        context = {
            'update_profile': update_profile,
        }
        print(context)
        return render(request, 'accounts/profile_update_form.html', context)

    def test_func(self):
        user = self.request.user
        updated_user = self.get_object().user

        return user.is_superuser or user.is_staff or user.pk == updated_user.pk


class UsersListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/users-list.html'
    context_object_name = "users"
    queryset = User.objects.select_related("profile").all()


class UserProfileView(DetailView):
    template_name = 'accounts/userprofile.html'
    form_class = UserInfoForm
    #queryset = Profile.objects.select_related("user").all()

    def get(self, request, *args, **kwargs):
        user_profile = User.objects.get(pk=self.kwargs["pk"])
        user = self.request.user
        context = {
            'user': user,
            'user_profile': user_profile,
        }

        return render(request, 'accounts/userprofile.html', context)


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)

    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")

    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("accounts.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default value")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})


# def login_view(request: HttpRequest) -> HttpResponse:
#     if request.method == "GET":
#         if request.user.is_authenticated:
#             return redirect('/admin/')
#
#         return render(request, "accounts/login.html")
#
#     username = request.POST["username"]
#     password = request.POST["password"]
#
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect('/admin/')
#     return render(request, "accounts/login.html", {"error": "Invalid login credentials"})
#
#
# def logout_view(request: HttpRequest) -> HttpResponse:
#     logout(request)
#
#     return redirect(reverse("accounts:login"))




