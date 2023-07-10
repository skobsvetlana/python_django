from time import sleep
from timeit import default_timer

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from shopapp.forms import ProductForm, OrderForm, GroupForm
from shopapp.models import Product, Order


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        cities = [
            {'name': 'Mumbai', 'population': '19,000,000', 'country': 'India'},
            {'name': 'Calcutta', 'population': '15,000,000', 'country': 'India'},
            {'name': 'New York', 'population': '20,000,000', 'country': 'USA'},
            {'name': 'Chicago', 'population': '7,000,000', 'country': 'USA'},
            {'name': 'Tokyo', 'population': '33,000,000', 'country': 'Japan'},
        ]
        greeting_str = "hello shop index!"
        num_messages = 6
        context = {
            "time_running": default_timer(),
            "products": products,
            "cities": cities,
            "greeting_str": greeting_str,
            "num_messages": num_messages,
        }

        return render(request, 'shopapp/shop_index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }

        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)
        # return self.get(request)


class ProductDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'shopapp/product-details.html'
    model = Product
    context_object_name = "product"


class ProductListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "shopapp.view_product", "shopapp.add_product",
    template_name = 'shopapp/create-product.html'

    model = Product
    fields = "name", "description", "quantity", "price"
    # form_class = GroupForm
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    # permission_required = "shopapp.view_product", "shopapp.change_product",
    template_name = 'shopapp/product_update_form.html'
    model = Product
    fields = "name", "description", "quantity", "price", "discount", "archived"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.object.pk)
        user = self.request.user
        if user == product.created_by or user.is_superuser:
            return super().form_valid(form)
        else:
            #return redirect(request.path)
            return redirect("shopapp:error_no_permission")


class ErrorView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {

        }

        return render(request, 'shopapp/error_no_permission.html', context=context)


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'shopapp/product_confirm_delete.html'
    permission_required = "shopapp.view_product", "shopapp.delete_product",
    model = Product
    success_url = reverse_lazy("shopapp:products_list")


class ProductArchiveView(PermissionRequiredMixin, DeleteView):
    template_name = 'shopapp/product_confirm_archive_form.html'
    permission_required = "shopapp.view_product", "shopapp.delete_product",
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    # template_name_suffix = "_confirm_archive_form"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "description": product.description,
                "quantity": product.quantity,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})



class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/order_list.html'
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products").all()
    )


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order",
    template_name = 'shopapp/order-details.html'
    context_object_name = "order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products").all()
    )


class OrderUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "shopapp.view_order", "shopapp.change_order"
    # model = Order
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products").all()
    )
    fields = "delivery_address", "promocode", "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )


class OrderCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "shopapp.view_order", "shopapp.add_order"
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    success_url = reverse_lazy("shopapp:orders_list")


class OrderDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "shopapp.view_order", "shopapp.delete_orderr"
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


class OrdersExportView(UserPassesTestMixin, ListView):
    template_name = 'shopapp/order-export.html'
    context_object_name = "export_orders"
    queryset = (
        Order.objects
        .order_by("pk")
        .select_related("user")
        .prefetch_related("products").all()
    )

    def test_func(self):
        return self.request.user.is_staff

    # def get_queryset(self) -> HttpResponse:
    #     orders = Order.objects.order_by("pk").select_related("user").prefetch_related("products").all()






# class ProductListView(TemplateView):
#     template_name = 'shopapp/products-list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["products"] = Product.objects.all()
#         return context


# def products_list(request: HttpRequest):
#     context = {
#         "products": Product.objects.all(),
#     }
#
#     return render(request, 'shopapp/products-list.html', context=context)


# class ProductDetailsView(View):
#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         #product = Product.objects.get(pk=pk)
#         product = get_object_or_404(Product, pk=pk)
#         context = {
#             "product": product
#         }
#
#         return render(request, 'shopapp/product-details.html', context=context)


# class ProductCreateView(UserPassesTestMixin, CreateView):
#     def test_func(self):
#     #     #return self.request.user.groups.filter(name="secret-group").exists()
#         return self.request.user.is_superuser
#
#     model = Product
#     fields = "name", "description", "quantity", "price", "created_by"
#     #form_class = GroupForm
#     success_url = reverse_lazy("shopapp:products_list")


# def create_product(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             '''# name = form.cleaned_data["name"]
#             # description = form.cleaned_data["description"]
#             # quantity = form.cleaned_data["quantity"]
#             # price = form.cleaned_data["price"]
#             # Product.objects.create(name=name, description=description, quantity=quantity, price=price)
#             #Product.objects.create(**form.cleaned_data)'''
#             form.save()
#             url = reverse("shopapp:products_list")
#             return  redirect(url)
#     else:
#         form = ProductForm()
#     context = {
#         "form": form,
#     }
#
#     return render(request, 'shopapp/create-product.html', context=context)


# def orders_list(request: HttpRequest):
#     context = {
#         "orders": Order.objects.select_related("user").prefetch_related("products").all(),
#     }
#
#     return render(request, 'shopapp/order_list.html', context=context)


# def create_order(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse("shopapp:orders_list")
#             return  redirect(url)
#     else:
#         form = OrderForm()
#     context = {
#         "form": form,
#     }
#
#     return render(request, 'shopapp/create-order.html', context=context)


# def shop_index(request: HttpRequest):
# print(request.path)
# print(request.method)
# print(request.headers)
# return HttpResponse("<h1>Hello!!!</h1>")
