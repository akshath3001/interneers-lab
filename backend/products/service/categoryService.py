from django.core.paginator import Paginator
from rest_framework import status

from ..repository.categoryRepository import CategoryRepository
from ..serializers import CategorySerializer, ProductSerializer


class CategoryService:
    @staticmethod
    def get_all_category(page, page_size):
        categories = CategoryRepository.get_all()
        if not categories.count():
            return {
                "data": {
                    "message": "Category doesn't exists",
                },
                "status": status.HTTP_404_NOT_FOUND,
            }
        paginator = Paginator(categories, page_size)
        paginated_categories = paginator.page(page)
        serialized_categories = CategorySerializer(paginated_categories, many=True).data
        return {
            "data": {
                "message": "Categories retrieved successfully",
                "category": serialized_categories,
                "num_pages": paginator.num_pages,
            },
            "status": status.HTTP_200_OK,
        }

    @staticmethod
    def get_category_products(category_id):
        category = CategoryRepository.get_by_id(category_id)
        if not category:
            return {
                "data": {
                    "message": "Category doesn't exists",
                    "category_id": str(category_id),
                },
                "status": status.HTTP_404_NOT_FOUND,
            }
        products = CategoryRepository.get_by_category(category)
        serialized_products = ProductSerializer(products, many=True).data
        if not products:
            return {
                "data": {
                    "message": f"No products belong to '{category.category_name}' category"
                },
                "status": status.HTTP_400_BAD_REQUEST,
            }

        return {
            "data": {
                "message": f"Products from '{category.category_name}' category retrieved successfully",
                "category_products": serialized_products,
            },
            "status": status.HTTP_200_OK,
        }

    @staticmethod
    def get_category(category_id):
        category = CategoryRepository.get_by_id(category_id)
        if not category:
            return {
                "data": {
                    "message": "Category doesn't exists",
                    "category_id": str(category_id),
                },
                "status": status.HTTP_404_NOT_FOUND,
            }
        serialized_category = CategorySerializer(category).data
        return {
            "data": {
                "message": "Category retrieved successfully",
                "category": serialized_category,
            },
            "status": status.HTTP_204_NO_CONTENT,
        }

    @staticmethod
    def create_category(category_data):
        category_serializer = CategorySerializer(data=category_data)
        if not category_serializer.is_valid():
            return {
                "data": category_serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
            }

        category, category_id = CategoryRepository.create(
            category_serializer.validated_data
        )

        serialized_category = CategorySerializer(category).data
        return {
            "data": {
                "message": "Category created successfully",
                "category_id": str(category_id),
                "category": serialized_category,
            },
            "status": status.HTTP_201_CREATED,
        }

    @staticmethod
    def create_categories(categories_data):
        category_details = []
        for category_data in categories_data:
            category_serializer = CategorySerializer(data=category_data)
            if not category_serializer.is_valid():
                return {
                    "data": category_serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            category, category_id = CategoryRepository.create(
                category_serializer.validated_data
            )
            serialized_category = CategorySerializer(category).data
            category_details.append(
                {"category_id": str(category_id), "category": serialized_category}
            )
        return category_details

    @staticmethod
    def update_category(category_id, data):
        category = CategoryRepository.get_by_id(category_id)
        if not category:
            return {
                "data": {
                    "message": "Category doesn't exists",
                    "category_id": str(category_id),
                },
                "status": status.HTTP_404_NOT_FOUND,
            }
        category_serializer = CategorySerializer(data=data, partial=True)
        if not category_serializer.is_valid():
            return {
                "data": category_serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
            }

        category_id = CategoryRepository.update(
            category, category_serializer.validated_data
        )
        return {
            "data": {
                "message": "Category updated successfully",
                "category_id": str(category_id),
            },
            "status": status.HTTP_204_NO_CONTENT,
        }

    @staticmethod
    def delete_category(category_id):
        category = CategoryRepository.get_by_id(category_id)
        if not category:
            return {
                "data": {
                    "message": "Category doesn't exists",
                    "category_id": str(category_id),
                },
                "status": status.HTTP_404_NOT_FOUND,
            }
        CategoryRepository.delete(category)
        return {
            "data": {
                "message": "Category deleted successfully",
                "category_id": str(category_id),
            },
            "status": status.HTTP_200_OK,
        }
