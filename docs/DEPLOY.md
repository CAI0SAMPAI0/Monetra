# Guia de Implantação (Deployment Guide)

Este documento descreve os passos necessários para realizar o deploy do Fynanpy em um ambiente de produção (ex: Heroku, Render, DigitalOcean).

## Pré-requisitos

- Python 3.12+
- Banco de dados (PostgreSQL recomendado)
- Variáveis de ambiente configuradas

## Variáveis de Ambiente Necessárias

As seguintes variáveis devem ser configuradas no ambiente de produção:

| Variável | Descrição | Exemplo |
| :--- | :--- | :--- |
| `SECRET_KEY` | Chave secreta do Django | `sua-chave-secreta-longa-e-aleatoria` |
| `DEBUG` | Deve ser `False` em produção | `False` |
| `ALLOWED_HOSTS` | Domínios permitidos | `fynanpy.herokuapp.com, fynanpy.com.br` |
| `DATABASE_URL` | URL de conexão com o banco de dados | `postgres://user:password@host:port/dbname` |
| `SECURE_SSL_REDIRECT` | Redirecionar HTTP para HTTPS | `True` |

## Checklist de Deploy

1. [ ] **Banco de Dados**: Certifique-se de que a `DATABASE_URL` está correta.
2. [ ] **Migrações**: Execute as migrações no servidor de produção:
   ```bash
   python manage.py migrate --settings=core.settings.production
   ```
3. [ ] **Arquivos Estáticos**: Colete os arquivos estáticos:
   ```bash
   python manage.py collectstatic --no-input --settings=core.settings.production
   ```
4. [ ] **Superusuário**: Crie um administrador inicial (se necessário):
   ```bash
   python manage.py createsuperuser --settings=core.settings.production
   ```
5. [ ] **Logs**: Verifique os logs do servidor para garantir que o Gunicorn iniciou corretamente.

## Comandos Úteis

### Rodando com Gunicorn manualmente
```bash
gunicorn core.wsgi
```

### Configurações de Produção
Para garantir que o Django use as configurações de produção, você pode definir a variável de ambiente `DJANGO_SETTINGS_MODULE`:
```bash
export DJANGO_SETTINGS_MODULE=core.settings.production
```
Ou passar via flag nos comandos: `--settings=core.settings.production`.
