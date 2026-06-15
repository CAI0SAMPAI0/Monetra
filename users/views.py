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
        user_transactions = Transaction.objects.filter(account__user=user)

        # Monthly stats
        monthly_transactions = user_transactions.filter(transaction_date__gte=start_of_month)
        monthly_income = monthly_transactions.filter(transaction_type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
        monthly_expense = monthly_transactions.filter(transaction_type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0

        context.update({
            'total_balance': total_balance,
            'monthly_income': monthly_income,
            'monthly_expense': monthly_expense,
            'monthly_balance': monthly_income - monthly_expense,
            'recent_transactions': user_transactions[:10],
            'active_accounts_count': accounts.count(),
        })

        return context
