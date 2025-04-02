import mongoengine
import sys
from django.test import TestCase
import subprocess
from products.models import Category, Product
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class IntegrationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        if "tests" in sys.argv:
            mongoengine.disconnect()
            mongoengine.connect(
                db="test_db",
                host="mongodb://aks:aks%403001@localhost:27018/test_db?authSource=admin",
                username="aks",
                password="aks@3001",
                authentication_source="admin",
                uuidRepresentation="standard",
                alias="test_alias",
            )
            print("Connected to test_db for integration testing")
        try:
            logger.info("Using test database for seeding.")

            from products.scripts.seed_test_data import seed_test_db

            logger.info("Running test seed script for test database...")
            seed_test_db()
            logger.info("Test seed script completed successfully for test database.")

        except subprocess.CalledProcessError as e:
            print(f"Failed to run seed script: {e}")

        # Demo products and categories for testing
        cls.product1 = {
            "product_name": "MacBook Pro M3",
            "product_category": ["Laptop", "Electronics"],
            "product_description": "Latest MacBook Pro with M3 chip",
            "product_price": "200000.00",
            "product_brand": "Apple",
            "product_quantity": 3,
        }
        cls.product2 = {
            "product_name": "Galaxy Tab S9",
            "product_category": ["Tablet", "Electronics"],
            "product_description": "Samsung's latest high-end tablet",
            "product_price": "90000.00",
            "product_brand": "Samsung",
            "product_quantity": 6,
        }
        cls.product3 = {
            "product_name": "Sony WH-1000XM5",
            "product_category": ["Headphones", "Electronics"],
            "product_description": "Top noise-canceling wireless headphones",
            "product_price": "30000.00",
            "product_brand": "Sony",
            "product_quantity": 10,
        }
        cls.product4 = {
            "product_name": "LG OLED C3",
            "product_category": ["TV", "Electronics"],
            "product_description": "OLED 4K Smart TV with AI Processor",
            "product_price": "150000.00",
            "product_brand": "LG",
            "product_quantity": 2,
        }
        cls.product5 = {
            "product_name": "Canon EOS R6 Mark II",
            "product_category": ["Camera", "Electronics"],
            "product_description": "Professional mirrorless camera",
            "product_price": "250000.00",
            "product_brand": "Canon",
            "product_quantity": 3,
        }
        cls.category1 = {
            "category_name": "Electronics",
            "category_description": "Gadgets and devices",
        }
        cls.category2 = {
            "category_name": "Clothing",
            "category_description": "Apparel and fashion",
        }
        cls.category3 = {
            "category_name": "Books",
            "category_description": "Educational and leisure books",
        }

    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     if "test" in sys.argv:
    #         mongoengine.disconnect()
    #         mongoengine.connect(
    #             db="test_db",
    #             host="mongodb://aks:aks%403001@localhost:27018/test_db?authSource=admin",
    #             username="aks",
    #             password="aks@3001",
    #             authentication_source="admin",
    #             uuidRepresentation="standard",
    #             alias="test_alias",
    #         )
    #         print("Connected to `test_db` for integration testing")
    #         try:
    #             logger.info("Using test database for seeding.")

    #             from products.scripts.seed_test_data import seed_test_db

    #             logger.info("Running test seed script for test database...")
    #             seed_test_db()
    #             logger.info(
    #                 "Test seed script completed successfully for test database."
    #             )

    #         except subprocess.CalledProcessError as e:
    #             print(f"Failed to run seed script: {e}")

    #     cls.product1 = {
    #         "product_name": "MacBook Pro M3",
    #         "product_category": ["Laptop", "Electronics"],
    #         "product_description": "Latest MacBook Pro with M3 chip",
    #         "product_price": "200000.00",
    #         "product_brand": "Apple",
    #         "product_quantity": 3,
    #     }
    #     cls.product2 = {
    #         "product_name": "Galaxy Tab S9",
    #         "product_category": ["Tablet", "Electronics"],
    #         "product_description": "Samsung's latest high-end tablet",
    #         "product_price": "90000.00",
    #         "product_brand": "Samsung",
    #         "product_quantity": 6,
    #     }
    #     cls.product3 = {
    #         "product_name": "Sony WH-1000XM5",
    #         "product_category": ["Headphones", "Electronics"],
    #         "product_description": "Top noise-canceling wireless headphones",
    #         "product_price": "30000.00",
    #         "product_brand": "Sony",
    #         "product_quantity": 10,
    #     }
    #     cls.product4 = {
    #         "product_name": "LG OLED C3",
    #         "product_category": ["TV", "Electronics"],
    #         "product_description": "OLED 4K Smart TV with AI Processor",
    #         "product_price": "150000.00",
    #         "product_brand": "LG",
    #         "product_quantity": 2,
    #     }
    #     cls.product5 = {
    #         "product_name": "Canon EOS R6 Mark II",
    #         "product_category": ["Camera", "Electronics"],
    #         "product_description": "Professional mirrorless camera",
    #         "product_price": "250000.00",
    #         "product_brand": "Canon",
    #         "product_quantity": 3,
    #     }
    #     cls.category1 = {
    #         "category_name": "Electronics",
    #         "category_description": "Gadgets and devices",
    #     }
    #     cls.category2 = {
    #         "category_name": "Clothing",
    #         "category_description": "Apparel and fashion",
    #     }
    #     cls.category3 = {
    #         "category_name": "Books",
    #         "category_description": "Educational and leisure books",
    #     }

    @classmethod
    def tearDownClass(cls):
        Category.objects.delete()
        Product.objects.delete()

        mongoengine.disconnect()
        super().tearDownClass()
        print("`test_db` cleaned successfully!")

    def setUp(self):
        Product.objects.delete()
        Category.objects.delete()

    def _fixture_setup(self):
        # Override to prevent Django from running SQL setup
        pass

    def _fixture_teardown(self):
        # Override to prevent Django from running SQL teardown
        pass

    # Testing get request for product list to return error message
    # when no products exist
    def test_get_product_list_no_products(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Products doesn't exists")

    # Testing post request to create product and return success message
    def test_create_single_product(self):
        response = self.client.post("/products/", self.product1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    # Testing get request with product_id to return the product
    def test_get_single_product(self):
        response = self.client.post("/products/", self.product1)
        prod = Product.objects.filter(
            product_name__iexact=self.product1["product_name"]
        ).first()
        response = self.client.get(f"/products/{prod.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["product"]["product_name"], self.product1["product_name"]
        )

    # Testing get request for product to return error message
    # when products doesn't exist
    def test_get_nonexistent_product(self):
        response = self.client.post("/products/", self.product1)
        prod = Product.objects.filter(
            product_name__iexact=self.product1["product_name"]
        ).first()
        product_id = prod.id
        response = self.client.delete(f"/products/{product_id}")

        response = self.client.get(f"/products/{product_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Product doesn't exists")

    # Testing post request to create invalid product(violating some constraint)
    # to return an error message
    def test_create_invalid_product(self):
        prod = self.product4
        prod["product_name"] = ""
        response = self.client.post("/products/", prod)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["product_name"][0], "This field may not be blank."
        )
        prod["product_price"] = -300
        response = self.client.post(
            "/products/",
            prod,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["product_price"][0], "Product price should be greater than 0"
        )

    # Testing put request with product_id to update a product
    def test_update_product(self):
        response = self.client.post("/products/", self.product1)
        prod = Product.objects.filter(
            product_name__iexact=self.product1["product_name"]
        ).first()
        updated_data = {"product_name": "Updated Product", "product_price": "500"}
        response = self.client.put(
            f"/products/{prod.id}", updated_data, content_type="application/json"
        )
        prod = Product.objects.filter(id=prod.id).first()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(prod.product_name, "Updated Product")

    # Testing delete request with product_id to delete a product
    def test_delete_product(self):
        response = self.client.post("/products/", self.product1)
        prod = Product.objects.filter(
            product_name__iexact=self.product1["product_name"]
        ).first()
        response = self.client.delete(f"/products/{prod.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 0)

    # Testing delete request to delete a nonexistent product to return
    # an error message
    def test_delete_nonexistent_product(self):
        response = self.client.post("/products/", self.product1)
        prod = Product.objects.filter(
            product_name__iexact=self.product1["product_name"]
        ).first()
        product_id = prod.id
        response = self.client.delete(f"/products/{product_id}")

        response = self.client.delete(f"/products/{product_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Product doesn't exists")

    # Testing get request for category to return error message
    # when category doesn't exist
    def test_get_category_not_found(self):
        response = self.client.post("/category/", self.category1)
        category = Category.objects.filter(
            category_name__iexact=self.category1["category_name"]
        ).first()
        category_id = category.id
        response = self.client.delete(f"/category/{category_id}")
        response = self.client.get(f"/category/{category_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Category doesn't exists")

    # Testing post request to create category and return success message
    def test_create_category(self):
        response = self.client.post("/category/", self.category1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)

    # Testing put request with category_id to update a category
    def test_update_category(self):
        response = self.client.post("/category/", self.category1)
        category = Category.objects.first()
        updated_data = {"category_name": "Updated Category"}
        response = self.client.put(
            f"/category/{category.id}", updated_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        category = Category.objects.first()
        self.assertEqual(category.category_name, "Updated Category")

    # Testing delete request with category_id to delete a product
    def test_delete_category(self):
        response = self.client.post("/category/", self.category1)
        category = Category.objects.first()
        response = self.client.delete(f"/category/{category.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 0)

    # Testing delete request to delete a nonexistent category to return
    # an error message
    def test_delete_nonexistent_category(self):
        response = self.client.post("/category/", self.category1)
        category = Category.objects.filter(
            category_name__iexact=self.category1["category_name"]
        ).first()
        category_id = category.id
        response = self.client.delete(f"/category/{category_id}")
        response = self.client.delete(f"/category/{category_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Category doesn't exists")

    # Testing get request with category_id to return all associated products
    def test_get_category_with_products(self):
        response = self.client.post("/category/", self.category1)
        category = Category.objects.first()

        response = self.client.post("/products/", self.product1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(f"/category/{category.id}?products=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["category_products"][0]["product_name"],
            self.product1["product_name"],
        )

    # Testing post request to add products to a category
    def test_add_product_to_category(self):
        response = self.client.post("/category/", self.category2)
        category = Category.objects.first()

        response = self.client.post("/products/", self.product1)
        product = Product.objects.first()

        response = self.client.post(f"/category/{category.id}/add/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["message"], "Product added to category successfully"
        )

    # Testing delete request to remove products from a category
    def test_remove_product_from_category(self):
        response = self.client.post("/category/", self.category1)
        category = Category.objects.first()

        response = self.client.post("/products/", self.product1)
        product = Product.objects.first()
        response = self.client.delete(f"/category/{category.id}/remove/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Product removed from category successfully"
        )
