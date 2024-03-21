from rest_framework import serializers

from order.models import Order
from product.serializers import ProductListSerializer


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "product",
            "created_at",
            "quantity",
        )
        read_only_fields = ("id", "created_at")


class OrderListSerializer(OrderSerializer):
    product = ProductListSerializer(read_only=True)
