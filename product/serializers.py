from rest_framework import serializers

from product.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "parent_category")


class NestedCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class CategoryListSerializer(CategorySerializer):
    parent_category = NestedCategoryListSerializer()
