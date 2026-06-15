import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from profiles.models import Profile
from categories.models import Category
from accounts.tests.factories import AccountFactory
from categories.tests.factories import CategoryFactory
from transactions.models import Transaction

User = get_user_model()

@pytest.mark.django_db
def test_profile_created_on_user_signup():
    '''8.4.1: Test automatic profile creation on user signup.'''
    user = User.objects.create_user(email='test_signals@example.com', password='password')
    assert Profile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_default_categories_created_on_user_signup():
    '''8.4.2: Test automatic default category creation on user signup.'''
    user = User.objects.create_user(email='test_cats@example.com', password='password')
    # According to categories/signals.py, it creates 10 categories
    assert Category.objects.filter(user=user).count() == 10
    assert Category.objects.filter(user=user, category_type='INCOME').count() == 3
    assert Category.objects.filter(user=user, category_type='EXPENSE').count() == 7


@pytest.mark.django_db
def test_account_balance_update_on_transaction_create():
    '''8.4.3: Test account balance update when creating a transaction (INCOME increases, EXPENSE decreases).'''
    account = AccountFactory(balance=Decimal('1000.00'))
    category_inc = CategoryFactory(user=account.user, category_type='INCOME')
    
    # INCOME should increase balance
    Transaction.objects.create(
        account=account,
        category=category_inc,
        transaction_type='INCOME',
        amount=Decimal('500.00'),
        transaction_date='2023-01-01'
    )
    account.refresh_from_db()
    assert account.balance == Decimal('1500.00')
    
    # EXPENSE should decrease balance
    category_exp = CategoryFactory(user=account.user, category_type='EXPENSE')
    Transaction.objects.create(
        account=account,
        category=category_exp,
        transaction_type='EXPENSE',
        amount=Decimal('200.00'),
        transaction_date='2023-01-01'
    )
    account.refresh_from_db()
    assert account.balance == Decimal('1300.00')


@pytest.mark.django_db
def test_account_balance_update_on_transaction_update():
    '''8.4.4: Test account balance update when updating a transaction (recalculating the difference).'''
    account = AccountFactory(balance=Decimal('1000.00'))
    category = CategoryFactory(user=account.user, category_type='INCOME')
    
    transaction = Transaction.objects.create(
        account=account,
        category=category,
        transaction_type='INCOME',
        amount=Decimal('500.00'),
        transaction_date='2023-01-01'
    )
    account.refresh_from_db()
    assert account.balance == Decimal('1500.00')
    
    # Update amount: 500 -> 700 (+200 diff)
    transaction.amount = Decimal('700.00')
    transaction.save()
    account.refresh_from_db()
    assert account.balance == Decimal('1700.00')
    
    # Update type: INCOME -> EXPENSE
    # Reverting 700 income: 1700 - 700 = 1000
    # Applying 700 expense: 1000 - 700 = 300
    transaction.transaction_type = 'EXPENSE'
    transaction.save()
    account.refresh_from_db()
    assert account.balance == Decimal('300.00')


@pytest.mark.django_db
def test_account_balance_update_on_transaction_delete():
    '''8.4.5: Test account balance update when deleting a transaction (reversing the impact).'''
    account = AccountFactory(balance=Decimal('1000.00'))
    category = CategoryFactory(user=account.user, category_type='INCOME')
    
    transaction = Transaction.objects.create(
        account=account,
        category=category,
        transaction_type='INCOME',
        amount=Decimal('500.00'),
        transaction_date='2023-01-01'
    )
    account.refresh_from_db()
    assert account.balance == Decimal('1500.00')
    
    transaction.delete()
    account.refresh_from_db()
    assert account.balance == Decimal('1000.00')
