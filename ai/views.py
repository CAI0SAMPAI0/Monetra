import time
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from transactions.models import Transaction
from accounts.models import Account

@login_required
def generate_summary_api(request):
    # Simulates background processing delay (1.5s)
    time.sleep(1.5)
    
    user = request.user
    
    # Calculate current month stats
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    
    # User's transactions
    user_transactions = Transaction.objects.filter(account__user=user)
    monthly_transactions = user_transactions.filter(transaction_date__gte=start_of_month)
    
    # Real Incomes & Expenses
    monthly_income = monthly_transactions.filter(transaction_type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
    monthly_expense = monthly_transactions.filter(transaction_type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
    
    # Percentage calculation
    if monthly_income > 0:
        expense_percentage = int((monthly_expense / monthly_income) * 100)
    else:
        expense_percentage = 0
        
    # Find the actual highest expense category
    highest_expense_cat = monthly_transactions.filter(
        transaction_type='EXPENSE'
    ).values('category__name').annotate(total=Sum('amount')).order_by('-total').first()
    
    if highest_expense_cat:
        highest_cat_name = highest_expense_cat['category__name']
        highest_cat_value = highest_expense_cat['total']
    else:
        highest_cat_name = "Nenhuma despesa"
        highest_cat_value = 0
        
    # Generate dynamic text matching their real data
    summary_lines = [
        f"Com base na análise inteligente da sua carteira para {user.email}:",
        ""
    ]
    
    if monthly_income == 0 and monthly_expense == 0:
        summary_lines.append("• Atualmente, você não possui transações registradas no mês atual. Adicione receitas e despesas para obter uma análise completa.")
    else:
        if monthly_income > 0:
            summary_lines.append(f"• Suas despesas acumuladas representam {expense_percentage}% das suas receitas totais deste mês (Receitas: R$ {monthly_income:.2f} | Despesas: R$ {monthly_expense:.2f}).")
        else:
            summary_lines.append(f"• Você registrou R$ {monthly_expense:.2f} em despesas, mas ainda não registrou receitas no mês atual. Cadastre suas fontes de renda para balancear seu orçamento.")
            
        if highest_cat_value > 0:
            summary_lines.append(f"• Alerta: O maior volume de saídas ocorreu na categoria '{highest_cat_name}', totalizando R$ {highest_cat_value:.2f}.")
            dica_valor = float(highest_cat_value) * 0.15
            summary_lines.append(f"• Dica: Ao economizar 15% na categoria '{highest_cat_name}' (cerca de R$ {dica_valor:.2f}), você poderá poupar mais este mês.")
            
    if monthly_expense > monthly_income and monthly_income > 0:
        summary_lines.append("\nAtenção: Suas saídas estão superando suas entradas. Recomendamos revisar despesas não essenciais imediatamente.")
    elif monthly_expense > 0:
        summary_lines.append("\nSeu perfil financeiro indica uma postura disciplinada. Continue monitorando seus limites orçamentários!")
        
    summary_text = "\n".join(summary_lines)
    
    return JsonResponse({
        'status': 'success',
        'summary': summary_text,
        'message': 'Resumo financeiro real gerado com sucesso pela inteligência artificial!'
    })
