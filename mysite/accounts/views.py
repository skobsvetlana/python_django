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
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.views import View
from django.shortcuts import get_object_or_404

from .forms import ProfileUpdateForm, UserUpdateForm, UserInfoForm
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib import messages

class UserInfoView(TemplateView):
    template_name = "accounts/user-info.html"


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


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):

    #permission_required = 'accounts.change_avatar'

    def get(self, request, *args, **kwargs):
        change_profile = User.objects.get(username=kwargs["username"])
        user_form = UserUpdateForm(instance=change_profile)
        profile_form = ProfileUpdateForm(instance=change_profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'change_profile': change_profile,
        }

        return render(request, 'accounts/profile_update_form.html', context)

    def post(self, request, *args, **kwargs):
        change_profile = User.objects.get(username=kwargs["username"])
        user_form = UserUpdateForm(
            request.POST,
            instance=change_profile
        )
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=change_profile.profile
        )

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile has been updated successfully')

            return redirect('accounts:userprofile', username=change_profile.username)
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            messages.error(request, 'Error updating you profile')

            return render(request, 'accounts/profile_update_form.html', context)

    def test_func(self):
        user = self.request.user
        change_profile = User.objects.get(username=self.kwargs["username"])

        return user.is_superuser or user.is_staff or user == change_profile


class UsersListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/users-list.html'
    context_object_name = "users"
    queryset = User.objects.select_related("profile").all()


class UserProfileView(View):
    template_name = 'accounts/other_userprofile.html'
    context_object_name = "userprofile"
    queryset = User.objects.select_related("profile").all()

    def get(self, request, *args, **kwargs):
        view_profile = User.objects.get(username=kwargs["username"])
        user_form = UserInfoForm(instance=view_profile)
        context = {
            'user_form': user_form,
            'view_profile': view_profile
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




