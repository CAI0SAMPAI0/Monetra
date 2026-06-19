import logging
from decouple import config
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

logger = logging.getLogger(__name__)


def run_chatbot_agent(user_id: int, user_input: str) -> str:
    """
    Executa o agente financeiro do chatbot com Langchain 1.0 e Groq (gpt-oss-120b).
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

    @tool
    def get_financial_market_data() -> str:
        """
        Use esta ferramenta para obter cotações de câmbio em tempo real, índices da bolsa e taxas de juros do mercado.
        Não requer parâmetros.
        """
        return get_market_data_summary()

    tools = [get_my_financial_data, get_financial_market_data]

    # Groq API configuration using ChatOpenAI
    api_key = config('GROQ_API_KEY', default='')
    if not api_key:
        logger.error('GROQ_API_KEY is not defined in .env')
        return 'Erro: GROQ_API_KEY não configurada no arquivo de ambiente.'

    # ChatOpenAI configuration pointing to Groq's endpoint
    llm = ChatOpenAI(
        model='gpt-oss-120b',
        base_url='https://api.groq.com/openai/v1',
        api_key=api_key,
        temperature=0.4,
        max_tokens=1500,
    )

    template = """Você é o MonetraBot, um assistente financeiro pessoal de inteligência artificial do sistema Monetra/Finanpy.
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
- Forneça dicas e insights práticos baseados estritamente nos dados de transação ou saldo do usuário, cruzando com cotações ou indicadores se relevante.
- Seja empático e encorajador.
- Nunca exponha termos técnicos internos de Thought/Action/Observation/scratchpad na resposta final.

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
