from django.db import models

from HerbalPureAPI import settings


class Order(models.Model):
    CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELED", "Canceled"),
        ("DELIVERED", "Delivered")
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user} - {self.status}"

    class Meta:
        ordering = ["-created_at"]
