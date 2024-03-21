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

    def get_queryset(self):
        category = self.request.query_params.get("category")
        promoted = self.request.query_params.get("promoted")

        queryset = self.queryset

        if category:
            queryset = queryset.filter(category_id=category)

        if promoted is not None:
            queryset = queryset.filter(promoted=promoted)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer

        if self.action == "retrieve":
            return ProductDetailSerializer

        return ProductSerializer
