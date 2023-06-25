from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    #login_view,
    #logout_view,
    MyLogoutView,
    get_cookie_view,
    set_cookie_view,
    get_session_view,
    set_session_view,
    UserInfoView,
    RegisterView,
)


app_name = "myauth"

urlpatterns = [
    #path("login/", login_view, name="login"),
    #path("logout/", logout_view, name="logout"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login"
    ),
    path("user_info/", UserInfoView.as_view(), name="user_info"),
    path("register/", RegisterView.as_view(), name="register"),
    path("cookie/get/", get_cookie_view, name="cookie_get"),
    path("cookie/set/", set_cookie_view, name="cookie_set"),
    path("session/get/", get_session_view, name="session_get"),
    path("session/set/", set_session_view, name="session_set"),
]