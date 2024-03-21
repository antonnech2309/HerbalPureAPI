# Generated by Django 5.0.3 on 2024-03-20 20:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "parent_category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subcategories",
                        to="product.category",
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("price", models.FloatField()),
                ("serving_size", models.CharField(max_length=100)),
                ("sale_quantity", models.IntegerField(blank=True, null=True)),
                ("total_amount", models.IntegerField()),
                ("discount", models.IntegerField()),
                ("features", models.JSONField(default=list)),
                ("instruction", models.TextField()),
                ("promoted", models.BooleanField()),
                ("company", models.CharField(max_length=100)),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="product.category",
                    ),
                ),
            ],
            options={
                "ordering": ["promoted", "name"],
            },
        ),
    ]
