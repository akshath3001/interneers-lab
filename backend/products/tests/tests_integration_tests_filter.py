import os
import sys

import mongoengine
from django.test import TestCase

from products.models import Category, Product
from products.service.categoryService import CategoryService
from products.service.productService import ProductService


class ProductIntegrationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if "test" in sys.argv:
            mongoengine.disconnect()
            mongoengine.connect(
                host=os.getenv("MONGO_TEST_HOST"),
                alias="test_alias",
            )
            print("Connected to test_db for integration testing")
            Product._meta["db_alias"] = "test_alias"
            Category._meta["db_alias"] = "test_alias"
            print("Connected to test DB using alias 'test_alias'")

        PRODUCTS = [
            {
                "product_name": "MacBook Pro M3",
                "product_category": ["Laptop", "Electronics"],
                "product_description": "Latest MacBook Pro with M3 chip",
                "product_price": "200000.00",
                "product_brand": "Apple",
                "product_quantity": 3,
            },
            {
                "product_name": "Galaxy Tab S9",
                "product_category": ["Tablet", "Electronics"],
                "product_description": "Samsung's latest high-end tablet",
                "product_price": "90000.00",
                "product_brand": "Samsung",
                "product_quantity": 6,
            },
            {
                "product_name": "Sony WH-1000XM5",
                "product_category": ["Headphones", "Electronics"],
                "product_description": "Top noise-canceling wireless headphones",
                "product_price": "30000.00",
                "product_brand": "Sony",
                "product_quantity": 10,
            },
            {
                "product_name": "LG OLED C3",
                "product_category": ["TV", "Electronics"],
                "product_description": "OLED 4K Smart TV with AI Processor",
                "product_price": "150000.00",
                "product_brand": "LG",
                "product_quantity": 2,
            },
            {
                "product_name": "Canon EOS R6 Mark II",
                "product_category": ["Camera", "Electronics"],
                "product_description": "Professional mirrorless camera",
                "product_price": "250000.00",
                "product_brand": "Canon",
                "product_quantity": 3,
            },
        ]
        CATEGORIES = [
            {
                "category_name": "Electronics",
                "category_description": "Gadgets and devices",
            },
            {
                "category_name": "Clothing",
                "category_description": "Apparel and fashion",
            },
            {
                "category_name": "Books",
                "category_description": "Educational and leisure books",
            },
        ]

        CategoryService.create_categories(CATEGORIES)
        ProductService.create_products(PRODUCTS)

    @classmethod
    def tearDownClass(cls):
        Category.objects.delete()
        Product.objects.delete()

        mongoengine.disconnect()
        super().tearDownClass()
        print("`test_db` cleaned successfully!")

    def _fixture_setup(self):
        # Override to prevent Django from running SQL setup
        pass

    def _fixture_teardown(self):
        # Override to prevent Django from running SQL teardown
        pass

    # Testing the various filter combinations for get requests in Products
    def test_filter_products_by_multiple_categories(self):
        category_1 = Category.objects.filter(category_name="Laptop")[0]
        category_2 = Category.objects.filter(category_name="Camera")[0]
        response = self.client.get(
            f"/products/?categories={category_1.id}&categories={category_2.id}&page_size=10"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["products"]), 2)

    def test_filter_products_by_price_range_and_brand(self):
        response = self.client.get(
            "/products/?min_price=50000&max_price=250000&product_brand=Apple"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["products"]), 1)

    def test_filter_products_by_category_and_quantity(self):
        category_1 = Category.objects.filter(category_name="Electronics")[0]
        response = self.client.get(
            f"/products/?categories={category_1.id}&min_quantity=1&page_size=10"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["products"]), 5)

    def test_filter_products_by_multiple_criteria(self):
        category_1 = Category.objects.filter(category_name="Electronics")[0]
        response = self.client.get(
            f"/products/?categories={category_1.id}&min_price=60000&max_price=300000&min_quantity=3"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["products"]), 3)
