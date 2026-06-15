import pytest
from categories.tests.factories import CategoryFactory


@pytest.mark.django_db
class TestCategoryModel:
    def test_create_category(self):
        category = CategoryFactory()
        assert category.user is not None
        assert category.name is not None
        assert category.created_at is not None
        assert category.updated_at is not None

    def test_str_method(self):
        category = CategoryFactory(name='Food')
        assert str(category) == 'Food'

    def test_category_type_choices(self):
        category = CategoryFactory(category_type='EXPENSE')
        assert category.get_category_type_display() == 'Saída'

    def test_unique_together_user_name(self):
        c1 = CategoryFactory(name='Food')
        with pytest.raises(Exception):
            CategoryFactory(user=c1.user, name='Food')
