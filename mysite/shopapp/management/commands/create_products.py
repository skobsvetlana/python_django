from django.core.management import BaseCommand
from shopapp.models import Product

class Command(BaseCommand):
    """
    Creates products
    """

    def handle(self, *args, **options):
        self.stdout.write("Create products")

        products = [
            ("Laptop", "", 4, 2999, 0),
            ("Desktop", "", 8, 4999, 0),
            ("Smartphone", "", 15, 999, 0),
        ]

        for name, description, quantity, price, discount in products:
            product, created = Product.objects.get_or_create(name=name,
                                                             description=description,
                                                             quantity=quantity,
                                                             price=price,
                                                             discount=discount,
                                                             )
            self.stdout.write(f"Created product - {product.name}")
            #product.save()

        self.stdout.write(self.style.SUCCESS("Products created"))
