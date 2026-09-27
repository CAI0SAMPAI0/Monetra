import pytest
from profiles.services.pluggy_service import categorize_pluggy_transaction


def test_categorize_fii_purchase_as_investment_even_if_pluggy_says_shopping():
    django_type, cat_name, cat_color = categorize_pluggy_transaction(
        tx_desc='Compra FII MXRF11 NuInvest',
        pluggy_cat='Shopping',
        tx_type_str='DEBIT',
        amount_val=-150.00,
        user_name='Caio Sampaio'
    )
    assert django_type == 'INVESTMENT'
    assert 'FII' in cat_name or 'Investimentos' in cat_name
    assert cat_color == '#0284C7'


def test_categorize_tesouro_direto_as_investment():
    django_type, cat_name, cat_color = categorize_pluggy_transaction(
        tx_desc='Aplicação Tesouro Selic 2029',
        pluggy_cat='Investments',
        tx_type_str='DEBIT',
        amount_val=-500.00,
        user_name='Caio Sampaio'
    )
    assert django_type == 'INVESTMENT'


def test_categorize_stock_purchase_as_investment():
    django_type, cat_name, cat_color = categorize_pluggy_transaction(
        tx_desc='Compra B3 ACOES WEGE3',
        pluggy_cat='Shopping',
        tx_type_str='DEBIT',
        amount_val=-300.00,
        user_name='Caio Sampaio'
    )
    assert django_type == 'INVESTMENT'


def test_fetch_transactions_uses_date_from_and_no_pagesize(monkeypatch):
    from unittest.mock import MagicMock
    from profiles.services.pluggy_service import PluggyService
    import requests

    service = PluggyService(client_id='fake_id', client_secret='fake_secret')
    monkeypatch.setattr(service, 'get_headers', lambda: {'X-API-KEY': 'fake'})

    captured_calls = []

    def mock_get(url, headers=None, params=None, timeout=None):
        captured_calls.append({'url': url, 'params': params})
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {'results': [], 'next': None}
        return resp

    monkeypatch.setattr(requests, 'get', mock_get)

    res = service.fetch_transactions(
        account_id='11111111-1111-1111-1111-111111111111',
        from_date='2026-06-01'
    )
    assert len(captured_calls) == 1
    call_params = captured_calls[0]['params']
    assert 'pageSize' not in call_params
    assert 'from' not in call_params
    assert call_params.get('dateFrom') == '2026-06-01'
    assert call_params.get('accountId') == '11111111-1111-1111-1111-111111111111'

