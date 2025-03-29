from rest_framework.response import Response
from rest_framework.views import APIView

from ..service.categoryService import CategoryService
from ..service.productService import ProductService


class CategoryController(APIView):
    def get(self, request, category_id):
        fetch_products = request.GET.get("products", "false")
        if fetch_products.lower() == "true":
            response = CategoryService.get_category_products(category_id)
        else:
            response = CategoryService.get_category(category_id)
        return Response(response["data"], status=response["status"])

    def post(self, request):
        response = CategoryService.create_category(request.data)
        return Response(response["data"], status=response["status"])

    def put(self, request, category_id):
        response = CategoryService.update_category(category_id, request.data)
        return Response(response["data"], status=response["status"])

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
