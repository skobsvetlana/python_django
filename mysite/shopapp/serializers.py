from rest_framework.serializers import ModelSerializer

from .models import Product

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
