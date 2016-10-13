from django.contrib import admin
from .models import Product


class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'color', 'style', 'brand')


admin.site.register(Product, PageAdmin)

