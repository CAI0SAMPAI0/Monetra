import logging
from decouple import config
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

logger = logging.getLogger(__name__)


def run_financial_agent(user_id: int, prompt_input: str) -> str:
    """
    Executa o agente financeiro do Langchain para análises em lote/dashboard.
    Usa o modelo llama-3.3-70b-versatile na API da Groq.
    """
    from chatbot.services.tools import get_user_financial_data, get_market_data_summary
    from langchain_core.tools import tool

    @tool
    def get_my_financial_data() -> str:
        """
        Use esta ferramenta para obter todas as informações sobre as suas contas, saldos, categorias e histórico de transações recentes.
        """
        return get_user_financial_data(user_id)

    @tool(name="get_my_financial_data()")
    def get_my_financial_data_alias() -> str:
        """
        Alias para get_my_financial_data. Use esta ferramenta se preferir o formato com parênteses.
        """
        return get_user_financial_data(user_id)

    @tool
    def get_financial_market_data(query: str = None) -> str:
        """
        Use esta ferramenta para obter cotações do mercado financeiro em tempo real.
        Se nenhum parâmetro 'query' for fornecido, retorna o resumo geral do mercado (câmbio e índices).
        Se um parâmetro 'query' for fornecido (ex: 'Bitcoin', 'BTC', 'PETR4', 'AAPL', 'USD'),
        pesquisa especificamente o preço atual, variação e estatísticas desse ativo em tempo real.
        """
        return get_market_data_summary(query)

    @tool(name="get_financial_market_data()")
    def get_financial_market_data_alias(query: str = None) -> str:
        """
        Alias para get_financial_market_data. Use esta ferramenta se preferir o formato com parênteses.
        """
        return get_market_data_summary(query)

    tools = [
        get_my_financial_data,
        get_my_financial_data_alias,
        get_financial_market_data,
        get_financial_market_data_alias
    ]

    # Groq API configuration using ChatOpenAI
    api_key = config('GROQ_API_KEY', default='')
    if not api_key:
        logger.error('GROQ_API_KEY is not defined in .env')
        return 'Erro: GROQ_API_KEY não configurada no arquivo de ambiente.'

    # ChatOpenAI configuration pointing to Groq's endpoint
    llm = ChatOpenAI(
        model='llama-3.3-70b-versatile',
        base_url='https://api.groq.com/openai/v1',
        api_key=api_key,
        temperature=0.4,
        max_tokens=1500,
    )

    template = """Você é o FynanBot, um consultor financeiro pessoal de inteligência artificial especializado do sistema Finanpy.
Você é extremamente amigável, prestativo, educado e profissional. Suas análises devem ser baseadas nos dados do usuário e do mercado.

Você tem acesso às seguintes ferramentas (tools):

{tools}

Use o seguinte formato de raciocínio:

Question: a pergunta ou solicitação que você deve responder
Thought: você deve sempre pensar sobre o que fazer e quais ferramentas usar
Action: a ação a tomar, deve ser uma de [{tool_names}]
Action Input: a entrada para a ação
Observation: o resultado da ação
... (este pensamento/ação/entrada/observação pode se repetir conforme necessário)
Thought: Eu agora sei a resposta final
Final Answer: a resposta final e detalhada em Português do Brasil para o usuário, incluindo dicas e insights de forma empática e prática.

Atenção:
- Ao escrever o campo "Action:", use exatamente o nome da ferramenta (ex: "get_my_financial_data"), sem adicionar parênteses "()" (ex: NÃO use "get_my_financial_data()").
- Forneça dicas e insights práticos baseados estritamente nos dados de transação ou saldo do usuário, cruzando com cotações ou indicadores se relevante.
- Seja empático e encorajador.
- Nunca exponha termos técnicos de Thought/Action/Observation na resposta final.

Inicie!

Question: {input}
Thought:{agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template)

    # Build the ReAct agent
    agent = create_react_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    try:
        response = executor.invoke({
            'input': prompt_input,
            'agent_scratchpad': []
        })
        return response.get('output', 'Não foi possível obter uma análise do assistente.')
    except Exception as e:
        logger.error(f'Error executing agent: {e}')
        return (
            'Olá! Identifiquei uma instabilidade ao conectar com meu cérebro de IA da Groq. '
            'Com base em seus registros locais de contas e transações, recomendamos continuar '
            'gerenciando seu saldo com disciplina e evitar despesas não-essenciais.'
        )
