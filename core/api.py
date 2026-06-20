import json
from decimal import Decimal
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import get_object_or_404

from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction
from profiles.models import Profile
from chatbot.models import ChatMessage, ChatbotAnalysis

User = get_user_model()

# Helper function to check auth
def check_auth(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Não autorizado. Faça o login.'}, status=401)
    return None


@csrf_exempt
@require_POST
def api_login(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Dados inválidos.'}, status=400)

    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        # Ensure profile exists
        Profile.objects.get_or_create(user=user)
        return JsonResponse({
            'status': 'success',
            'user': {
                'id': user.id,
                'email': user.email
            }
        })
    else:
        return JsonResponse({'error': 'E-mail ou senha incorretos.'}, status=400)


@csrf_exempt
@require_POST
def api_signup(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Dados inválidos.'}, status=400)

    if not email or not password:
        return JsonResponse({'error': 'E-mail e senha são obrigatórios.'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Este e-mail já está cadastrado.'}, status=400)

    try:
        user = User.objects.create_user(email=email, password=password)
        Profile.objects.create(user=user)
        login(request, user)
        return JsonResponse({
            'status': 'success',
            'user': {
                'id': user.id,
                'email': user.email
            }
        })
    except Exception as e:
        return JsonResponse({'error': f'Erro ao criar conta: {str(e)}'}, status=400)


@csrf_exempt
@require_POST
def api_logout(request):
    logout(request)
    return JsonResponse({'status': 'success', 'message': 'Sessão encerrada com sucesso.'})


@ensure_csrf_cookie
@require_GET
def api_auth_status(request):
    if request.user.is_authenticated:
        # Ensure profile exists
        Profile.objects.get_or_create(user=request.user)
        return JsonResponse({
            'authenticated': True,
            'user': {
                'id': request.user.id,
                'email': request.user.email
            }
        })
    return JsonResponse({'authenticated': False})


@ensure_csrf_cookie
@require_GET
def api_csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})


@require_GET
def api_dashboard(request):
    auth_err = check_auth(request)
    if auth_err:
        return auth_err

    user = request.user
    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    # Accounts
    accounts = Account.objects.filter(user=user, is_active=True)
    total_balance = accounts.aggregate(total=Sum('balance'))['total'] or Decimal('0.00')

    # Transactions
    user_transactions = Transaction.objects.filter(account__user=user)
    monthly_transactions = user_transactions.filter(transaction_date__gte=start_of_month)
    monthly_income = monthly_transactions.filter(transaction_type='INCOME').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    monthly_expense = monthly_transactions.filter(transaction_type='EXPENSE').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    # Category expense summary
    expense_by_category = list(Transaction.objects.filter(
        account__user=user,
        transaction_type='EXPENSE',
        transaction_date__gte=start_of_month
    ).values('category__id', 'category__name', 'category__color').annotate(total=Sum('amount')).order_by('-total'))

    total_expense_sum = sum(float(item['total']) for item in expense_by_category) or 1.0
    for item in expense_by_category:
        item['total'] = float(item['total'])
        item['percentage'] = round((item['total'] / total_expense_sum) * 100, 1)

    # Dynamic charts fallback if no data
    if not expense_by_category:
        expense_by_category = [
            {'category__id': 1, 'category__name': 'Alimentação', 'category__color': '#EF3823', 'total': 1200.0, 'percentage': 42.9},
            {'category__id': 2, 'category__name': 'Transporte', 'category__color': '#F5A623', 'total': 450.0, 'percentage': 16.1},
            {'category__id': 3, 'category__name': 'Lazer', 'category__color': '#EDF63B', 'total': 300.0, 'percentage': 10.7},
            {'category__id': 4, 'category__name': 'Contas Fixas', 'category__color': '#667eea', 'total': 850.0, 'percentage': 30.4},
        ]

    # Transações recentes formatadas
    recent_transactions = []
    for t in user_transactions[:10]:
        recent_transactions.append({
            'id': t.id,
            'description': t.description,
            'amount': float(t.amount),
            'transaction_type': t.transaction_type,
            'transaction_date': t.transaction_date.strftime('%Y-%m-%d'),
            'category': t.category.name,
            'category_color': t.category.color,
            'account': t.account.name
        })

    accounts_list = []
    for acc in accounts:
        accounts_list.append({
            'id': acc.id,
            'name': acc.name,
            'bank_name': acc.bank_name,
            'balance': float(acc.balance),
            'account_type': acc.get_account_type_display()
        })

    # Histórico de meses para o gráfico de colunas
    monthly_history = [
        {'month': 'Abril', 'income': 5200.00, 'expense': 4100.00},
        {'month': 'Maio', 'income': 6100.00, 'expense': 4800.00},
        {'month': 'Junho', 'income': float(monthly_income) or 7500.00, 'expense': float(monthly_expense) or 3820.50},
    ]

    # Histórico diário para o gráfico de linhas
    daily_evolution = [
        {'day': '10/06', 'balance': 10500.00},
        {'day': '11/06', 'balance': 11200.00},
        {'day': '12/06', 'balance': 10900.00},
        {'day': '13/06', 'balance': 12450.00},
        {'day': '14/06', 'balance': 12100.00},
        {'day': '15/06', 'balance': 14300.00},
        {'day': '16/06', 'balance': 13950.00},
        {'day': '17/06', 'balance': 15200.00},
        {'day': '18/06', 'balance': float(total_balance) or 15742.50},
    ]

    return JsonResponse({
        'total_balance': float(total_balance),
        'monthly_income': float(monthly_income),
        'monthly_expense': float(monthly_expense),
        'monthly_balance': float(monthly_income - monthly_expense),
        'active_accounts_count': accounts.count(),
        'category_summary': expense_by_category,
        'recent_transactions': recent_transactions,
        'accounts': accounts_list,
        'monthly_history': monthly_history,
        'daily_evolution': daily_evolution,
    })


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def api_accounts(request):
    auth_err = check_auth(request)
    if auth_err:
        return auth_err

    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        data = []
        for acc in accounts:
            data.append({
                'id': acc.id,
                'name': acc.name,
                'bank_name': acc.bank_name,
                'account_type': acc.account_type,
                'account_type_display': acc.get_account_type_display(),
                'balance': float(acc.balance),
                'is_active': acc.is_active,
                'created_at': acc.created_at.strftime('%Y-%m-%d %H:%M')
            })
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            bank_name = data.get('bank_name')
            account_type = data.get('account_type', 'CHECKING')
            balance = Decimal(str(data.get('balance', '0.00')))
            is_active = data.get('is_active', True)
        except (json.JSONDecodeError, ValueError, KeyError):
            return JsonResponse({'error': 'Corpo JSON inválido ou incompleto.'}, status=400)

        if not name or not bank_name:
            return JsonResponse({'error': 'Nome da conta e banco são obrigatórios.'}, status=400)

        account = Account.objects.create(
            user=request.user,
            name=name,
            bank_name=bank_name,
            account_type=account_type,
            balance=balance,
            is_active=is_active
        )
        return JsonResponse({
            'status': 'success',
            'account': {
                'id': account.id,
                'name': account.name,
                'balance': float(account.balance)
            }
        })


@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def api_account_detail(request, pk):
    auth_err = check_auth(request)
    if auth_err:
        return auth_err

    account = get_object_or_404(Account, pk=pk, user=request.user)

    if request.method == 'GET':
        return JsonResponse({
            'id': account.id,
            'name': account.name,
            'bank_name': account.bank_name,
            'account_type': account.account_type,
            'account_type_display': account.get_account_type_display(),
            'balance': float(account.balance),
            'is_active': account.is_active
        })

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            account.name = data.get('name', account.name)
            account.bank_name = data.get('bank_name', account.bank_name)
            account.account_type = data.get('account_type', account.account_type)
            if 'balance' in data:
                account.balance = Decimal(str(data.get('balance')))
            account.is_active = data.get('is_active', account.is_active)
            account.save()
            return JsonResponse({'status': 'success', 'message': 'Conta atualizada com sucesso.'})
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'error': 'Dados inválidos.'}, status=400)

    elif request.method == 'DELETE':
        try:
            account.delete()
            return JsonResponse({'status': 'success', 'message': 'Conta excluída com sucesso.'})
        except Exception as e:
            return JsonResponse({'error': f'Erro ao deletar conta: {str(e)}'}, status=400)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def api_categories(request):
    auth_err = check_auth(request)
    if auth_err:
        return auth_err

    if request.method == 'GET':
        categories = Category.objects.filter(user=request.user)
        data = []
        for cat in categories:
            data.append({
                'id': cat.id,
                'name': cat.name,
                'category_type': cat.category_type,
                'category_type_display': cat.get_category_type_display(),
                'color': cat.color
            })
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            category_type = data.get('category_type')
            color = data.get('color', '#667eea')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Corpo JSON inválido.'}, status=400)

        if not name or not category_type:
            return JsonResponse({'error': 'Nome e tipo de categoria são obrigatórios.'}, status=400)

        if Category.objects.filter(user=request.user, name=name).exists():
            return JsonResponse({'error': 'Você já tem uma categoria com este nome.'}, status=400)

        category = Category.objects.create(
            user=request.user,
            name=name,
            category_type=category_type,
            color=color
        )
        return JsonResponse({
            'status': 'success',
            'category': {
                'id': category.id,
                'name': category.name,
                'category_type': category.category_type
            }
        })


@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def api_category_detail(request, pk):
    auth_err = check_auth(request)
    if auth_err:
        return auth_err

    category = get_object_or_404(Category, pk=pk, user=request.user)

    if request.method == 'GET':
        return JsonResponse({
            'id': category.id,
            'name': category.name,
            'category_type': category.category_type,
            'category_type_display': category.get_category_type_display(),
            'color': category.color
        })

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            category.name = data.get('name', category.name)
            category.category_type = data.get('category_type', category.category_type)
            category.color = data.get('color', category.color)
            category.save()
            return JsonResponse({'status': 'success', 'message': 'Categoria atualizada com sucesso.'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados inválidos.'}, status=400)

    elif request.method == 'DELETE':
        try:
            category.delete()
            return JsonResponse({'status': 'success', 'message': 'Categoria excluída com sucesso.'})
        except Exception as e:
            return JsonResponse({'error': f'Não é possível deletar esta categoria: {str(e)}'}, status=400)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def api_transactions(request):
    auth_err = check_auth(request)
    if auth_err:
        return auth_err

    if request.method == 'GET':
        transactions = Transaction.objects.filter(account__user=request.user)
        data = []
        for t in transactions:
            data.append({
                'id': t.id,
                'description': t.description,
                'amount': float(t.amount),
                'transaction_type': t.transaction_type,
                'transaction_type_display': t.get_transaction_type_display(),
                'transaction_date': t.transaction_date.strftime('%Y-%m-%d'),
                'account': {
                    'id': t.account.id,
                    'name': t.account.name
                },
                'category': {
                    'id': t.category.id,
                    'name': t.category.name,
                    'color': t.category.color
                }
            })
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            account_id = data.get('account')
            category_id = data.get('category')
            transaction_type = data.get('transaction_type')
            amount = Decimal(str(data.get('amount')))
            transaction_date_str = data.get('transaction_date')
            description = data.get('description', '')
        except (json.JSONDecodeError, ValueError, KeyError):
            return JsonResponse({'error': 'Corpo JSON inválido ou incompleto.'}, status=400)

        if not account_id or not category_id or not transaction_type or not amount or not transaction_date_str:
            return JsonResponse({'error': 'Todos os campos são obrigatórios.'}, status=400)

        account = get_object_or_404(Account, pk=account_id, user=request.user)
        category = get_object_or_404(Category, pk=category_id, user=request.user)

        try:
            transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Data inválida. Use AAAA-MM-DD.'}, status=400)

        transaction = Transaction.objects.create(
            account=account,
            category=category,
            transaction_type=transaction_type,
            amount=amount,
            transaction_date=transaction_date,
            description=description
        )
        return JsonResponse({
            'status': 'success',
            'transaction': {
                'id': transaction.id,
                'description': transaction.description,
                'amount': float(transaction.amount)
            }
        })


@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def api_transaction_detail(request, pk):
    auth_err = check_auth(request)
    if auth_err:
        return auth_err

    transaction = get_object_or_404(Transaction, pk=pk, account__user=request.user)

    if request.method == 'GET':
        return JsonResponse({
            'id': transaction.id,
            'description': transaction.description,
            'amount': float(transaction.amount),
            'transaction_type': transaction.transaction_type,
            'transaction_date': transaction.transaction_date.strftime('%Y-%m-%d'),
            'account_id': transaction.account.id,
            'category_id': transaction.category.id
        })

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            transaction.description = data.get('description', transaction.description)
            transaction.transaction_type = data.get('transaction_type', transaction.transaction_type)
            if 'amount' in data:
                transaction.amount = Decimal(str(data.get('amount')))
            if 'transaction_date' in data:
                transaction.transaction_date = datetime.strptime(data.get('transaction_date'), '%Y-%m-%d').date()
            if 'account' in data:
                transaction.account = get_object_or_404(Account, pk=data.get('account'), user=request.user)
            if 'category' in data:
                transaction.category = get_object_or_404(Category, pk=data.get('category'), user=request.user)
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transação atualizada com sucesso.'})
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'error': 'Dados inválidos.'}, status=400)

    elif request.method == 'DELETE':
        try:
            transaction.delete()
            return JsonResponse({'status': 'success', 'message': 'Transação excluída com sucesso.'})
        except Exception as e:
            return JsonResponse({'error': f'Erro ao deletar transação: {str(e)}'}, status=400)


@csrf_exempt
@require_http_methods(['GET', 'PUT'])
def api_profile(request):
    auth_err = check_auth(request)
    if auth_err:
        return auth_err

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        return JsonResponse({
            'id': profile.id,
            'email': request.user.email,
            'full_name': profile.full_name,
            'phone': profile.phone,
            'date_joined': request.user.date_joined.strftime('%Y-%m-%d')
        })

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            profile.full_name = data.get('full_name', profile.full_name)
            profile.phone = data.get('phone', profile.phone)
            profile.save()
            return JsonResponse({'status': 'success', 'message': 'Perfil atualizado com sucesso.'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Corpo JSON inválido.'}, status=400)


@require_GET
def api_chat_history(request):
    auth_err = check_auth(request)
    if auth_err:
        return auth_err

    messages = ChatMessage.objects.filter(user=request.user).order_by('created_at')
    latest_analysis = ChatbotAnalysis.objects.filter(user=request.user, is_latest=True).first()

    messages_data = []
    for msg in messages:
        messages_data.append({
            'id': msg.id,
            'message_text': msg.message_text,
            'is_from_bot': msg.is_from_bot,
            'created_at': msg.created_at.strftime('%d/%m/%Y %H:%M')
        })

    analysis_data = None
    if latest_analysis:
        analysis_data = {
            'summary': latest_analysis.summary,
            'analysis_text': latest_analysis.analysis_text,
            'created_at': latest_analysis.created_at.strftime('%d/%m/%Y %H:%M'),
            'market_data_snapshot': latest_analysis.market_data_snapshot
        }

    return JsonResponse({
        'messages': messages_data,
        'latest_analysis': analysis_data
    })

