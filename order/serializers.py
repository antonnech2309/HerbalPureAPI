from rest_framework import serializers

from order.models import Order, OrderProduct
from product.serializers import ProductListSerializer


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = (
            "id",
            "product",
            "quantity",
        )


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "products",
            "status",
        )

    def create(self, validated_data):
        products_data = validated_data.pop("products")
        order = Order.objects.create(**validated_data)

        for product_data in products_data:
            product = product_data.get("product")
            quantity = product_data.get("quantity")
            if product and quantity:
                OrderProduct.objects.create(order=order, product=product, quantity=quantity)

        return order


class OrderProductListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(many=False)

    class Meta:
        model = OrderProduct
        fields = (
            "product",
            "quantity",
            "total"
        )


class OrderListSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "products",
            "status",
            "created_at",
            "order_price"
        )

    def get_products(self, obj):
        products = OrderProduct.objects.filter(order=obj)
        return [OrderProductListSerializer(product).data for product in products]
