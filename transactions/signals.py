from decimal import Decimal
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Transaction


@receiver(post_save, sender=Transaction)
def update_balance_on_create(sender, instance, created, **kwargs):
    if created:
        account = instance.account
        amount = Decimal(str(instance.amount))
        if instance.transaction_type == 'INCOME':
            account.balance += amount
        else:
            account.balance -= amount
        account.save()


@receiver(post_delete, sender=Transaction)
def update_balance_on_delete(sender, instance, **kwargs):
    account = instance.account
    amount = Decimal(str(instance.amount))
    if instance.transaction_type == 'INCOME':
        account.balance -= amount
    else:
        account.balance += amount
    account.save()


@receiver(pre_save, sender=Transaction)
def update_balance_on_update(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Transaction.objects.get(pk=instance.pk)
        old_account = old_instance.account
        new_account = instance.account

        old_amount = Decimal(str(old_instance.amount))
        new_amount = Decimal(str(instance.amount))

        # Revert old balance
        if old_instance.transaction_type == 'INCOME':
            old_account.balance -= old_amount
        else:
            old_account.balance += old_amount
        
        if old_account == new_account:
            # Apply new balance to the same account
            if instance.transaction_type == 'INCOME':
                old_account.balance += new_amount
            else:
                old_account.balance -= new_amount
            old_account.save()
        else:
            # Apply to different accounts
            old_account.save()
            if instance.transaction_type == 'INCOME':
                new_account.balance += new_amount
            else:
                new_account.balance -= new_amount
            new_account.save()
