from django.contrib import admin

from .models import Category, Product

admin.register(Product)
admin.register(Category)
