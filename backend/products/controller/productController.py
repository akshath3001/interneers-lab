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
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", ProductPagination.page_size))
        response = ProductService.get_all_products(page, page_size)
        return Response(response["data"], status=response["status"])

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
