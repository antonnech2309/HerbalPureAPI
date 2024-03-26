import os
import uuid

from django.db import models
from django.template.defaultfilters import slugify

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
            return f"{self.parent_category.name}/{self.name}"

        return self.name

    class Meta:
        ordering = ["name"]


def product_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/", filename)


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, upload_to=product_image_file_path)
    description = models.TextField()
    price = models.FloatField()
    serving_size = models.CharField(max_length=100)
    capsules_amount = models.IntegerField(blank=True, null=True)
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
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:

            if self.capsules_amount:
                self.slug = slugify(
                    f"{self.name} {self.company} {self.category.name} "
                    f"{self.capsules_amount} capsules"
                )
            else:
                self.slug = slugify(
                    f"{self.name} {self.company} {self.category.name}"
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.company} {self.category.name}"

    class Meta:
        ordering = ["promoted", "name"]
