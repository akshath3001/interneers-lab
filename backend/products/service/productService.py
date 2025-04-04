import logging

from django.core.paginator import Paginator
from rest_framework import status

from ..repository.categoryRepository import CategoryRepository
from ..repository.productRepository import ProductRepository
from ..serializers import ProductSerializer

logger = logging.getLogger(__name__)


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
            return {"data": serializer.errors, "status": status.HTTP_400_BAD_REQUEST}

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
    def create_products(data_list):
        if not isinstance(data_list, list):
            return {
                "data": {"error": "Invalid data format. Expected a list."},
                "status": status.HTTP_400_BAD_REQUEST,
            }

        product_details = []
        errors = []

        for data in data_list:
            serializer = ProductSerializer(data=data)
            if not serializer.is_valid():
                errors.append(serializer.errors)
            validated_data = serializer.validated_data
            category_names = validated_data.pop("product_category", [])
            categories = CategoryRepository.get_or_create(category_names)

            product, product_id = ProductRepository.create(validated_data, categories)
            serialized_product = ProductSerializer(product).data

            product_details.append(
                {"product_id": str(product_id), "product": serialized_product}
            )

        if errors:
            return {"data": {"errors": errors}, "status": status.HTTP_400_BAD_REQUEST}

        return {
            "data": {
                "message": "Products created successfully",
                "products": product_details,
            },
            "status": status.HTTP_201_CREATED,
        }

    @staticmethod
    def get_filtered_products(filters, page, page_size):
        products = ProductRepository.get_filtered(filters)
        paginator = Paginator(products, page_size)
        serialized_products = ProductSerializer(paginator.page(page), many=True).data
        return {
            "data": {
                "message": "Products based on applied filters retrieved",
                "products": serialized_products,
            },
            "status": status.HTTP_200_OK,
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

        serializer = ProductSerializer(data=data, partial=True)
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

    @staticmethod
    def add_product_to_category(category_id, product_id):
        category = CategoryRepository.get_by_id(category_id)
        product = ProductRepository.get_by_id(product_id)

        if not category or not product:
            return {
                "data": {
                    "message": "Category or Product not found",
                    "category_id": str(category_id),
                    "product_id": str(product_id),
                },
                "status": status.HTTP_404_NOT_FOUND,
            }

        if category in product.product_category:
            return {
                "data": {"message": "Product already in category"},
                "status": status.HTTP_400_BAD_REQUEST,
            }
        category_data = product.product_category
        category_data.append(category)
        ProductRepository.update_category(product, category_data)
        return {
            "data": {"message": "Product added to category successfully"},
            "status": status.HTTP_201_CREATED,
        }

    @staticmethod
    def remove_product_from_category(category_id, product_id):
        category = CategoryRepository.get_by_id(category_id)
        product = ProductRepository.get_by_id(product_id)

        if not category or not product:
            return {
                "data": {
                    "message": "Category or Product not found",
                    "category_id": str(category_id),
                    "product_id": str(product_id),
                },
                "status": status.HTTP_404_NOT_FOUND,
            }

        if category not in product.product_category:
            return {
                "data": {"message": "Product is not in the category"},
                "status": status.HTTP_400_BAD_REQUEST,
            }
        category_data = product.product_category
        category_data.remove(category)
        ProductRepository.update_category(product, category_data)
        return {
            "data": {"message": "Product removed from category successfully"},
            "status": status.HTTP_200_OK,
        }

    @staticmethod
    def migrate_products_without_category(category_id):
        products_without_category = ProductRepository.get_by_category(category=None)
        if not products_without_category:
            logger.info("No products need category migration.")
        else:
            for product in products_without_category:
                ProductService.add_product_to_category(
                    category_id=category_id,
                    product_id=product.id,
                )
                logger.info(
                    f"Assigned default category to product: {product.product_name}"
                )

    @staticmethod
    def migrate_products_without_brands(DEFAULT_BRAND):
        products_without_brand = ProductRepository.get_by_brand(brand=None)

        if not products_without_brand:
            logger.info("No products need brand migration.")
        else:
            for product in products_without_brand:
                ProductRepository.update_brand(product, DEFAULT_BRAND)
                logger.info(
                    f"Assigned default brand to product: {product.product_name}"
                )
