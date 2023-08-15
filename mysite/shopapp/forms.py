from django.forms import ModelForm, ImageField
from django.core import validators
from django.contrib.auth.models import Group

from .models import Product, Order
from django import forms


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "name", "description", "quantity", "price", "discount", "preview"

    # images = ImageField(
    #     widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}),
    #     required=False
    # )

    images = MultipleFileField()


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "delivery_address", "promocode", "user", "products"


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = "name",



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


