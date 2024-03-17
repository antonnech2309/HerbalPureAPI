from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        if self.parent_category:
            return self.parent_category.name

        return self.name
