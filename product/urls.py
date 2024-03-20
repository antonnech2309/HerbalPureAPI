from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import CategoryViewSet, ProductViewSet

router = DefaultRouter()

router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)


urlpatterns = [
    path("", include(router.urls))
]

app_name = "product"
