from django import forms
from django.core import validators

from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "description", "quantity", "price", "discount"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "delivery_address", "promocode", "user", "products"


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     description = forms.CharField(
#         label="Product description",
#         widget=forms.Textarea(attrs={"rows": 7, "cols": 50}),
#         validators=[validators.RegexValidator(
#             regex=r"great",
#             message="Field must contain word 'greate'"
#         )],
#     )
#     quantity = forms.IntegerField(min_value=0)
#     price = forms.DecimalField(min_value=0, max_value=10000000, decimal_places=2)
