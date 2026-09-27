import logging
import uuid
import re
import requests
from decimal import Decimal
from datetime import datetime, date, timedelta
from django.utils import timezone
from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction

logger = logging.getLogger(__name__)

PLUGGY_API_URL = 'https://api.pluggy.ai'


def is_valid_uuid(val: str) -> bool:
    """Check if a given string is a valid UUID."""
    if not val:
        return False
    try:
        uuid_obj = uuid.UUID(str(val).strip())
        return str(uuid_obj) == str(val).strip().lower() or len(str(val).strip()) == 36
    except (ValueError, AttributeError, TypeError):
        return False


def categorize_pluggy_transaction(
    tx_desc: str,
    pluggy_cat: str,
    tx_type_str: str,
    amount_val: float,
    user_name: str = ''
) -> tuple[str, str, str]:
    """
    Categorizes a transaction imported from Pluggy Open Finance.
    Returns: (django_tx_type, cat_name, cat_color)
    """
    desc_upper = (tx_desc or '').upper()
    cat_lower = (pluggy_cat or '').lower()
    clean_user = (user_name or '').upper()

    is_same_person = (
        'SAME PERSON' in cat_lower or
        'MESMA TITULARIDADE' in desc_upper or
        (clean_user and len(clean_user) > 3 and clean_user in desc_upper) or
        'CAIO MATOS' in desc_upper
    )
    is_cdb_sweep = (
        'CDB' in desc_upper or
        'RDB' in desc_upper or
        'APLICACAO' in desc_upper or
        'RESGATE' in desc_upper or
        'APLICAÇÃO' in desc_upper or
        'INVEST FACIL' in desc_upper or
        'CAIXINHA' in desc_upper or
        'INVESTIMENTO' in desc_upper or
        ('fixed income' in cat_lower and ('APLICACAO' in desc_upper or 'RESGATE' in desc_upper)) or
        ('investments' in cat_lower and ('APLICACAO' in desc_upper or 'RESGATE' in desc_upper or 'RDB' in desc_upper or 'CDB' in desc_upper))
    )
    is_investment = (
        'FII' in desc_upper or
        'FUNDO IMOBILIARIO' in desc_upper or
        'FUNDO IMOBILIÁRIO' in desc_upper or
        'TESOURO DIRETO' in desc_upper or
        'TESOURO SELIC' in desc_upper or
        'TESOURO IPCA' in desc_upper or
        'AÇÕES' in desc_upper or
        'ACOES' in desc_upper or
        'B3' in desc_upper or
        'CLEAR CORRETORA' in desc_upper or
        'RICO CORRETORA' in desc_upper or
        'NUINVEST' in desc_upper or
        'INTER DTVM' in desc_upper or
        'XP INVESTIMENTOS' in desc_upper or
        'SUBSCRIÇÃO' in desc_upper or
        'SUBSCRICAO' in desc_upper or
        'TITULOS PUBLICOS' in desc_upper or
        'TÍTULOS PÚBLICOS' in desc_upper or
        ('investments' in cat_lower and not is_same_person and not is_cdb_sweep)
    )

    if is_investment:
        django_tx_type = 'INVESTMENT'
        if any(k in desc_upper for k in ['FII', 'FUNDO IMOBILIARIO', 'FUNDO IMOBILIÁRIO']):
            cat_name = 'Aplicações em FII'
        elif any(k in desc_upper for k in ['AÇÕES', 'ACOES', 'B3']):
            cat_name = 'Ações / Renda Variável'
        elif any(k in desc_upper for k in ['TESOURO', 'TITULOS', 'TÍTULOS']):
            cat_name = 'Tesouro Direto / Títulos'
        else:
            cat_name = 'Investimentos Diversos'
        cat_color = '#0284C7'
    elif is_same_person or is_cdb_sweep:
        django_tx_type = 'TRANSFER'
        cat_name = 'Transferência Entre Contas' if is_same_person else 'Aplicação / Resgate CDB'
        cat_color = '#637585'
    else:
        django_tx_type = 'INCOME' if tx_type_str == 'CREDIT' or float(amount_val or 0) > 0 else 'EXPENSE'
        cat_name = pluggy_cat or ('Receitas Diversas' if django_tx_type == 'INCOME' else 'Outros Gastos')
        cat_color = '#1DCF72' if django_tx_type == 'INCOME' else '#E84040'

    return django_tx_type, cat_name, cat_color


