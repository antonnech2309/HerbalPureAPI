from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.response import Response

from HerbalPureAPI import settings
from order.models import Order
from order.serializers import OrderSerializer, OrderListSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return OrderListSerializer
        return OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            # Customize the response data here
            response_data = {
                "id": serializer.instance.id,
                "message": "Order created successfully!",
            }

            try:
                message = (f"Your order was created successfully! "
                           f"{serializer.instance.__str__()}")

                send_mail(
                    f"Message from Herbal Pure Company",
                    message,
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                )
            except Exception as e:
                response_data["message"] = ("Order created successfully, "
                                            "but failed to send an email.")

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
