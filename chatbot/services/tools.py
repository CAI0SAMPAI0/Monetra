from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum
from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction
from chatbot.services.market import fetch_realtime_market_data


def get_user_financial_data(user_id: int) -> str:
    """
    Recupera e formata os dados financeiros do usuário para a IA.
    Retorna contas, categorias e transações recentes (últimos 30 dias).
    """
    try:
        # Contas
        accounts = Account.objects.filter(user_id=user_id, is_active=True)
        accounts_summary = []
        total_balance = Decimal('0.00')
        for acc in accounts:
            accounts_summary.append(f"- {acc.name} ({acc.bank_name}): R$ {acc.balance:.2f}")
            total_balance += acc.balance
        
        accounts_str = '\n'.join(accounts_summary) if accounts_summary else 'Nenhuma conta cadastrada.'
        
        # Categorias
        categories = Category.objects.filter(user_id=user_id)
        categories_str = ', '.join([f"{cat.name} ({cat.get_category_type_display()})" for cat in categories])
        if not categories_str:
            categories_str = 'Nenhuma categoria cadastrada.'

        # Transações dos últimos 30 dias
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        transactions = Transaction.objects.filter(
            account__user_id=user_id,
            transaction_date__gte=thirty_days_ago
        ).order_by('-transaction_date')

        # Totais de Entrada/Saída no período
        totals = transactions.values('transaction_type').annotate(total_amount=Sum('amount'))
        inflow = Decimal('0.00')
        outflow = Decimal('0.00')
        for t in totals:
            if t['transaction_type'] == 'INCOME':
                inflow = t['total_amount'] or Decimal('0.00')
            elif t['transaction_type'] == 'EXPENSE':
                outflow = t['total_amount'] or Decimal('0.00')

        trans_list = []
        for trans in transactions[:15]:  # Limita a 15 transações para otimizar tokens
            trans_list.append(
                f"- {trans.transaction_date.strftime('%d/%m/%Y')} | {trans.get_transaction_type_display()} | "
                f"R$ {trans.amount:.2f} | Categoria: {trans.category.name} | Descrição: {trans.description or 'Sem descrição'}"
            )
        
        transactions_str = '\n'.join(trans_list) if trans_list else 'Nenhuma transação registrada nos últimos 30 dias.'

        summary = (
            f"=== PANORAMA FINANCEIRO DO USUÁRIO ===\n"
            f"Saldo Total Consolidado: R$ {total_balance:.2f}\n\n"
            f"Contas Ativas:\n{accounts_str}\n\n"
            f"Categorias Disponíveis:\n{categories_str}\n\n"
            f"Resumo dos Últimos 30 Dias:\n"
            f"- Total Receitas: R$ {inflow:.2f}\n"
            f"- Total Despesas: R$ {outflow:.2f}\n"
            f"- Saldo do Período: R$ {(inflow - outflow):.2f}\n\n"
            f"Transações Recentes (últimas 15):\n{transactions_str}"
        )
        return summary
    except Exception as e:
        return f"Erro ao coletar dados financeiros locais: {str(e)}"


def get_market_data_summary() -> str:
    """
    Recupera e formata dados de mercado em tempo real.
    """
    try:
        data = fetch_realtime_market_data()
        
        currencies_str = '\n'.join([f"- {k.replace('_', '/')}: {v}" for k, v in data['currencies'].items()])
        stocks_str = '\n'.join([f"- {k}: {v}" for k, v in data['stocks'].items()])
        indicators_str = '\n'.join([f"- {k}: {v}" for k, v in data['real_estate'].items()])

        summary = (
            f"=== DADOS DO MERCADO FINANCEIRO EM TEMPO REAL ===\n"
            f"Câmbio:\n{currencies_str}\n\n"
            f"Índices de Ações:\n{stocks_str}\n\n"
            f"Indicadores Macroeconômicos e Imobiliários:\n{indicators_str}"
        )
        return summary
    except Exception as e:
        return f"Erro ao coletar dados de mercado: {str(e)}"
