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

Para iniciar o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O sistema estará acessível em `http://127.0.0.1:8000/`.

## Comandos Úteis

- Criar um superusuário: `python manage.py createsuperuser`
- Criar novas migrações: `python manage.py makemigrations`
- Rodar testes: `python manage.py test`
