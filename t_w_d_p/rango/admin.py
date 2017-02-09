from django.contrib import admin
from .models import Product, Category, UserProfile


class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'color', 'style', 'brand')


admin.site.register(Product, PageAdmin)
admin.site.register(Category)
admin.site.register(UserProfile)



