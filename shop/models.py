from uuid import uuid4

from django.db import models

class Category(models.Model):
    name = models.CharField(verbose_name = "category_name",max_length = 100)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(verbose_name = "product id", unique = True, primary_key = True)
    name = models.CharField(verbose_name = "product name", max_length = 100)
    price = models.DecimalField(verbose_name = "product price", max_digits = 10,decimal_places = 2)
    descrition = models.TextField(null=True,blank= True)
    category = models.ForeignKey(to=Category,on_delete = models.PROTECT)

    def __str__(self):
        return self.name
