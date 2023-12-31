from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.cache import cache_page

from shopapp.views import (
    ShopIndexView,
    GroupsListView,
    UserOrdersListView,
    UserOrdersExportView,
    #products_list,
    #orders_list,
    #create_product,
    #create_order,
    ProductDetailsView,
    ProductListView,
    OrderListView,
    OrderDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductArchiveView,
    LatestProductsFeed,
    OrderUpdateView,
    OrderCreateView,
    OrderDeleteView,
    ErrorView,
    ProductsDataExportView,
    OrdersExportView,
    ProductViewSet,
    OrderViewSet,
)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path("api/", include(routers.urls)),
    path("", ShopIndexView.as_view(), name="index"),
    #path("", cache_page(60 * 3)(ShopIndexView.as_view()), name="index"),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="user_orders"),
    #path("products/", products_list, name="products_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/latest/feed/", LatestProductsFeed(), name="products_feed"),
    path("products/create/", ProductCreateView.as_view(), name="create_product"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductArchiveView.as_view(), name="product_archive"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/export/", ProductsDataExportView.as_view(), name="products_export"),
    #path("orders/", orders_list, name="orders_list"),
    path("orders/", OrderListView.as_view(), name="orders_list"),
    #path("orders/create/", create_order, name="create_order"),
    path("orders/create/", OrderCreateView.as_view(), name="create_order"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="update_order"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="delete_order"),
    path("errors/", ErrorView.as_view(), name="error_no_permission"),
    path("orders/export/", OrdersExportView.as_view(), name="orders_export"),
    path("users/<int:user_id>/orders/export/", UserOrdersExportView.as_view(), name="orders_export"),
]