from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum

from .forms import SignupForm, LoginForm
from accounts.models import Account
from transactions.models import Transaction


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:dashboard')
        return super().get(request, *args, **kwargs)


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('users:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Conta criada com sucesso!')
        return response


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'auth/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Login realizado com sucesso!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.method.upper() == 'POST':
            messages.info(request, 'Você saiu da sua conta.')
        return super().dispatch(request, *args, **kwargs)


from dateutil.relativedelta import relativedelta
from decimal import Decimal


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # User accounts & total balance
        accounts = list(Account.objects.filter(user=user, is_active=True))
        total_balance = sum((acc.balance for acc in accounts), Decimal('0.00'))

        # Fetch recent transactions for the user
        user_transactions = Transaction.objects.filter(account__user=user).select_related('account', 'category')
        latest_tx = user_transactions.order_by('-transaction_date').first()
        today = timezone.now().date()
        ref_date = latest_tx.transaction_date if latest_tx else today

        # Monthly stats (single aggregation query)
        monthly_stats = user_transactions.filter(
            transaction_date__year=ref_date.year,
            transaction_date__month=ref_date.month
        ).values('transaction_type').annotate(total=Sum('amount'))

        monthly_income = Decimal('0.00')
        monthly_expense = Decimal('0.00')
        for stat in monthly_stats:
            if stat['transaction_type'] == 'INCOME':
                monthly_income = stat['total'] or Decimal('0.00')
            elif stat['transaction_type'] == 'EXPENSE':
                monthly_expense = stat['total'] or Decimal('0.00')

        # Expense by category (single query)
        expense_by_category = list(user_transactions.filter(
            transaction_date__year=ref_date.year,
            transaction_date__month=ref_date.month,
            transaction_type='EXPENSE'
        ).values('category__name', 'category__color').annotate(total=Sum('amount')).order_by('-total')[:6])

        if not expense_by_category:
            expense_by_category = list(user_transactions.filter(
                transaction_type='EXPENSE'
            ).values('category__name', 'category__color').annotate(total=Sum('amount')).order_by('-total')[:6])

        total_expense_sum = sum(item['total'] for item in expense_by_category) or Decimal('1.00')
        for item in expense_by_category:
            item['percentage'] = round((float(item['total']) / float(total_expense_sum)) * 100, 1)

        # Monthly history - single query for the 6 months period
        six_months_ago = (ref_date.replace(day=1) - relativedelta(months=5))
        history_txs = list(user_transactions.filter(
            transaction_date__gte=six_months_ago
        ).values('transaction_date', 'transaction_type', 'amount'))

        months_names = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        monthly_history = []
        for i in range(5, -1, -1):
            m_start = ref_date.replace(day=1) - relativedelta(months=i)
            m_next = m_start + relativedelta(months=1)
            
            m_inc = sum(tx['amount'] for tx in history_txs if tx['transaction_type'] == 'INCOME' and m_start <= tx['transaction_date'] < m_next)
            m_exp = sum(tx['amount'] for tx in history_txs if tx['transaction_type'] == 'EXPENSE' and m_start <= tx['transaction_date'] < m_next)
            
            monthly_history.append({
                'month': f'{months_names[m_start.month - 1]}',
                'income': float(m_inc),
                'expense': float(m_exp),
            })

        # Daily evolution - in-memory from history_txs
        recent_dates = sorted(list(set(tx['transaction_date'] for tx in history_txs)))[-10:]
        daily_evolution = []
        if recent_dates:
            running_balance = float(total_balance)
            for d in recent_dates:
                d_inc = sum(tx['amount'] for tx in history_txs if tx['transaction_date'] == d and tx['transaction_type'] == 'INCOME')
                d_exp = sum(tx['amount'] for tx in history_txs if tx['transaction_date'] == d and tx['transaction_type'] == 'EXPENSE')
                daily_evolution.append({
                    'day': d.strftime('%d/%m'),
                    'balance': running_balance + float(d_inc) - float(d_exp)
                })
        else:
            daily_evolution.append({
                'day': today.strftime('%d/%m'),
                'balance': float(total_balance)
            })

        context.update({
            'total_balance': total_balance,
            'monthly_income': monthly_income,
            'monthly_expense': monthly_expense,
            'monthly_balance': monthly_income - monthly_expense,
            'recent_transactions': user_transactions[:10],
            'active_accounts_count': len(accounts),
            'category_summary': expense_by_category,
            'monthly_history': monthly_history,
            'daily_evolution': daily_evolution,
            'active_tab': 'dashboard',
            'reference_month': f'{months_names[ref_date.month - 1]}/{ref_date.year}',
        })

        return context
