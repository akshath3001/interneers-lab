from django.core.paginator import Paginator
from rest_framework import status

from ..repository.productCategoryRepository import CategoryRepository
from ..repository.productRepository import ProductRepository
from ..serializers import ProductSerializer


class ProductService:
    @staticmethod
    def get_all_products(page, page_size):
        products = ProductRepository.get_all()
        if not products.count():
            return {
                "data": {
                    "message": "Products doesn't exists",
                },
                "status": status.HTTP_404_NOT_FOUND,
            }
        paginator = Paginator(products, page_size)
        serialized_products = ProductSerializer(paginator.page(page), many=True).data
        return {
            "data": {
                "message": "Products retrieved successfully",
                "product": serialized_products,
            },
            "status": status.HTTP_200_OK,
        }

    @staticmethod
    def get_product(product_id):
        product = ProductRepository.get_by_id(product_id)
        if not product:
            return {
                "data": {
                    "message": "Product doesn't exists",
                    "product_id": str(product_id),
                },
                "status": status.HTTP_404_NOT_FOUND,
            }
        serialized_products = ProductSerializer(product).data
        return {
            "data": {
                "message": "Product retrieved successfully",
                "product": serialized_products,
            },
            "status": status.HTTP_200_OK,
        }

    @staticmethod
    def create_product(data):
        serializer = ProductSerializer(data=data)
        if not serializer.is_valid():
            return {"data": serializer.errors, "status": 400}

        validated_data = serializer.validated_data
        category_names = validated_data.pop("product_category", [])
        categories = CategoryRepository.get_or_create(category_names)

        product, product_id = ProductRepository.create(validated_data, categories)
        serialized_product = ProductSerializer(product).data

        return {
            "data": {
                "message": "Product created successfully",
                "product_id": str(product_id),
                "product": serialized_product,
            },
            "status": status.HTTP_201_CREATED,
        }

    @staticmethod
    def update_product(product_id, data):
        product = ProductRepository.get_by_id(product_id)
        if not product:
            return {
                "data": {
                    "message": "Product doesn't exists",
                    "product_id": str(product_id),
                },
                "status": status.HTTP_404_NOT_FOUND,
            }
        serializer = ProductSerializer(product, data=data, partial=True)
        if not serializer.is_valid():
            return {"data": serializer.errors, "status": status.HTTP_400_BAD_REQUEST}

        validated_data = serializer.validated_data
        category_names = validated_data.pop("product_category", [])

        if category_names is not None:
            categories = CategoryRepository.get_or_create(category_names)
            ProductRepository.update(product, validated_data, categories)
            return {
                "data": {
                    "message": "Product updated successfully",
                    "product_id": str(product_id),
                },
                "status": status.HTTP_204_NO_CONTENT,
            }

    @staticmethod
    def delete_product(product_id):
        product = ProductRepository.get_by_id(product_id)
        if not product:
            return {
                "data": {
                    "message": "Product doesn't exists",
                    "product_id": str(product_id),
                },
                "status": status.HTTP_404_NOT_FOUND,
            }
        ProductRepository.delete(product)
        return {
            "data": {
                "message": "Product deleted successfully",
                "product_id": str(product_id),
            },
            "status": status.HTTP_200_OK,
        }
