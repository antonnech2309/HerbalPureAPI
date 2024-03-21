# Generated by Django 5.0.3 on 2024-03-21 08:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0003_alter_order_user"),
        ("product", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="products",
        ),
        migrations.AddField(
            model_name="order",
            name="product",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="product.product",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="quantity",
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="OrderProduct",
        ),
    ]