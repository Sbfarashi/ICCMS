from extensions import db
from models.category import Category


class CategoryService:

    # =====================================================
    # Get All Categories
    # =====================================================

    @staticmethod
    def get_all():

        return (

            Category.query

            .order_by(

                Category.name.asc()

            )

            .all()

        )

    # =====================================================
    # Get One Category
    # =====================================================

    @staticmethod
    def get(category_id):

        return Category.query.get_or_404(
            category_id
        )

    # =====================================================
    # Create Category
    # =====================================================

    @staticmethod
    def create(name, description):

        existing = Category.query.filter_by(
            name=name
        ).first()

        if existing:

            return False, "Category already exists."

        category = Category(

            name=name,

            description=description

        )

        db.session.add(category)

        db.session.commit()

        return True, "Category created successfully."

    # =====================================================
    # Update Category
    # =====================================================

    @staticmethod
    def update(category, name, description):

        duplicate = (

            Category.query

            .filter(

                Category.id != category.id,

                Category.name == name

            )

            .first()

        )

        if duplicate:

            return False, "Category already exists."

        category.name = name

        category.description = description

        db.session.commit()

        return True, "Category updated successfully."

    # =====================================================
    # Delete Category
    # =====================================================

    @staticmethod
    def delete(category_id):

        category = Category.query.get_or_404(
            category_id
        )

        db.session.delete(category)

        db.session.commit()

        return True, "Category deleted successfully."