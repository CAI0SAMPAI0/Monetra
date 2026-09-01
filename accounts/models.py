from django.conf import settings
from django.db import models


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('CHECKING', 'Conta Corrente'),
        ('SAVINGS', 'Poupança'),
        ('WALLET', 'Carteira'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts'
    )
    name = models.CharField('nome da conta', max_length=100)
    bank_name = models.CharField('nome do banco', max_length=100)
    account_type = models.CharField(
        'tipo de conta',
        max_length=20,
        choices=ACCOUNT_TYPES,
        default='CHECKING'
    )
    balance = models.DecimalField(
        'saldo',
        max_digits=12,
        decimal_places=2,
        default=0
    )
    is_active = models.BooleanField('ativa', default=True)
    pluggy_item_id = models.CharField('Item ID na Pluggy', max_length=255, blank=True, null=True, help_text='UUID do Item na Pluggy')
    pluggy_account_id = models.CharField('Account ID na Pluggy', max_length=255, blank=True, null=True, help_text='UUID da Conta na Pluggy')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'conta'
        verbose_name_plural = 'contas'
        ordering = ['name']
        indexes = [
            models.Index(fields=['user', 'name']),
        ]

    def __str__(self):
        return self.name

    @property
    def bank_brand(self):
        name_lower = f'{self.name} {self.bank_name}'.lower()
        if 'santander' in name_lower:
            return {
                'name': 'Santander',
                'bg_class': 'bg-[#EC0000]/15',
                'text_class': 'text-[#EC0000]',
                'border_class': 'border-[#EC0000]/30',
                'initials': 'SAN',
                'color': '#EC0000',
            }
        elif 'nu' in name_lower or 'nubank' in name_lower:
            return {
                'name': 'Nubank',
                'bg_class': 'bg-[#820AD1]/15',
                'text_class': 'text-[#A644FF]',
                'border_class': 'border-[#820AD1]/30',
                'initials': 'Nu',
                'color': '#820AD1',
            }
        elif 'itaú' in name_lower or 'itau' in name_lower:
            return {
                'name': 'Itaú',
                'bg_class': 'bg-[#EC7000]/15',
                'text_class': 'text-[#FF851B]',
                'border_class': 'border-[#EC7000]/30',
                'initials': 'Itaú',
                'color': '#EC7000',
            }
        elif 'bradesco' in name_lower:
            return {
                'name': 'Bradesco',
                'bg_class': 'bg-[#CC092F]/15',
                'text_class': 'text-[#FF3355]',
                'border_class': 'border-[#CC092F]/30',
                'initials': 'BRA',
                'color': '#CC092F',
            }
        elif 'inter' in name_lower:
            return {
                'name': 'Inter',
                'bg_class': 'bg-[#FF7A00]/15',
                'text_class': 'text-[#FF7A00]',
                'border_class': 'border-[#FF7A00]/30',
                'initials': 'inter',
                'color': '#FF7A00',
            }
        elif 'brasil' in name_lower or 'bb' in name_lower:
            return {
                'name': 'Banco do Brasil',
                'bg_class': 'bg-[#003882]/20',
                'text_class': 'text-[#FFD700]',
                'border_class': 'border-[#FFD700]/30',
                'initials': 'BB',
                'color': '#FFD700',
            }
        elif 'c6' in name_lower:
            return {
                'name': 'C6 Bank',
                'bg_class': 'bg-[#1C2A38]',
                'text_class': 'text-[#E2EAF0]',
                'border_class': 'border-[#374B5C]',
                'initials': 'C6',
                'color': '#E2EAF0',
            }
        elif 'caixa' in name_lower:
            return {
                'name': 'Caixa',
                'bg_class': 'bg-[#005CA9]/15',
                'text_class': 'text-[#2196F3]',
                'border_class': 'border-[#005CA9]/30',
                'initials': 'CX',
                'color': '#2196F3',
            }
        elif 'mercado' in name_lower or 'pago' in name_lower:
            return {
                'name': 'Mercado Pago',
                'bg_class': 'bg-[#009EE3]/15',
                'text_class': 'text-[#00AEF0]',
                'border_class': 'border-[#009EE3]/30',
                'initials': 'MP',
                'color': '#009EE3',
            }
        elif 'btg' in name_lower:
            return {
                'name': 'BTG Pactual',
                'bg_class': 'bg-[#001E62]/20',
                'text_class': 'text-[#4D88FF]',
                'border_class': 'border-[#001E62]/40',
                'initials': 'BTG',
                'color': '#4D88FF',
            }
        else:
            return {
                'name': self.bank_name or 'Banco',
                'bg_class': 'bg-[#C09B2A]/10',
                'text_class': 'text-[#C09B2A]',
                'border_class': 'border-[#C09B2A]/20',
                'initials': (self.name[:2] if self.name else 'BK').upper(),
                'color': '#C09B2A',
            }

