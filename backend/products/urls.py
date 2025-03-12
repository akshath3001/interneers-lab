from django.urls import path
from .views import ProductListAPI, ProductAPI

urlpatterns = [
    path('products/', ProductListAPI.as_view(), name="products_list"),
    path('products/<int:product_id>', ProductAPI.as_view(), name="product")
]
