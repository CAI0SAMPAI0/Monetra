from datetime import date, timedelta
import pytest
from django.contrib.auth import get_user_model
from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction
from chatbot.models import ChatSession
from chatbot.services.suggestions import generate_profile_suggestions

User = get_user_model()


@pytest.mark.django_db
class TestSuggestionsService:
    def test_session_saved_suggestions_prioritized(self):
        user = User.objects.create_user(email='sug1@example.com', password='password123')
        session = ChatSession.objects.create(
            user=user,
            title='Sessão com sugestões',
            latest_suggestions=['Como investir em FIIs?', 'Qual minha taxa Selic?']
        )
        suggestions = generate_profile_suggestions(user, session)
        assert suggestions == ['Como investir em FIIs?', 'Qual minha taxa Selic?']

    def test_user_with_investments_gets_investment_prompts(self):
        user = User.objects.create_user(email='sug2@example.com', password='password123')
        session = ChatSession.objects.create(user=user, title='Investimentos')
        Account.objects.create(
            user=user,
            name='Nubank Investimentos',
            account_type='INVESTMENT',
            balance=3000.00
        )
        suggestions = generate_profile_suggestions(user, session)
        assert len(suggestions) >= 3
        # Should include question about investments or reserve
        has_inv_prompt = any('investimento' in s.lower() or 'reserva' in s.lower() for s in suggestions)
        assert has_inv_prompt

    def test_user_with_scheduled_tx_gets_scheduled_prompt(self):
        user = User.objects.create_user(email='sug3@example.com', password='password123')
        acc = Account.objects.create(user=user, name='Conta Corrente', balance=500.00)
        cat = Category.objects.create(user=user, name='Ações', category_type='INVESTMENT')
        Transaction.objects.create(
            account=acc,
            category=cat,
            amount=200.00,
            transaction_type='INVESTMENT',
            transaction_date=date.today(),
            settlement_date=date.today() + timedelta(days=2),
            description='Compra PETR4'
        )
        suggestions = generate_profile_suggestions(user)
        has_scheduled = any('agendada' in s.lower() or 'liquidação' in s.lower() or 'próxim' in s.lower() for s in suggestions)
        assert has_scheduled
