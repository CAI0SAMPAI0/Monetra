from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('full_name', 'phone', 'pluggy_client_id', 'pluggy_client_secret', 'pluggy_item_id')
        widgets = {
            'pluggy_client_id': forms.TextInput(attrs={'placeholder': 'Ex: d246965e-... ou seu Client ID'}),
            'pluggy_client_secret': forms.PasswordInput(render_value=True, attrs={'placeholder': '••••••••••••••••'}),
            'pluggy_item_id': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Cole aqui os Item IDs dos seus bancos (um por linha ou separados por vírgula):\nExemplo:\n692dda9c-99e8-4612-a0c6-2d993cd02fc4 (Santander)\ne4b21908-1123-4889-b124-7890abcdef12 (Nubank)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2.5 bg-[#0F1720] border border-[#1C2A38] rounded-md text-[#C8D4DF] text-sm focus:outline-none focus:border-[#C09B2A] transition-all'
            })

