from rest_framework import serializers


class CategorySerializer(serializers.Serializer):
    category_name = serializers.CharField(max_length=100)
    category_description = serializers.CharField(max_length=200)


class ProductSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=100)
    product_category = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )
    product_brand = serializers.CharField(max_length=100)
    product_description = serializers.CharField(
        max_length=200, required=False, allow_blank=True
    )
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    product_quantity = serializers.IntegerField(default=0)
    category = CategorySerializer(source="product_category", many=True, read_only=True)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_product_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Product price should be greater than 0")
        return value

    def validate_product_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Product quantity can't be negative")
        return value

    # def validate_product_brand(self, value):
    #     if not value.strip():
    #         raise serializers.ValidationError("Product brand is required")
    #     return value
