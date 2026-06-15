import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from users.tests.factories import UserFactory
from profiles.models import Profile

@pytest.mark.django_db
class TestProfileViews:
    def test_profile_detail_view(self, client):
        user = UserFactory()
        # Profile is created by signal
        client.force_login(user)
        url = reverse('profiles:profile_detail')
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.context['profile'] == user.profile

    def test_profile_update_view_post(self, client):
        user = UserFactory()
        client.force_login(user)
        url = reverse('profiles:profile_update')
        data = {
            'full_name': 'Novo Nome Completo',
            'phone': '123456789',
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('profiles:profile_detail')
        user.profile.refresh_from_db()
        assert user.profile.full_name == 'Novo Nome Completo'
        
        messages = list(get_messages(response.wsgi_request))
        assert any('Perfil atualizado com sucesso!' in str(m) for m in messages)
