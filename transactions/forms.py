from django import forms
from .models import Transaction
from accounts.models import Account
from categories.models import Category


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = (
            'account',
            'category',
            'transaction_type',
            'amount',
            'transaction_date',
            'description'
        )
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['account'].queryset = Account.objects.filter(user=self.user)
            self.fields['category'].queryset = Category.objects.filter(user=self.user)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200'
            })
    
    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        category = cleaned_data.get('category')
        
        if category and transaction_type:
            if category.category_type != transaction_type:
                self.add_error('category', 'A categoria deve corresponder ao tipo de transação.')
        
        amount = cleaned_data.get('amount')
        if amount and amount <= 0:
            self.add_error('amount', 'O valor deve ser maior que zero.')
            
        return cleaned_data
