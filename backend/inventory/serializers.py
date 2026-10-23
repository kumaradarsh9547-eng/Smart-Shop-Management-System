from rest_framework import serializers
from .models import Product, Sale
class ProductSerializer(serializers.ModelSerializer):
    stock_value = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','name','category','price','cost_price','quantity','stock_value','status','created_at']
    def get_stock_value(self, obj): return float(obj.price * obj.quantity)
    def get_status(self, obj): return 'Low stock' if obj.quantity <= 5 else 'In stock'
class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id','product','product_name','quantity','unit_price','total','payment_method','created_at']
        read_only_fields = ['id','product_name','unit_price','total','created_at']
