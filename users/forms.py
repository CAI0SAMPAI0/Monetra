from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2.5 bg-[#0F1720] border border-[#1C2A38] rounded-md text-[#C8D4DF] text-sm focus:outline-none focus:border-[#C09B2A] transition-all'
            })


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2.5 bg-[#0F1720] border border-[#1C2A38] rounded-md text-[#C8D4DF] text-sm focus:outline-none focus:border-[#C09B2A] transition-all'
            })
