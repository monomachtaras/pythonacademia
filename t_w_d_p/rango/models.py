from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    userLogo = models.ImageField(upload_to='user_images', blank=True)

    def __str__(self):
        return self.userLogo


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, blank=False, on_delete=models.PROTECT)
    name = models.CharField(max_length=128, unique=True)
    price = models.IntegerField()
    color = models.CharField(max_length=20)
    style = models.CharField(max_length=20)
    season = models.CharField(max_length=20)
    like = models.IntegerField()
    brand = models.CharField(max_length=20)
    productLogo = models.FileField(upload_to='product_images', blank=True)

    def __str__(self):
        return self.name + ' ' + str(self.price) + ' ' + str(self.productLogo)