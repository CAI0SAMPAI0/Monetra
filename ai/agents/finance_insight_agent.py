import logging
from decouple import config
from langchain_openai import ChatOpenAI
from chatbot.services.agent import build_antia_financial_system_prompt

logger = logging.getLogger(__name__)


def run_financial_agent(user_id: int, prompt_input: str) -> str:
    """
    Executa o agente financeiro para análises e resumos aplicando a diretriz AntIA v3.
    """
    from chatbot.services.tools import get_user_financial_data, get_market_data_summary

    financial_data = get_user_financial_data(user_id)
    market_data = get_market_data_summary()

    api_key = config('GROQ_API_KEY', default='')
    if not api_key:
        logger.error('GROQ_API_KEY is not defined in .env')
        return 'Erro: GROQ_API_KEY não configurada no arquivo de ambiente.'

    llm = ChatOpenAI(
        model='openai/gpt-oss-20b',
        base_url='https://api.groq.com/openai/v1',
        api_key=api_key,
        temperature=0.35,
        max_tokens=1500,
        max_retries=2,
    )

    system_instruction = build_antia_financial_system_prompt(financial_data, market_data)

    try:
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt_input}
        ]
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        logger.error(f'Error executing agent: {e}')
        return (
            'O serviço de análise automática está temporariamente indisponível para conexão externa. '
            'Seus registros locais permanecem salvos e você pode acompanhar os saldos e transações no painel principal.'
        )
