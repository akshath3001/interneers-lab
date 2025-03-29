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
    def get_by_category(category):
        return Product.objects(product_category__size=0)

    @staticmethod
    def get_by_brand(brand):
        return Product.objects(product_brand__exists=False)

    @staticmethod
    def get_filtered(filters):
        query = {}

        if filters.get("product_name"):
            query["product_name__icontains"] = filters["product_name"]

        if filters.get("product_brand"):
            query["product_brand__icontains"] = filters["product_brand"]

        if filters.get("categories"):
            query["product_category__in"] = filters["categories"]

        if filters.get("min_price"):
            query["product_price__gte"] = float(filters["min_price"])

        if filters.get("max_price"):
            query["product_price__lte"] = float(filters["max_price"])

        if filters.get("min_quantity"):
            query["product_quantity__gte"] = int(filters["min_quantity"])

        if filters.get("max_quantity"):
            query["product_quantity__lte"] = int(filters["max_quantity"])

        return list(Product.objects(**query))

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
    def update_category(product, categories):
        product.product_category = categories
        product.updated_at = datetime.datetime.now()
        product.save()
        return product.id

    @staticmethod
    def update_brand(product, brand):
        product.product_brand = brand["product_brand"]
        product.updated_at = datetime.datetime.now()
        product.save()
        return product.id

    @staticmethod
    def delete(product):
        product.delete()
        return product.id
