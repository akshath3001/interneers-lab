import mongoengine
import sys
from django.test import TestCase
import subprocess


class IntegrationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        if "test" in sys.argv:
            mongoengine.connect(
                db="test_db",
                host="mongodb://aks:aks%403001@localhost:27018/test_db?authSource=admin",
                username="aks",
                password="aks@3001",
                authentication_source="admin",
                uuidRepresentation="standard",
            )
            print("Connected to `test_db` for integration testing")

            try:
                subprocess.run(
                    ["python", "products/seeds/seed_test_data.py"], check=True
                )
                print("Seed script executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to run seed script: {e}")

    @classmethod
    def tearDownClass(cls):
        from products.models import Category, Product

        Category.objects.delete()
        Product.objects.delete()

        mongoengine.disconnect()
        super().tearDownClass()
        print("`test_db` cleaned successfully!")

    # Integration tests to be included
