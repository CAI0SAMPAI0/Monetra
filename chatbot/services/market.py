import logging
import time
import requests

logger = logging.getLogger(__name__)

# Simple in-memory cache configuration
_cache = {
    'data': None,
    'timestamp': 0
}
CACHE_TTL = 300  # 5 minutes in seconds


def fetch_realtime_market_data() -> dict:
    """
    Fetches real-time financial market data (currencies) and returns mock fallback data
    for stocks and real estate to ensure resilience. Uses in-memory caching to optimize performance.
    """
    current_time = time.time()
    if _cache['data'] and (current_time - _cache['timestamp'] < CACHE_TTL):
        logger.debug('Returning cached market data')
        return _cache['data'].copy()

    market_data = {
        'currencies': {
            'USD_BRL': 'R$ 5.45',
            'EUR_BRL': 'R$ 5.85',
        },
        'stocks': {
            'Ibovespa': '129.500 pts',
            'S&P_500': '5.430 pts',
            'NASDAQ': '17.700 pts',
        },
        'real_estate': {
            'Selic': '10.50% a.a.',
            'IPCA_12m': '3.93%',
            'IGP-M_12m': '0.96%',
        }
    }

    try:
        # AwesomeAPI - Free and open API for currency rates
        response = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL', timeout=3)
        if response.status_code == 200:
            data = response.json()
            market_data['currencies']['USD_BRL'] = f"R$ {float(data['USDBRL']['bid']):.2f}"
            market_data['currencies']['EUR_BRL'] = f"R$ {float(data['EURBRL']['bid']):.2f}"
            
            # Cache the successful response
            _cache['data'] = market_data.copy()
            _cache['timestamp'] = current_time
    except Exception as e:
        logger.warning(f"Failed to fetch real-time currencies from AwesomeAPI: {e}")
        # If API call fails but we have cached data, return cached data as fallback
        if _cache['data']:
            logger.info('Returning expired cached market data due to API failure')
            return _cache['data'].copy()

    return market_data


