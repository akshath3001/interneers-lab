import logging

from django.db.utils import OperationalError

from .service.categoryService import CategoryService
from .service.productService import ProductService

logger = logging.getLogger(__name__)

DEFAULT_CATEGORY = {
    "category_name": "Uncategorized",
    "category_description": "Products that were added before categories existed",
}

DEFAULT_BRAND = {"product_brand": "Unbranded"}


def migrate_existing_products():
    try:
        category_details, category_id = CategoryService.create_category(
            DEFAULT_CATEGORY
        )

        ProductService.migrate_products_without_category(category_id)

        ProductService.migrate_products_without_brands(DEFAULT_BRAND)

        logger.info(
            "Successfully migrated existing products to have both category and brand."
        )

    except OperationalError:
        logger.warning("Database is not ready yet. Skipping product migration.")
    except Exception as e:
        logger.error(f"Error migrating existing products: {e}", exc_info=True)
