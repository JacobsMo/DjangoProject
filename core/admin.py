from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "quantity", "category")
    list_display_links = ("name", "price", "quantity", "category")
    search_fields = ("name", "price", "quantity", "category", "time_create", "time_update")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name", "description")    


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
