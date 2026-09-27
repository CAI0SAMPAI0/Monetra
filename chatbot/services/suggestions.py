from datetime import date
from django.db.models import Sum
from accounts.models import Account
from transactions.models import Transaction


def generate_profile_suggestions(user, session=None) -> list[str]:
    """
    Gera dinamicamente sugestões contextuais de perguntas para o usuário
    com base no histórico salvo da sessão ativa ou nos dados reais de contas,
    investimentos e transações do usuário.
    """
    if session and session.latest_suggestions and isinstance(session.latest_suggestions, list):
        if len(session.latest_suggestions) > 0:
            return list(session.latest_suggestions)

    if not user or not user.is_authenticated:
        return [
            'Qual é meu saldo consolidado?',
            'Onde gastei mais este mês?',
            'Como posso economizar?'
        ]

    suggestions = []
    today = date.today()

    # 1. Investimentos e reserva
    has_investments = (
        Account.objects.filter(user=user, account_type='INVESTMENT', is_active=True).exists()
        or Transaction.objects.filter(account__user=user, transaction_type='INVESTMENT').exists()
    )
    if has_investments:
        suggestions.append('Como está o rendimento dos meus investimentos e minha reserva?')

    # 2. Transações agendadas / liquidações D+N
    has_scheduled = Transaction.objects.filter(
        account__user=user,
        settlement_date__gte=today
    ).exists()
    if has_scheduled:
        suggestions.append('Quais transações e liquidações estão agendadas para os próximos dias?')

    # 3. Principal categoria de despesa do mês atual
    first_of_month = today.replace(day=1)
    top_cat = (
        Transaction.objects.filter(
            account__user=user,
            transaction_type='EXPENSE',
            transaction_date__gte=first_of_month
        )
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
        .first()
    )
    if top_cat and top_cat.get('category__name'):
        cat_name = top_cat['category__name']
        suggestions.append(f'Como posso otimizar meus gastos com {cat_name}?')

    # 4. Multi-contas e saldo consolidado
    accounts_count = Account.objects.filter(user=user, is_active=True).count()
    if accounts_count > 1:
        suggestions.append('Qual é meu saldo consolidado entre todas as contas?')

    # Sugestões complementares para atingir pelo menos 3 a 4 itens
    fallbacks = [
        'Onde gastei mais este mês?',
        'Como posso economizar com base nos meus gastos?',
        'Analise meus hábitos de consumo',
        'Qual o balanço entre receitas e despesas este mês?'
    ]

    for item in fallbacks:
        if len(suggestions) >= 4:
            break
        if item not in suggestions:
            suggestions.append(item)

    return suggestions[:4]
