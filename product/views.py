from rest_framework import viewsets

from product.models import Category, Product
from product.serializers import CategorySerializer, ParentCategorySerializer, ProductSerializer, ProductListSerializer, \
    ProductDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        if self.action == "list":
            return Category.objects.filter(parent_category=None)
        return Category.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ParentCategorySerializer
        return CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer

        if self.action == "retrieve":
            return ProductDetailSerializer

        return ProductSerializer
