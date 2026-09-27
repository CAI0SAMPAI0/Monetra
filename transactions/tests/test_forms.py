import pytest
from decimal import Decimal
from datetime import date, timedelta
from transactions.forms import TransactionForm
from accounts.tests.factories import AccountFactory
from categories.tests.factories import CategoryFactory


@pytest.mark.django_db
class TestTransactionForm:
    def test_transaction_form_valid_investment(self):
        account = AccountFactory()
        user = account.user
        category = CategoryFactory(user=user, category_type='INVESTMENT')

        tx_date = date.today()
        settle_date = tx_date + timedelta(days=2)

        data = {
            'account': account.id,
            'category': category.id,
            'transaction_type': 'INVESTMENT',
            'amount': '350.00',
            'transaction_date': tx_date.isoformat(),
            'settlement_date': settle_date.isoformat(),
            'description': 'Compra FII XPML11'
        }
        form = TransactionForm(data=data, user=user)
        assert form.is_valid(), form.errors

    def test_transaction_form_category_mismatch_error(self):
        account = AccountFactory()
        user = account.user
        category = CategoryFactory(user=user, category_type='EXPENSE')

        data = {
            'account': account.id,
            'category': category.id,
            'transaction_type': 'INVESTMENT',
            'amount': '100.00',
            'transaction_date': date.today().isoformat(),
        }
        form = TransactionForm(data=data, user=user)
        assert not form.is_valid()
        assert 'category' in form.errors
        assert 'A categoria deve corresponder ao tipo de transação.' in form.errors['category']

    def test_transaction_form_settlement_date_before_transaction_date(self):
        account = AccountFactory()
        user = account.user
        category = CategoryFactory(user=user, category_type='INVESTMENT')

        tx_date = date.today()
        invalid_settle = tx_date - timedelta(days=1)

        data = {
            'account': account.id,
            'category': category.id,
            'transaction_type': 'INVESTMENT',
            'amount': '150.00',
            'transaction_date': tx_date.isoformat(),
            'settlement_date': invalid_settle.isoformat(),
            'description': 'Data inválida'
        }
        form = TransactionForm(data=data, user=user)
        assert not form.is_valid()
        assert 'settlement_date' in form.errors
        assert 'A data de liquidação não pode ser anterior à data da transação.' in form.errors['settlement_date']
