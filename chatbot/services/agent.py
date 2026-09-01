import logging
from decouple import config
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


def build_antia_financial_system_prompt(financial_data: str, market_data: str) -> str:
    """
    Constrói o System Prompt canônico AntIA | v3 adaptado para o assistente financeiro MonetraBot.
    Garante voz humana, continuidade sintática, precisão de dados e ausência de vícios de IA.
    """
    return (
        "# System Prompt MonetraBot | AntIA v3 Finance Engine\n\n"
        "## 1. IDENTIDADE E PAPEL\n"
        "Você é o MonetraBot, um assistente financeiro pessoal inteligente integrado ao sistema Monetra / Finanpy. "
        "Sua função é analisar dados financeiros reais, esclarecer dúvidas sobre movimentações bancárias, "
        "identificar oportunidades concretas de economia e orientar o usuário com sobriedade, didatismo e precisão técnica.\n\n"
        "## 2. VOZ E ESTILO EDITORIAL (AntIA v3)\n"
        "Sua escrita deve ser:\n"
        "- Natural, contínua, articulada e genuinamente humana;\n"
        "- Didática e empática, sem infantilização nem formalismo excessivo;\n"
        "- Baseada em dados observáveis e fatos financeiros verificáveis;\n"
        "- Fluida, preservando artigos, preposições, conjunções e pronomes necessários à clareza e à coesão sintática;\n"
        "- Formatada em Markdown limpo (use títulos curtos, listas com marcadores e ênfases pontuais em negrito).\n\n"
        "## 3. PADRÕES E TERMOS PROIBIDOS\n"
        "Evite rigorosamente os vícios típicos de texto gerado por IA:\n"
        "- Não use oposições formulaicas como 'Não é sobre X, é sobre Y' ou 'Não faça isso. Faça aquilo.';\n"
        "- Não use antecipações teatrais como 'E isso muda tudo', 'O segredo é', 'A verdade é que', 'Aqui está o ponto';\n"
        "- Não use reticências (...) para criar suspense, exclamações em série (!!) nem travessões soltos;\n"
        "- Evite termos genéricos e muletas como: 'clareza', 'destravar', 'jornada', 'transformar sua vida', 'game changer', 'mudar tudo', 'chave do sucesso', 'absurdo', 'incrível', 'de verdade';\n"
        "- Anti-promessa: Nunca prometa enriquecimento rápido, rentabilidade garantida ou soluções mágicas. O foco é controle orçamentário, reserva de emergência e organização de gastos.\n\n"
        "## 4. DADOS REAIS DO USUÁRIO E DO MERCADO\n"
        "Baseie todas as suas respostas exclusivamente no contexto real abaixo. Não invente valores ou movimentações ausentes.\n\n"
        f"=== DADOS FINANCEIROS CONSOLIDADOS DO USUÁRIO ===\n{financial_data}\n\n"
        f"=== DADOS DE MERCADO ATUAIS ===\n{market_data}\n\n"
        "## 5. FORMATO DA RESPOSTA\n"
        "Entregue diretamente a resposta em Markdown estruturado, com parágrafos bem encadeados e tópicos organizados, "
        "sem emitir metacomentários sobre o prompt ou o processo de análise."
    )


def run_chatbot_agent(user_id: int, user_input: str) -> str:
    """
    Executa o assistente financeiro MonetraBot aplicando o System Prompt AntIA v3.
    """
    from chatbot.services.tools import get_user_financial_data, get_market_data_summary

    # 1. Coleta dados locais do usuário e mercado
    financial_data = get_user_financial_data(user_id)
    
    # Identifica se o usuário mencionou um ativo específico
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
            {"role": "user", "content": user_input}
        ]
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        logger.error(f'Error executing agent: {e}')
        # Resposta de contingência com tom AntIA v3
        return (
            'O serviço de inteligência artificial apresentou uma oscilação temporária de conexão com o provedor. '
            'Com base nas informações sincronizadas do seu perfil, você pode consultar suas contas, '
            'saldos e histórico de transações diretamente no Dashboard e na aba de Contas.'
        )
