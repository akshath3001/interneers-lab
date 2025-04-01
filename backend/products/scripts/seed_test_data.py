import mongoengine
import logging


from products.service.categoryService import CategoryService
from products.service.productService import ProductService

logger = logging.getLogger(__name__)

mongoengine.connect(
    "test_db", host="mongodb://aks:aks%403001@localhost:27018/test_db?authSource=admin"
)

CATEGORIES = [
    {"category_name": "Electronics", "category_description": "Gadgets and devices"},
    {"category_name": "Clothing", "category_description": "Apparel and fashion"},
    {"category_name": "Books", "category_description": "Educational and leisure books"},
]

PRODUCTS = [
    {
        "product_name": "MacBook Pro M3",
        "product_category": ["Laptop", "Electronics"],
        "product_description": "Latest MacBook Pro with M3 chip",
        "product_price": 200000.00,
        "product_brand": "Apple",
        "product_quantity": 3,
    },
    {
        "product_name": "Galaxy Tab S9",
        "product_category": ["Tablet", "Electronics"],
        "product_description": "Samsung's latest high-end tablet",
        "product_price": 90000.00,
        "product_brand": "Samsung",
        "product_quantity": 6,
    },
    {
        "product_name": "Sony WH-1000XM5",
        "product_category": ["Headphones", "Electronics"],
        "product_description": "Top noise-canceling wireless headphones",
        "product_price": 30000.00,
        "product_brand": "Sony",
        "product_quantity": 10,
    },
]


def seed_categories():
    categories_details = CategoryService.create_categories(CATEGORIES)
    logger.info(categories_details)


def seed_products():
    products_details = ProductService.create_products(PRODUCTS)
    logger.info(products_details)


def seed_test_db():
    seed_categories()
    seed_products()
    print("Test data seeded successfully")


# if __name__ == "__main__":
#     run()
