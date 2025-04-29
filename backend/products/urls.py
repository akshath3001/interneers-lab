from django.urls import path

from .controller.productController import ProductController, ProductListController
from .controller.categoryController import (
    CategoryController,
    CategoryProductController,
    CategoryListController,
)

urlpatterns = [
    # product paths
    path("products/", ProductListController.as_view(), name="product_list"),
    path("products/<str:product_id>", ProductController.as_view(), name="product"),
    # category paths
    path(
        "category/",
        CategoryListController.as_view(),
        name="category",
    ),
    path(
        "category/<str:category_id>",
        CategoryController.as_view(),
        name="category_details",
    ),
    # Add/Remove product from category paths
    path(
        "category/<str:category_id>/add/<str:product_id>",
        CategoryProductController.as_view(),
        name="add_product_to_category",
    ),
    path(
        "category/<str:category_id>/remove/<str:product_id>",
        CategoryProductController.as_view(),
        name="remove_product_from_category",
    ),
]
