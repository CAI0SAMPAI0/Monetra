import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from .factories import AccountFactory
from users.tests.factories import UserFactory
from accounts.models import Account

@pytest.mark.django_db
class TestAccountViews:
    def test_account_list_view(self, client):
        user = UserFactory()
        AccountFactory.create_batch(3, user=user)
        # Create another account for different user
        AccountFactory()
        
        client.force_login(user)
        url = reverse('accounts:account_list')
        response = client.get(url)
        
        assert response.status_code == 200
        assert len(response.context['accounts']) == 3
        assert 'total_balance' in response.context

    def test_account_create_view_post(self, client):
        user = UserFactory()
        client.force_login(user)
        url = reverse('accounts:account_create')
        data = {
            'name': 'Nova Conta',
            'bank_name': 'Banco Teste',
            'account_type': 'CHECKING',
            'balance': '1000.00',
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('accounts:account_list')
        assert Account.objects.filter(name='Nova Conta', user=user).exists()
        
        messages = list(get_messages(response.wsgi_request))
        assert any('Conta criada com sucesso!' in str(m) for m in messages)

    def test_account_update_view_post(self, client):
        user = UserFactory()
        account = AccountFactory(user=user, name='Antigo Nome')
        client.force_login(user)
        url = reverse('accounts:account_update', kwargs={'pk': account.pk})
        data = {
            'name': 'Novo Nome',
            'bank_name': account.bank_name,
            'account_type': account.account_type,
            'balance': '2000.00',
        }
        response = client.post(url, data)
        assert response.status_code == 302
        account.refresh_from_db()
        assert account.name == 'Novo Nome'
        
        messages = list(get_messages(response.wsgi_request))
        assert any('Conta atualizada com sucesso!' in str(m) for m in messages)

    def test_account_delete_view_post(self, client):
        user = UserFactory()
        account = AccountFactory(user=user)
        client.force_login(user)
        url = reverse('accounts:account_delete', kwargs={'pk': account.pk})
        response = client.post(url)
        assert response.status_code == 302
        assert not Account.objects.filter(pk=account.pk).exists()
        
        messages = list(get_messages(response.wsgi_request))
        assert any('Conta excluída com sucesso!' in str(m) for m in messages)

    def test_account_access_denied_other_user(self, client):
        user1 = UserFactory()
        user2 = UserFactory()
        account_user1 = AccountFactory(user=user1)
        
        client.force_login(user2)
        
        # Test update
        url_update = reverse('accounts:account_update', kwargs={'pk': account_user1.pk})
        response = client.get(url_update)
        assert response.status_code == 404
        
        # Test delete
        url_delete = reverse('accounts:account_delete', kwargs={'pk': account_user1.pk})
        response = client.post(url_delete)
        assert response.status_code == 404
