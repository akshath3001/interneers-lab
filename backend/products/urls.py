from django.urls import path

from .controller.productController import ProductController, ProductListController

urlpatterns = [
    # product paths
    path("products/", ProductListController.as_view(), name="product_list"),
    path("products/<str:product_id>", ProductController.as_view(), name="product"),
]
