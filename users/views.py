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
        accounts = Account.objects.filter(user=user, is_active=True)
        total_balance = accounts.aggregate(total=Sum('balance'))['total'] or Decimal('0.00')

        # User transactions
        user_transactions = Transaction.objects.filter(account__user=user).select_related('account', 'category')
        latest_tx = user_transactions.order_by('-transaction_date').first()
        today = timezone.now().date()
        ref_date = latest_tx.transaction_date if latest_tx else today

        # Monthly stats (based on reference active month)
        period_txs = user_transactions.filter(
            transaction_date__year=ref_date.year,
            transaction_date__month=ref_date.month
        )
        monthly_income = period_txs.filter(transaction_type='INCOME').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        monthly_expense = period_txs.filter(transaction_type='EXPENSE').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        # Gastos reais por categoria no período
        expense_by_category = list(period_txs.filter(
            transaction_type='EXPENSE'
        ).values('category__name', 'category__color').annotate(total=Sum('amount')).order_by('-total')[:6])

        # Se não houver despesas no mês de referência, busca as últimas despesas gerais
        if not expense_by_category:
            expense_by_category = list(user_transactions.filter(
                transaction_type='EXPENSE'
            ).values('category__name', 'category__color').annotate(total=Sum('amount')).order_by('-total')[:6])

        total_expense_sum = sum(item['total'] for item in expense_by_category) or Decimal('1.00')
        for item in expense_by_category:
            item['percentage'] = round((float(item['total']) / float(total_expense_sum)) * 100, 1)

        # Histórico real dos últimos 6 meses para o gráfico de barras
        months_names = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        monthly_history = []
        for i in range(5, -1, -1):
            m_start = ref_date.replace(day=1) - relativedelta(months=i)
            m_next = m_start + relativedelta(months=1)
            m_inc = user_transactions.filter(
                transaction_type='INCOME',
                transaction_date__gte=m_start,
                transaction_date__lt=m_next
            ).aggregate(total=Sum('amount'))['total'] or 0
            m_exp = user_transactions.filter(
                transaction_type='EXPENSE',
                transaction_date__gte=m_start,
                transaction_date__lt=m_next
            ).aggregate(total=Sum('amount'))['total'] or 0
            monthly_history.append({
                'month': f'{months_names[m_start.month - 1]}',
                'income': float(m_inc),
                'expense': float(m_exp),
            })

        # Histórico diário real de movimentações
        distinct_days = list(user_transactions.values_list('transaction_date', flat=True).distinct().order_by('transaction_date'))[-10:]
        daily_evolution = []
        if distinct_days:
            for d in distinct_days:
                d_txs = user_transactions.filter(transaction_date=d)
                d_inc = d_txs.filter(transaction_type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
                d_exp = d_txs.filter(transaction_type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
                daily_evolution.append({
                    'day': d.strftime('%d/%m'),
                    'balance': float(total_balance) + float(d_inc) - float(d_exp)
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
            'active_accounts_count': accounts.count(),
            'category_summary': expense_by_category,
            'monthly_history': monthly_history,
            'daily_evolution': daily_evolution,
            'reference_month': f'{months_names[ref_date.month - 1]}/{ref_date.year}',
        })

        return context

