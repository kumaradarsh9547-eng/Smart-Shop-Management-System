from django.db import models
class Product(models.Model):
    CATEGORY_CHOICES = [('Electronics','Electronics'),('Home Appliances','Home Appliances'),('Kitchen','Kitchen'),('Accessories','Accessories'),('Home & Living','Home & Living'),('Other','Other')]
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default='Electronics')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
class Sale(models.Model):
    PAYMENT_CHOICES = [('Cash','Cash'),('UPI','UPI'),('Card','Card')]
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='sales')
    product_name = models.CharField(max_length=120)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='Cash')
    created_at = models.DateTimeField(auto_now_add=True)
