import logging
import os

from django.apps import AppConfig
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"

    def ready(self):
        # doing this(os.environ check) to prevent double execution of seed scripts
        if os.environ.get("RUN_MAIN") == "true":
            try:
                from seeds.seed_categories import seed_categories
                from seeds.seed_test_data import seed_test_db

                logger.info("Running category seed script on startup...")
                seed_categories()
                logger.info("Category seed script completed successfully.")
                logger.info("Running test seed script on startup...")
                seed_test_db()
                logger.info("test seed script completed successfully.")
            except OperationalError:
                logger.warning("Database is not ready yet. Skipping category seeding.")
            except Exception as e:
                logger.error(f"Error running seed script: {e}", exc_info=True)
