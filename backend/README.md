# API Documentation
This API provides product management functionality, including product creation retrieval, updation, and deletion. It is also following the Controller-Service-Repository (CSR) architecture for clean separation of concerns.

---

## Table of Contents

1. [Getting Started with Git & Forking](#getting-started-with-git-and-forking)
2.

---

## Model

### Category
Represents a product category
```
{
  "category_name": "StringField - the name of category"
}
```
### Product
Represents a product with its details
```
{
  "product_name": "StringField (required) - name of the product",
  "product_category": "ListField - categories the product belongs to",
  "product_brand": "StringField (required) - brand of the product",
  "product_description": "StringField - description of the product",
  "product_price": "DecimalField (required) - price of the product",
  "product_quantity": "IntField - available stock quantity",
  "created_at": "DateTimeField - timestamp of product creation",
  "updated_at": "DateTimeField - timestamp of the last product update"
}
```

---

## Serializers
Serializers are used to convert complex data types (such as model instances), into native Python data types, and vice versa, that can be easily rendered into JSON. It also ensured the fields are correctly formatted and validated (such as ensuring the product price and product quantity is greater than zero) before being processed.

## API Endpoints
All the API endpoints are inheriting the APIView class, ensuring that the API follows RESTful principles while keeping the controller logic clean and easily customizable