from rest_framework import serializers

from order.models import Order, OrderProduct
from product.models import Product
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
            if product and quantity <= product.total_amount:
                product.total_amount -= quantity
                Product.objects.filter(id=product.id).update(
                    total_amount=product.total_amount
                )
                OrderProduct.objects.create(
                    order=order, product=product, quantity=quantity
                )
            else:
                order.delete()
                raise serializers.ValidationError(
                    "Not enough products in stock."
                )

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

    @staticmethod
    def get_products(obj):
        products = OrderProduct.objects.filter(order=obj)
        products_data = []

        for product in products:
            product_data = OrderProductListSerializer(product).data
            product_data["product"]["image"] = (
                    "https://herbalpureapi.onrender.com" +
                    product.product.image.url
            )
            products_data.append(product_data)

        return products_data


# POST request
# {
#     "products": [
#         {
#             "product": 1,
#             "quantity": 2
#         },
#         {
#             "product": 2,
#             "quantity": 1
#         }
#     ]
# }

