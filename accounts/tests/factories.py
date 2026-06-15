import factory
from accounts.models import Account
from users.tests.factories import UserFactory


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('word')
    bank_name = factory.Faker('company')
    account_type = factory.Iterator(['CHECKING', 'SAVINGS', 'WALLET'])
    balance = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    is_active = True
