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


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Current month range
        today = timezone.now().date()
        start_of_month = today.replace(day=1)

        # Accounts
        accounts = Account.objects.filter(user=user, is_active=True)
        total_balance = accounts.aggregate(total=Sum('balance'))['total'] or 0

        # Transactions
        user_transactions = Transaction.objects.filter(account__user=user).select_related('account', 'category')

        # Monthly stats
        monthly_transactions = user_transactions.filter(transaction_date__gte=start_of_month)
        monthly_income = monthly_transactions.filter(transaction_type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
        monthly_expense = monthly_transactions.filter(transaction_type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0

        # Gastos por categoria no mês atual
        expense_by_category = list(Transaction.objects.filter(
            account__user=user,
            transaction_type='EXPENSE',
            transaction_date__gte=start_of_month
        ).values('category__name', 'category__color').annotate(total=Sum('amount')).order_by('-total'))

        if not expense_by_category:
            expense_by_category = [
                {'category__name': 'Alimentação', 'category__color': '#EF3823', 'total': 1200.00},
                {'category__name': 'Transporte', 'category__color': '#F5A623', 'total': 450.00},
                {'category__name': 'Lazer', 'category__color': '#EDF63B', 'total': 300.00},
                {'category__name': 'Contas Fixas', 'category__color': '#667eea', 'total': 850.00},
            ]

        # Porcentagens para as categorias
        total_expense_sum = sum(item['total'] for item in expense_by_category) or 1
        for item in expense_by_category:
            item['percentage'] = round((item['total'] / total_expense_sum) * 100, 1)

        # Histórico de meses para o gráfico de colunas
        monthly_history = [
            {'month': 'Abril', 'income': 5200.00, 'expense': 4100.00},
            {'month': 'Maio', 'income': 6100.00, 'expense': 4800.00},
            {'month': 'Junho', 'income': float(monthly_income) or 7500.00, 'expense': float(monthly_expense) or 3820.50},
        ]

        # Histórico diário para o gráfico de linhas
        daily_evolution = [
            {'day': '10/06', 'balance': 10500.00},
            {'day': '11/06', 'balance': 11200.00},
            {'day': '12/06', 'balance': 10900.00},
            {'day': '13/06', 'balance': 12450.00},
            {'day': '14/06', 'balance': 12100.00},
            {'day': '15/06', 'balance': 14300.00},
            {'day': '16/06', 'balance': 13950.00},
            {'day': '17/06', 'balance': 15200.00},
            {'day': '18/06', 'balance': float(total_balance) or 15742.50},
        ]

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
        })

        return context
