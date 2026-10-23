from decimal import Decimal
from django.db import transaction
from django.db.models import Sum, F, Count
from django.http import FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Sale
from .serializers import ProductSerializer, SaleSerializer

def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def dashboard(request):
    sales_total = Sale.objects.aggregate(total=Sum('total'))['total'] or Decimal('0')
    sales_count = Sale.objects.count()
    products = Product.objects.all()
    return Response({'total_products': products.count(), 'stock_units': products.aggregate(n=Sum('quantity'))['n'] or 0,
        'sales_revenue': float(sales_total), 'low_stock': products.filter(quantity__lte=5).count(),
        'sales_count': sales_count, 'inventory_value': float(sum((p.cost_price*p.quantity for p in products), Decimal('0'))),
        'estimated_profit': float(sum(((s.unit_price - (s.product.cost_price if s.product_id else Decimal('0'))) * s.quantity for s in Sale.objects.select_related('product')), Decimal('0'))),
        'category_breakdown': list(products.values('category').annotate(count=Count('id')).order_by('-count'))})

@api_view(['GET','POST'])
def products(request):
    if request.method == 'GET':
        qs = Product.objects.all().order_by('name')
        category = request.query_params.get('category')
        search = request.query_params.get('search')
        if category and category != 'All categories': qs = qs.filter(category=category)
        if search: qs = qs.filter(name__icontains=search)
        return Response(ProductSerializer(qs, many=True).data)
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE','PATCH'])
def product_detail(request, pk):
    try: product = Product.objects.get(pk=pk)
    except Product.DoesNotExist: return Response({'error':'Product not found.'}, status=404)
    if request.method == 'DELETE':
        if product.sales.exists(): return Response({'error':'This product has sales history, so it cannot be deleted. Set its quantity to 0 instead.'}, status=400)
        product.delete(); return Response(status=204)
    serializer = ProductSerializer(product, data=request.data, partial=True)
    if serializer.is_valid(): serializer.save(); return Response(serializer.data)
    return Response(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET','POST'])
def sales(request):
    if request.method == 'GET':
        qs = Sale.objects.select_related('product').all().order_by('-created_at')[:100]
        return Response(SaleSerializer(qs, many=True).data)
    product_id = request.data.get('product')
    try: qty = int(request.data.get('quantity', 0))
    except (TypeError, ValueError): return Response({'error':'Enter a valid quantity.'}, status=400)
    if qty < 1: return Response({'error':'Quantity must be at least 1.'}, status=400)
    try: payment = request.data.get('payment_method', 'Cash'); product = Product.objects.get(pk=product_id)
    except (Product.DoesNotExist, ValueError, TypeError): return Response({'error':'Choose a valid product.'}, status=400)
    if payment not in ['Cash','UPI','Card']: return Response({'error':'Choose Cash, UPI or Card.'}, status=400)
    if qty > product.quantity: return Response({'error':f'Only {product.quantity} units are available.'}, status=400)
    with transaction.atomic():
        product.quantity -= qty; product.save(update_fields=['quantity'])
        sale = Sale.objects.create(product=product, product_name=product.name, quantity=qty, unit_price=product.price, total=product.price*qty, payment_method=payment)
    return Response(SaleSerializer(sale).data, status=201)

@api_view(['POST'])
def seed_demo(request):
    if Product.objects.exists() or Sale.objects.exists():
        return Response({'message':'Your database already contains data. Demo seed skipped to protect it.'}, status=409)
    demo = [
        ('LED Bulb 9W','Electronics',120,72,18),('Mixer Grinder 750W','Kitchen',1899,1420,4),('Electric Kettle','Home Appliances',999,690,8),('USB Cable','Accessories',149,55,3),('Ceiling Fan','Home Appliances',2299,1720,6),('Extension Board','Electronics',399,220,12),('Steel Water Bottle','Home & Living',299,145,16),('Induction Cooktop','Kitchen',2499,1900,5),('Emergency Light','Electronics',799,510,7),('Lunch Box Set','Home & Living',449,260,10),('Mobile Charger','Accessories',349,190,2),('Table Fan','Home Appliances',1399,950,9),('Smart LED Strip','Electronics',599,330,14),('Storage Container Set','Kitchen',499,285,11),('Plastic Stool','Home & Living',249,135,20)]
    for name, cat, price, cost, qty in demo: Product.objects.create(name=name, category=cat, price=price, cost_price=cost, quantity=qty)
    # Seed a few illustrative sales, while reducing the matching stock consistently.
    for name, qty, payment in [('LED Bulb 9W',2,'UPI'),('Steel Water Bottle',1,'Cash'),('Extension Board',1,'Card'),('Mixer Grinder 750W',1,'UPI')]:
        p = Product.objects.get(name=name)
        if p.quantity >= qty:
            p.quantity -= qty; p.save(update_fields=['quantity'])
            Sale.objects.create(product=p, product_name=p.name, quantity=qty, unit_price=p.price, total=p.price*qty, payment_method=payment)
    return Response({'message':'Demo inventory and sample sales loaded.', 'products_created':len(demo)}, status=201)
