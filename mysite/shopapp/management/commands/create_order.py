from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from shopapp.models import Order, Product


class Command(BaseCommand):
    @transaction.atomic()
    def handle(self, *args, **options):
        #with transaction.atomic():
        #   ...

       self.stdout.write("Create order with products")
       user = User.objects.get(username="admin")
       # products: Sequence[Product] = Product.objects.all()
        # defer("ненужные поля",)
        # only("нужные поля",)
       products: Sequence[Product] = Product.objects.defer("price", "description", "created_at").all()
       order, created = Order.objects.get_or_create(
           delivery_address="Kazan 1",
           promocode= "promo2",
           user=user,
       )
       for product in products:
           order.products.add(product)

       self.stdout.write(f"reated order {order}")