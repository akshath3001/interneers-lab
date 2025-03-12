from django.db import models

class Category(models.Model):
    category_name=models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class Brand(models.Model):
    brand_name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.brand_name


class Product(models.Model):
    product_name=models.CharField(max_length=100)
    product_category=models.ManyToManyField(Category, related_name="product_category")
    product_description=models.TextField(max_length=200, blank=True)
    product_price=models.DecimalField(max_digits=10, decimal_places=2)
    product_brand=models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='product_brand')
    product_quantity=models.IntegerField(default=0)
    date_updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name