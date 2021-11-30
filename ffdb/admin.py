from django.contrib import admin
from .models import foodItems, foodStock

# Register your models here.

admin.site.register(foodItems)
admin.site.register(foodStock)