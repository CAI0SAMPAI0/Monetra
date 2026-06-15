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
