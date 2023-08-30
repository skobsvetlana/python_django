from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    #login_view,
    #logout_view,
    HelloView,
    MyLogoutView,
    get_cookie_view,
    set_cookie_view,
    get_session_view,
    set_session_view,
    UserInfoView,
    AboutMeView,
    #MyLoginView,
    ProfileUpdateView,
    UsersListView,
    UserProfileView,
    RegisterView,
    FooBarView,
)


app_name = "accounts"

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
    #path("login/", login_view, name="login"),
    #path("logout/", logout_view, name="logout"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html",
            redirect_authenticated_user=True,
        ),
    name="login"
    ),
    #path("login/", MyLoginView.as_view(), name="login"),
    path("user_info/", UserInfoView.as_view(), name="user_info"),
    path("about-me/", AboutMeView.as_view(), name="about_me"),
    path("<pk>/update/", ProfileUpdateView.as_view(), name="profile_update"),
    path("users/", UsersListView.as_view(), name="users_list"),
    path("<pk>/", UserProfileView.as_view(), name="userprofile"),
    path("register/", RegisterView.as_view(), name="register"),

    path("cookie/get/", get_cookie_view, name="cookie_get"),
    path("cookie/set/", set_cookie_view, name="cookie_set"),

    path("session/get/", get_session_view, name="session_get"),
    path("session/set/", set_session_view, name="session_set"),

    path("foo-bar/", FooBarView.as_view(), name="foo_bar"),
]