class PluggyService:
    """
    Service to authenticate and sync financial data from Pluggy Open Finance API.
    Docs: https://docs.pluggy.ai
    """

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id.strip() if client_id else ''
        self.client_secret = client_secret.strip() if client_secret else ''
        self.api_key = None

    def authenticate(self) -> bool:
        """
        Authenticate with Pluggy API and obtain an apiKey token.
        """
        if not self.client_id or not self.client_secret:
            raise ValueError('Client ID e Client Secret da Pluggy são obrigatórios.')

        url = f'{PLUGGY_API_URL}/auth'
        payload = {
            'clientId': self.client_id,
            'clientSecret': self.client_secret
        }

        try:
            response = requests.post(url, json=payload, timeout=15)
            if response.status_code == 200:
                data = response.json()
                self.api_key = data.get('apiKey')
                return bool(self.api_key)
            else:
                logger.error(f'Pluggy auth failed ({response.status_code}): {response.text}')
                raise ValueError(f'Credenciais inválidas ou erro na autenticação Pluggy: {response.text}')
        except requests.RequestException as e:
            logger.error(f'Pluggy connection error: {e}')
            raise ConnectionError(f'Erro de conexão com o servidor da Pluggy: {str(e)}')

    def get_headers(self) -> dict:
        if not self.api_key:
            self.authenticate()
        return {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

    def fetch_item_by_id(self, item_id: str) -> dict:
        """
        Fetch details for a specific connected item (bank connection).
        Returns connector information (bank name, logo, primary color).
        """
        if not item_id or not is_valid_uuid(item_id):
            return {}
        headers = self.get_headers()
        url = f'{PLUGGY_API_URL}/items/{item_id.strip()}'
        try:
            response = requests.get(url, headers=headers, timeout=12)
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            logger.warning(f'Error querying item {item_id}: {e}')
            return {}

    def fetch_accounts_for_item(self, item_id: str) -> list:
        """
        Fetch bank accounts for a specific Pluggy item (institution connection).
        """
        if not item_id or not is_valid_uuid(item_id):
            logger.warning(f'Skipping invalid UUID item_id: {item_id}')
            return []

        headers = self.get_headers()
        url = f'{PLUGGY_API_URL}/accounts'
        params = {'itemId': item_id.strip()}

        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
        else:
            logger.error(f'Failed to fetch accounts for itemId {item_id} ({response.status_code}): {response.text}')
            raise ValueError(f'Erro ao buscar contas para o Item ID {item_id}: {response.text}')

    def fetch_investments_for_item(self, item_id: str) -> list:
        """
        Fetch investment assets (CDB, Renda Fixa, Ações, FIIs, Fundos) for a specific item.
        """
        if not item_id or not is_valid_uuid(item_id):
            return []

        headers = self.get_headers()
        url = f'{PLUGGY_API_URL}/investments'
        params = {'itemId': item_id.strip()}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data.get('results', [])
            else:
                logger.warning(f'Could not fetch investments for itemId {item_id}: {response.text}')
                return []
        except Exception as e:
            logger.error(f'Exception fetching investments for {item_id}: {e}')
            return []

    def fetch_transactions(self, account_id: str, from_date: str = None, page_size: int = 100, max_pages: int = 5) -> list:
        """
        Fetch transactions for a given Pluggy account using Pluggy V2 API with cursor pagination.
        Optimized with pageSize=100 and a max_pages cap to prevent long blocking network calls.
        """
        if not account_id or not is_valid_uuid(account_id):
            return []

        headers = self.get_headers()
        all_transactions = []
        next_cursor = None
        page_count = 0

        while page_count < max_pages:
            if next_cursor:
                if next_cursor.startswith('?') or 'after=' in next_cursor:
                    if next_cursor.startswith('/'):
                        url = f'{PLUGGY_API_URL}{next_cursor}'
                    elif next_cursor.startswith('?'):
                        url = f'{PLUGGY_API_URL}/v2/transactions{next_cursor}'
                    else:
                        url = f'{PLUGGY_API_URL}/v2/transactions?{next_cursor}'
                    params = None
                else:
                    url = f'{PLUGGY_API_URL}/v2/transactions'
                    params = {
                        'accountId': account_id.strip(),
                        'after': next_cursor
                    }
                    if from_date:
                        params['dateFrom'] = from_date
            else:
                url = f'{PLUGGY_API_URL}/v2/transactions'
                params = {
                    'accountId': account_id.strip()
                }
                if from_date:
                    params['dateFrom'] = from_date

            try:
                response = requests.get(url, headers=headers, params=params, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results', [])
                    all_transactions.extend(results)
                    next_cursor = data.get('next')
                    page_count += 1
                    if not next_cursor or not results:
                        break
                else:
                    logger.error(f'Failed to fetch transactions ({response.status_code}): {response.text}')
                    break
            except Exception as e:
                logger.error(f'Exception fetching transactions: {e}')
                break

        return all_transactions

    def sync_user_data(self, user) -> dict:
        """
        Main synchronization method:
        1. Authenticates
        2. Discovers item IDs from profile (multiple UUIDs supported) and user accounts
        3. Fetches accounts and updates balances
        4. Fetches and synchronizes investments (CDB, Fundos, Ações)
        5. Fetches and imports transactions
        """
        self.authenticate()

        # Gather item IDs from multiple sources
        item_ids = set()

        # 1. Profile item_ids_list (supports multiple lines/commas)
        if user.profile.pluggy_item_id:
            extracted_uuids = user.profile.pluggy_item_ids_list
            for uid in extracted_uuids:
                item_ids.add(uid)

        # 2. Account-specific pluggy_item_id
        acc_item_ids = Account.objects.filter(
            user=user,
            pluggy_item_id__isnull=False
        ).values_list('pluggy_item_id', flat=True)
        for i_id in acc_item_ids:
            if i_id and is_valid_uuid(i_id.strip()):
                item_ids.add(i_id.strip())


        if not item_ids:
            raise ValueError(
                'Nenhuma conexão bancária (Item ID) ativa encontrada na Pluggy. '
                'Por favor, conecte sua conta no dashboard da Pluggy (ou Pluggy Connect) '
                'e preencha o Item ID (UUID válido de 36 caracteres) no seu Perfil.'
            )

        accounts_synced = 0
        transactions_synced = 0
        investments_synced = 0

        type_mapping = {
            'CHECKING': 'CHECKING',
            'SAVINGS': 'SAVINGS',
            'CREDIT': 'WALLET',
            'INVESTMENT': 'INVESTMENT',
            'BANK': 'CHECKING',
        }

        for item_id in item_ids:
            # Fetch item metadata (connector name, logo, primary color)
            item_info = self.fetch_item_by_id(item_id)
            connector = item_info.get('connector') or {}
            connector_name = connector.get('name')
            connector_logo = connector.get('imageUrl')

            # 1. Fetch & Sync Accounts
            pluggy_accounts = self.fetch_accounts_for_item(item_id)

            # Resolve main bank name
            main_bank_name = connector_name or 'Banco Conectado'
            if main_bank_name == 'Banco Conectado':
                # Check accounts in this item for recognized bank names
                for p_acc in pluggy_accounts:
                    p_name = f"{p_acc.get('name', '')} {p_acc.get('marketingName', '')}".lower()
                    if any(k in p_name for k in ['nu', 'nubank', 'nu pagamentos']):
                        main_bank_name = 'Nubank'
                        break
                    elif 'santander' in p_name:
                        main_bank_name = 'Santander'
                        break
                    elif 'itau' in p_name or 'itaú' in p_name:
                        main_bank_name = 'Itaú'
                        break
                    elif 'bradesco' in p_name:
                        main_bank_name = 'Bradesco'
                        break
                    elif 'inter' in p_name:
                        main_bank_name = 'Inter'
                        break
                    elif 'brasil' in p_name or 'bb' in p_name:
                        main_bank_name = 'Banco do Brasil'
                        break
                    elif 'caixa' in p_name:
                        main_bank_name = 'Caixa'
                        break
                    elif 'c6' in p_name:
                        main_bank_name = 'C6 Bank'
                        break
                    elif 'mercado' in p_name or 'pago' in p_name:
                        main_bank_name = 'Mercado Pago'
                        break
                    elif 'btg' in p_name:
                        main_bank_name = 'BTG Pactual'
                        break

            # Pre-cache user categories for fast O(1) in-memory lookup
            user_categories = {c.name.strip().lower(): c for c in Category.objects.filter(user=user)}

            for p_acc in pluggy_accounts:
                p_account_id = p_acc.get('id')
                acc_name = p_acc.get('name') or p_acc.get('marketingName') or f'Conta Pluggy ({item_id[:8]})'
                
                # Bank name resolution
                bank_name = main_bank_name
                if isinstance(p_acc.get('institution'), dict):
                    bank_name = p_acc.get('institution', {}).get('name') or bank_name
                elif p_acc.get('bankName'):
                    bank_name = p_acc.get('bankName')
                if bank_name == 'Banco Conectado' and main_bank_name != 'Banco Conectado':
                    bank_name = main_bank_name

                p_type = p_acc.get('type', 'CHECKING')
                django_type = type_mapping.get(p_type, 'CHECKING')
                raw_balance = p_acc.get('balance', 0)
                balance = Decimal(str(raw_balance))

                # Look up account by pluggy_account_id or name
                account = None
                if p_account_id:
                    account = Account.objects.filter(user=user, pluggy_account_id=p_account_id).first()

                if not account:
                    account = Account.objects.filter(user=user, name=acc_name).first()

                is_pluggy_generic_logo = bool(connector_logo and ('pluggy.ai' in connector_logo or 'sandbox' in connector_logo))
                clean_logo = None if is_pluggy_generic_logo else connector_logo

                if not account:
                    account = Account.objects.create(
                        user=user,
                        name=acc_name,
                        bank_name=bank_name,
                        account_type=django_type,
                        balance=balance,
                        is_active=True,
                        pluggy_item_id=item_id,
                        pluggy_account_id=p_account_id,
                        logo_url=clean_logo
                    )
                else:
                    account.balance = balance
                    account.bank_name = bank_name
                    account.pluggy_item_id = item_id
                    account.pluggy_account_id = p_account_id
                    if account.logo_url and ('pluggy.ai' in account.logo_url or 'sandbox' in account.logo_url):
                        account.logo_url = None
                    elif clean_logo and not account.logo_url:
                        account.logo_url = clean_logo
                    account.save(update_fields=['balance', 'bank_name', 'pluggy_item_id', 'pluggy_account_id', 'logo_url', 'updated_at'])

                accounts_synced += 1

                # Incremental transactions sync
                if p_account_id:
                    latest_tx = Transaction.objects.filter(account=account).order_by('-transaction_date').first()
                    if latest_tx:
                        window_date = latest_tx.transaction_date - timedelta(days=15)
                        from_date = window_date.strftime('%Y-%m-%d')
                    else:
                        window_date = date.today() - timedelta(days=90)
                        from_date = window_date.strftime('%Y-%m-%d')

                    # Pre-load existing transactions in the window for O(1) deduplication
                    existing_txs = set(
                        Transaction.objects.filter(
                            account=account,
                            transaction_date__gte=window_date
                        ).values_list('transaction_date', 'amount', 'description')
                    )

                    p_transactions = self.fetch_transactions(p_account_id, from_date=from_date, page_size=100, max_pages=5)
                    txs_to_create = []

                    for p_tx in p_transactions:
                        tx_desc = (p_tx.get('description') or 'Transação Open Finance')[:255]
                        raw_amount = abs(float(p_tx.get('amount', 0)))
                        tx_amount = Decimal(str(raw_amount))
                        tx_type_str = p_tx.get('type', 'DEBIT')
                        pluggy_cat = p_tx.get('category') or ''

                        # Date parsing
                        raw_date = p_tx.get('date')
                        if raw_date:
                            try:
                                tx_date = datetime.strptime(raw_date[:10], '%Y-%m-%d').date()
                            except Exception:
                                tx_date = date.today()
                        else:
                            tx_date = date.today()

                        tx_key = (tx_date, tx_amount, tx_desc)
                        if tx_key in existing_txs:
                            continue
                        user_name = (user.profile.full_name or user.get_full_name() or '')
                        django_tx_type, cat_name, cat_color = categorize_pluggy_transaction(
                            tx_desc=tx_desc,
                            pluggy_cat=pluggy_cat,
                            tx_type_str=tx_type_str,
                            amount_val=float(p_tx.get('amount', 0)),
                            user_name=user_name
                        )

                        cat_lookup = cat_name[:50].strip().lower()
                        category = user_categories.get(cat_lookup)
                        if not category:
                            category = Category.objects.create(
                                user=user,
                                name=cat_name[:50],
                                category_type=django_tx_type,
                                color=cat_color
                            )
                            user_categories[cat_lookup] = category

                        txs_to_create.append(Transaction(
                            account=account,
                            category=category,
                            transaction_type=django_tx_type,
                            amount=tx_amount,
                            transaction_date=tx_date,
                            description=tx_desc
                        ))
                        existing_txs.add(tx_key)

                    if txs_to_create:
                        Transaction.objects.bulk_create(txs_to_create)
                        transactions_synced += len(txs_to_create)

            # 2. Fetch & Sync Investments for this item
            pluggy_investments = self.fetch_investments_for_item(item_id)
            if pluggy_investments:
                total_inv_balance = Decimal('0.00')
                active_count = 0

                for inv in pluggy_investments:
                    status = (inv.get('status') or '').upper()
                    raw_bal = inv.get('balance')
                    if raw_bal is None:
                        raw_bal = inv.get('value', 0)
                    bal = Decimal(str(raw_bal or 0))
                    # Only include ACTIVE positions with positive balance
                    if status == 'ACTIVE' and bal > 0:
                        total_inv_balance += bal
                        active_count += 1

                # Update any previous generic "Banco Conectado" investment for this item
                if main_bank_name != 'Banco Conectado':
                    Account.objects.filter(
                        user=user,
                        pluggy_item_id=item_id,
                        name__startswith='Banco Conectado'
                    ).update(
                        name=f'{main_bank_name} - Investimentos',
                        bank_name=main_bank_name,
                        logo_url=connector_logo
                    )

                if active_count > 0 or total_inv_balance > 0:
                    inv_name = f'{main_bank_name} - Investimentos'
                    inv_acc = Account.objects.filter(user=user, name=inv_name).first()
                    if not inv_acc:
                        inv_acc = Account.objects.filter(user=user, pluggy_item_id=item_id, account_type='INVESTMENT').first()

                    if not inv_acc:
                        inv_acc = Account.objects.create(
                            user=user,
                            name=inv_name,
                            bank_name=main_bank_name,
                            account_type='INVESTMENT',
                            balance=total_inv_balance,
                            is_active=True,
                            pluggy_item_id=item_id,
                            logo_url=connector_logo
                        )
                    else:
                        inv_acc.name = inv_name
                        inv_acc.balance = total_inv_balance
                        inv_acc.account_type = 'INVESTMENT'
                        inv_acc.bank_name = main_bank_name
                        inv_acc.pluggy_item_id = item_id
                        if connector_logo:
                            inv_acc.logo_url = connector_logo
                        inv_acc.save(update_fields=['name', 'balance', 'account_type', 'bank_name', 'pluggy_item_id', 'logo_url', 'updated_at'])

                    investments_synced += 1
                else:
                    inv_name = f'{main_bank_name} - Investimentos'
                    inv_acc = Account.objects.filter(user=user, name=inv_name).first()
                    if inv_acc:
                        inv_acc.balance = Decimal('0.00')
                        inv_acc.save(update_fields=['balance'])



        # Update profile last sync time
        user.profile.pluggy_last_sync = timezone.now()
        user.profile.save(update_fields=['pluggy_last_sync'])

        msg_parts = [f'{accounts_synced} contas', f'{transactions_synced} movimentações']
        if investments_synced > 0:
            msg_parts.append(f'{investments_synced} carteiras de investimentos')

        return {
            'success': True,
            'accounts_synced': accounts_synced,
            'transactions_synced': transactions_synced,
            'investments_synced': investments_synced,
            'message': f'Sincronização realizada com sucesso! {", ".join(msg_parts)} atualizadas.'
        }
