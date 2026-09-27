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
                'class': 'w-full px-3.5 py-2.5 bg-[#F7F9FC] dark:bg-[#1C2026] border border-[#E6E9ED] dark:border-white/10 rounded-xl text-[#17191E] dark:text-[#F1F4FA] text-sm focus:outline-none focus:border-[#019F60] dark:focus:border-[#C1FF7E] transition-all'
            })
