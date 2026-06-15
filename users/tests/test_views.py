import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .factories import UserFactory

User = get_user_model()

@pytest.mark.django_db
class TestAuthViews:
    def test_signup_view_get(self, client):
        url = reverse('users:signup')
        response = client.get(url)
        assert response.status_code == 200
        assert 'auth/signup.html' in [t.name for t in response.templates]

    def test_signup_view_post(self, client):
        url = reverse('users:signup')
        data = {
            'email': 'test@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('users:dashboard')
        assert User.objects.filter(email='test@example.com').exists()
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        assert any('Conta criada com sucesso!' in str(m) for m in messages)

    def test_login_view_get(self, client):
        url = reverse('users:login')
        response = client.get(url)
        assert response.status_code == 200
        assert 'auth/login.html' in [t.name for t in response.templates]

    def test_login_view_post(self, client):
        user = UserFactory(email='user@example.com')
        url = reverse('users:login')
        data = {
            'username': 'user@example.com',
            'password': 'password',
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('users:dashboard')
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        assert any('Login realizado com sucesso!' in str(m) for m in messages)

    def test_logout_view_post(self, client):
        user = UserFactory()
        client.force_login(user)
        url = reverse('users:logout')
        response = client.post(url)
        assert response.status_code == 302
        
        # Check info message
        messages = list(get_messages(response.wsgi_request))
        assert any('Você saiu da sua conta.' in str(m) for m in messages)

@pytest.mark.django_db
class TestDashboardView:
    def test_dashboard_access_denied_anonymous(self, client):
        url = reverse('users:dashboard')
        response = client.get(url)
        assert response.status_code == 302
        assert reverse('users:login') in response.url

    def test_dashboard_view_context(self, client):
        user = UserFactory()
        client.force_login(user)
        url = reverse('users:dashboard')
        response = client.get(url)
        assert response.status_code == 200
        assert 'total_balance' in response.context
        assert 'monthly_income' in response.context
        assert 'monthly_expense' in response.context
        assert 'monthly_balance' in response.context
        assert 'recent_transactions' in response.context
        assert 'active_accounts_count' in response.context
