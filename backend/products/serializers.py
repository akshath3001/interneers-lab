from rest_framework import serializers
from .models import Product, Category, Brand

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields='__all__'

class ProductSerializer(serializers.ModelSerializer):
    product_category=serializers.ListField(child=serializers.CharField(), write_only=True)
    product_brand=serializers.CharField(write_only=True)
    category = CategorySerializer(source='product_category', many=True, read_only=True)
    brand = BrandSerializer(source='product_brand', read_only=True)
    class Meta:
        model=Product
        fields=['id', 'product_name', 'product_category', 
                'category', 'product_description', 
                'product_price', 'product_brand', 
                'brand', 'product_quantity']
        depth=1
    
    def validate_product_price(self, value):
        if value<=0:
            raise serializers.ValidationError("Product price should be greater than 0")
        return value
    
    def validate_product_quantity(self, value):
        if value<0:
            raise serializers.ValidationError("Product quantity can't be -ve")
        return value
    
    def update(self, instance, validated_data):
        category_names = validated_data.pop('product_category', [])
        brand_name = validated_data.pop('product_brand', None)
        
        if brand_name:
            brand=Brand.objects.filter(brand_name__iexact=brand_name).first()
            if not brand:
                brand=Brand.objects.create(brand_name=brand_name.capitalize())
            instance.brand_name=brand
        
        if category_names is not None:
            categories=[]
            for category_name in category_names:
                category=Category.objects.filter(category_name__iexact=category_name).first()
                if not category:
                    category=Category.objects.create(category_name=category_name.capitalize())
                categories.append(category)   

            instance.product_category.set(categories)
        
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)
        instance.save()        
        return instance
    
    def create(self, validated_data):
        category_names = validated_data.pop('product_category', [])
        brand_name = validated_data.pop('product_brand', None)
        
        brand=Brand.objects.filter(brand_name__iexact=brand_name).first()
        if not brand:
            brand=Brand.objects.create(brand_name=brand_name.capitalize())
        categories=[]
        for category_name in category_names:
            category=Category.objects.filter(category_name__iexact=category_name).first()
            if not category:
                category=Category.objects.create(category_name=category_name.capitalize())
            categories.append(category)
        
        product = Product.objects.create(product_brand=brand, **validated_data)
        product.product_category.set(categories) 
        return product