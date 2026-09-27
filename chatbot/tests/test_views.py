import json
from unittest.mock import MagicMock
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from chatbot.models import ChatSession, ChatMessage

User = get_user_model()


@pytest.fixture
def auth_client(client):
    user = User.objects.create_user(email='test_chat_view@example.com', password='password123')
    client.force_login(user)
    return client, user


@pytest.mark.django_db
class TestChatViews:
    def test_chat_view_creates_session_if_none_exists(self, auth_client):
        client, user = auth_client
        url = reverse('chatbot:chat')
        response = client.get(url)
        assert response.status_code == 200
        assert ChatSession.objects.filter(user=user).count() == 1
        active_session = response.context['active_session']
        assert active_session.title == 'Nova conversa'
        assert 'initial_suggestions' in response.context
        assert len(response.context['initial_suggestions']) > 0

    def test_create_new_session_endpoint(self, auth_client):
        client, user = auth_client
        url = reverse('chatbot:new_session')
        response = client.post(url)
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'
        assert 'session_id' in data
        assert ChatSession.objects.filter(user=user, id=data['session_id']).exists()

    def test_delete_session_endpoint(self, auth_client):
        client, user = auth_client
        session = ChatSession.objects.create(user=user, title='Sessão para deletar')
        ChatMessage.objects.create(user=user, session=session, message_text='Oi', is_from_bot=False)

        url = reverse('chatbot:delete_session', kwargs={'session_id': session.id})
        response = client.post(url)
        assert response.status_code == 200
        assert not ChatSession.objects.filter(id=session.id).exists()
        assert not ChatMessage.objects.filter(session_id=session.id).exists()

    def test_send_message_attaches_to_session_and_updates_title(self, auth_client, monkeypatch):
        client, user = auth_client
        session = ChatSession.objects.create(user=user, title='Nova conversa')

        # Mock AI response
        monkeypatch.setattr(
            'chatbot.views.run_chatbot_agent',
            lambda user_id, msg, session=None: ('Resposta do bot', ['Sugestão 1', 'Sugestão 2'])
        )

        url = reverse('chatbot:send')
        payload = {
            'message': 'Qual é o meu saldo de investimentos?',
            'session_id': str(session.id)
        }
        response = client.post(url, data=json.dumps(payload), content_type='application/json')
        assert response.status_code == 200
        data = response.json()
        assert data['response'] == 'Resposta do bot'
        assert data['suggestions'] == ['Sugestão 1', 'Sugestão 2']
        assert data['session_id'] == str(session.id)

        session.refresh_from_db()
        assert 'investimentos' in session.title.lower()
        assert session.messages.count() == 2
