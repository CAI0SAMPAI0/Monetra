import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from .factories import TransactionFactory
from accounts.tests.factories import AccountFactory
from categories.tests.factories import CategoryFactory
from users.tests.factories import UserFactory
from transactions.models import Transaction

@pytest.mark.django_db
class TestTransactionViews:
    def test_transaction_list_view(self, client):
        user = UserFactory()
        account = AccountFactory(user=user)
        TransactionFactory.create_batch(5, account=account)
        # Create another transaction for different user
        TransactionFactory()
        
        client.force_login(user)
        url = reverse('transactions:transaction_list')
        response = client.get(url)
        
        assert response.status_code == 200
        assert len(response.context['transactions']) == 5

    def test_transaction_create_view_post(self, client):
        user = UserFactory()
        account = AccountFactory(user=user)
        category = CategoryFactory(user=user, category_type='EXPENSE')
        client.force_login(user)
        url = reverse('transactions:transaction_create')
        data = {
            'account': account.pk,
            'category': category.pk,
            'transaction_type': 'EXPENSE',
            'amount': '50.00',
            'transaction_date': '2023-10-27',
            'description': 'Nova Transação',
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('transactions:transaction_list')
        assert Transaction.objects.filter(description='Nova Transação').exists()
        
        messages = list(get_messages(response.wsgi_request))
        assert any('Transação registrada com sucesso!' in str(m) for m in messages)

    def test_transaction_update_view_post(self, client):
        user = UserFactory()
        account = AccountFactory(user=user)
        category = CategoryFactory(user=user, category_type='INCOME')
        transaction = TransactionFactory(account=account, category=category, transaction_type='INCOME', description='Antiga Descrição')
        client.force_login(user)
        url = reverse('transactions:transaction_update', kwargs={'pk': transaction.pk})
        data = {
            'account': account.pk,
            'category': category.pk,
            'transaction_type': 'INCOME',
            'amount': '150.00',
            'transaction_date': '2023-10-28',
            'description': 'Nova Descrição',
        }
        response = client.post(url, data)
        assert response.status_code == 302
        transaction.refresh_from_db()
        assert transaction.description == 'Nova Descrição'
        assert transaction.transaction_type == 'INCOME'
        
        messages = list(get_messages(response.wsgi_request))
        assert any('Transação atualizada com sucesso!' in str(m) for m in messages)

    def test_transaction_delete_view_post(self, client):
        user = UserFactory()
        account = AccountFactory(user=user)
        transaction = TransactionFactory(account=account)
        client.force_login(user)
        url = reverse('transactions:transaction_delete', kwargs={'pk': transaction.pk})
        response = client.post(url)
        assert response.status_code == 302
        assert not Transaction.objects.filter(pk=transaction.pk).exists()
        
        messages = list(get_messages(response.wsgi_request))
        assert any('Transação excluída com sucesso!' in str(m) for m in messages)
