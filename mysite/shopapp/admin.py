from django.contrib import admin
from  django.db.models import QuerySet
from django.http import HttpRequest

from .models import Product, Order
from .admin_mixins import ExportAsCSVMixin

class OrderInline(admin.TabularInline):
    model = Product.orders.through

@admin.action(description="Archive products")
def mark_archived(modelAdmin: admin.ModelAdmin, request: HttpRequest, querryset: QuerySet):
    querryset.update(archived=True)


@admin.action(description="Unarchive products")
def mark_unarchived(modelAdmin: admin.ModelAdmin, request: HttpRequest, querryset: QuerySet):
    querryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv",
    ]
    inlines = [
        OrderInline,
    ]
    #list_display = "pk", "name", "description", "quantity", "price", "discount", "created_at", "archived"
    list_display = "pk", "name", "description_short", "quantity", "price", "discount", "created_at", "archived"
    list_display_links = "pk", "name"
    ordering = "-name", "pk"
    search_fields = "name", "description", "price"
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("wide",),
        }),
        ("Extra options", {
            "fields": ("quantity", "archived"),
            "classes": ("wide", "collapse",),
            "description": "Extra options. Field 'archived' is for soft delete.",
        }),
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) <= 50:
            return obj.description
        else:
            return obj.description[:50] + "..."

#admin.site.register(Product, ProductAdmin)


# class ProductInline(admin.TabularInline):
class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username