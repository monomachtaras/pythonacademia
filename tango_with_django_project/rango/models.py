from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    user_logo = models.ImageField(upload_to='user_images', blank=True)

    def __str__(self):
        return self.user_logo


class Product(models.Model):
    categories = (
        ('Fashion', 'Fashion'), ('Watches', 'Watches'), ('Fine Jewelry', 'Fine Jewelry'),
        ('Fashion Jewelry', 'Fashion Jewelry'), ('Engagement & Wedding', 'Engagement & Wedding'),
        ('Men\'s Jewelry', 'Men\'s Jewelry'), ('Vintage & Antique', 'Vintage & Antique'),
        ('Loose Diamonds', 'Loose Diamonds'), ('Loose Beads', 'Loose Beads')
                )
    name = models.CharField(max_length=128, unique=True)
    price = models.IntegerField()
    category = models.CharField(max_length=25, choices=categories, default='Fashion')
    color = models.CharField(max_length=20)
    style = models.CharField(max_length=20)
    season = models.CharField(max_length=20)
    like = models.IntegerField()
    brand = models.CharField(max_length=20)
    product_logo = models.FileField(upload_to='product_images', blank=True)

    def __str__(self):
        return self.name + ' ' + str(self.price) + ' ' + str(self.product_logo)