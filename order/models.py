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
