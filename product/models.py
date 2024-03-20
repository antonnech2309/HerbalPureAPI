from django.db import models

from order.models import Order


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subcategories"
    )

    def __str__(self):
        if self.parent_category:
            return self.parent_category.name

        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    serving_size = models.CharField(max_length=100)
    sale_quantity = models.IntegerField(blank=True, null=True)
    total_amount = models.IntegerField()
    discount = models.IntegerField()
    features = models.JSONField(default=list)
    instruction = models.TextField()
    promoted = models.BooleanField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    company = models.CharField(max_length=100)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="products"
    )

    def __str__(self):
        return f"{self.name} {self.company} {self.category.name}"
