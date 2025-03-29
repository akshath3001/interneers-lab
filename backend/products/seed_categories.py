import logging

from django.db.utils import OperationalError

from .service.categoryService import CategoryService

logger = logging.getLogger(__name__)

CATEGORIES = [
    {"category_name": "Electronics", "category_description": "Gadgets and devices"},
    {"category_name": "Clothing", "category_description": "Apparel and fashion"},
    {"category_name": "Books", "category_description": "Educational and leisure books"},
]


def seed_categories():
    try:
        categories_details = CategoryService.create_categories(CATEGORIES)
        logger.info(categories_details)
    except OperationalError:
        logger.warning("Database is not ready yet. Skipping category seeding.")
    except Exception as e:
        logger.error(f"Error while seeding categories: {e}", exc_info=True)
