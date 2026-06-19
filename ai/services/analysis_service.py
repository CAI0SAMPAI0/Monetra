import logging
from datetime import datetime, timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db.models import Sum
from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction
from ai.models import AIAnalysis
from ai.agents.finance_insight_agent import run_financial_agent

logger = logging.getLogger(__name__)
User = get_user_model()


def get_user_financial_context(user) -> str:
    """
    Coleta e formata os dados financeiros consolidados do usuário para enviar ao agente de IA.
    """
    try:
        accounts = Account.objects.filter(user=user, is_active=True)
        total_balance = accounts.aggregate(total=Sum('balance'))['total'] or Decimal('0.00')
        
        accounts_summary = []
        for acc in accounts:
            accounts_summary.append(f"- {acc.name} ({acc.bank_name}): R$ {acc.balance:.2f}")
        
        accounts_str = '\n'.join(accounts_summary) if accounts_summary else 'Nenhuma conta cadastrada.'
        
        categories = Category.objects.filter(user=user)
        categories_str = ', '.join([f"{cat.name} ({cat.get_category_type_display()})" for cat in categories])
        if not categories_str:
            categories_str = 'Nenhuma categoria cadastrada.'

        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        transactions = Transaction.objects.filter(
            account__user=user,
            transaction_date__gte=thirty_days_ago
        ).order_by('-transaction_date')

        totals = transactions.values('transaction_type').annotate(total_amount=Sum('amount'))
        inflow = Decimal('0.00')
        outflow = Decimal('0.00')
        for t in totals:
            if t['transaction_type'] == 'INCOME':
                inflow = t['total_amount'] or Decimal('0.00')
            elif t['transaction_type'] == 'EXPENSE':
                outflow = t['total_amount'] or Decimal('0.00')

        trans_list = []
        for trans in transactions[:15]:
            trans_list.append(
                f"- {trans.transaction_date.strftime('%d/%m/%Y')} | {trans.get_transaction_type_display()} | "
                f"R$ {trans.amount:.2f} | Categ: {trans.category.name} | Desc: {trans.description or 'Sem descrição'}"
            )
        
        transactions_str = '\n'.join(trans_list) if trans_list else 'Nenhuma transação nos últimos 30 dias.'

        context = (
            f"=== CONTEXTO FINANCEIRO DO USUÁRIO ===\n"
            f"Email: {user.email}\n"
            f"Saldo Total Consolidado: R$ {total_balance:.2f}\n\n"
            f"Contas Ativas:\n{accounts_str}\n\n"
            f"Categorias do Usuário:\n{categories_str}\n\n"
            f"Estatísticas dos últimos 30 dias:\n"
            f"- Total Receitas: R$ {inflow:.2f}\n"
            f"- Total Despesas: R$ {outflow:.2f}\n"
            f"- Balanço: R$ {(inflow - outflow):.2f}\n\n"
            f"Histórico de Transações Recentes:\n{transactions_str}"
        )
        return context
    except Exception as e:
        logger.error(f"Erro ao gerar contexto financeiro para o usuário {user.email}: {e}")
        return "Erro ao processar o contexto financeiro local."


def run_analysis_for_user(user) -> AIAnalysis:
    """
    Executa a análise de IA para um usuário específico, persiste o resultado no banco
    e marca como a mais recente.
    """
    try:
        logger.info(f"Iniciando análise financeira para o usuário: {user.email}")
        
        # 1. Coleta dados locais
        context = get_user_financial_context(user)
        
        # 2. Executa o agente financeiro do Langchain
        prompt_input = (
            f"Por favor, faça uma análise detalhada da minha saúde financeira com base no contexto abaixo. "
            f"Identifique padrões de consumo, aponte áreas críticas de desperdício e forneça 3 dicas práticas "
            f"e empáticas em Português do Brasil para me ajudar a economizar.\n\n{context}"
        )
        
        analysis_text = run_financial_agent(user.id, prompt_input)
        
        # 3. Gera resumo rápido para o dashboard
        summary = analysis_text.split('.')[0][:100]
        if len(summary) < len(analysis_text.split('.')[0]):
            summary += '...'
        if not summary.strip():
            summary = 'Análise Financeira Inteligente'
            
        # 4. Desmarca análises anteriores e persiste a nova como is_latest=True
        AIAnalysis.objects.filter(user=user).update(is_latest=False)
        
        analysis = AIAnalysis.objects.create(
            user=user,
            analysis_text=analysis_text,
            summary=summary,
            is_latest=True
        )
        
        logger.info(f"Análise persistida com sucesso para {user.email} (ID: {analysis.id})")
        return analysis
    except Exception as e:
        logger.error(f"Falha na geração de análise para {user.email}: {e}")
        return None


def run_analysis_for_all_users() -> dict:
    """
    Itera sobre todos os usuários ativos do sistema para gerar e salvar as análises de IA.
    """
    users = User.objects.filter(is_active=True)
    total = users.count()
    success = 0
    errors = 0
    
    logger.info(f"Iniciando processamento em lote de análise para {total} usuários.")
    
    for user in users:
        result = run_analysis_for_user(user)
        if result:
            success += 1
        else:
            errors += 1
            
    logger.info(f"Processamento concluído: Total: {total} | Sucessos: {success} | Erros: {errors}")
    return {
        'total': total,
        'success': success,
        'errors': errors
    }
