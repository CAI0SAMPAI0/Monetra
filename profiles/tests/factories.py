import factory
from profiles.models import Profile
from users.tests.factories import UserFactory


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    full_name = factory.Faker('name')
    phone = factory.Faker('phone_number')
