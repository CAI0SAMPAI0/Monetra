import logging
from decouple import config
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

logger = logging.getLogger(__name__)


def run_chatbot_agent(user_id: int, user_input: str) -> str:
    """
    Executa o agente financeiro do chatbot com Groq (llama-3.1-8b-instant).
    Usa um único prompt estruturado com contexto pré-carregado para evitar limites de taxa (429) e timeouts.
    """
    from chatbot.services.tools import get_user_financial_data, get_market_data_summary

    # 1. Coleta dados locais do usuário e mercado upfront
    financial_data = get_user_financial_data(user_id)
    
    # Tenta identificar se o usuário perguntou sobre um ativo específico
    asset_query = None
    user_words = user_input.lower().split()
    keywords = ['petr4', 'vale3', 'itub4', 'bbas3', 'mglu3', 'wege3', 'btc', 'bitcoin', 'eth', 'ethereum', 'usd', 'dolar', 'dólar', 'eur', 'euro']
    for word in user_words:
        word_clean = ''.join(c for c in word if c.isalnum())
        if word_clean in keywords:
            asset_query = word_clean
            break
            
    market_data = get_market_data_summary(asset_query)

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
        "Você é o MonetraBot, um assistente financeiro pessoal de inteligência artificial do sistema Monetra/Finanpy.\n"
        "Você é extremamente amigável, prestativo, educado e profissional. Suas análises devem ser baseadas nos dados do usuário e do mercado fornecidos abaixo.\n\n"
        f"=== DADOS FINANCEIROS DO USUÁRIO ===\n{financial_data}\n\n"
        f"=== DADOS DE MERCADO ATUAIS ===\n{market_data}\n\n"
        "Instruções cruciais:\n"
        "1. Dê dicas e insights práticos e empáticos baseados diretamente nos dados do usuário.\n"
        "2. Responda em Português do Brasil de forma limpa e objetiva, sem expor termos técnicos do prompt interno.\n"
        "3. Não invente dados que não estão presentes no contexto."
    )

    try:
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ]
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        logger.error(f'Error executing agent: {e}')
        # Fallback response complying with RNF024
        return (
            'Olá! Tive uma instabilidade temporária ao me conectar ao meu cérebro de IA (Groq). '
            'No entanto, analisando os dados locais do seu perfil, lembre-se de manter o controle '
            'das suas contas e registrar todas as suas receitas e despesas!'
        )

