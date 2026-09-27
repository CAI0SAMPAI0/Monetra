from django.db import models
from accounts.models import Account
from categories.models import Category


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'Entrada'),
        ('EXPENSE', 'Saída'),
        ('TRANSFER', 'Transferência'),
        ('INVESTMENT', 'Investimento'),
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
    settlement_date = models.DateField(
        'data de liquidação / agendada',
        null=True,
        blank=True,
        help_text='Data em que a transação é efetivamente liquidada (ex: D+1, D+2).'
    )
    description = models.CharField('descrição', max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'transação'
        verbose_name_plural = 'transações'
        ordering = ['-transaction_date']

    @property
    def is_scheduled(self) -> bool:
        if not self.settlement_date:
            return False
        from django.utils import timezone
        return self.settlement_date > timezone.now().date()

    def __str__(self):
        return f'{self.description} - R$ {self.amount:.2f}' if self.description else f'Transação R$ {self.amount:.2f}'
