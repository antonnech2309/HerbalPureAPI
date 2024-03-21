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
