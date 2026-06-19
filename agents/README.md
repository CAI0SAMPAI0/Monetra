# Time de Agentes IA - Finanpy

Este diretório contém as definições e instruções para os agentes de IA especializados que atuam no desenvolvimento do projeto Finanpy. Cada agente é um especialista na stack tecnológica definida e possui responsabilidades claras para garantir a qualidade e a consistência do código.

## Agentes Disponíveis

| Agente | Especialidade | Quando Usar |
| :--- | :--- | :--- |
| [**Backend Specialist**](backend.md) | Django, Python, SQLite | Criação de modelos, views, lógica de negócio e APIs. |
| [**Frontend Specialist**](frontend.md) | DTL, TailwindCSS, UX/UI | Criação de templates, estilização, responsividade e interface. |
| [**QA Specialist**](qa.md) | Playwright, Django Tests | Automação de testes, verificação de fluxos e validação de UI. |
| [**AI Integration Expert**](ai_integration_expert.md) | LangChain 1.0, LLMs, MCP | Diretrizes, ferramentas e padrões para integração de agentes de IA no Django. |

## Como Trabalhar com os Agentes

1.  **Contexto**: Sempre forneça o arquivo `GEMINI.md` e o `PRD.md` para situar o agente.
2.  **MCP Servers**:
    - Os agentes técnicos utilizam o server `context7` para garantir que o código siga as documentações mais recentes das bibliotecas.
    - O agente de QA utiliza o server `playwright` para interagir diretamente com a interface do sistema.
3.  **Sinergia**: O Backend cria a estrutura de dados, o Frontend consome essa estrutura nos templates, e o QA valida a entrega final.
