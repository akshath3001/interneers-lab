import datetime

from mongoengine import (
    DateTimeField,
    DecimalField,
    Document,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)


class Category(Document):
    category_name = StringField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name


class Product(Document):
    product_name = StringField(max_length=100, required=True)
    product_category = ListField(ReferenceField(Category))
    product_brand = StringField(max_length=100, required=True)
    product_description = StringField(max_length=200, default="")
    product_price = DecimalField(precision=2, required=True)
    product_quantity = IntField(default=0)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    meta = {"collection": "products"}

    def __str__(self):
        return self.product_name
