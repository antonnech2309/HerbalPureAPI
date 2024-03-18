from django.contrib.auth import get_user_model
from django.db import models


class OrderStatus(models.Model):
    CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELED", "Canceled"),
        ("DELIVERED", "Delivered")
    ]

    status = models.CharField(
        max_length=50,
        choices=CHOICES,
    )

    def __str__(self):
        return self.status


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.status}"
