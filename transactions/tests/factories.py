import factory
from datetime import date
from transactions.models import Transaction
from accounts.tests.factories import AccountFactory
from categories.tests.factories import CategoryFactory


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    account = factory.SubFactory(AccountFactory)
    category = factory.SubFactory(CategoryFactory)
    transaction_type = factory.Iterator(['INCOME', 'EXPENSE'])
    amount = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    transaction_date = factory.Faker('date_between', start_date='-1y', end_date='today')
    description = factory.Faker('sentence')
