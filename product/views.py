from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from product.models import Category, Product
from product.serializers import CategorySerializer, ParentCategorySerializer, ProductSerializer, ProductListSerializer, \
    ProductDetailSerializer, ProductImageSerializer


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
        if self.action == "upload_image":
            return ProductImageSerializer

        return ProductSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[],
    )
    def upload_image(self, request, slug=None):
        """Endpoint for uploading image to specific product"""
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "category",
                type=int,
                description="Filter by product category id (ex. ?category=1)",
            ),
            OpenApiParameter(
                "promoted",
                type=bool,
                description="Filter by product promotion (ex. ?promoted=True) "
                            "(boolean must be capitalized: True, False)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
