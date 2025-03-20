from ..models import Category


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
