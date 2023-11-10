from io import TextIOWrapper

from django.contrib import admin
from  django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .common import save_csv_products, save_csv_orders
from .models import Product, Order, ProductImages
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm


class OrderInline(admin.TabularInline):
    model = Product.orders.through

@admin.action(description="Archive products")
def mark_archived(modelAdmin: admin.ModelAdmin, request: HttpRequest, querryset: QuerySet):
    querryset.update(archived=True)


@admin.action(description="Unarchive products")
def mark_unarchived(modelAdmin: admin.ModelAdmin, request: HttpRequest, querryset: QuerySet):
    querryset.update(archived=False)


class ProductInline(admin.StackedInline):
    model = ProductImages


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = "shopapp/products_changelist.html"
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv",
    ]
    inlines = [
        OrderInline,
        ProductInline
    ]
    #list_display = "pk", "name", "description", "quantity", "price", "discount", "created_at", "archived"
    list_display = ("pk", "name", "description_short", "quantity",
                    "price", "discount", "created_at", "created_by",
                    "archived",
                    )
    list_display_links = "pk", "name"
    ordering = "-name", "pk"
    search_fields = "name", "description", "price"
    #readonly_fields = ["created_by", "created_at"]
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("wide",),
        }),
        ("Images", {
            "fields": ("preview",),
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

    # def save_model(self, request, obj, form, change):
    #     obj.created_by = request.user
    #     super().save_model(request, obj, form, change)

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form
            }

            return render(request, "admin/csv_form.html", context)

        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form
            }

            return render(request, "admin/csv_form.html", context, status=400)

        save_csv_products(
            file=form.files["csv_file"].file,
            encoding=request.encoding,
        )
        self.message_user(request, "Data from csv uploaded")

        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv/",
                self.import_csv,
                name="import_products_csv",
            ),
        ]

        return new_urls + urls


#admin.site.register(Product, ProductAdmin)


# class ProductInline(admin.TabularInline):
class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "shopapp/orders_changelist.html"
    inlines = [
        ProductInline,
    ]
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form
            }

            return render(request, "admin/csv_form.html", context)

        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form
            }

            return render(request, "admin/csv_form.html", context, status=400)

        save_csv_orders(
            file=form.files["csv_file"].file,
            encoding=request.encoding,
        )
        self.message_user(request, "Data from csv uploaded")

        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import_orders.csv/",
                self.import_csv,
                name="import_orders.csv",
            )
        ]
        return new_urls + urls
