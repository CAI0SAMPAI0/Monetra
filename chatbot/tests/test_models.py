import pytest
from django.contrib.auth import get_user_model
from chatbot.models import ChatSession, ChatMessage

User = get_user_model()


@pytest.mark.django_db
class TestChatSessionModels:
    def test_create_chat_session(self):
        user = User.objects.create_user(email='chat_user@example.com', password='password123')
        session = ChatSession.objects.create(
            user=user,
            title='Análise de Gastos Setembro',
            latest_suggestions=['Como economizar?', 'Qual meu saldo?']
        )
        assert session.id is not None
        assert str(session) == f'Session: Análise de Gastos Setembro ({user.email})'
        assert session.latest_suggestions == ['Como economizar?', 'Qual meu saldo?']
        assert session.created_at is not None
        assert session.updated_at is not None

    def test_create_chat_message_with_session(self):
        user = User.objects.create_user(email='chat_msg@example.com', password='password123')
        session = ChatSession.objects.create(user=user, title='Conversa 1')
        
        user_msg = ChatMessage.objects.create(
            user=user,
            session=session,
            message_text='Olá, quanto gastei esse mês?',
            is_from_bot=False
        )
        bot_msg = ChatMessage.objects.create(
            user=user,
            session=session,
            message_text='Você gastou R$ 150,00.',
            is_from_bot=True
        )

        assert user_msg.session == session
        assert bot_msg.session == session
        assert session.messages.count() == 2
        assert list(session.messages.all()) == [user_msg, bot_msg]
