from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Transaction
from .forms import TransactionForm

from accounts.models import Account


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 50

    def get_queryset(self):
        qs = Transaction.objects.filter(account__user=self.request.user).select_related('account', 'category')

        # Filter by Account
        account_id = self.request.GET.get('account')
        if account_id and account_id.isdigit():
            qs = qs.filter(account_id=int(account_id))

        # Filter by Type (INCOME / EXPENSE / TRANSFER)
        tx_type = self.request.GET.get('type')
        if tx_type in ['INCOME', 'EXPENSE', 'TRANSFER']:
            qs = qs.filter(transaction_type=tx_type)


        # Filter by search term
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(description__icontains=search.strip())

        return qs.order_by('-transaction_date', '-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = Account.objects.filter(user=self.request.user)
        context['selected_account'] = self.request.GET.get('account', '')
        context['selected_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:transaction_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Transação registrada com sucesso!')
        return super().form_valid(form)

class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(account__user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Transação atualizada com sucesso!')
        return super().form_valid(form)

from django.contrib.messages.views import SuccessMessageMixin

class TransactionDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transactions:transaction_list')
    success_message = 'Transação excluída com sucesso!'

    def get_queryset(self):
        return Transaction.objects.filter(account__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
