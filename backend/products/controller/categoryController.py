from django.core.paginator import EmptyPage
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from ..service.categoryService import CategoryService
from ..service.productService import ProductService


class ProductPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 10


class CategoryListController(APIView, ProductPagination):
    def get(self, request):
        try:
            page = int(request.GET.get("page", "1"))
            page_size = int(request.GET.get("page_size", "3"))
            response = CategoryService.get_all_category(page, page_size)
            return Response(response["data"], status=response["status"])
        except EmptyPage:
            return Response(
                {
                    "message": "Category doesn't exists",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request):
        response = CategoryService.create_category(request.data)
        return Response(response["data"], status=response["status"])


class CategoryController(APIView):
    def get(self, request, category_id):
        fetch_products = request.GET.get("products", "false")
        if fetch_products.lower() == "true":
            response = CategoryService.get_category_products(category_id)
        else:
            response = CategoryService.get_category(category_id)
        return Response(data=response["data"], status=response["status"])

    def post(self, request):
        response = CategoryService.create_category(request.data)
        return Response(response["data"], status=response["status"])

    def put(self, request, category_id):
        response = CategoryService.update_category(category_id, request.data)
        return Response(data=response["data"], status=response["status"])

    def delete(self, request, category_id):
        response = CategoryService.delete_category(category_id)
        return Response(response["data"], status=response["status"])


class CategoryProductController(APIView):
    def post(self, request, category_id, product_id):
        response = ProductService.add_product_to_category(category_id, product_id)
        return Response(response["data"], status=response["status"])

    def delete(self, request, category_id, product_id):
        response = ProductService.remove_product_from_category(category_id, product_id)
        return Response(response["data"], status=response["status"])
