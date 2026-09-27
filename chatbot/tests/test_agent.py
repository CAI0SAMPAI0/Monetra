from unittest.mock import MagicMock
import pytest
from django.contrib.auth import get_user_model
from chatbot.models import ChatSession, ChatMessage
from chatbot.services.agent import run_chatbot_agent

User = get_user_model()


@pytest.mark.django_db
def test_agent_includes_multi_turn_history(monkeypatch):
    user = User.objects.create_user(email='history_test@example.com', password='password123')
    session = ChatSession.objects.create(user=user, title='Conversa Multi-Turn')

    # Add prior messages to session
    ChatMessage.objects.create(user=user, session=session, message_text='Minha reserva é de 2k', is_from_bot=False)
    ChatMessage.objects.create(user=user, session=session, message_text='Entendido, 2k cobrem 4 meses.', is_from_bot=True)

    captured_messages = []

    class MockCompletion:
        def __init__(self):
            msg = MagicMock()
            msg.content = 'Ótimo progresso!\n\n---SUGESTÕES---\n- Qual o próximo passo?\n- Como aumentar a reserva?'
            self.choices = [MagicMock(message=msg)]

    def mock_create(*args, **kwargs):
        captured_messages.extend(kwargs.get('messages', []))
        return MockCompletion()

    monkeypatch.setattr('chatbot.services.agent.config', lambda key, default='': 'fake_token')

    class MockOpenAI:
        def __init__(self, **kwargs):
            self.chat = MagicMock()
            self.chat.completions.create = mock_create

    monkeypatch.setattr('chatbot.services.agent.OpenAI', MockOpenAI)
    monkeypatch.setattr('chatbot.services.tools.get_user_financial_data', lambda u_id: 'Dados mock')
    monkeypatch.setattr('chatbot.services.tools.get_market_data_summary', lambda q: 'Mercado mock')

    resp, suggestions = run_chatbot_agent(user.id, 'E agora, quanto falta para 6 meses?', session=session)

    assert resp == 'Ótimo progresso!'
    assert len(suggestions) == 2
    assert suggestions[0] == 'Qual o próximo passo?'

    # Verify history was captured in the messages payload
    roles = [m['role'] for m in captured_messages]
    assert roles == ['system', 'user', 'assistant', 'user']
    assert captured_messages[1]['content'] == 'Minha reserva é de 2k'
    assert captured_messages[2]['content'] == 'Entendido, 2k cobrem 4 meses.'
    assert captured_messages[3]['content'] == 'E agora, quanto falta para 6 meses?'

    # Verify suggestions were persisted to session
    session.refresh_from_db()
    assert session.latest_suggestions == suggestions
