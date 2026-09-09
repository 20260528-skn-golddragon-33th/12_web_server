from django.contrib import admin
from .models import Category, Discount, Product, Review

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'available')
    list_filter = ('available',)
    search_fields = ('name',)


admin.site.register([Category, Discount, Review])