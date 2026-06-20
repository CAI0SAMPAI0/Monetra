import logging
from decouple import config
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

logger = logging.getLogger(__name__)


def run_financial_agent(user_id: int, prompt_input: str) -> str:
    """
    Executa o agente financeiro do Langchain para análises em lote/dashboard.
    Usa um único prompt estruturado com contexto pré-carregado para evitar limites de taxa (429) e timeouts.
    """
    from chatbot.services.tools import get_user_financial_data, get_market_data_summary

    # Coleta dados locais
    financial_data = get_user_financial_data(user_id)
    market_data = get_market_data_summary()

    # Groq API configuration using ChatOpenAI
    api_key = config('GROQ_API_KEY', default='')
    if not api_key:
        logger.error('GROQ_API_KEY is not defined in .env')
        return 'Erro: GROQ_API_KEY não configurada no arquivo de ambiente.'

    # ChatOpenAI configuration pointing to Groq's endpoint
    llm = ChatOpenAI(
        model='llama-3.1-8b-instant',
        base_url='https://api.groq.com/openai/v1',
        api_key=api_key,
        temperature=0.4,
        max_tokens=1500,
        max_retries=2,
    )

    system_instruction = (
        "Você é o FynanBot, um consultor financeiro pessoal de inteligência artificial especializado do sistema Finanpy.\n"
        "Você é extremamente amigável, prestativo, educado e profissional. Sua tarefa é fazer uma análise da saúde financeira do usuário baseando-se nos dados fornecidos.\n\n"
        f"=== DADOS FINANCEIROS DO USUÁRIO ===\n{financial_data}\n\n"
        f"=== DADOS DE MERCADO ATUAIS ===\n{market_data}\n\n"
        "Instruções:\n"
        "- Identifique padrões de consumo, áreas de desperdício e forneça 3 dicas práticas e empáticas em Português do Brasil.\n"
        "- Seja empático e encorajador.\n"
        "- Não invente dados."
    )

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
            'Olá! Identifiquei uma instabilidade ao conectar com meu cérebro de IA da Groq. '
            'Com base em seus registros locais de contas e transações, recomendamos continuar '
            'gerenciando seu saldo com disciplina e evitar despesas não-essenciais.'
        )

