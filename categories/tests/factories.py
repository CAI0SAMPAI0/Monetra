import factory
from categories.models import Category
from users.tests.factories import UserFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('word')
    category_type = factory.Iterator(['INCOME', 'EXPENSE'])
    color = factory.Faker('hex_color')
