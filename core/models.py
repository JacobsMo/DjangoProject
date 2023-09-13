from django.db import models
from datetime import datetime


class Product(models.Model):
    name = models.CharField(max_length=255)
    # usd format
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True)
    time_create = models.DateTimeField(default=datetime.now())
    time_update = models.DateTimeField(default=datetime.now())


class Category(models.Model):
    name = models.CharField(max_length=70, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Categories"
        verbose_name_plural = "Categories"
