from unittest import TestCase
from unittest.mock import MagicMock, patch

from parameterized import parameterized
from rest_framework import status

from products.service.categoryService import CategoryService


class TestCategoryService(TestCase):
    # Parameterized test for testing get_category_products for success and
    # failure(category doesn't exist and no products in category)
    @parameterized.expand(
        [
            (
                True,
                True,
                2,
                status.HTTP_200_OK,
                "Products from 'Electronics' category retrieved successfully",
            ),
            (
                True,
                False,
                0,
                status.HTTP_400_BAD_REQUEST,
                "No products belong to 'Electronics' category",
            ),
            (
                False,
                False,
                0,
                status.HTTP_404_NOT_FOUND,
                "Category doesn't exists",
            ),
        ]
    )
    @patch("products.service.categoryService.ProductSerializer")
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_category")
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_id")
    def test_get_category_products(
        self,
        category_exists,
        has_products,
        product_count,
        expected_status,
        expected_message,
        mock_get_by_id,
        mock_get_by_category,
        mock_product_serializer,
    ):
        mock_category = MagicMock()
        mock_category.category_name = "Electronics"

        mock_get_by_id.return_value = mock_category if category_exists else None
        mock_products = [MagicMock()] * product_count if has_products else []
        mock_get_by_category.return_value = mock_products
        mock_product_serializer.return_value.data = [
            {"name": "Mock Product"}
        ] * product_count

        response = CategoryService.get_category_products("cat-123")

        self.assertEqual(response["status"], expected_status)
        self.assertIn("message", response["data"])
        self.assertEqual(response["data"]["message"], expected_message)

    # Parameterized test for testing get_category for success and failure
    @parameterized.expand(
        [
            (
                True,
                status.HTTP_204_NO_CONTENT,
                "Category retrieved successfully",
            ),
            (
                False,
                status.HTTP_404_NOT_FOUND,
                "Category doesn't exists",
            ),
        ]
    )
    @patch("products.serializers.CategorySerializer")
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_id")
    def test_get_category(
        self,
        exists,
        expected_status,
        expected_message,
        mock_get_by_id,
        mock_category_serializer,
    ):
        mock_category = MagicMock()
        mock_get_by_id.return_value = mock_category if exists else None
        mock_category_serializer.return_value.data = {"category_name": "Mock"}

        response = CategoryService.get_category("cat-001")

        self.assertEqual(response["status"], expected_status)
        self.assertIn("message", response["data"])
        self.assertEqual(response["data"]["message"], expected_message)

    # Parameterized test for testing create_category for success and
    # failure(missing required field)
    @parameterized.expand(
        [
            (
                {
                    "category_name": "Electronics",
                    "category_description": "Test_description",
                },
                True,
                "123",
                status.HTTP_201_CREATED,
                "Category created successfully",
            ),
            (
                {"category_name": ""},
                False,
                None,
                status.HTTP_400_BAD_REQUEST,
                {"category_name": ["This field may not be blank."]},
            ),
        ]
    )
    @patch("products.repository.categoryRepository.CategoryRepository.create")
    @patch("products.serializers.CategorySerializer")
    def test_create_category(
        self,
        input_data,
        is_valid,
        created_id,
        expected_status,
        expected_message,
        mock_category_serializer,
        mock_create,
    ):
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.is_valid.return_value = is_valid
        mock_serializer_instance.validated_data = input_data if is_valid else {}
        mock_serializer_instance.errors = (
            {} if is_valid else {"category_name": ["This field may not be blank."]}
        )
        mock_category_serializer.return_value = mock_serializer_instance

        if is_valid:
            mock_category = MagicMock()
            mock_category.category_name = input_data["category_name"]
            mock_create.return_value = (mock_category, created_id)
            mock_serializer_instance.data = {
                "category_name": input_data["category_name"]
            }

        response = CategoryService.create_category(input_data)
        self.assertEqual(response["status"], expected_status)

        if is_valid:
            self.assertEqual(response["data"]["message"], expected_message)
            self.assertEqual(response["data"]["category_id"], created_id)
            self.assertEqual(
                response["data"]["category"]["category_name"],
                input_data["category_name"],
            )

    # Parameterized test for testing update_category for success and
    # failure(serialization error and missing field value)
    @parameterized.expand(
        [
            (
                "cat123",
                {"category_name": "Updated"},
                True,
                True,
                status.HTTP_204_NO_CONTENT,
                "Category updated successfully",
            ),
            (
                "cat124",
                {"category_name": ""},
                False,
                True,
                status.HTTP_400_BAD_REQUEST,
                None,
            ),
            (
                "cat125",
                {"category_name": "Name"},
                True,
                False,
                status.HTTP_404_NOT_FOUND,
                None,
            ),
        ]
    )
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_id")
    @patch("products.repository.categoryRepository.CategoryRepository.update")
    @patch("products.serializers.CategorySerializer")
    def test_update_category(
        self,
        category_id,
        input_data,
        is_valid,
        exists,
        expected_status,
        expected_message,
        mock_serializer,
        mock_update,
        mock_get_by_id,
    ):
        mock_category = MagicMock()
        mock_get_by_id.return_value = mock_category if exists else None

        mock_serializer_instance = MagicMock()
        mock_serializer_instance.is_valid.return_value = is_valid
        mock_serializer_instance.validated_data = input_data
        mock_serializer_instance.errors = {"category_name": ["Invalid"]}

        mock_serializer.return_value = mock_serializer_instance
        mock_update.return_value = category_id

        response = CategoryService.update_category(category_id, input_data)
        self.assertEqual(response["status"], expected_status)
        if expected_message:
            assert response["data"]["message"] == expected_message

    # Parameterized test for testing delete-category for success and failure
    @parameterized.expand(
        [
            (
                "cat00",
                True,
                status.HTTP_200_OK,
                "Category deleted successfully",
            ),
            (
                "cat01",
                False,
                status.HTTP_404_NOT_FOUND,
                "Category doesn't exists",
            ),
        ]
    )
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_id")
    @patch("products.repository.categoryRepository.CategoryRepository.delete")
    def test_delete_category(
        self,
        category_id,
        exists,
        expected_status,
        expected_message,
        mock_delete,
        mock_get_by_id,
    ):
        mock_category = MagicMock()
        mock_get_by_id.return_value = mock_category if exists else None

        response = CategoryService.delete_category(category_id)
        self.assertEqual(response["status"], expected_status)
        self.assertEqual(response["data"]["message"], expected_message)
