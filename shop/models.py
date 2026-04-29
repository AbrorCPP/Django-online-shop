import uuid

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(verbose_name = "category_name",max_length = 100)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,  # Har safar yangi UUID generatsiya qiladi
        editable=False       # Foydalanuvchi buni o'zgartira olmaydi
    )
    name = models.CharField(verbose_name = "product name", max_length = 100)
    price = models.DecimalField(verbose_name = "product price", max_digits = 10,decimal_places = 2)
    descrition = models.TextField(null=True,blank= True)
    category = models.ForeignKey(to=Category,on_delete = models.PROTECT)
    image = models.ImageField(upload_to = "images/products",null = True, blank= "True")
    is_available = models.BooleanField(default=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.name
