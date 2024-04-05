from django.db import models

from HerbalPureAPI import settings


class OrderProduct(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total(self) -> float:
        if self.product.discount:
            return round(self.quantity * (
                    self.product.price -
                    (self.product.price * self.product.discount / 100)
            ), 2)

        return round(self.quantity * self.product.price, 2)

    def __str__(self):
        return f"{self.product.__str__()} - {self.quantity} units - {self.total}$"


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

    @property
    def order_price(self) -> float:
        return round(
            sum([product.total for product in self.orderproduct_set.all()]),
            2
        )

    def __str__(self):
        products = [product.__str__() for product in self.products.all()]

        return (f"Order with products: {', '.join(products)} - "
                f"total price is {self.order_price}$")

    class Meta:
        ordering = ["-created_at"]
