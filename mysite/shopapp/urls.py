from django.urls import path
from shopapp.views import (
    ShopIndexView,
    GroupsListView,
    #products_list,
    #orders_list,
    create_product,
    create_order,
    ProductDetailsView,
    ProductListView,
    OrderListView,
    OrderDetailView,
)

app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    #path("products/", products_list, name="products_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/create/", create_product, name="create_product"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    #path("orders/", orders_list, name="orders_list"),
    path("orders/", OrderListView.as_view(), name="orders_list"),
    path("orders/create/", create_order, name="create_order"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
]