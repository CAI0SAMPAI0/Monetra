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
                'class': 'w-full px-3 py-2.5 bg-[#0F1720] border border-[#1C2A38] rounded-md text-[#C8D4DF] text-sm focus:outline-none focus:border-[#C09B2A] transition-all'
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
