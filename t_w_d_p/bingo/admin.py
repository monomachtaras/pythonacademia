from django.contrib import admin

from .models import Number, Age, City, TimeDate


admin.site.register(Number)
admin.site.register(Age)
admin.site.register(City)
admin.site.register(TimeDate)