def search_market_asset(query: str) -> dict:
    """
    Pesquisa as cotações de uma criptomoeda, moeda ou ação específica.
    Integra com AwesomeAPI para câmbio/cryptos e Yahoo Finance para ações.
    """
    if not query:
        return {}

    query_clean = query.strip().lower()
    
    # Dicionário de mapeamento para AwesomeAPI (moedas e cryptos)
    currencies_map = {
        'bitcoin': 'BTC-BRL',
        'btc': 'BTC-BRL',
        'ethereum': 'ETH-BRL',
        'eth': 'ETH-BRL',
        'dolar': 'USD-BRL',
        'dólar': 'USD-BRL',
        'usd': 'USD-BRL',
        'euro': 'EUR-BRL',
        'eur': 'EUR-BRL',
        'libra': 'GBP-BRL',
        'gbp': 'GBP-BRL',
        'litecoin': 'LTC-BRL',
        'ltc': 'LTC-BRL',
        'dogecoin': 'DOGE-BRL',
        'doge': 'DOGE-BRL',
        'xrp': 'XRP-BRL',
    }

    # Dicionário de mapeamento de nomes comuns para ações (Yahoo Finance)
    stocks_map = {
        'petrobras': 'PETR4.SA',
        'petr4': 'PETR4.SA',
        'petr3': 'PETR3.SA',
        'vale': 'VALE3.SA',
        'vale3': 'VALE3.SA',
        'itau': 'ITUB4.SA',
        'itaú': 'ITUB4.SA',
        'itub4': 'ITUB4.SA',
        'bradesco': 'BBDC4.SA',
        'bbdc4': 'BBDC4.SA',
        'banco do brasil': 'BBAS3.SA',
        'bbas3': 'BBAS3.SA',
        'magalu': 'MGLU3.SA',
        'mglu3': 'MGLU3.SA',
        'weg': 'WEGE3.SA',
        'wege3': 'WEGE3.SA',
        'apple': 'AAPL',
        'aapl': 'AAPL',
        'microsoft': 'MSFT',
        'msft': 'MSFT',
        'google': 'GOOGL',
        'googl': 'GOOGL',
        'goog': 'GOOGL',
        'amazon': 'AMZN',
        'amzn': 'AMZN',
        'tesla': 'TSLA',
        'tsla': 'TSLA',
        'nvidia': 'NVDA',
        'nvda': 'NVDA',
    }

    # 1. Verificar se é moeda ou criptomoeda no AwesomeAPI
    awesome_symbol = None
    if query_clean in currencies_map:
        awesome_symbol = currencies_map[query_clean]
    elif query_clean.upper() in ['BTC', 'ETH', 'LTC', 'USD', 'EUR', 'GBP', 'DOGE', 'XRP']:
        awesome_symbol = f"{query_clean.upper()}-BRL"

    if awesome_symbol:
        try:
            # Substitui hífen para a resposta da AwesomeAPI (ex: BTC-BRL -> BTCBRL)
            api_key_symbol = awesome_symbol.replace('-', '')
            url = f"https://economia.awesomeapi.com.br/last/{awesome_symbol}"
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                asset_data = data[api_key_symbol]
                
                bid = float(asset_data['bid'])
                pct_change = float(asset_data['pctChange'])
                high = float(asset_data['high'])
                low = float(asset_data['low'])
                
                # Formatação de preços
                if 'BTC' in awesome_symbol:
                    price_str = f"R$ {bid:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                    high_str = f"R$ {high:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                    low_str = f"R$ {low:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                else:
                    price_str = f"R$ {bid:.2f}".replace('.', ',')
                    high_str = f"R$ {high:.2f}".replace('.', ',')
                    low_str = f"R$ {low:.2f}".replace('.', ',')

                return {
                    'name': asset_data['name'],
                    'symbol': awesome_symbol,
                    'price': price_str,
                    'variation': f"{pct_change:+.2f}%",
                    'high': high_str,
                    'low': low_str,
                    'source': 'AwesomeAPI'
                }
        except Exception as e:
            logger.warning(f"Error fetching specific asset from AwesomeAPI: {e}")

    # 2. Verificar se é ação no Yahoo Finance
    yahoo_symbol = None
    if query_clean in stocks_map:
        yahoo_symbol = stocks_map[query_clean]
    elif len(query_clean) >= 5 and query_clean[-1].isdigit() and query_clean[:4].isalpha():
        yahoo_symbol = f"{query_clean.upper()}.SA"
    elif query_clean.upper() in ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX']:
        yahoo_symbol = query_clean.upper()

    if yahoo_symbol:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=3)
            if response.status_code == 200:
                data = response.json()
                result = data['chart']['result'][0]
                meta = result['meta']
                
                price = meta['regularMarketPrice']
                prev_close = meta['chartPreviousClose']
                variation = ((price - prev_close) / prev_close) * 100 if prev_close else 0.0
                
                currency = meta.get('currency', 'USD')
                currency_symbol = 'R$' if currency == 'BRL' else '$'
                
                indicators = result.get('indicators', {})
                quote = indicators.get('quote', [{}])[0]
                highs = quote.get('high', [])
                lows = quote.get('low', [])
                
                highs_valid = [h for h in highs if h is not None]
                lows_valid = [l for l in lows if l is not None]
                
                high_val = max(highs_valid) if highs_valid else price
                low_val = min(lows_valid) if lows_valid else price

                return {
                    'name': f"Ação {yahoo_symbol}",
                    'symbol': yahoo_symbol,
                    'price': f"{currency_symbol} {price:.2f}".replace('.', ','),
                    'variation': f"{variation:+.2f}%",
                    'high': f"{currency_symbol} {high_val:.2f}".replace('.', ','),
                    'low': f"{currency_symbol} {low_val:.2f}".replace('.', ','),
                    'source': 'Yahoo Finance'
                }
        except Exception as e:
            logger.warning(f"Error fetching specific asset from Yahoo Finance: {e}")

    # Fallback se nada for encontrado ou APIs falharem
    mock_assets = {
        'bitcoin': ('Bitcoin (BTC)', 'BTC-BRL', 'R$ 348.500,00', '+1,45%', 'R$ 352.000,00', 'R$ 341.000,00'),
        'btc': ('Bitcoin (BTC)', 'BTC-BRL', 'R$ 348.500,00', '+1,45%', 'R$ 352.000,00', 'R$ 341.000,00'),
        'ethereum': ('Ethereum (ETH)', 'ETH-BRL', 'R$ 18.450,00', '-0,85%', 'R$ 18.900,00', 'R$ 18.100,00'),
        'eth': ('Ethereum (ETH)', 'ETH-BRL', 'R$ 18.450,00', '-0,85%', 'R$ 18.900,00', 'R$ 18.100,00'),
        'petr4': ('Petróleo Brasileiro S.A. (PETR4)', 'PETR4.SA', 'R$ 38,45', '+0,92%', 'R$ 38,90', 'R$ 37,80'),
        'vale3': ('Vale S.A. (VALE3)', 'VALE3.SA', 'R$ 62,30', '-1,15%', 'R$ 63,10', 'R$ 61,80'),
    }
    
    for key, val in mock_assets.items():
        if key in query_clean:
            return {
                'name': val[0],
                'symbol': val[1],
                'price': val[2],
                'variation': val[3],
                'high': val[4],
                'low': val[5],
                'source': 'Mock Engine'
            }

    return {
        'name': query.upper(),
        'symbol': query.upper(),
        'price': 'Indisponível',
        'variation': 'N/A',
        'high': 'N/A',
        'low': 'N/A',
        'source': 'None'
    }


