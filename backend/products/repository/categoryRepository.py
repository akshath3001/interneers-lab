from ..models import Category, Product


class CategoryRepository:
    @staticmethod
    def get_or_create(category_names):
        categories = []
        for category_name in category_names:
            category = Category.objects.filter(
                category_name__iexact=category_name.capitalize()
            ).first()
            if not category:
                category = Category.objects.create(
                    category_name=category_name.capitalize()
                )
            categories.append(category)
        return categories

    @staticmethod
    def get_by_category(category):
        return Product.objects.filter(product_category=category)

    @staticmethod
    def get_by_id(category_id):
        return Category.objects.filter(id=category_id).first()

    @staticmethod
    def create(category_data):
        existing_category = Category.objects(
            category_name=category_data["category_name"]
        ).first()
        if existing_category:
            return existing_category, existing_category.id
        category = Category(**category_data)
        category.save()
        return category, str(category.id)

    @staticmethod
    def update(category, updated_data):
        for key, value in updated_data.items():
            setattr(category, key, value)
        category.save()
        return category.id

    @staticmethod
    def delete(category):
        category.delete()
