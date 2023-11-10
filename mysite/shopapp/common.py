from csv import DictReader
from io import TextIOWrapper

from django.contrib.auth.models import User
from shopapp.models import Product, Order


def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)

    products = [
        Product(**row)
        for row in reader
    ]

    Product.objects.bulk_create(products)

    return products


def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    data = list(DictReader(csv_file))

    for order in data:
        _import_order(order)


def _import_order(order_data):
    order_data['products'] = _validate_products_data(order_data['products'])
    user = User.objects.get(pk=order_data['user'])
    order = Order(
        delivery_address=order_data['delivery_address'],
        promocode=order_data['promocode'],
        created_at=order_data['created_at'],
        user=user)
    order.save()
    products = []
    for product in order_data['products']:
        product_instance = Product.objects.get(pk=product)
        products.append(product_instance)
    order.products.add(*products)


def _validate_products_data(data):
    products = map(int, data.split(","))

    return products
