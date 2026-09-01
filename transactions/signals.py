from decimal import Decimal
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Transaction


@receiver(post_save, sender=Transaction)
def update_balance_on_create(sender, instance, created, **kwargs):
    if kwargs.get('raw') or getattr(instance, '_skip_signal', False):
        return
    # Pluggy accounts have authoritative live balances from Open Finance
    if instance.account.pluggy_account_id:
        return
    if created and instance.transaction_type in ['INCOME', 'EXPENSE']:
        account = instance.account
        amount = Decimal(str(instance.amount))
        if instance.transaction_type == 'INCOME':
            account.balance += amount
        elif instance.transaction_type == 'EXPENSE':
            account.balance -= amount
        account.save(update_fields=['balance'])


@receiver(post_delete, sender=Transaction)
def update_balance_on_delete(sender, instance, **kwargs):
    if getattr(instance, '_skip_signal', False):
        return
    if instance.account.pluggy_account_id:
        return
    if instance.transaction_type in ['INCOME', 'EXPENSE']:
        account = instance.account
        amount = Decimal(str(instance.amount))
        if instance.transaction_type == 'INCOME':
            account.balance -= amount
        elif instance.transaction_type == 'EXPENSE':
            account.balance += amount
        account.save(update_fields=['balance'])


@receiver(pre_save, sender=Transaction)
def update_balance_on_update(sender, instance, **kwargs):
    if kwargs.get('raw') or getattr(instance, '_skip_signal', False):
        return
    if instance.account.pluggy_account_id:
        return
    if instance.pk:
        try:
            old_instance = Transaction.objects.get(pk=instance.pk)
        except Transaction.DoesNotExist:
            return
        old_account = old_instance.account
        new_account = instance.account

        old_amount = Decimal(str(old_instance.amount))
        new_amount = Decimal(str(instance.amount))

        # Revert old balance
        if old_instance.transaction_type == 'INCOME':
            old_account.balance -= old_amount
        elif old_instance.transaction_type == 'EXPENSE':
            old_account.balance += old_amount

        if old_account == new_account:
            if instance.transaction_type == 'INCOME':
                old_account.balance += new_amount
            elif instance.transaction_type == 'EXPENSE':
                old_account.balance -= new_amount
            old_account.save(update_fields=['balance'])
        else:
            old_account.save(update_fields=['balance'])
            if instance.transaction_type == 'INCOME':
                new_account.balance += new_amount
            elif instance.transaction_type == 'EXPENSE':
                new_account.balance -= new_amount
            new_account.save(update_fields=['balance'])

