from timeit import default_timer

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import Group

from shopapp.forms import ProductForm
from shopapp.models import Product, Order

def shop_index(request: HttpRequest):
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


def groups_list(request: HttpRequest):
    context = {
        "groups": Group.objects.prefetch_related('permissions').all(),
    }

    return render(request, 'shopapp/groups-list.html', context=context)


def products_list(request: HttpRequest):
    context = {
        "products": Product.objects.all(),
    }

    return render(request, 'shopapp/products-list.html', context=context)


def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data["name"]
            # description = form.cleaned_data["description"]
            # quantity = form.cleaned_data["quantity"]
            # price = form.cleaned_data["price"]
            # Product.objects.create(name=name, description=description, quantity=quantity, price=price)
            #Product.objects.create(**form.cleaned_data)
            form.save()
            url = reverse("shopapp:products_list")
            return  redirect(url)
    else:
        form = ProductForm()
    context = {
        "form": form,
    }

    return render(request, 'shopapp/create-product.html', context=context)


def orders_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all(),
    }

    return render(request, 'shopapp/orders-list.html', context=context)




#def shop_index(request: HttpRequest):
    # print(request.path)
    # print(request.method)
    # print(request.headers)
    #return HttpResponse("<h1>Hello!!!</h1>")
