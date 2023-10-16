from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ArticleListView,
)

app_name = "BlogApp"

# routers = DefaultRouter()
# routers.register("articles", ArticleListView)

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="articles"),
]