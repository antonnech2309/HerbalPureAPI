from rest_framework import viewsets

from product.models import Category
from product.serializers import CategorySerializer, ParentCategorySerializer


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
