from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
       self.stdout.write("Start demo bulk actions")
       # info = [
       #     ("smartphone1", 199),
       #     ("smartphone2", 299),
       #     ("smartphone3", 399),
       # ]
       #
       # products = [
       #     Product(name=name, price=price)
       #     for name, price in info
       # ]
       # result = Product.objects.bulk_create(products)
       # for obj in result:
       #     print(obj)
       result = Product.objects.filter(
           name_contains="smartphone"
       ).update(discount=10)

       self.stdout.write("Done")