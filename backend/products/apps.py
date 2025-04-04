import logging
import os
import mongoengine
from django.apps import AppConfig
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"

    def ready(self):
        ## doing this(os.environ check) to prevent double execution of seed scripts
        if os.environ.get("RUN_MAIN") == "true":
            try:
                # if os.environ.get("USE_TEST_DB", "false") == "false":
                logger.info("Using main database for seeding.")
                mongoengine.disconnect()
                mongoengine.connect(
                    db="interneers_lab_mongodb",
                    host="mongodb://aks:aks%403001@localhost:27018/interneers_lab_mongodb?authSource=admin",
                    username="aks",
                    password="aks@3001",
                    authentication_source="admin",
                    uuidRepresentation="standard",
                    alias="default",
                )

                from products.scripts.seed_categories import seed_categories

                logger.info("Running category seed script for main database...")
                seed_categories()
                logger.info(
                    "Category seed script completed successfully for main database."
                )

            except OperationalError:
                logger.warning("Database is not ready yet. Skipping seeding.")
            except Exception as e:
                logger.error(f"Error running seed script: {e}", exc_info=True)
