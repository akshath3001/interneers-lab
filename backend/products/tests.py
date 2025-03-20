from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.product1 = {
            "product_name": "MacBook Pro M3",
            "product_category": ["Laptop", "Electronics"],
            "product_description": "Latest MacBook Pro with M3 chip",
            "product_price": "200000.00",
            "product_brand": "Apple",
            "product_quantity": 3,
        }
        self.product2 = {
            "product_name": "Galaxy Tab S9",
            "product_category": ["Tablet", "Electronics"],
            "product_description": "Samsung's latest high-end tablet",
            "product_price": "90000.00",
            "product_brand": "Samsung",
            "product_quantity": 6,
        }
        self.product3 = {
            "product_name": "Sony WH-1000XM5",
            "product_category": ["Headphones", "Electronics"],
            "product_description": "Top noise-canceling wireless headphones",
            "product_price": "30000.00",
            "product_brand": "Sony",
            "product_quantity": 10,
        }
        self.product4 = {
            "product_name": "LG OLED C3",
            "product_category": ["TV", "Electronics"],
            "product_description": "OLED 4K Smart TV with AI Processor",
            "product_price": "150000.00",
            "product_brand": "LG",
            "product_quantity": 2,
        }
        self.product5 = {
            "product_name": "Canon EOS R6 Mark II",
            "product_category": ["Camera", "Electronics"],
            "product_description": "Professional mirrorless camera",
            "product_price": "250000.00",
            "product_brand": "Canon",
            "product_quantity": 3,
        }

    def test_get_product_list_no_products(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Products don't exist")

    def test_create_single_product(self):
        response = self.client.post("/products/", self.product1, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_create_multiple_products(self):
        data = [self.product2, self.product3, self.product4]
        response = self.client.post("/products/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)

    def test_get_product_list(self):
        data = [self.product2, self.product3, self.product4, self.product5]
        response = self.client.post("/products/", data, format="json")
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_get_single_product(self):
        response = self.client.post("/products/", self.product1, format="json")
        prod = Product.objects.filter(
            product_name__iexact=self.product1["product_name"]
        ).first()
        response = self.client.get(f"/products/{prod.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["product_name"], self.product1["product_name"])

    def test_get_nonexistent_product(self):
        response = self.client.get("/products/100")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Product doesn't exist")

    def test_create_invalid_product(self):
        prod = self.product1
        prod["product_name"] = ""
        response = self.client.post("/products/", prod, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["product_name"][0], "This field may not be blank."
        )
        prod["product_price"] = -300
        response = self.client.post("/products/", prod, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["product_price"][0], "Product price should be greater than 0"
        )

    def test_update_product(self):
        response = self.client.post("/products/", self.product1, format="json")
        prod = Product.objects.filter(
            product_name__iexact=self.product1["product_name"]
        ).first()
        updated_data = {"product_name": "Updated Product", "price": 500}
        response = self.client.put(f"/products/{prod.id}", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        prod = Product.objects.filter(id=prod.id).first()
        self.assertEqual(prod.product_name, "Updated Product")

    def test_delete_product(self):
        response = self.client.post("/products/", self.product1, format="json")
        prod = Product.objects.filter(
            product_name__iexact=self.product1["product_name"]
        ).first()
        response = self.client.delete(f"/products/{prod.id}", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_delete_nonexistent_product(self):
        response = self.client.delete("/products/100")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Product doesn't exist")
