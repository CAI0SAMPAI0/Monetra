from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'category_type', 'color')
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2.5 bg-[#0F1720] border border-[#1C2A38] rounded-md text-[#C8D4DF] text-sm focus:outline-none focus:border-[#C09B2A] transition-all'
            })
