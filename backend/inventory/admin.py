from django.contrib import admin
from .models import Product, Sale
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin): list_display = ('name','category','price','cost_price','quantity'); search_fields = ('name',); list_filter = ('category',)
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin): list_display = ('product_name','quantity','total','payment_method','created_at'); list_filter = ('payment_method','created_at')
