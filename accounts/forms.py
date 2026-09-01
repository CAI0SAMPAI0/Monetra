from django import forms
from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'bank_name', 'account_type', 'balance', 'pluggy_item_id')
        widgets = {
            'pluggy_item_id': forms.TextInput(attrs={'placeholder': 'UUID da Conexão / Item ID na Pluggy (opcional)'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2.5 bg-[#0F1720] border border-[#1C2A38] rounded-md text-[#C8D4DF] text-sm focus:outline-none focus:border-[#C09B2A] transition-all'
            })
