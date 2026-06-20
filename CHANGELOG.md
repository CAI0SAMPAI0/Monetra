# Changelog

Todos os marcos importantes e alterações do projeto Monetra (Finanpy) serão documentados neste arquivo.

---

## [1.2.0] - 2026-06-19
### Adicionado
- **Conteinerização com Docker**: Criado o `Dockerfile` de produção otimizado com multi-stage build (copiando assets estáticos compilados na imagem base do Node).
- **Docker Compose**: Criado `docker-compose.yml` para orquestração local, provisionando o banco PostgreSQL local de forma automática e integrada à aplicação Django com health checks.
- **Pipeline de CI/CD**: Criado arquivo de workflow GitHub Actions em `.github/workflows/ci.yml` cobrindo jobs de:
  - Linting (`flake8`)
  - Testes Unitários e de Integração (`pytest` utilizando banco de dados Postgres ativo em container de teste no GitHub Actions)
  - Docker Build Validation (verificação automatizada do build do Dockerfile)
- **Documentação de Implantação**: Atualização do guia `docs/setup.md`, `docs/README.md` e criação do `README.md` principal do repositório cobrindo as instruções de Docker e Docker Compose.
- **Análise de Ativos Customizados**: Atualização da tool `get_financial_market_data` para aceitar um parâmetro opcional de pesquisa. Permite consultar e analisar dinamicamente cotações em tempo real de criptomoedas (como Bitcoin/Ethereum pelo AwesomeAPI) e de ações (como Petrobras/Vale/Apple pelo Yahoo Finance) de acordo com o pedido do usuário.

### Corrigido
- **Latência do Chatbot**: Implementado cache em memória (5 min TTL) para as consultas de cotações em tempo real da AwesomeAPI, eliminando chamadas HTTP bloqueantes redundantes.
- **Formatação ReAct**: Otimização do prompt do agente para reduzir a ocorrência de erros de parser ("Invalid Format: Missing Action") do Langchain.
- **Sincronização AJAX do Chat**: Adicionado o envio do snapshot do mercado financeiro no payload JSON para evitar perda de dados no painel lateral do chat.
- **Sanitização Segura**: Ajuste no front-end (`escapeHTML`) para prevenir falhas de JavaScript no tratamento de retornos vazios ou indefinidos.

---

## [1.1.0] - 2026-06-19
### Adicionado
- **Migração Neon PostgreSQL**: Migração completa de todos os dados do banco local SQLite para a nuvem através da integração do Neon PostgreSQL com o parsing dinâmico de `dj-database-url`.
- **MonetraBot (Chatbot de Finanças)**: Criação da app `chatbot` que disponibiliza um assistente em tempo real usando Langchain 1.0 e Groq API (`llama-3.1-8b-instant`).
  - **Tools Dinâmicas**: Criação de ferramentas com isolamento de contexto do usuário (`get_my_financial_data`) para segurança total de dados.
  - **Cotações em Tempo Real**: Tool `get_financial_market_data` buscando moedas em tempo real pela AwesomeAPI.
  - **Interface Glassmorphism**: Chat de conversação com estilização escura sofisticada combinando com a identidade visual da Landing Page.
  - **Armazenamento de Diálogos**: Histórico de mensagens do chat persistido no banco de dados Neon PostgreSQL na tabela `ChatbotAnalysis`.
- **Testes Automatizados**: Criação e verificação de **57 testes automatizados** integrados de Modelos, Views, Permissões, Sinais e Integração Geral cobrindo as novas camadas e regras de negócio.

---

## [1.0.0] - 2026-06-18
### Adicionado
- **Lote de IA (run_finance_analysis)**: Comando de gerenciamento para rodar análises em lote para todos os usuários (`python manage.py run_finance_analysis`).
- **Dashboard de Insights**: Painel de visualização com resumo dos insights criados pelo agente de IA.
- **Gestão Financeira Completa**:
  - Cadastro de usuários com login via email e criação automatizada de perfil.
  - CRUD de Contas Bancárias (Corrente, Poupança, Carteira).
  - CRUD de Categorias (Receitas/Despesas) com badges e cores customizadas.
  - CRUD de Transações (Receitas/Despesas) com recálculo automático de saldos via Django Signals.
- **Visualização**: Dashboard consolidado de finanças com integração do Chart.js para análise visual de gastos por categoria.
