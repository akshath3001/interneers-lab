import datetime

from ..models import Product


class ProductRepository:
    @staticmethod
    def get_all():
        return Product.objects.all()

    @staticmethod
    def get_by_id(product_id):
        return Product.objects.filter(id=product_id).first()

    @staticmethod
    def create(validated_data, categories):
        product = Product(**validated_data)
        product.product_category = categories
        product.save()
        return product, str(product.id)

    @staticmethod
    def update(product, updated_data, categories):
        for key, value in updated_data.items():
            setattr(product, key, value)
        product.product_category = categories
        product.updated_at = datetime.datetime.now()
        product.save()
        return product.id

    @staticmethod
    def delete(product):
        product.delete()
        return product.id
