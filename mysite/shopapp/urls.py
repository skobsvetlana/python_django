from django.urls import path
from shopapp.views import shop_index

app_name = "shopapp"

urlpatterns = [
    path("", shop_index, name="index"),
]