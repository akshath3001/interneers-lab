import decimal
import logging
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from parameterized import parameterized
from rest_framework import status

from products.service.productService import ProductService

logger = logging.getLogger(__name__)


class TestProductService(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    # Parameterized test for testing get_product for both success and failure
    @parameterized.expand(
        [
            (
                MagicMock(product_name="Laptop", product_price="1000.00"),
                {
                    "status": status.HTTP_200_OK,
                    "message": "Product retrieved successfully",
                    "product_name": "Laptop",
                    "product_price": "1000.00",
                },
            ),
            (
                None,
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Product doesn't exists",
                    "product_name": None,
                    "product_price": None,
                },
            ),
        ]
    )
    @patch("products.serializers.ProductSerializer")
    @patch("products.repository.productRepository.ProductRepository.get_by_id")
    def test_get_product(
        self,
        mock_product,
        expected_response,
        mock_get_by_id,
        mock_product_serializer,
    ):
        mock_get_by_id.return_value = mock_product

        if mock_product:
            mock_serializer_instance = mock_product_serializer.return_value
            mock_serializer_instance.data = {
                "product_name": mock_product.product_name,
                "product_price": mock_product.product_price,
            }

        response = ProductService.get_product("123")
        self.assertEqual(response["status"], expected_response["status"])
        self.assertEqual(response["data"]["message"], expected_response["message"])
        if mock_product:
            self.assertEqual(
                response["data"]["product"]["product_name"],
                expected_response["product_name"],
            )
            self.assertEqual(
                response["data"]["product"]["product_price"],
                expected_response["product_price"],
            )

    # Parameterized test for testing create_product for both success and failure
    @parameterized.expand(
        [
            (
                {
                    "product_name": "Laptop",
                    "product_price": "1000.00",
                    "product_category": ["Electronics"],
                    "product_brand": "Dell",
                },
                True,
                "123",
                status.HTTP_201_CREATED,
                "Product created successfully",
            ),
            (
                {
                    "product_name": "",
                    "product_price": "1000.00",
                    "product_category": ["Electronics"],
                    "product_brand": "",
                },
                False,
                None,
                status.HTTP_400_BAD_REQUEST,
                {
                    "product_name": ["This field may not be blank."],
                    "product_brand": ["This field is required."],
                },
            ),
            (
                {
                    "product_name": "Laptop",
                    "product_price": "-1000",
                    "product_category": ["Electronics"],
                    "product_brand": "Dell",
                },
                False,
                None,
                status.HTTP_400_BAD_REQUEST,
                {"product_price": ["A valid number is required."]},
            ),
        ]
    )
    @patch("products.repository.productRepository.ProductRepository.create")
    @patch("products.repository.categoryRepository.CategoryRepository.get_or_create")
    @patch("products.serializers.ProductSerializer")
    @patch("products.serializers.ProductSerializer")
    def test_create_product(
        self,
        input_data,
        is_valid,
        created_id,
        expected_status,
        expected_message,
        mock_product_serializer_1,
        mock_product_serializer_2,
        mock_get_or_create,
        mock_create,
    ):
        mock_serializer_instance_1 = MagicMock()
        mock_serializer_instance_1.is_valid.return_value = is_valid
        mock_serializer_instance_1.validated_data = input_data if is_valid else {}
        mock_serializer_instance_1.errors = (
            {} if is_valid else {"product_price": ["Invalid value"]}
        )

        mock_serializer_instance_2 = MagicMock()
        mock_serializer_instance_2.data = {
            "product_name": input_data["product_name"],
            "product_price": str(input_data["product_price"]),
            "product_category": input_data["product_category"],
            "product_brand": input_data["product_brand"],
        }

        mock_product_serializer_1.return_value = mock_serializer_instance_1
        mock_product_serializer_2.return_value = mock_serializer_instance_2

        mock_category_1 = MagicMock()
        mock_category_1.name = "Electronics"
        mock_get_or_create.return_value = [mock_category_1]

        if is_valid:
            mock_product = MagicMock()
            mock_product.product_name = input_data["product_name"]
            mock_product.product_price = decimal.Decimal(input_data["product_price"])
            mock_product.product_category = [mock_category_1]
            mock_product.product_brand = input_data["product_brand"]

            mock_create.return_value = (mock_product, created_id)
            mock_product_serializer_2.return_value.data = (
                mock_serializer_instance_2.data
            )

        response = ProductService.create_product(input_data)

        self.assertEqual(response["status"], expected_status)

        if is_valid:
            self.assertEqual(response["data"]["message"], expected_message)
            self.assertEqual(response["data"]["product_id"], created_id)
            self.assertEqual(
                response["data"]["product"]["product_name"],
                mock_serializer_instance_2.data["product_name"],
            )
            self.assertEqual(
                response["data"]["product"]["product_price"],
                mock_serializer_instance_2.data["product_price"],
            )

    # Parameterized test for testing update_product for both success and failure
    @parameterized.expand(
        [
            (
                MagicMock(),
                {"product_name": "Updated Laptop"},
                True,
                status.HTTP_204_NO_CONTENT,
                "Product updated successfully",
            ),
            (
                None,
                {"product_name": "Updated Laptop"},
                True,
                status.HTTP_404_NOT_FOUND,
                "Product doesn't exists",
            ),
            (
                MagicMock(),
                {"product_name": ""},
                False,
                status.HTTP_400_BAD_REQUEST,
                "This field may not be blank.",
            ),
        ]
    )
    @patch("products.repository.productRepository.ProductRepository.get_by_id")
    @patch("products.serializers.ProductSerializer")
    @patch("products.repository.productRepository.ProductRepository.update")
    def test_update_product(
        self,
        mock_product,
        update_data,
        is_valid,
        expected_status,
        expected_message,
        mock_update,
        mock_product_serializer,
        mock_get_by_id,
    ):
        mock_get_by_id.return_value = mock_product

        mock_serializer_instance = MagicMock()
        mock_serializer_instance.is_valid.return_value = is_valid
        mock_serializer_instance.validated_data = update_data if is_valid else {}
        mock_product_serializer.return_value = mock_serializer_instance

        if mock_product and is_valid:
            mock_update.return_value = "123"

        response = ProductService.update_product("123", update_data)

        self.assertEqual(response["status"], expected_status)
        if expected_status != 400:
            self.assertEqual(response["data"]["message"], expected_message)
        else:
            self.assertEqual(response["data"]["product_name"][0], expected_message)

    # Parameterized test for testing delete_product for both success and failure
    @parameterized.expand(
        [
            (
                MagicMock(),
                status.HTTP_200_OK,
                "Product deleted successfully",
            ),
            (
                None,
                status.HTTP_404_NOT_FOUND,
                "Product doesn't exists",
            ),
        ]
    )
    @patch("products.repository.productRepository.ProductRepository.get_by_id")
    @patch("products.repository.productRepository.ProductRepository.delete")
    def test_delete_product(
        self,
        mock_product,
        expected_status,
        expected_message,
        mock_delete,
        mock_get_by_id,
    ):
        mock_get_by_id.return_value = mock_product
        response = ProductService.delete_product("123")

        self.assertEqual(response["status"], expected_status)
        self.assertEqual(response["data"]["message"], expected_message)


if __name__ == "__main__":
    main(verbosity=2)
