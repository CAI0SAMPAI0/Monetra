import pytest
from decimal import Decimal
from transactions.tests.factories import TransactionFactory


@pytest.mark.django_db
class TestTransactionModel:
    def test_create_transaction(self):
        transaction = TransactionFactory()
        assert transaction.account is not None
        assert transaction.category is not None
        assert transaction.created_at is not None
        assert transaction.updated_at is not None

    def test_str_method_with_description(self):
        transaction = TransactionFactory(description='Lunch', amount=Decimal('25.50'))
        assert str(transaction) == 'Lunch - R$ 25.50'

    def test_str_method_without_description(self):
        transaction = TransactionFactory(description='', amount=Decimal('100.00'))
        assert str(transaction) == 'Transação R$ 100.00'

    def test_transaction_type_choices(self):
        transaction = TransactionFactory(transaction_type='INCOME')
        assert transaction.get_transaction_type_display() == 'Entrada'
