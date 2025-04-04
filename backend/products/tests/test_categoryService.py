import logging
import unittest
from unittest.mock import MagicMock, patch

from rest_framework import status

from products.service.categoryService import CategoryService

logger = logging.getLogger(__name__)


class TestCategoryService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    # Testing for get_category_products to return the products belonging to the category
    @patch("products.serializers.ProductSerializer")
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_id")
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_category")
    def test_get_category_products_success(
        self, mock_get_by_category, mock_get_by_id, mock_product_serializer
    ):
        mock_category = MagicMock(
            category_name="Electronics", category_description="Test description"
        )
        mock_get_by_id.return_value = mock_category

        mock_product_1 = MagicMock(product_name="product1", product_price="5000.00")
        mock_product_2 = MagicMock(product_name="product2", product_price="50000.00")
        mock_get_by_category.return_value = [mock_product_1, mock_product_2]

        mock_serializer_instance = mock_product_serializer.return_value
        mock_serializer_instance.data = [
            {"product_name": "product1", "product_price": "5000.00"},
            {"product_name": "product2", "product_price": "50000.00"},
        ]

        response = CategoryService.get_category_products("123")
        self.assertEqual(response["status"], status.HTTP_200_OK)
        self.assertEqual(
            response["data"]["message"],
            "Products from 'Electronics' category retrieved successfully",
        )

    # Testing for get_category_products to return error message in case of
    # wrong category_id
    @patch(
        "products.repository.categoryRepository.CategoryRepository.get_by_id",
        return_value=None,
    )
    def test_get_category_products_failure(self, mock_get_by_id):
        response = CategoryService.get_category_products("123")
        self.assertEqual(response["status"], status.HTTP_404_NOT_FOUND)
        self.assertEqual(response["data"]["message"], "Category doesn't exists")

    # Testing for create_category to return the correct response for
    # category creation
    @patch("products.repository.categoryRepository.CategoryRepository.create")
    @patch("products.serializers.CategorySerializer.is_valid", return_value=True)
    @patch(
        "products.serializers.CategorySerializer.validated_data", new_callable=MagicMock
    )
    @patch("products.serializers.CategorySerializer.data", new_callable=MagicMock)
    def test_create_category_success(
        self, mock_data, mock_validated_data, mock_is_valid, mock_create
    ):
        mock_create.return_value = (MagicMock(), "123")
        response = CategoryService.create_category(
            {
                "category_name": "Electronics",
                "category_description": "Test electronics description",
            }
        )
        self.assertEqual(response["status"], status.HTTP_201_CREATED)
        self.assertEqual(response["data"]["message"], "Category created successfully")
        self.assertEqual(response["data"]["category_id"], "123")

    # Testing for create_category to return the error during serilizer.is_valid()
    # failure due to missing category_description
    @patch("products.serializers.CategorySerializer")
    def test_create_category_failure(self, mock_category_serializer):
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.is_valid.return_value = False
        response = CategoryService.create_category(
            {"category_name": "Electronics", "category_description": ""}
        )
        self.assertEqual(response["status"], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response["data"],
            {"category_description": ["This field may not be blank."]},
        )

    # Testing for update_category to return the correct response for
    # category updation
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_id")
    @patch("products.serializers.CategorySerializer")
    def test_update_category_success(self, mock_category_serializer, mock_get_by_id):
        mock_category = MagicMock()
        mock_get_by_id.return_value = mock_category
        mock_category_serializer.is_valid.return_value = True
        mock_category_serializer.validated_data = {"category_name": "Updated Name"}

        with patch(
            "products.repository.categoryRepository.CategoryRepository.update",
            return_value="123",
        ):
            response = CategoryService.update_category(
                "123", {"category_name": "Updated Name"}
            )
        self.assertEqual(response["status"], status.HTTP_204_NO_CONTENT)
        self.assertEqual(response["data"]["message"], "Category updated successfully")

    # Testing for update_category to return the error response for when category
    # doesn't exists
    @patch(
        "products.repository.categoryRepository.CategoryRepository.get_by_id",
        return_value=None,
    )
    def test_update_category_failure(self, mock_get_by_id):
        response = CategoryService.update_category(
            "123", {"category_name": "Updated Name"}
        )
        self.assertEqual(response["status"], status.HTTP_404_NOT_FOUND)
        self.assertEqual(response["data"]["message"], "Category doesn't exists")

    # Testing for get_category to return the correct response for retrieving
    # category details
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_id")
    @patch("products.serializers.CategorySerializer")
    def test_get_category_success(self, MockCategorySerializer, mock_get_by_id):
        mock_category = MagicMock()
        mock_category.category_name = "Electronics"
        mock_category.category_description = "Test electronics description"
        mock_get_by_id.return_value = mock_category

        mock_category_serializer = MagicMock()
        MockCategorySerializer.return_value.data = {
            "category_name": "Electronics",
            "category_description": "Test electronics description",
        }
        MockCategorySerializer.return_value = mock_category_serializer

        response = CategoryService.get_category("123")

        # MockCategorySerializer.assert_called_with(mock_category)
        self.assertEqual(response["status"], status.HTTP_204_NO_CONTENT)
        self.assertEqual(response["data"]["message"], "Category retrieved successfully")
        self.assertEqual(
            response["data"]["category"],
            {
                "category_name": "Electronics",
                "category_description": "Test electronics description",
            },
        )

    # Testing for get_category to return the error response for when category
    # doens't exist
    @patch(
        "products.repository.categoryRepository.CategoryRepository.get_by_id",
        return_value=None,
    )
    def test_get_category_failure(self, mock_get_by_id):
        response = CategoryService.get_category("123")
        self.assertEqual(response["status"], status.HTTP_404_NOT_FOUND)
        self.assertEqual(response["data"]["message"], "Category doesn't exists")

    # Testing for delete_category to return the correct response for deleting category
    @patch("products.repository.categoryRepository.CategoryRepository.get_by_id")
    @patch("products.repository.categoryRepository.CategoryRepository.delete")
    def test_delete_category_success(self, mock_delete, mock_get_by_id):
        mock_get_by_id.return_value = MagicMock()
        response = CategoryService.delete_category("123")
        self.assertEqual(response["status"], status.HTTP_200_OK)
        self.assertEqual(response["data"]["message"], "Category deleted successfully")

    # Testing for delete_category to return the error response for when the category
    # doesn't exists
    @patch(
        "products.repository.categoryRepository.CategoryRepository.get_by_id",
        return_value=None,
    )
    def test_delete_category_failure(self, mock_get_by_id):
        response = CategoryService.delete_category("123")
        self.assertEqual(response["status"], status.HTTP_404_NOT_FOUND)
        self.assertEqual(response["data"]["message"], "Category doesn't exists")


if __name__ == "__main__":
    unittest.main(verbosity=2)
