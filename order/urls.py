from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order.views import OrderViewSet

router = DefaultRouter()

router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "order"
