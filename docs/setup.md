# Guia de Configuração (Setup)

Siga os passos abaixo para configurar o ambiente de desenvolvimento local.

## Pré-requisitos

- Python 3.12 ou superior instalado.
- Gerenciador de pacotes `pip`.

## Instalação

1.  **Clone o repositório**:
    ```bash
    git clone <url-do-repositorio>
    cd finanpy
    ```

2.  **Crie e ative o ambiente virtual**:
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute as migrações do banco de dados**:
    ```bash
    python manage.py migrate
    ```

## Executando o Projeto

### Método 1: Usando Docker Compose (Recomendado)

O Docker Compose automatiza a criação do banco de dados PostgreSQL e a inicialização da aplicação em containers.

1.  **Certifique-se de que o Docker e Docker Compose estão instalados**.
2.  **Inicie os containers**:
    ```bash
    docker-compose up --build
    ```
3.  O sistema estará acessível em `http://localhost:8000/`.

### Método 2: Executando Localmente Nativamente

Para iniciar o servidor de desenvolvimento local (fora do Docker):

1.  **Inicie o servidor**:
    ```bash
    python manage.py runserver
    ```
2.  O sistema estará acessível em `http://127.0.0.1:8000/`.

## Comandos Úteis

-   **Criar um superusuário**: `python manage.py createsuperuser`
-   **Criar novas migrações**: `python manage.py makemigrations`
-   **Aplicar migrações**: `python manage.py migrate`
-   **Executar testes unitários**:
    ```bash
    pytest
    ```
-   **Executar testes com cobertura**:
    ```bash
    pytest --cov=. --cov-report=html
    ```
-   **Executar Análise de IA em lote**:
    ```bash
    python manage.py run_finance_analysis
    ```

