import logging
from decouple import config
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

logger = logging.getLogger(__name__)


def run_chatbot_agent(user_id: int, user_input: str) -> str:
    """
    Executa o agente financeiro do chatbot com Langchain 1.0 e Groq (llama-3.1-8b-instant).
    Usa tools closure-bound para garantir isolamento absoluto do usuário.
    """
    from chatbot.services.tools import get_user_financial_data, get_market_data_summary
    from langchain_core.tools import tool

    @tool
    def get_my_financial_data() -> str:
        """
        Use esta ferramenta para obter todas as informações sobre as suas contas, saldos, categorias e histórico de transações recentes.
        Não requer parâmetros.
        """
        return get_user_financial_data(user_id)

    @tool("get_my_financial_data()")
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

    @tool("get_financial_market_data()")
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
        model='llama-3.1-8b-instant',
        base_url='https://api.groq.com/openai/v1',
        api_key=api_key,
        temperature=0.4,
        max_tokens=1500,
    )

    template = """Você é o MonetraBot, um assistente financeiro pessoal de inteligência artificial do sistema Monetra/Finanpy.
Você é extremamente amigável, prestativo, educado e profissional. Suas análises devem ser baseadas nos dados do usuário e do mercado.

Você tem acesso às seguintes ferramentas (tools):

{tools}

Use o seguinte formato de raciocínio estrito:

Question: a pergunta ou solicitação que você deve responder
Thought: você deve sempre pensar sobre o que fazer e quais ferramentas usar. Sempre escreva "Thought:" no início de cada linha de pensamento.
Action: a ação a tomar, deve ser uma de [{tool_names}]
Action Input: a entrada para a ação
Observation: o resultado da ação
... (este raciocínio de Thought/Action/Action Input/Observation pode se repetir no máximo 3 vezes)
Thought: Eu agora sei a resposta final
Final Answer: a resposta final e detalhada em Português do Brasil para o usuário, contendo dicas e insights úteis baseados nos dados.

Instruções cruciais de formatação:
1. Sempre use uma das ferramentas acima para coletar dados reais antes de dar a resposta final se o usuário perguntar sobre o saldo dele, transações, contas ou cotações de mercado.
2. Cada linha com "Thought:" deve ser seguida imediatamente por uma "Action:" e "Action Input:", OU por uma "Thought: Eu agora sei a resposta final" e depois "Final Answer:". Nunca pule passos.
3. Nunca retorne termos técnicos como "Thought:", "Action:", "Action Input:" ou "Observation:" na resposta final (Final Answer). A resposta final deve ser um texto limpo, empático e amigável direcionado ao usuário em Português (Brasil).
4. Ao preencher o campo "Action:", use exatamente o nome da ferramenta (ex: "get_my_financial_data"), NUNCA adicione parênteses "()" (ex: NÃO use "get_my_financial_data()").

Inicie!

Question: {input}
Thought:{agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template)

    # Build the ReAct agent
    agent = create_react_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    try:
        response = executor.invoke({
            'input': user_input,
            'agent_scratchpad': []
        })
        return response.get('output', 'Não foi possível obter uma resposta do assistente.')
    except Exception as e:
        logger.error(f'Error executing agent: {e}')
        # Fallback response complying with RNF024
        return (
            'Olá! Tive uma instabilidade temporária ao me conectar ao meu cérebro de IA (Groq). '
            'No entanto, analisando os dados locais do seu perfil, lembre-se de manter o controle '
            'das suas contas e registrar todas as suas receitas e despesas!'
        )
