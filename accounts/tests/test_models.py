import pytest
from accounts.tests.factories import AccountFactory


@pytest.mark.django_db
class TestAccountModel:
    def test_create_account(self):
        account = AccountFactory()
        assert account.user is not None
        assert account.name is not None
        assert account.created_at is not None
        assert account.updated_at is not None

    def test_str_method(self):
        account = AccountFactory(name='My Bank')
        assert str(account) == 'My Bank'

    def test_account_type_choices(self):
        account = AccountFactory(account_type='SAVINGS')
        assert account.get_account_type_display() == 'Poupança'
