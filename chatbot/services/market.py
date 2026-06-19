import logging
import requests

logger = logging.getLogger(__name__)


def fetch_realtime_market_data() -> dict:
    """
    Fetches real-time financial market data (currencies) and returns mock fallback data
    for stocks and real estate to ensure resilience.
    """
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
        response = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL', timeout=5)
        if response.status_code == 200:
            data = response.json()
            market_data['currencies']['USD_BRL'] = f"R$ {float(data['USDBRL']['bid']):.2f}"
            market_data['currencies']['EUR_BRL'] = f"R$ {float(data['EURBRL']['bid']):.2f}"
    except Exception as e:
        logger.warning(f"Failed to fetch real-time currencies from AwesomeAPI: {e}")

    return market_data
