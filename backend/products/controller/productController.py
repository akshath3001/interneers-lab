from django.core.paginator import EmptyPage
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from ..service.productService import ProductService


class ProductPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 10


class ProductListController(APIView, ProductPagination):
    def get(self, request):
        try:
            page = int(request.GET.get("page", "1"))
            page_size = int(request.GET.get("page_size", "3"))

            filters = {
                "product_name": request.GET.get("product_name"),
                "product_brand": request.GET.get("product_brand"),
                "categories": request.GET.getlist("categories"),
                "min_price": request.GET.get("min_price"),
                "max_price": request.GET.get("max_price"),
                "min_quantity": request.GET.get("min_quantity"),
                "max_quantity": request.GET.get("max_quantity"),
            }
            if any(filters.values()):
                response = ProductService.get_filtered_products(
                    filters, page, page_size
                )
            else:
                response = ProductService.get_all_products(page, page_size)
            return Response(response["data"], status=response["status"])
        except EmptyPage:
            return Response(
                {
                    "message": "Products doesn't exists",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request):
        product_data = request.data
        response = ProductService.create_product(product_data)
        return Response(response["data"], status=response["status"])


class ProductController(APIView):
    def get(self, request, product_id):
        response = ProductService.get_product(product_id)
        return Response(response["data"], status=response["status"])

    def put(self, request, product_id):
        response = ProductService.update_product(product_id, request.data)
        return Response(response["data"], status=response["status"])

    def delete(self, request, product_id):
        response = ProductService.delete_product(product_id)
        return Response(response["data"], status=response["status"])
