# Documentação Finanpy

Bem-vindo à documentação do Finanpy, um sistema de gestão de finanças pessoais desenvolvido com Django.

## Índice da Documentação

### 1. [Arquitetura do Projeto](./architecture.md)
Entenda a estrutura do projeto, organização de apps Django e decisões arquiteturais.

### 2. [Padrões de Código](./coding-standards.md)
Guidelines e convenções de código que devem ser seguidas no desenvolvimento.

### 3. [Design System](./design-system.md)
Paleta de cores, tipografia, componentes e padrões visuais do projeto.

### 4. [Modelos de Dados](./data-models.md)
Estrutura dos models Django e relacionamentos entre entidades.

### 5. [Setup e Desenvolvimento](./setup.md)
Instruções para configurar o ambiente e iniciar o desenvolvimento.

### 6. [Segurança](./security.md)
Instruções de segurança da aplicação.

### 7. [Agente de IA Financeiro](./ai-finance-agent.md)
Funcionamento do agente de IA financeiro, fluxo de análise, integração e comandos.

### 8. [Guia de Deploy](./DEPLOY.md)
Instruções para implantar a aplicação em produção.

### 9. [Setup de Desenvolvimento](./setup.md)
Guia passo a passo para configuração local nativa e via Docker.

---

## Visão Geral do Projeto

O Finanpy é um sistema de gestão de finanças pessoais que permite:
- Gerenciar múltiplas contas bancárias
- Categorizar transações financeiras
- Visualizar entradas e saídas
- Acompanhar saldo e balanço através de um dashboard interativo
- Obter insights gerados por IA e conversar com o MonetraBot

### Stack Tecnológica

- **Backend**: Python 3.12+ e Django 6+
- **Frontend**: Django Template Language + TailwindCSS
- **Banco de Dados**: Neon PostgreSQL
- **Integração de IA**: Langchain 1.0 e Groq API
- **Autenticação**: Django Auth (nativo)
- **Containerização**: Docker & Docker Compose

### Princípios do Projeto

- **Simplicidade**: Evitar over-engineering
- **Eficiência**: Código limpo e performático
- **Responsividade**: Interface adaptável para diferentes dispositivos
- **Segurança**: Proteção de dados e autenticação segura

---

Para mais detalhes, consulte o [PRD (Product Requirements Document)](../PRD.md) do projeto.