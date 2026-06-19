# Agente Especialista em Integração de IA (LangChain 1.0 & Django)

Este documento atua como uma referência técnica de engenharia (um "agente documental") para guiar a concepção, o desenvolvimento e a integração de agentes de Inteligência Artificial no ecossistema do Finanpy.

---

## 🧭 Diretrizes Gerais para Agentes com LangChain 1.0

O **LangChain 1.0** traz mudanças significativas na estrutura de importações, uso de runnables (LCEL - LangChain Expression Language) e definição de agentes. Ao criar agentes no Finanpy, siga as regras abaixo:

### 1. Importações Atualizadas
Evite caminhos legados de importação (`langchain.agents.*` ou `langchain.llms.*`). Utilize as bibliotecas de ecossistema dedicadas:
- Modelos de chat compatíveis com OpenAI: `from langchain_openai import ChatOpenAI`
- Estruturas de ferramentas: `from langchain_core.tools import tool`
- Prompts estruturados: `from langchain_core.prompts import ChatPromptTemplate`
- Orquestradores de agentes: `from langgraph.prebuilt import create_react_agent` ou `from langchain.agents import create_react_agent`

### 2. Definição Limpa de Tools (Ferramentas)
Ferramentas devem ser decoradas com `@tool` e possuir **docstrings claras**. O LLM utiliza a docstring da função para decidir quando e como chamar a ferramenta.

```python
from langchain_core.tools import tool

@tool
def query_user_balance(user_id: int) -> float:
    """
    Consulta o saldo consolidado de todas as contas do usuário logado.
    Use esta tool sempre que o usuário perguntar o saldo atual ou precisar calcular capacidade de gastos.
    """
    # Lógica de integração com o Django ORM
    ...
```

---

## ⚡ Padrões de Integração com Django

Integrar agentes de IA em um framework síncrono como o Django requer cuidados arquiteturais específicos para evitar gargalos de performance e manter a segurança de dados.

### 1. Isolamento de Contexto do Banco (Segurança Crucial)
O agente **nunca** deve ter acesso livre para executar raw queries SQL (`SELECT * FROM ...`) ou acessar dados gerais sem filtros por usuário.
- Cada tool deve receber explicitamente o `user_id` ou o objeto `user` autenticado.
- No escopo interno da tool, filtre rigorosamente os dados utilizando o Django ORM:
  `Account.objects.filter(user_id=user_id)`

### 2. Conversão de Modelos Django para Formatos Prontos para IA
Modelos complexos do Django possuem referências circulares e campos que geram queries adicionais (N+1). Sempre converta os dados obtidos no ORM em formatos serializáveis simples (dicionários, strings formatadas ou JSON) antes de retorná-los para a tool do LangChain.

```python
# Exemplo de conversão de dados do ORM para o agente
transactions = Transaction.objects.filter(account__user_id=user_id)[:30]
data_summary = [
    f"Data: {t.transaction_date} | Tipo: {t.transaction_type} | Valor: R${t.amount} | Categ: {t.category.name}"
    for t in transactions
]
return "\n".join(data_summary)
```

### 3. Tratamento de Transações do Banco de Dados
Evite que tools executem escritas diretas no banco que possam deixar o estado inconsistente. Quando for necessário alterar o estado do banco (ex: salvar análise), isole a escrita na camada de serviço (`services/`), fora do controle direto da execução autônoma do agente.

---

## 🌐 Uso do MCP Server do Context7 para Documentação Atualizada

> [!IMPORTANT]
> A API do LangChain e as bibliotecas parceiras (como LangGraph) evoluem com frequência. Sempre utilize o **MCP Server do Context7** para buscar as especificações mais recentes das APIs e evitar deprecations.

### Como o agente de desenvolvimento deve interagir com o MCP:
1. Ao planejar modificações no agente ou nas chains, invoque ferramentas de busca do MCP informando que deseja consultar a documentação oficial da versão `langchain 1.0` ou `langgraph`.
2. Questione especificamente sobre a sintaxe de:
   - `create_react_agent`
   - `AgentExecutor`
   - Uso de `MessagesPlaceholder` para controle de histórico.

---

## 📋 Exemplo Prático: Fluxo Básico de Criação de um Agente

Abaixo está o modelo recomendado de implementação de um agente de insights financeiros integrado ao Django.

```python
# ai/agents/finance_insight_agent.py
import logging
from decouple import config
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_react_agent

logger = logging.getLogger(__name__)

# 1. Definição das Tools
@tool
def get_user_accounts_summary(user_id: int) -> str:
    """
    Retorna uma string contendo as contas ativas do usuário e seus respectivos saldos.
    Use para responder perguntas sobre saldo global ou individual.
    """
    from accounts.models import Account
    try:
        accounts = Account.objects.filter(user_id=user_id, is_active=True)
        if not accounts.exists():
            return "O usuário não possui contas cadastradas."
        
        lines = [f"- {acc.name} ({acc.bank_name}): R$ {acc.balance}" for acc in accounts]
        return "\n".join(lines)
    except Exception as e:
        logger.error(f"Erro ao buscar contas: {e}")
        return "Erro ao processar a solicitação de contas."

# 2. Inicialização do LLM compatível com Groq / OpenAI
def get_llm():
    # Detecta qual provedor está configurado
    if config('GROQ_API_KEY', default=''):
        return ChatOpenAI(
            model='llama-3.3-70b-versatile',
            base_url=config('GROQ_BASE_URL', default='https://api.groq.com/openai/v1'),
            api_key=config('GROQ_API_KEY'),
            temperature=0.7,
        )
    return ChatOpenAI(
        model='gpt-4o-mini',  # Fallback OpenAI
        api_key=config('OPENAI_API_KEY'),
        temperature=0.5,
    )

# 3. Orquestração do Agente
def run_financial_agent(user_id: int, prompt_input: str) -> str:
    llm = get_llm()
    tools = [get_user_accounts_summary]
    
    # Template do System Prompt em Português
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Você é o FynanBot, um assistente de finanças pessoais do Finanpy. "
                   "Ajude o usuário com base nos dados reais fornecidos pelas tools. "
                   "Sempre responda em português do Brasil de forma empática e prática. "
                   "ID do usuário sob análise: {user_id}."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Criar o agente LangChain (padrão ReAct)
    # Nota: Em LangChain 1.0, prefira o create_react_agent com prompt estruturado
    agent = create_react_agent(llm, tools, prompt_template)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    response = executor.invoke({
        "input": prompt_input,
        "user_id": user_id,
        "agent_scratchpad": []
    })
    
    return response.get("output", "Não foi possível gerar uma resposta.")
```

---

## 📈 Boas Práticas e Governança
- **Temperatura (Temperature)**: Use `0.2` a `0.5` para análises financeiras que exigem consistência matemática. Use `0.7` apenas se precisar de mais variedade na redação dos textos.
- **Tratamento de Exceções**: Toda tool que acessa banco ou APIs externas deve estar envolvida em blocos `try/except` para impedir falhas catastróficas na execução em lote.
- **Auditoria de Custo**: Mantenha logs da quantidade de tokens consumidos em cada chamada (`cb` do LangChain / `get_openai_callback`) para fins de telemetria e projeção de custos.
