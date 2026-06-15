import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction
from decimal import Decimal

User = get_user_model()

@pytest.mark.django_db
def test_full_flow_signup_to_transaction(client):
    '''8.5.1: Test full flow: Signup -> Create Account -> Create Category -> Record first transaction.'''
    # 1. Signup
    signup_url = reverse('users:signup')
    client.post(signup_url, {
        'email': 'integration@example.com',
        'password1': 'password123',
        'password2': 'password123'
    })
    user = User.objects.get(email='integration@example.com')
    client.force_login(user)
    
    # 2. Create Account
    account_create_url = reverse('accounts:account_create')
    client.post(account_create_url, {
        'name': 'Main Bank',
        'bank_name': 'Test Bank',
        'account_type': 'CHECKING',
        'balance': '1000.00'
    })
    account = Account.objects.get(user=user, name='Main Bank')
    
    # 3. Create Category
    category_create_url = reverse('categories:category_create')
    client.post(category_create_url, {
        'name': 'Bonus',
        'category_type': 'INCOME',
        'color': '#00FF00'
    })
    category = Category.objects.get(user=user, name='Bonus')
    
    # 4. Record first transaction
    transaction_create_url = reverse('transactions:transaction_create')
    client.post(transaction_create_url, {
        'account': account.id,
        'category': category.id,
        'transaction_type': 'INCOME',
        'amount': '500.00',
        'transaction_date': '2023-01-01',
        'description': 'First income'
    })
    
    assert Transaction.objects.filter(account=account).count() == 1
    account.refresh_from_db()
    assert account.balance == Decimal('1500.00')


@pytest.mark.django_db
def test_complex_flow_multiple_transactions(client):
    '''8.5.2: Test complex flow: Multiple transactions across different accounts and categories, verifying final balances.'''
    user = User.objects.create_user(email='complex@example.com', password='password')
    client.force_login(user)
    
    acc1 = Account.objects.create(user=user, name='Acc 1', balance=Decimal('1000.00'))
    acc2 = Account.objects.create(user=user, name='Acc 2', balance=Decimal('2000.00'))
    
    cat_inc = Category.objects.create(user=user, name='Inc', category_type='INCOME')
    cat_exp = Category.objects.create(user=user, name='Exp', category_type='EXPENSE')
    
    # Trans 1: Acc 1, Income 500 -> 1500
    Transaction.objects.create(account=acc1, category=cat_inc, transaction_type='INCOME', amount=Decimal('500.00'), transaction_date='2023-01-01')
    
    # Trans 2: Acc 1, Expense 200 -> 1300
    Transaction.objects.create(account=acc1, category=cat_exp, transaction_type='EXPENSE', amount=Decimal('200.00'), transaction_date='2023-01-01')
    
    # Trans 3: Acc 2, Expense 500 -> 1500
    Transaction.objects.create(account=acc2, category=cat_exp, transaction_type='EXPENSE', amount=Decimal('500.00'), transaction_date='2023-01-01')
    
    acc1.refresh_from_db()
    acc2.refresh_from_db()
    
    assert acc1.balance == Decimal('1300.00')
    assert acc2.balance == Decimal('1500.00')


@pytest.mark.django_db
def test_isolation_user_a_cannot_see_user_b_data(client):
    '''8.5.3: Test isolation: Ensure User A cannot see or modify data from User B.'''
    user_a = User.objects.create_user(email='user_a@example.com', password='password')
    user_b = User.objects.create_user(email='user_b@example.com', password='password')
    
    acc_b = Account.objects.create(user=user_b, name='Secret Account', balance=Decimal('1000.00'))
    cat_b = Category.objects.create(user=user_b, name='Secret Cat', category_type='EXPENSE')
    trans_b = Transaction.objects.create(account=acc_b, category=cat_b, transaction_type='EXPENSE', amount=Decimal('10.00'), transaction_date='2023-01-01')
    
    client.force_login(user_a)
    
    # Try to access User B's account (update page)
    response = client.get(reverse('accounts:account_update', kwargs={'pk': acc_b.pk}))
    assert response.status_code == 404
    
    # Try to access User B's category (update page)
    response = client.get(reverse('categories:category_update', kwargs={'pk': cat_b.pk}))
    assert response.status_code == 404
    
    # Try to access User B's transaction (update page)
    response = client.get(reverse('transactions:transaction_update', kwargs={'pk': trans_b.pk}))
    assert response.status_code == 404
