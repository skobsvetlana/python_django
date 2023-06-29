from django.db import models
from django.contrib.auth.models import User

from mysite import settings


class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]
        #verbose_name_plural = "products"
        #db_table = "tech_products"

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=False)
    archived = models.BooleanField(default=False)


    # @property
    # def description_short(self) -> str:
    #     if len(self.description) <= 50:
    #         return self.description
    #     else:
    #         return self.description[:50] + "..."

    def __str__(self) -> str:
        return f"Product (pk={self.pk}, " \
               f"name={self.name!r}, " \
               f"price={self.price}, " \
               f"created_by={self.created_by})"


class Order(models.Model):
    delivery_address = models.TextField(null=False, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")