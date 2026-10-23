from django.urls import path
from .views import products, product_detail, sales
urlpatterns = [path('products/', products), path('products/<int:pk>/', product_detail), path('sales/', sales)]
