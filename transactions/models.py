from django.db import models
from accounts.models import Account
from categories.models import Category


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'Entrada'),
        ('EXPENSE', 'Saída'),
    ]

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='transactions'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions'
    )
    transaction_type = models.CharField(
        'tipo de transação',
        max_length=10,
        choices=TRANSACTION_TYPES
    )
    amount = models.DecimalField(
        'valor',
        max_digits=12,
        decimal_places=2
    )
    transaction_date = models.DateField('data da transação')
    description = models.CharField('descrição', max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'transação'
        verbose_name_plural = 'transações'
        ordering = ['-transaction_date']

    def __str__(self):
        return f'{self.description} - R$ {self.amount:.2f}' if self.description else f'Transação R$ {self.amount:.2f}'
