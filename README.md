---
title: Monetra
emoji: 💰
colorFrom: green
colorTo: blue
sdk: docker
app_port: 8000
pinned: false
---


# Monetra (Finanpy) - Gestão de Finanças Pessoais

Monetra (Finanpy) é um sistema completo e moderno de gestão de finanças pessoais desenvolvido com **Python 3.12+** e **Django 6+**. Ele permite aos usuários gerenciar múltiplas contas bancárias, categorizar receitas e despesas, acompanhar sua saúde financeira por meio de um dashboard interativo, e obter insights personalizados gerados por Inteligência Artificial (Langchain 1.0 + Groq API).

---

## 🚀 Principais Funcionalidades

- **Dashboard Financeiro**: Resumo consolidado de saldos, receitas e despesas do mês corrente, histórico de transações e gráficos interativos de gastos por categoria.
- **Gestão de Contas Bancárias**: CRUD de contas bancárias (Conta Corrente, Poupança, Carteira).
- **Categorias Personalizadas**: Categorização inteligente de receitas e despesas com cores customizadas e suporte a categorias padrão automáticas para novos usuários.
- **Registro de Transações**: Lançamento de receitas e despesas com atualização automática e segura do saldo das contas (proteção por signals).
- **Agente de Insights Financeiros**: Um job em lote que analisa o padrão de consumo do usuário e gera conselhos práticos e diretos em português (Brasil).
- **MonetraBot (Chatbot Interativo)**: Chatbot interativo no sistema que permite ao usuário conversar em tempo real sobre suas finanças, combinando dados locais com cotações de mercado reais (AwesomeAPI).

---

## 🛠️ Stack Tecnológica

- **Backend**: Python 3.12+ | Django 6+ | Gunicorn (Servidor WSGI)
- **Frontend**: Django Template Language | Tailwind CSS (Compilado nativamente com Node.js)
- **Banco de Dados**: Neon PostgreSQL (produção e desenvolvimento local)
- **Integração de IA**: Langchain 1.0 (via `langchain_classic`) | Groq API (`llama-3.3-70b-versatile`)
- **Containerização**: Docker & Docker Compose
- **Integração Contínua**: GitHub Actions (Linting, Pytest com DB real Postgres, Docker Build validation)

---

## 📦 Como Executar o Projeto

Você pode rodar a aplicação localmente de duas formas: usando Docker Compose (recomendado) ou configurando o ambiente Python nativo.

### Opção A: Usando Docker Compose (Recomendado)

O Docker Compose inicializa um banco de dados PostgreSQL local e o container da aplicação Django de forma totalmente automatizada.

1. **Clone o repositório e acesse a pasta**:
   ```bash
   git clone https://github.com/CAI0SAMPAI0/Monetra.git
   cd Monetra
   ```

2. **Crie o arquivo `.env` na raiz do projeto** e preencha as variáveis de ambiente necessárias:
   ```env
   SECRET_KEY=sua_chave_secreta_django
   DEBUG=True
   GROQ_API_KEY=sua_chave_da_groq_aqui
   # Se quiser usar o banco do Neon no docker, preencha NEON_POSTGRESQL.
   # Caso contrário, o Docker usará o PostgreSQL local (db) por padrão.
   ```

3. **Inicie os containers**:
   ```bash
   docker-compose up --build
   ```

4. A aplicação estará disponível em `http://localhost:8000/`.

---

### Opção B: Configuração Local Nativa

1. **Crie e ative o ambiente virtual**:
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Instale as dependências de desenvolvimento**:
   ```bash
   pip install -r requirements/development.txt
   ```

3. **Instale dependências do Tailwind e compile o CSS**:
   Certifique-se de ter o Node.js instalado.
   ```bash
   python manage.py tailwind install
   python manage.py tailwind build
   ```

4. **Execute as migrações e rode o servidor**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## 🧪 Rodando Testes e Validações

O projeto possui uma suíte robusta com **57 testes automatizados** e cobertura completa.

Para rodar os testes localmente:
```bash
pytest
```

Para gerar relatório de cobertura (Coverage):
```bash
pytest --cov=. --cov-report=html
# Abra htmlcov/index.html no navegador para verificar a cobertura.
```

---

## 📈 Comandos Úteis de Gerenciamento

- **Executar Análise de IA em Batch**:
  Gera novos insights baseados nos dados financeiros para todos os usuários do sistema.
  ```bash
  python manage.py run_finance_analysis
  ```
  *(Opcional) Executar para um usuário específico:*
  ```bash
  python manage.py run_finance_analysis --user_id <ID>
  ```

- **Criar Administrador (Superuser)**:
  ```bash
  python manage.py createsuperuser
  ```

---

## 📖 Documentação Detalhada

A documentação interna detalhada do projeto está localizada na pasta `/docs`:

- [Estrutura da Arquitetura](file:///C:/Users/caio/Documents/GitHub/fynanpy/docs/architecture.md)
- [Modelagem de Dados](file:///C:/Users/caio/Documents/GitHub/fynanpy/docs/data-models.md)
- [Padrões de Código](file:///C:/Users/caio/Documents/GitHub/fynanpy/docs/coding-standards.md)
- [Design System & Interface](file:///C:/Users/caio/Documents/GitHub/fynanpy/docs/design-system.md)
- [Guia de Segurança](file:///C:/Users/caio/Documents/GitHub/fynanpy/docs/security.md)
- [Agente Financeiro de IA](file:///C:/Users/caio/Documents/GitHub/fynanpy/docs/ai-finance-agent.md)
- [Guia de Deploy](file:///C:/Users/caio/Documents/GitHub/fynanpy/docs/DEPLOY.md)
- [Setup de Desenvolvimento](file:///C:/Users/caio/Documents/GitHub/fynanpy/docs/setup.md)
