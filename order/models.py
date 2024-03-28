from django.db import models

from HerbalPureAPI import settings


class OrderProduct(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total(self) -> float:
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.order} - {self.product} ({self.quantity})"


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
    products = models.ManyToManyField("product.Product", through=OrderProduct)

    def __str__(self):
        return f"{self.user} - {self.status}"

    class Meta:
        ordering = ["-created_at"]
