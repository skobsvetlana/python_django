from rest_framework.serializers import ModelSerializer

from .models import Product, Order

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk",
            "name",
            "description",
            "quantity",
            "price",
            "discount",
            "created_at",
            "created_by",
            "archived",
            "preview",
        )


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "pk",
            "delivery_address",
            "promocode",
            "created_at",
            "user",
        )