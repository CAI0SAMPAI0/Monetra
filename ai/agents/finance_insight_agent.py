import logging
from decouple import config
from openai import OpenAI
from chatbot.services.agent import build_antia_financial_system_prompt

logger = logging.getLogger(__name__)


def run_financial_agent(user_id: int, prompt_input: str) -> str:
    """
    Executa o agente financeiro para análises e resumos aplicando a diretriz AntIA v3.
    Utiliza DeepSeek-V4.1-Flash via Hugging Face Router.
    """
    from chatbot.services.tools import get_user_financial_data, get_market_data_summary

    financial_data = get_user_financial_data(user_id)
    market_data = get_market_data_summary()

    api_key = config('HF_TOKEN_SEEK', default=config('HF_TOKEN', default=''))
    if not api_key:
        logger.error('HF_TOKEN_SEEK is not defined in .env')
        return 'Erro: HF_TOKEN_SEEK não configurada no arquivo de ambiente.'

    client = OpenAI(
        base_url='https://router.huggingface.co/v1',
        api_key=api_key,
        timeout=60.0,
    )

    system_instruction = build_antia_financial_system_prompt(financial_data, market_data)

    try:
        messages = [
            {'role': 'system', 'content': system_instruction},
            {'role': 'user', 'content': prompt_input}
        ]
        completion = client.chat.completions.create(
            model='deepseek-ai/DeepSeek-V4.1-Flash:novita',
            messages=messages,
            temperature=0.35,
            max_tokens=4000,
        )
        msg = completion.choices[0].message
        content = msg.content or ''
        if not content.strip():
            content = (
                'Resumo financeiro gerado com base nas contas e transações cadastradas. '
                'Consulte o painel principal para ver o detalhamento dos saldos.'
            )
        return content
    except Exception as e:
        logger.error(f'Error executing agent: {e}')
        return (
            'O serviço de análise automática está temporariamente indisponível para conexão externa. '
            'Seus registros locais permanecem salvos e você pode acompanhar os saldos e transações no painel principal.'
        )
