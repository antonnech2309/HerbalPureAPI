from rest_framework import serializers

from product.models import Category


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
