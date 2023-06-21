from timeit import default_timer

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from shopapp.forms import ProductForm, OrderForm, GroupForm
from shopapp.models import Product, Order

class ShopIndexView(View):
    def get(self, request: HttpRequest) ->HttpResponse:
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
    def get(self, request: HttpRequest) ->HttpResponse:
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
        #return self.get(request)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/product-details.html'
    model = Product
    context_object_name = "product"


# class ProductDetailsView(View):
#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         #product = Product.objects.get(pk=pk)
#         product = get_object_or_404(Product, pk=pk)
#         context = {
#             "product": product
#         }
#
#         return render(request, 'shopapp/product-details.html', context=context)


class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    #model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


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


class ProductCreateView(CreateView):
    model = Product
    fields = "name", "description", "quantity", "price"
    #form_class = GroupForm
    success_url = reverse_lazy("shopapp:products_list")


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


class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "description", "quantity", "price", "discount", "archived"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk":self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")


class ProductArchiveView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")
    template_name_suffix = "_confirm_archive_form"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products").all()
    )


class OrderDetailView(DetailView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products").all()
    )


# def orders_list(request: HttpRequest):
#     context = {
#         "orders": Order.objects.select_related("user").prefetch_related("products").all(),
#     }
#
#     return render(request, 'shopapp/order_list.html', context=context)


def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse("shopapp:orders_list")
            return  redirect(url)
    else:
        form = OrderForm()
    context = {
        "form": form,
    }

    return render(request, 'shopapp/create_order.html', context=context)


#def shop_index(request: HttpRequest):
    # print(request.path)
    # print(request.method)
    # print(request.headers)
    #return HttpResponse("<h1>Hello!!!</h1>")
