import logging
import unittest
from unittest.mock import MagicMock, patch

from django.apps import apps
from django.conf import settings
from rest_framework import status

from products.service.productService import ProductService

logger = logging.getLogger(__name__)


class TestProductService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not apps.ready:
            apps.populate(settings.INSTALLED_APPS)

    # Testing get_product to successfully retrieve the products as per the
    # product_id and return the details
    @patch("products.serializers.ProductSerializer")
    @patch("products.repository.productRepository.ProductRepository.get_by_id")
    def test_get_product_success(self, mock_get_by_id, mock_product_serializer):
        mock_product = MagicMock(product_name="Laptop", product_price="1000.00")
        mock_get_by_id.return_value = mock_product

        mock_serializer_instance = mock_product_serializer.return_value
        mock_serializer_instance.data = {
            "product_name": "Laptop",
            "product_price": "1000.00",
        }

        response = ProductService.get_product("123")
        self.assertEqual(response["status"], status.HTTP_200_OK)
        self.assertEqual(response["data"]["message"], "Product retrieved successfully")
        self.assertEqual(
            response["data"]["product"]["product_name"],
            "Laptop",
        )
        self.assertEqual(
            response["data"]["product"]["product_price"],
            "1000.00",
        )

    # Testing get_product to return the error message when the
    # product doesn't exists
    @patch(
        "products.repository.productRepository.ProductRepository.get_by_id",
        return_value=None,
    )
    def test_get_product_failure(self, mock_get_by_id):
        response = ProductService.get_product("123")
        self.assertEqual(response["status"], status.HTTP_404_NOT_FOUND)
        self.assertEqual(response["data"]["message"], "Product doesn't exists")

    # Testing create_product to successfully create the products
    # and return the product_id
    @patch("products.repository.productRepository.ProductRepository.create")
    @patch("products.serializers.ProductSerializer.is_valid", return_value=True)
    @patch(
        "products.serializers.ProductSerializer.validated_data", new_callable=MagicMock
    )
    @patch("products.serializers.ProductSerializer.data", new_callable=MagicMock)
    def test_create_product_success(
        self, mock_data, mock_validated_data, mock_is_valid, mock_create
    ):
        mock_create.return_value = (MagicMock(), "123")
        response = ProductService.create_product(
            {"product_name": "Laptop", "product_price": "1000.00"}
        )
        self.assertEqual(response["status"], status.HTTP_201_CREATED)
        self.assertEqual(response["data"]["message"], "Product created successfully")
        self.assertEqual(response["data"]["product_id"], "123")

    # Testing create_product to return the error message when the endpoint
    # fails to create the product to due serializer error(missing required fields)
    @patch("products.serializers.ProductSerializer")
    def test_create_product_failure(self, mock_product_serializer):
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.is_valid.return_value = False
        response = ProductService.create_product(
            {"product_name": "", "product_price": "1000.00"}
        )
        self.assertEqual(response["status"], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response["data"]["product_name"][0],
            "This field may not be blank.",
        )

    # Testing update_product to successfully update the products based on the
    # details received and return the product_id, updated product
    @patch("products.repository.productRepository.ProductRepository.get_by_id")
    @patch("products.serializers.ProductSerializer")
    def test_update_product_success(self, mock_product_serializer, mock_get_by_id):
        mock_product = MagicMock()
        mock_get_by_id.return_value = mock_product
        mock_product_serializer.is_valid.return_value = True
        mock_product_serializer.validated_data = {"product_name": "Updated Laptop"}

        with patch(
            "products.repository.productRepository.ProductRepository.update",
            return_value="123",
        ):
            response = ProductService.update_product(
                "123", {"product_name": "Updated Laptop"}
            )
        self.assertEqual(response["status"], status.HTTP_204_NO_CONTENT)
        self.assertEqual(response["data"]["message"], "Product updated successfully")

    # Testing update_product to return the error message when the given
    # product_id doesn't exist
    @patch(
        "products.repository.productRepository.ProductRepository.get_by_id",
        return_value=None,
    )
    def test_update_product_failure(self, mock_get_by_id):
        response = ProductService.update_product(
            "123", {"product_name": "Updated Laptop"}
        )
        self.assertEqual(response["status"], status.HTTP_404_NOT_FOUND)
        self.assertEqual(response["data"]["message"], "Product doesn't exists")

    # Testing delete_product to successfully delete the products
    # and return the correct message
    @patch("products.repository.productRepository.ProductRepository.get_by_id")
    @patch("products.repository.productRepository.ProductRepository.delete")
    def test_delete_product_success(self, mock_delete, mock_get_by_id):
        mock_get_by_id.return_value = MagicMock()
        response = ProductService.delete_product("123")
        self.assertEqual(response["status"], status.HTTP_200_OK)
        self.assertEqual(response["data"]["message"], "Product deleted successfully")

    # Testing delete_product to return the error message when the product
    # doesn't exist
    @patch(
        "products.repository.productRepository.ProductRepository.get_by_id",
        return_value=None,
    )
    def test_delete_product_failure(self, mock_get_by_id):
        response = ProductService.delete_product("123")
        self.assertEqual(response["status"], status.HTTP_404_NOT_FOUND)
        self.assertEqual(response["data"]["message"], "Product doesn't exists")

    # Testing add_product_to_category to add a product corresponding to the
    # given product_id to a category corresponding to a category_id
    @patch("products.repository.productRepository.ProductRepository.get_by_id")
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_id")
    @patch("products.repository.productRepository.ProductRepository.update_category")
    def test_add_product_to_category_success(
        self, mock_update_category, mock_get_category, mock_get_product
    ):
        mock_category = MagicMock(id="456")
        mock_product = MagicMock(id="123", product_category=[])
        mock_get_category.return_value = mock_category
        mock_get_product.return_value = mock_product

        response = ProductService.add_product_to_category("456", "123")

        self.assertEqual(response["status"], status.HTTP_200_OK)
        self.assertEqual(
            response["data"]["message"], "Product added to category successfully"
        )

    # Testing add_product_to_category to return an error message when either
    # the product or the category doesn't exists
    @patch("products.repository.productRepository.ProductRepository.get_by_id")
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_id")
    def test_add_product_to_category_failure_category_or_product_not_found(
        self, mock_get_category, mock_get_product
    ):
        mock_get_category.return_value = None
        mock_get_product.return_value = MagicMock(id="123", product_category=[])

        response = ProductService.add_product_to_category("456", "123")

        self.assertEqual(response["status"], status.HTTP_404_NOT_FOUND)
        self.assertEqual(response["data"]["message"], "Category or Product not found")

    # Testing add_product_to_category to return an error message when product
    # already exists in the category
    @patch("products.repository.productRepository.ProductRepository.get_by_id")
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_id")
    @patch("products.repository.productRepository.ProductRepository.update_category")
    def test_add_product_to_category_failure_product_already_in_category(
        self, mock_update_category, mock_get_category, mock_get_product
    ):
        mock_category = MagicMock(id="456")
        mock_product = MagicMock(id="123", product_category=[mock_category])
        mock_get_category.return_value = mock_category
        mock_get_product.return_value = mock_product

        response = ProductService.add_product_to_category("456", "123")

        self.assertEqual(response["status"], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["data"]["message"], "Product already in category")

    # Testing remove_product_to_category to add a product corresponding to the
    # given product_id to a category corresponding to a category_id
    @patch("products.repository.productRepository.ProductRepository.get_by_id")
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_id")
    @patch("products.repository.productRepository.ProductRepository.update_category")
    def test_remove_product_from_category_success(
        self, mock_update_category, mock_get_category, mock_get_product
    ):
        mock_category = MagicMock(id="456")
        mock_product = MagicMock(id="123", product_category=[mock_category])
        mock_get_category.return_value = mock_category
        mock_get_product.return_value = mock_product

        response = ProductService.remove_product_from_category("456", "123")

        self.assertEqual(response["status"], status.HTTP_200_OK)
        self.assertEqual(
            response["data"]["message"], "Product removed from category successfully"
        )

    # Testing remove_product_to_category to return an error message when either
    # the product or the category doesn't exists
    @patch("products.repository.productRepository.ProductRepository.get_by_id")
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_id")
    def test_remove_product_from_category_failure_category_or_product_not_found(
        self, mock_get_category, mock_get_product
    ):
        mock_get_category.return_value = None
        mock_get_product.return_value = MagicMock(id="123", product_category=[])

        response = ProductService.remove_product_from_category("456", "123")

        self.assertEqual(response["status"], status.HTTP_404_NOT_FOUND)
        self.assertEqual(response["data"]["message"], "Category or Product not found")

    # Testing remove_product_to_category to return an error message when product
    # doesn't exists in the category
    @patch("products.repository.productRepository.ProductRepository.get_by_id")
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_id")
    @patch("products.repository.productRepository.ProductRepository.update_category")
    def test_remove_product_from_category_failure_product_not_in_category(
        self, mock_update_category, mock_get_category, mock_get_product
    ):
        mock_category = MagicMock(id="456")
        mock_product = MagicMock(id="123", product_category=[])
        mock_get_category.return_value = mock_category
        mock_get_product.return_value = mock_product

        response = ProductService.remove_product_from_category("456", "123")

        self.assertEqual(response["status"], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["data"]["message"], "Product is not in the category")


if __name__ == "__main__":
    unittest.main(verbosity=2)
