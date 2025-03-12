from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer
from .models import Product
# Create your views here.

class ProductPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10

class ProductListAPI(APIView, ProductPagination):
    def get(self, request):
        products=Product.objects.all()
        if not products.exists():
            return Response({"message":"Products don't exist"}, status=status.HTTP_404_NOT_FOUND)

        paginator=ProductPagination()
        paginated_products=paginator.paginate_queryset(products, request, view=self)
        serializer=ProductSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)
        
    def post(self, request):
        is_many=isinstance(request.data, list)
        serializer=ProductSerializer(data=request.data, many= is_many)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Products created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductAPI(APIView): 
    def get_product(self,product_id):
        try:
            product= Product.objects.get(pk=product_id)
            return product
        except Product.DoesNotExist:
            return Response({"message":"Product doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, product_id):
        product=self.get_product(product_id)
        if isinstance(product, Response):
            return product
        serializer=ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, product_id):
        product=self.get_product(product_id)
        if isinstance(product, Response):
            return product     
        serializer=ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Product updated successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors)
    
    def delete(self, request, product_id):
        product=self.get_product(product_id)
        if isinstance(product, Response):
            return product
        product.delete()
        return Response({"message":"Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        
        




    

