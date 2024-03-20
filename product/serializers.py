from rest_framework import serializers

from product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "parent_category")


class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class ParentCategorySerializer(serializers.ModelSerializer):
    subcategories = ChildCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "name", "subcategories")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "serving_size",
            "sale_quantity",
            "total_amount",
            "discount",
            "features",
            "instruction",
            "promoted",
            "category",
            "company",
            "order",
        )


class ProductDetailSerializer(ProductSerializer):
    category = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "serving_size",
            "sale_quantity",
            "total_amount",
            "discount",
            "features",
            "instruction",
            "promoted",
            "category",
            "company",
            "order",
            "slug",
        )


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "company",
            "discount",
            "promoted"
        )

# Post request for creating Prodyct
# {
#     "name": "string",
#     "description": "string",
#     "price": 0,
#     "serving_size": "string",
#     "sale_quantity": 0,
#     "total_amount": 0,
#     "discount": 0,
#     "features": [
#         "string"
#     ],
#     "instruction": "string",
#     "promoted": true,
#     "category": 2,
#     "company": "string",
#    }
