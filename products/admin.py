from django.contrib import admin
from .models import Category, Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active') # Muestra la categoria en la lista

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
# Register your models here.
