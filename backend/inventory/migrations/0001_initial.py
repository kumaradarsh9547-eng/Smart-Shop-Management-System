from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name='Product', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=120)),
            ('category', models.CharField(choices=[('Electronics','Electronics'),('Home Appliances','Home Appliances'),('Kitchen','Kitchen'),('Accessories','Accessories'),('Home & Living','Home & Living'),('Other','Other')], default='Electronics', max_length=40)),
            ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ('cost_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ('quantity', models.PositiveIntegerField(default=0)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
        ]),
        migrations.CreateModel(name='Sale', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('product_name', models.CharField(max_length=120)),
            ('quantity', models.PositiveIntegerField()),
            ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ('total', models.DecimalField(decimal_places=2, max_digits=12)),
            ('payment_method', models.CharField(choices=[('Cash','Cash'),('UPI','UPI'),('Card','Card')], default='Cash', max_length=10)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales', to='inventory.product')),
        ]),
    ]
