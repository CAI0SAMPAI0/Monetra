## Lista de Tarefas

### Sprint 0: Configuração Inicial do Projeto (Setup)

#### Tarefa 0.1: Configuração do Ambiente de Desenvolvimento
**Descrição**: Preparar ambiente local para desenvolvimento do projeto

**Subtarefas**:
- [X] 0.1.1: Criar diretório do projeto `finanpy`
- [X] 0.1.2: Criar ambiente virtual Python: `python -m venv venv`
- [X] 0.1.3: Ativar ambiente virtual
- [X] 0.1.4: Criar arquivo `requirements.txt` com dependências iniciais:
  ```
  Django==4.2.7
  python-decouple==3.8
  ```
- [X] 0.1.5: Instalar dependências: `pip install -r requirements.txt`
- [X] 0.1.6: Criar arquivo `.gitignore` com conteúdo padrão para Django:
  ```
  venv/
  __pycache__/
  *.pyc
  db.sqlite3
  .env
  *.log
  media/
  staticfiles/
  ```

#### Tarefa 0.2: Criação do Projeto Django
**Descrição**: Inicializar projeto Django e configurar estrutura base

**Subtarefas**:
- [X] 0.2.1: Criar projeto Django: `django-admin startproject core .`
- [X] 0.2.2: Renomear diretório do projeto de `core` para `core` se necessário
- [X] 0.2.3: Testar servidor de desenvolvimento: `python manage.py runserver`
- [X] 0.2.4: Verificar acesso em `http://localhost:8000`

#### Tarefa 0.3: Configuração de Settings
**Descrição**: Configurar arquivo settings.py com boas práticas

**Subtarefas**:
- [X] 0.3.1: Criar arquivo `.env` na raiz do projeto
- [X] 0.3.2: Mover SECRET_KEY para arquivo `.env`
- [X] 0.3.3: Configurar DEBUG através de variável de ambiente
- [X] 0.3.4: Configurar ALLOWED_HOSTS
- [X] 0.3.5: Adicionar configuração para usar aspas simples no código
- [X] 0.3.6: Configurar LANGUAGE_CODE = 'pt-br'
- [X] 0.3.7: Configurar TIME_ZONE = 'America/Sao_Paulo'
- [X] 0.3.8: Configurar USE_I18N = True
- [X] 0.3.9: Configurar USE_TZ = True

#### Tarefa 0.4: Criação de Apps Django
**Descrição**: Criar todos os apps necessários do projeto

**Subtarefas**:
- [X] 0.4.1: Criar app `users`: `python manage.py startapp users`
- [X] 0.4.2: Criar app `profiles`: `python manage.py startapp profiles`
- [X] 0.4.3: Criar app `accounts`: `python manage.py startapp accounts`
- [X] 0.4.4: Criar app `categories`: `python manage.py startapp categories`
- [X] 0.4.5: Criar app `transactions`: `python manage.py startapp transactions`
- [X] 0.4.6: Adicionar todos os apps em INSTALLED_APPS no settings.py:
  ```python
  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'users',
      'profiles',
      'accounts',
      'categories',
      'transactions',
  ]
  ```

#### Tarefa 0.5: Configuração de TailwindCSS
**Descrição**: Integrar TailwindCSS ao projeto Django

**Subtarefas**:
- [X] 0.5.1: Instalar django-tailwind: adicionar `django-tailwind==3.8.0` ao requirements.txt
- [X] 0.5.2: Instalar dependência: `pip install django-tailwind`
- [X] 0.5.3: Adicionar 'tailwind' ao INSTALLED_APPS
- [X] 0.5.4: Executar: `python manage.py tailwind init`
- [X] 0.5.5: Adicionar app theme gerado ao INSTALLED_APPS
- [X] 0.5.6: Configurar TAILWIND_APP_NAME no settings.py
- [X] 0.5.7: Instalar dependências do Tailwind: `python manage.py tailwind install`
- [X] 0.5.8: Configurar NPM_BIN_PATH no settings.py se necessário

#### Tarefa 0.6: Estrutura de Templates e Static
**Descrição**: Criar estrutura de diretórios para templates e arquivos estáticos

**Subtarefas**:
- [X] 0.6.1: Criar diretório `templates` na raiz do projeto
- [X] 0.6.2: Criar diretório `static` na raiz do projeto
- [X] 0.6.3: Configurar TEMPLATES no settings.py para incluir diretório templates:
  ```python
  'DIRS': [BASE_DIR / 'templates'],
  ```
- [X] 0.6.4: Configurar STATIC_URL e STATICFILES_DIRS no settings.py:
  ```python
  STATIC_URL = '/static/'
  STATICFILES_DIRS = [BASE_DIR / 'static']
  ```
- [X] 0.6.5: Criar subdiretórios em templates: `templates/base/`, `templates/auth/`, etc.

#### Tarefa 0.7: Configuração Inicial do Git
**Descrição**: Inicializar repositório Git e fazer commit inicial

**Subtarefas**:
- [X] 0.7.1: Inicializar repositório Git: `git init`
- [X] 0.7.2: Verificar que .gitignore está configurado corretamente
- [X] 0.7.3: Adicionar arquivos: `git add .`
- [X] 0.7.4: Fazer commit inicial: `git commit -m "Initial project setup"`
- [X] 0.7.5: Criar arquivo README.md com informações básicas do projeto

---

### Sprint 1: Autenticação e Sistema de Usuários ✅ CONCLUÍDA

#### Tarefa 1.1: Model de Usuário Customizado
**Descrição**: Criar model customizado que herda de User do Django para permitir login com email

**Subtarefas**:
- [X] 1.1.1: Abrir arquivo `users/models.py`
- [X] 1.1.2: Importar AbstractUser e models do Django
- [X] 1.1.3: Criar classe CustomUser herdando de AbstractUser
- [X] 1.1.4: Definir campo email como único: `email = models.EmailField(unique=True)`
- [X] 1.1.5: Definir USERNAME_FIELD = 'email'
- [X] 1.1.6: Definir REQUIRED_FIELDS = []
- [X] 1.1.7: Adicionar campos created_at e updated_at
- [X] 1.1.8: Adicionar método __str__ retornando email
- [X] 1.1.9: Configurar AUTH_USER_MODEL = 'users.CustomUser' no settings.py
- [X] Tarefa 1.1 concluída

#### Tarefa 1.2: Configuração do Admin para CustomUser
**Descrição**: Configurar Django Admin para gerenciar usuários customizados

**Subtarefas**:
- [X] 1.2.1: Abrir arquivo `users/admin.py`
- [X] 1.2.2: Importar UserAdmin do Django
- [X] 1.2.3: Importar CustomUser model
- [X] 1.2.4: Criar classe CustomUserAdmin herdando de UserAdmin
- [X] 1.2.5: Configurar list_display com email, is_staff, is_active, date_joined
- [X] 1.2.6: Configurar ordering = ['email']
- [X] 1.2.7: Registrar CustomUser com CustomUserAdmin
- [X] Tarefa 1.2 concluída

#### Tarefa 1.3: Model de Profile
**Descrição**: Criar model de perfil de usuário com informações adicionais

**Subtarefas**:
- [X] 1.3.1: Abrir arquivo `profiles/models.py`
- [X] 1.3.2: Importar models e User (get_user_model)
- [X] 1.3.3: Criar classe Profile com campo OneToOneField para User
- [X] 1.3.4: Adicionar campo full_name (CharField, max_length=200, blank=True)
- [X] 1.3.5: Adicionar campo phone (CharField, max_length=20, blank=True)
- [X] 1.3.6: Adicionar campos created_at e updated_at
- [X] 1.3.7: Adicionar método __str__ retornando full_name ou email do usuário
- [X] 1.3.8: Adicionar Meta com verbose_name e verbose_name_plural
- [X] Tarefa 1.3 concluída

#### Tarefa 1.4: Signal para Criação Automática de Profile
**Descrição**: Implementar signal para criar perfil automaticamente ao criar usuário

**Subtarefas**:
- [X] 1.4.1: Criar arquivo `profiles/signals.py`
- [X] 1.4.2: Importar post_save signal e receiver decorator
- [X] 1.4.3: Importar User model (get_user_model)
- [X] 1.4.4: Importar Profile model
- [X] 1.4.5: Criar função create_profile com decorator @receiver(post_save, sender=User)
- [X] 1.4.6: Verificar if created e criar Profile.objects.create(user=instance)
- [X] 1.4.7: Abrir arquivo `profiles/apps.py`
- [X] 1.4.8: Override método ready() para importar signals
- [X] 1.4.9: Adicionar import de signals no método ready
- [X] Tarefa 1.4 concluída

#### Tarefa 1.5: Configuração do Admin para Profile
**Descrição**: Configurar Django Admin para gerenciar perfis

**Subtarefas**:
- [X] 1.5.1: Abrir arquivo `profiles/admin.py`
- [X] 1.5.2: Importar admin e Profile model
- [X] 1.5.3: Criar classe ProfileAdmin
- [X] 1.5.4: Configurar list_display com user email, full_name, phone
- [X] 1.5.5: Configurar search_fields com user email e full_name
- [X] 1.5.6: Registrar Profile com ProfileAdmin
- [X] Tarefa 1.5 concluída

#### Tarefa 1.6: Migrations Iniciais
**Descrição**: Criar e aplicar migrations para users e profiles

**Subtarefas**:
- [X] 1.6.1: Executar: `python manage.py makemigrations users`
- [X] 1.6.2: Verificar arquivo de migration gerado
- [X] 1.6.3: Executar: `python manage.py makemigrations profiles`
- [X] 1.6.4: Verificar arquivo de migration gerado
- [X] 1.6.5: Executar: `python manage.py migrate`
- [X] 1.6.6: Verificar que tabelas foram criadas no db.sqlite3
- [X] Tarefa 1.6 concluída

#### Tarefa 1.7: Template Base
**Descrição**: Criar template base com estrutura HTML e TailwindCSS

**Subtarefas**:
- [X] 1.7.1: Criar arquivo `templates/base.html`
- [X] 1.7.2: Adicionar DOCTYPE e estrutura HTML5 básica
- [X] 1.7.3: Adicionar tag {% load static %} e {% load tailwind_tags %}
- [X] 1.7.4: Adicionar {% tailwind_css %} no head
- [X] 1.7.5: Configurar meta tags (charset, viewport)
- [X] 1.7.6: Adicionar link para Google Fonts (Inter)
- [X] 1.7.7: Adicionar classe bg-bg-primary ao body
- [X] 1.7.8: Criar bloco {% block title %}
- [X] 1.7.9: Criar bloco {% block content %}
- [X] 1.7.10: Adicionar estrutura de mensagens do Django com estilização
- [X] Tarefa 1.7 concluída

#### Tarefa 1.8: View de Registro (Signup)
**Descrição**: Criar view para cadastro de novos usuários

**Subtarefas**:
- [X] 1.8.1: Criar arquivo `users/forms.py`
- [X] 1.8.2: Importar UserCreationForm e forms do Django
- [X] 1.8.3: Importar get_user_model
- [X] 1.8.4: Criar classe SignupForm herdando de UserCreationForm
- [X] 1.8.5: Adicionar campo email ao Meta.fields
- [X] 1.8.6: Configurar widgets com classes TailwindCSS
- [X] 1.8.7: Adicionar validação customizada para email único
- [X] 1.8.8: Abrir arquivo `users/views.py`
- [X] 1.8.9: Criar SignupView como CreateView
- [X] 1.8.10: Configurar form_class = SignupForm
- [X] 1.8.11: Configurar template_name = 'auth/signup.html'
- [X] 1.8.12: Configurar success_url para dashboard
- [X] 1.8.13: Override form_valid para fazer login automático após cadastro
- [X] Tarefa 1.8 concluída

#### Tarefa 1.9: Template de Registro
**Descrição**: Criar template HTML para página de cadastro

**Subtarefas**:
- [X] 1.9.1: Criar arquivo `templates/auth/signup.html`
- [X] 1.9.2: Extender base.html
- [X] 1.9.3: Adicionar título da página no block title
- [X] 1.9.4: Criar container centralizado com max-width
- [X] 1.9.5: Adicionar logo/nome Finanpy com gradiente
- [X] 1.9.6: Criar card com bg-bg-secondary e border
- [X] 1.9.7: Adicionar título "Criar Conta"
- [X] 1.9.8: Criar formulário com method POST e csrf_token
- [X] 1.9.9: Renderizar campos do form com classes TailwindCSS
- [X] 1.9.10: Adicionar botão de submit estilizado
- [X] 1.9.11: Adicionar link para página de login
- [X] 1.9.12: Adicionar tratamento de erros do formulário
- [X] Tarefa 1.9 concluída

#### Tarefa 1.10: View de Login
**Descrição**: Criar view para autenticação de usuários

**Subtarefas**:
- [X] 1.10.1: No arquivo `users/forms.py`, criar LoginForm
- [X] 1.10.2: Adicionar campo email (EmailField)
- [X] 1.10.3: Adicionar campo password (CharField com widget PasswordInput)
- [X] 1.10.4: Aplicar classes TailwindCSS aos widgets
- [X] 1.10.5: No arquivo `users/views.py`, criar LoginView como FormView
- [X] 1.10.6: Configurar form_class = LoginForm
- [X] 1.10.7: Configurar template_name = 'auth/login.html'
- [X] 1.10.8: Configurar success_url para dashboard
- [X] 1.10.9: Implementar método form_valid com authenticate e login
- [X] 1.10.10: Adicionar tratamento de credenciais inválidas
- [X] 1.10.11: Adicionar mensagem de erro para login inválido
- [X] Tarefa 1.10 concluída

#### Tarefa 1.11: Template de Login
**Descrição**: Criar template HTML para página de login

**Subtarefas**:
- [X] 1.11.1: Criar arquivo `templates/auth/login.html`
- [X] 1.11.2: Extender base.html
- [X] 1.11.3: Adicionar título da página
- [X] 1.11.4: Criar container centralizado
- [X] 1.11.5: Adicionar logo/nome Finanpy com gradiente
- [X] 1.11.6: Criar card de login estilizado
- [X] 1.11.7: Adicionar título "Entrar"
- [X] 1.11.8: Criar formulário de login
- [X] 1.11.9: Renderizar campos com estilização
- [X] 1.11.10: Adicionar botão de submit
- [X] 1.11.11: Adicionar link para página de cadastro
- [X] 1.11.12: Adicionar exibição de mensagens de erro
- [X] Tarefa 1.11 concluída

#### Tarefa 1.12: View de Logout
**Descrição**: Criar view para logout de usuários

**Subtarefas**:
- [X] 1.12.1: No arquivo `users/views.py`, importar LogoutView do Django
- [X] 1.12.2: Criar LogoutView personalizada se necessário
- [X] 1.12.3: Configurar LOGOUT_REDIRECT_URL = '/' no settings.py
- [X] 1.12.4: Adicionar mensagem de sucesso ao fazer logout
- [X] Tarefa 1.12 concluída

#### Tarefa 1.13: URLs de Autenticação
**Descrição**: Configurar URLs para views de autenticação

**Subtarefas**:
- [X] 1.13.1: Criar arquivo `users/urls.py`
- [X] 1.13.2: Importar path do Django
- [X] 1.13.3: Importar views de users
- [X] 1.13.4: Criar urlpatterns list
- [X] 1.13.5: Adicionar path para signup: path('signup/', SignupView.as_view(), name='signup')
- [X] 1.13.6: Adicionar path para login: path('login/', LoginView.as_view(), name='login')
- [X] 1.13.7: Adicionar path para logout: path('logout/', LogoutView.as_view(), name='logout')
- [X] 1.13.8: Abrir arquivo `core/urls.py`
- [X] 1.13.9: Adicionar include de users.urls: path('auth/', include('users.urls'))
- [X] Tarefa 1.13 concluída

#### Tarefa 1.14: Página Inicial Pública
**Descrição**: Criar página inicial para usuários não autenticados

**Subtarefas**:
- [X] 1.14.1: Criar arquivo `users/views.py` adicionar HomeView
- [X] 1.14.2: Criar TemplateView para home
- [X] 1.14.3: Configurar template_name = 'home.html'
- [X] 1.14.4: Override método get para redirecionar usuários autenticados
- [X] 1.14.5: Criar arquivo `templates/home.html`
- [X] 1.14.6: Extender base.html
- [X] 1.14.7: Criar seção hero com gradiente
- [X] 1.14.8: Adicionar logo e nome Finanpy
- [X] 1.14.9: Adicionar tagline/descrição do produto
- [X] 1.14.10: Adicionar botões de Cadastrar e Entrar estilizados
- [X] 1.14.11: Criar seção de features/funcionalidades
- [X] 1.14.12: Listar principais funcionalidades com ícones
- [X] 1.14.13: Adicionar URL no urls.py: path('', HomeView.as_view(), name='home')
- [X] Tarefa 1.14 concluída

#### Tarefa 1.15: Testes Manuais de Autenticação
**Descrição**: Testar fluxo completo de autenticação

**Subtarefas**:
- [X] 1.15.1: Iniciar servidor de desenvolvimento
- [X] 1.15.2: Acessar página inicial e verificar layout
- [X] 1.15.3: Clicar em "Cadastrar" e verificar redirecionamento
- [X] 1.15.4: Testar cadastro com email inválido
- [X] 1.15.5: Testar cadastro com senha fraca
- [X] 1.15.6: Cadastrar usuário válido
- [X] 1.15.7: Verificar redirecionamento após cadastro
- [X] 1.15.8: Fazer logout
- [X] 1.15.9: Tentar login com credenciais inválidas
- [X] 1.15.10: Fazer login com credenciais válidas
- [X] 1.15.11: Verificar que usuário autenticado é redirecionado da home
- [X] 1.15.12: Verificar criação automática do perfil no admin
- [X] Tarefa 1.15 concluída

---

### Sprint 2: Gestão de Contas Bancárias ✅ CONCLUÍDA

#### Tarefa 2.1: Model de Account ✅
**Descrição**: Criar model para representar contas bancárias do usuário

**Subtarefas**:
- [X] 2.1.1: Abrir arquivo `accounts/models.py`
- [X] 2.1.2: Importar models e get_user_model
- [X] 2.1.3: Criar classe Account com ForeignKey para User
- [X] 2.1.4: Adicionar campo name (CharField, max_length=100)
- [X] 2.1.5: Adicionar campo bank_name (CharField, max_length=100)
- [X] 2.1.6: Criar choices para account_type (CHECKING, SAVINGS, WALLET)
- [X] 2.1.7: Adicionar campo account_type com choices
- [X] 2.1.8: Adicionar campo balance (DecimalField, max_digits=12, decimal_places=2, default=0)
- [X] 2.1.9: Adicionar campo is_active (BooleanField, default=True)
- [X] 2.1.10: Adicionar campos created_at e updated_at
- [X] 2.1.11: Adicionar método __str__ retornando name
- [X] 2.1.12: Adicionar Meta com ordering, verbose_name e indexes

#### Tarefa 2.2: Admin de Account ✅
**Descrição**: Configurar Django Admin para gerenciar contas

**Subtarefas**:
- [X] 2.2.1: Abrir arquivo `accounts/admin.py`
- [X] 2.2.2: Importar admin e Account model
- [X] 2.2.3: Criar classe AccountAdmin
- [X] 2.2.4: Configurar list_display: user email, name, bank_name, account_type, balance, is_active
- [X] 2.2.5: Configurar list_filter: account_type, is_active
- [X] 2.2.6: Configurar search_fields: name, bank_name, user__email
- [X] 2.2.7: Configurar readonly_fields: created_at, updated_at
- [X] 2.2.8: Registrar Account com AccountAdmin

#### Tarefa 2.3: Form de Account ✅
**Descrição**: Criar formulário para cadastro e edição de contas

**Subtarefas**:
- [X] 2.3.1: Criar arquivo `accounts/forms.py`
- [X] 2.3.2: Importar forms e Account model
- [X] 2.3.3: Criar classe AccountForm herdando de forms.ModelForm
- [X] 2.3.4: Configurar Meta com model = Account
- [X] 2.3.5: Definir fields: name, bank_name, account_type, balance
- [X] 2.3.6: Configurar widgets com classes TailwindCSS para cada campo
- [X] 2.3.7: Adicionar labels em português para cada campo
- [X] 2.3.8: Adicionar placeholders nos widgets
- [X] 2.3.9: Configurar choices de account_type em português

#### Tarefa 2.4: View de Listagem de Contas ✅
**Descrição**: Criar view para listar contas do usuário

**Subtarefas**:
- [X] 2.4.1: Abrir arquivo `accounts/views.py`
- [X] 2.4.2: Importar LoginRequiredMixin e ListView
- [X] 2.4.3: Importar Account model
- [X] 2.4.4: Criar AccountListView herdando de LoginRequiredMixin e ListView
- [X] 2.4.5: Configurar model = Account
- [X] 2.4.6: Configurar template_name = 'accounts/account_list.html'
- [X] 2.4.7: Configurar context_object_name = 'accounts'
- [X] 2.4.8: Override get_queryset para filtrar por usuário: self.request.user
- [X] 2.4.9: Adicionar ordenação por nome
- [X] 2.4.10: Adicionar cálculo de saldo total no get_context_data

#### Tarefa 2.5: Template de Listagem de Contas ✅
**Descrição**: Criar template HTML para listar contas

**Subtarefas**:
- [X] 2.5.1: Criar arquivo `templates/accounts/account_list.html`
- [X] 2.5.2: Extender base.html
- [X] 2.5.3: Adicionar título "Minhas Contas"
- [X] 2.5.4: Criar header com título e botão "Nova Conta"
- [X] 2.5.5: Criar container com grid responsivo
- [X] 2.5.6: Iterar sobre accounts com for loop
- [X] 2.5.7: Para cada conta, criar card estilizado
- [X] 2.5.8: Exibir nome da conta em destaque
- [X] 2.5.9: Exibir nome do banco e tipo de conta
- [X] 2.5.10: Exibir saldo formatado com R$
- [X] 2.5.11: Adicionar botões de Editar e Excluir
- [X] 2.5.12: Adicionar mensagem quando não houver contas
- [X] 2.5.13: Adicionar card com saldo total consolidado

#### Tarefa 2.6: View de Criação de Conta ✅
**Descrição**: Criar view para cadastrar nova conta

**Subtarefas**:
- [X] 2.6.1: No arquivo `accounts/views.py`, importar CreateView
- [X] 2.6.2: Importar AccountForm
- [X] 2.6.3: Criar AccountCreateView herdando de LoginRequiredMixin e CreateView
- [X] 2.6.4: Configurar model = Account
- [X] 2.6.5: Configurar form_class = AccountForm
- [X] 2.6.6: Configurar template_name = 'accounts/account_form.html'
- [X] 2.6.7: Configurar success_url para lista de contas
- [X] 2.6.8: Override form_valid para associar user: form.instance.user = self.request.user
- [X] 2.6.9: Adicionar mensagem de sucesso
- [X] 2.6.10: Adicionar context extra com título da página

#### Tarefa 2.7: View de Edição de Conta ✅
**Descrição**: Criar view para editar conta existente

**Subtarefas**:
- [X] 2.7.1: No arquivo `accounts/views.py`, importar UpdateView
- [X] 2.7.2: Criar AccountUpdateView herdando de LoginRequiredMixin e UpdateView
- [X] 2.7.3: Configurar model, form_class e template_name
- [X] 2.7.4: Configurar success_url
- [X] 2.7.5: Override get_queryset para filtrar por usuário
- [X] 2.7.6: Adicionar mensagem de sucesso
- [X] 2.7.7: Adicionar context extra com título

#### Tarefa 2.8: View de Exclusão de Conta ✅
**Descrição**: Criar view para excluir conta

**Subtarefas**:
- [X] 2.8.1: No arquivo `accounts/views.py`, importar DeleteView
- [X] 2.8.2: Criar AccountDeleteView herdando de LoginRequiredMixin e DeleteView
- [X] 2.8.3: Configurar model = Account
- [X] 2.8.4: Configurar template_name = 'accounts/account_confirm_delete.html'
- [X] 2.8.5: Configurar success_url para lista de contas
- [X] 2.8.6: Override get_queryset para filtrar por usuário
- [X] 2.8.7: Adicionar mensagem de sucesso
- [X] 2.8.8: Adicionar validação para não excluir conta com transações (implementar depois)

#### Tarefa 2.9: Template de Form de Conta ✅
**Descrição**: Criar template HTML para criar/editar conta

**Subtarefas**:
- [X] 2.9.1: Criar arquivo `templates/accounts/account_form.html`
- [X] 2.9.2: Extender base.html
- [X] 2.9.3: Adicionar título dinâmico (Nova Conta ou Editar Conta)
- [X] 2.9.4: Criar container centralizado
- [X] 2.9.5: Criar card com formulário
- [X] 2.9.6: Adicionar form com method POST e csrf_token
- [X] 2.9.7: Renderizar campos do form com {{ form.as_p }} ou manualmente
- [X] 2.9.8: Estilizar cada campo individualmente com TailwindCSS
- [X] 2.9.9: Adicionar botão de Salvar
- [X] 2.9.10: Adicionar botão de Cancelar
- [X] 2.9.11: Adicionar exibição de erros do formulário

#### Tarefa 2.10: Template de Confirmação de Exclusão ✅
**Descrição**: Criar template para confirmar exclusão de conta

**Subtarefas**:
- [X] 2.10.1: Criar arquivo `templates/accounts/account_confirm_delete.html`
- [X] 2.10.2: Extender base.html
- [X] 2.10.3: Adicionar título "Confirmar Exclusão"
- [X] 2.10.4: Criar card com mensagem de confirmação
- [X] 2.10.5: Exibir nome da conta a ser excluída
- [X] 2.10.6: Adicionar aviso sobre exclusão permanente
- [X] 2.10.7: Criar form com method POST e csrf_token
- [X] 2.10.8: Adicionar botão de Confirmar Exclusão (vermelho)
- [X] 2.10.9: Adicionar botão de Cancelar
- [X] 2.10.10: Estilizar com cores de alerta

#### Tarefa 2.11: URLs de Accounts ✅
**Descrição**: Configurar URLs para views de contas

**Subtarefas**:
- [X] 2.11.1: Criar arquivo `accounts/urls.py`
- [X] 2.11.2: Importar path e views
- [X] 2.11.3: Criar urlpatterns list
- [X] 2.11.4: Adicionar path para list: path('', AccountListView.as_view(), name='account_list')
- [X] 2.11.5: Adicionar path para create: path('new/', AccountCreateView.as_view(), name='account_create')
- [X] 2.11.6: Adicionar path para update: path('<int:pk>/edit/', AccountUpdateView.as_view(), name='account_update')
- [X] 2.11.7: Adicionar path para delete: path('<int:pk>/delete/', AccountDeleteView.as_view(), name='account_delete')
- [X] 2.11.8: No arquivo `core/urls.py`, incluir accounts.urls: path('accounts/', include('accounts.urls'))

#### Tarefa 2.12: Migration de Account ✅
**Descrição**: Criar e aplicar migration para model Account

**Subtarefas**:
- [X] 2.12.1: Executar: `python manage.py makemigrations accounts`
- [X] 2.12.2: Verificar arquivo de migration gerado
- [X] 2.12.3: Executar: `python manage.py migrate`
- [X] 2.12.4: Verificar tabela no banco de dados

#### Tarefa 2.13: Testes Manuais de Accounts ✅
**Descrição**: Testar CRUD completo de contas

**Subtarefas**:
- [X] 2.13.1: Fazer login no sistema
- [X] 2.13.2: Acessar página de contas
- [X] 2.13.3: Verificar mensagem de lista vazia
- [X] 2.13.4: Criar nova conta corrente
- [X] 2.13.5: Verificar redirecionamento e mensagem de sucesso
- [X] 2.13.6: Criar conta poupança
- [X] 2.13.7: Criar conta tipo carteira
- [X] 2.13.8: Verificar que todas as contas aparecem na listagem
- [X] 2.13.9: Editar nome de uma conta
- [X] 2.13.10: Editar saldo de uma conta
- [X] 2.13.11: Tentar excluir uma conta
- [X] 2.13.12: Verificar que conta foi excluída
- [X] 2.13.13: Verificar que outro usuário não vê as contas
- [X] 2.13.14: Verificar cálculo de saldo total

- [X] Tarefa 2.13 concluída

---

### Sprint 3: Gestão de Categorias ✅ CONCLUÍDA

#### Tarefa 3.1: Model de Category
**Descrição**: Criar model para categorias de transações

**Subtarefas**:
- [X] 3.1.1: Abrir arquivo `categories/models.py`
- [X] 3.1.2: Importar models e get_user_model
- [X] 3.1.3: Criar classe Category com ForeignKey para User
- [X] 3.1.4: Adicionar campo name (CharField, max_length=50)
- [X] 3.1.5: Criar choices para category_type (INCOME, EXPENSE)
- [X] 3.1.6: Adicionar campo category_type com choices
- [X] 3.1.7: Adicionar campo color (CharField, max_length=7, default='#667eea')
- [X] 3.1.8: Adicionar campos created_at e updated_at
- [X] 3.1.9: Adicionar método __str__ retornando name
- [X] 3.1.10: Adicionar Meta com ordering e verbose_name
- [X] 3.1.11: Adicionar unique_together para (user, name)

#### Tarefa 3.2: Admin de Category
**Descrição**: Configurar Django Admin para categorias

**Subtarefas**:
- [X] 3.2.1: Abrir arquivo `categories/admin.py`
- [X] 3.2.2: Importar admin e Category model
- [X] 3.2.3: Criar classe CategoryAdmin
- [X] 3.2.4: Configurar list_display: user email, name, category_type, color
- [X] 3.2.5: Configurar list_filter: category_type
- [X] 3.2.6: Configurar search_fields: name, user__email
- [X] 3.2.7: Configurar readonly_fields: created_at, updated_at
- [X] 3.2.8: Registrar Category com CategoryAdmin

#### Tarefa 3.3: Form de Category
**Descrição**: Criar formulário para categorias

**Subtarefas**:
- [X] 3.3.1: Criar arquivo `categories/forms.py`
- [X] 3.3.2: Importar forms e Category model
- [X] 3.3.3: Criar CategoryForm herdando de forms.ModelForm
- [X] 3.3.4: Configurar Meta com model e fields
- [X] 3.3.5: Definir fields: name, category_type, color
- [X] 3.3.6: Configurar widgets com classes TailwindCSS
- [X] 3.3.7: Usar input type color para campo color
- [X] 3.3.8: Adicionar labels em português
- [X] 3.3.9: Adicionar placeholders
- [X] 3.3.10: Traduzir choices para português

#### Tarefa 3.4: View de Listagem de Categorias
**Descrição**: Criar view para listar categorias

**Subtarefas**:
- [X] 3.4.1: Abrir arquivo `categories/views.py`
- [X] 3.4.2: Importar LoginRequiredMixin e ListView
- [X] 3.4.3: Importar Category model
- [X] 3.4.4: Criar CategoryListView
- [X] 3.4.5: Configurar model, template_name e context_object_name
- [X] 3.4.6: Override get_queryset para filtrar por usuário
- [X] 3.4.7: Adicionar ordenação por categoria_type e name
- [X] 3.4.8: Adicionar separação de categorias de entrada e saída no context

#### Tarefa 3.5: Template de Listagem de Categorias
**Descrição**: Criar template para listar categorias

**Subtarefas**:
- [X] 3.5.1: Criar arquivo `templates/categories/category_list.html`
- [X] 3.5.2: Extender base.html
- [X] 3.5.3: Adicionar título "Minhas Categorias"
- [X] 3.5.4: Criar header com botão "Nova Categoria"
- [X] 3.5.5: Criar duas seções: Entradas e Saídas
- [X] 3.5.6: Iterar sobre categorias de entrada
- [X] 3.5.7: Para cada categoria, criar badge com nome e cor
- [X] 3.5.8: Adicionar botões de Editar e Excluir
- [X] 3.5.9: Repetir para categorias de saída
- [X] 3.5.10: Adicionar mensagem quando não houver categorias
- [X] 3.5.11: Usar cores diferentes para entrada (verde) e saída (vermelho)

#### Tarefa 3.6: View de Criação de Categoria
**Descrição**: Criar view para cadastrar categoria

**Subtarefas**:
- [X] 3.6.1: No `categories/views.py`, importar CreateView
- [X] 3.6.2: Importar CategoryForm
- [X] 3.6.3: Criar CategoryCreateView
- [X] 3.6.4: Configurar model, form_class e template_name
- [X] 3.6.5: Configurar success_url
- [X] 3.6.6: Override form_valid para associar usuário
- [X] 3.6.7: Adicionar mensagem de sucesso
- [X] 3.6.8: Adicionar tratamento de erro para nome duplicado

#### Tarefa 3.7: View de Edição de Categoria
**Descrição**: Criar view para editar categoria

**Subtarefas**:
- [X] 3.7.1: No `categories/views.py`, importar UpdateView
- [X] 3.7.2: Criar CategoryUpdateView
- [X] 3.7.3: Configurar atributos necessários
- [X] 3.7.4: Override get_queryset para filtrar por usuário
- [X] 3.7.5: Adicionar mensagem de sucesso

#### Tarefa 3.8: View de Exclusão de Categoria
**Descrição**: Criar view para excluir categoria

**Subtarefas**:
- [X] 3.8.1: No `categories/views.py`, importar DeleteView
- [X] 3.8.2: Criar CategoryDeleteView
- [X] 3.8.3: Configurar atributos necessários
- [X] 3.8.4: Override get_queryset
- [X] 3.8.5: Adicionar mensagem de sucesso
- [X] 3.8.6: Adicionar validação para não excluir categoria com transações

#### Tarefa 3.9: Templates de Form e Delete de Categoria
**Descrição**: Criar templates para forms de categoria

**Subtarefas**:
- [X] 3.9.1: Criar `templates/categories/category_form.html`
- [X] 3.9.2: Extender base e criar formulário estilizado
- [X] 3.9.3: Adicionar preview da cor selecionada
- [X] 3.9.4: Adicionar botões de ação
- [X] 3.9.5: Criar `templates/categories/category_confirm_delete.html`
- [X] 3.9.6: Adicionar mensagem de confirmação
- [X] 3.9.7: Estilizar com cores de alerta

#### Tarefa 3.10: URLs de Categories
**Descrição**: Configurar URLs para views de categorias

**Subtarefas**:
- [X] 3.10.1: Criar arquivo `categories/urls.py`
- [X] 3.10.2: Adicionar paths para todas as views
- [X] 3.10.3: Incluir no `core/urls.py`

#### Tarefa 3.11: Migration de Category
**Descrição**: Criar e aplicar migrations

**Subtarefas**:
- [X] 3.11.1: Executar makemigrations
- [X] 3.11.2: Verificar migration
- [X] 3.11.3: Executar migrate
- [X] 3.11.4: Verificar no banco

#### Tarefa 3.12: Categorias Padrão
**Descrição**: Criar signal para adicionar categorias padrão ao novo usuário

**Subtarefas**:
- [X] 3.12.1: Criar arquivo `categories/signals.py`
- [X] 3.12.2: Criar função para criar categorias padrão
- [X] 3.12.3: Definir lista de categorias padrão (Salário, Alimentação, Transporte, etc)
- [X] 3.12.4: Conectar ao signal post_save de User
- [X] 3.12.5: Importar signals no apps.py
- [X] 3.12.6: Testar criação automática

#### Tarefa 3.13: Testes Manuais de Categories ✅
**Descrição**: Testar CRUD de categorias

**Subtarefas**:
- [X] 3.13.1: Fazer login
- [X] 3.13.2: Acessar página de categorias
- [X] 3.13.3: Verificar categorias padrão criadas
- [X] 3.13.4: Criar categoria de entrada personalizada
- [X] 3.13.5: Criar categoria de saída personalizada
- [X] 3.13.6: Testar seletor de cor
- [X] 3.13.7: Editar categoria
- [X] 3.13.8: Tentar criar categoria com nome duplicado
- [X] 3.13.9: Excluir categoria
- [X] 3.13.10: Verificar separação visual entre entradas e saídas

---

### Sprint 4: Gestão de Transações ✅ CONCLUÍDA

#### Tarefa 4.1: Model de Transaction
**Descrição**: Criar model para transações financeiras

**Subtarefas**:
- [X] 4.1.1: Abrir arquivo `transactions/models.py`
- [X] 4.1.2: Importar models, Account e Category
- [X] 4.1.3: Criar classe Transaction
- [X] 4.1.4: Adicionar ForeignKey para Account (on_delete=PROTECT)
- [X] 4.1.5: Adicionar ForeignKey para Category (on_delete=PROTECT)
- [X] 4.1.6: Criar choices para transaction_type (INCOME, EXPENSE)
- [X] 4.1.7: Adicionar campo transaction_type
- [X] 4.1.8: Adicionar campo amount (DecimalField, max_digits=12, decimal_places=2)
- [X] 4.1.9: Adicionar campo transaction_date (DateField)
- [X] 4.1.10: Adicionar campo description (TextField, blank=True)
- [X] 4.1.11: Adicionar created_at e updated_at
- [X] 4.1.12: Adicionar método __str__
- [X] 4.1.13: Adicionar Meta com ordering por -transaction_date
- [X] Tarefa 4.1 concluída

#### Tarefa 4.2: Signal para Atualização de Saldo
**Descrição**: Criar signals para atualizar saldo da conta automaticamente

**Subtarefas**:
- [X] 4.2.1: Criar arquivo `transactions/signals.py`
- [X] 4.2.2: Importar post_save, post_delete, pre_save
- [X] 4.2.3: Criar função update_balance_on_create
- [X] 4.2.4: Conectar ao post_save de Transaction
- [X] 4.2.5: Implementar lógica: se INCOME adiciona, se EXPENSE subtrai
- [X] 4.2.6: Criar função update_balance_on_delete
- [X] 4.2.7: Implementar lógica reversa ao excluir
- [X] 4.2.8: Criar função update_balance_on_update usando pre_save
- [X] 4.2.9: Salvar valores antigos antes de atualizar
- [X] 4.2.10: Recalcular saldo considerando mudanças
- [X] 4.2.11: Importar signals no apps.py
- [X] 4.2.12: Adicionar tratamento de erros
- [X] Tarefa 4.2 concluída

#### Tarefa 4.3: Admin de Transaction
**Descrição**: Configurar Django Admin para transações

**Subtarefas**:
- [X] 4.3.1: Abrir arquivo `transactions/admin.py`
- [X] 4.3.2: Criar TransactionAdmin
- [X] 4.3.3: Configurar list_display: transaction_date, description, account, category, transaction_type, amount
- [X] 4.3.4: Configurar list_filter: transaction_type, transaction_date, category
- [X] 4.3.5: Configurar search_fields: description, account__name
- [X] 4.3.6: Configurar date_hierarchy: transaction_date
- [X] 4.3.7: Configurar readonly_fields: created_at, updated_at
- [X] 4.3.8: Registrar Transaction
- [X] Tarefa 4.3 concluída

#### Tarefa 4.4: Form de Transaction
**Descrição**: Criar formulário para transações

**Subtarefas**:
- [X] 4.4.1: Criar arquivo `transactions/forms.py`
- [X] 4.4.2: Criar TransactionForm
- [X] 4.4.3: Definir fields: account, category, transaction_type, amount, transaction_date, description
- [X] 4.4.4: Configurar widgets com TailwindCSS
- [X] 4.4.5: Usar DateInput com type='date'
- [X] 4.4.6: Adicionar labels em português
- [X] 4.4.7: Adicionar placeholders
- [X] 4.4.8: Adicionar método __init__ para filtrar accounts e categories do usuário
- [X] 4.4.9: Adicionar validação: category_type deve corresponder a transaction_type
- [X] 4.4.10: Adicionar validação: amount deve ser positivo
- [X] Tarefa 4.4 concluída

#### Tarefa 4.5: View de Listagem de Transações
**Descrição**: Criar view para listar transações com filtros

**Subtarefas**:
- [X] 4.5.1: Abrir `transactions/views.py`
- [X] 4.5.2: Importar ListView e Transaction
- [X] 4.5.3: Criar TransactionListView
- [X] 4.5.4: Override get_queryset para filtrar por usuário (via account__user)
- [X] 4.5.5: Implementar filtros por data_inicio, data_fim (GET params)
- [X] 4.5.6: Implementar filtro por conta (GET param)
- [X] 4.5.7: Implementar filtro por categoria (GET param)
- [X] 4.5.8: Adicionar paginação (paginate_by = 20)
- [X] 4.5.9: Adicionar estatísticas no context: total_income, total_expense, balance
- [X] 4.5.10: Passar contas e categorias do usuário para o context (para filtros)
- [X] Tarefa 4.5 concluída

#### Tarefa 4.6: Template de Listagem de Transações
**Descrição**: Criar template para listar transações

**Subtarefas**:
- [X] 4.6.1: Criar `templates/transactions/transaction_list.html`
- [X] 4.6.2: Extender base.html
- [X] 4.6.3: Criar header com título e botão "Nova Transação"
- [X] 4.6.4: Criar seção de filtros com formulário GET
- [X] 4.6.5: Adicionar inputs para data início e fim
- [X] 4.6.6: Adicionar select para conta
- [X] 4.6.7: Adicionar select para categoria
- [X] 4.6.8: Adicionar botão "Filtrar" e "Limpar Filtros"
- [X] 4.6.9: Criar seção de cards com estatísticas (Total Entradas, Total Saídas, Balanço)
- [X] 4.6.10: Criar tabela responsiva para transações
- [X] 4.6.11: Colunas: Data, Descrição, Conta, Categoria, Tipo, Valor, Ações
- [X] 4.6.12: Usar cores diferentes para INCOME (verde) e EXPENSE (vermelho)
- [X] 4.6.13: Adicionar botões Editar e Excluir
- [X] 4.6.14: Adicionar paginação
- [X] 4.6.15: Adicionar mensagem quando lista vazia
- [X] Tarefa 4.6 concluída

#### Tarefa 4.7: View de Criação de Transação
**Descrição**: Criar view para registrar nova transação

**Subtarefas**:
- [X] 4.7.1: No `transactions/views.py`, criar TransactionCreateView
- [X] 4.7.2: Configurar form_class = TransactionForm
- [X] 4.7.3: Configurar template e success_url
- [X] 4.7.4: Override get_form_kwargs para passar request.user ao form
- [X] 4.7.5: Adicionar mensagem de sucesso
- [X] 4.7.6: Adicionar tratamento de erro
- [X] Tarefa 4.7 concluída

#### Tarefa 4.8: View de Edição de Transação
**Descrição**: Criar view para editar transação

**Subtarefas**:
- [X] 4.8.1: Criar TransactionUpdateView
- [X] 4.8.2: Configurar atributos necessários
- [X] 4.8.3: Override get_queryset para filtrar por usuário
- [X] 4.8.4: Override get_form_kwargs
- [X] 4.8.5: Adicionar mensagem de sucesso
- [X] Tarefa 4.8 concluída

#### Tarefa 4.9: View de Exclusão de Transação
**Descrição**: Criar view para excluir transação

**Subtarefas**:
- [X] 4.9.1: Criar TransactionDeleteView
- [X] 4.9.2: Configurar atributos
- [X] 4.9.3: Override get_queryset
- [X] 4.9.4: Adicionar mensagem de sucesso
- [X] Tarefa 4.9 concluída

#### Tarefa 4.10: Templates de Form e Delete
**Descrição**: Criar templates para forms de transação

**Subtarefas**:
- [X] 4.10.1: Criar `templates/transactions/transaction_form.html`
- [X] 4.10.2: Criar formulário estilizado
- [X] 4.10.3: Adicionar JavaScript para filtrar categorias baseado no tipo
- [X] 4.10.4: Criar `templates/transactions/transaction_confirm_delete.html`
- [X] 4.10.5: Adicionar informações da transação
- [X] 4.10.6: Adicionar aviso sobre atualização de saldo
- [X] Tarefa 4.10 concluída

#### Tarefa 4.11: URLs de Transactions
**Descrição**: Configurar URLs para transações

**Subtarefas**:
- [X] 4.11.1: Criar `transactions/urls.py`
- [X] 4.11.2: Adicionar paths para list, create, update, delete
- [X] 4.11.3: Incluir no `core/urls.py`
- [X] Tarefa 4.11 concluída

#### Tarefa 4.12: Migration de Transaction
**Descrição**: Criar e aplicar migrations

**Subtarefas**:
- [X] 4.12.1: Executar makemigrations
- [X] 4.12.2: Revisar migration
- [X] 4.12.3: Executar migrate
- [X] 4.12.4: Verificar tabela
- [X] Tarefa 4.12 concluída

#### Tarefa 4.13: Testes Manuais de Transactions
**Descrição**: Testar funcionalidades de transações

**Subtarefas**:
- [X] 4.13.1: Criar transação de entrada
- [X] 4.13.2: Verificar atualização de saldo da conta
- [X] 4.13.3: Criar transação de saída
- [X] 4.13.4: Verificar subtração do saldo
- [X] 4.13.5: Editar transação e verificar recálculo
- [X] 4.13.6: Excluir transação e verificar reversão do saldo
- [X] 4.13.7: Testar filtros por data
- [X] 4.13.8: Testar filtros por conta
- [X] 4.13.9: Testar filtros por categoria
- [X] 4.13.10: Testar combinação de filtros
- [X] 4.13.11: Verificar cálculo de estatísticas
- [X] 4.13.12: Testar paginação
- [X] 4.13.13: Testar validação de categoria vs tipo
- [X] 4.13.14: Verificar que usuário só vê suas transações
- [X] Tarefa 4.13 concluída

---

### Sprint 5: Dashboard e Visualizações ✅ CONCLUÍDA

#### Tarefa 5.1: View do Dashboard
**Descrição**: Criar view principal do dashboard com estatísticas

**Subtarefas**:
- [X] 5.1.1: Criar arquivo `users/views.py` (ou usar existente)
- [X] 5.1.2: Importar TemplateView e modelos necessários
- [X] 5.1.3: Criar DashboardView herdando de LoginRequiredMixin e TemplateView
- [X] 5.1.4: Configurar template_name = 'dashboard.html'
- [X] 5.1.5: Override get_context_data
- [X] 5.1.6: Calcular saldo total de todas as contas do usuário
- [X] 5.1.7: Calcular total de entradas do mês atual
- [X] 5.1.8: Calcular total de saídas do mês atual
- [X] 5.1.9: Calcular balanço do mês (entradas - saídas)
- [X] 5.1.10: Buscar últimas 10 transações do usuário
- [X] 5.1.11: Calcular totais por categoria do mês
- [X] 5.1.12: Contar número de contas ativas
- [X] 5.1.13: Adicionar todos os dados ao context

#### Tarefa 5.2: Template do Dashboard
**Descrição**: Criar template HTML do dashboard principal

**Subtarefas**:
- [X] 5.2.1: Criar arquivo `templates/dashboard.html`
- [X] 5.2.2: Extender base.html
- [X] 5.2.3: Adicionar título "Dashboard"
- [X] 5.2.4: Criar seção de boas-vindas com nome do usuário
- [X] 5.2.5: Criar grid com 4 cards de estatísticas principais
- [X] 5.2.6: Card 1: Saldo Total (gradiente primário)
- [X] 5.2.7: Card 2: Entradas do Mês (verde)
- [X] 5.2.8: Card 3: Saídas do Mês (vermelho)
- [X] 5.2.9: Card 4: Balanço do Mês (azul se positivo, vermelho se negativo)
- [X] 5.2.10: Criar seção "Ações Rápidas" com botões
- [X] 5.2.11: Botão para Nova Transação
- [X] 5.2.12: Botão para Nova Conta
- [X] 5.2.13: Botão para Nova Categoria
- [X] 5.2.14: Criar seção "Transações Recentes"
- [X] 5.2.15: Listar últimas transações em tabela compacta
- [X] 5.2.16: Link "Ver Todas" para página de transações
- [X] 5.2.17: Criar seção "Gastos por Categoria"
- [X] 5.2.18: Exibir top 5 categorias do mês com barras de progresso
- [X] 5.2.19: Usar cores das categorias
- [X] 5.2.20: Adicionar responsividade mobile-first

#### Tarefa 5.3: Menu de Navegação Principal
**Descrição**: Criar componente de navegação consistente

**Subtarefas**:
- [X] 5.3.1: Criar arquivo `templates/includes/navbar.html`
- [X] 5.3.2: Criar estrutura de navbar com TailwindCSS
- [X] 5.3.3: Adicionar logo/nome Finanpy à esquerda
- [X] 5.3.4: Adicionar links de navegação no centro
- [X] 5.3.5: Link para Dashboard
- [X] 5.3.6: Link para Contas
- [X] 5.3.7: Link para Categorias
- [X] 5.3.8: Link para Transações
- [X] 5.3.9: Adicionar dropdown de usuário à direita
- [X] 5.3.10: Exibir nome/email do usuário
- [X] 5.3.11: Link para Ver Perfil
- [X] 5.3.12: Link para Editar Perfil
- [X] 5.3.13: Botão de Logout
- [X] 5.3.14: Adicionar indicador de página ativa
- [X] 5.3.15: Implementar menu hambúrguer para mobile
- [X] 5.3.16: Incluir navbar no base.html

#### Tarefa 5.4: Visualização de Perfil
**Descrição**: Criar página para visualizar dados do perfil

**Subtarefas**:
- [X] 5.4.1: No `profiles/views.py`, criar ProfileDetailView
- [X] 5.4.2: Configurar para buscar perfil do usuário logado
- [X] 5.4.3: Configurar template_name
- [X] 5.4.4: Criar `templates/profiles/profile_detail.html`
- [X] 5.4.5: Exibir foto placeholder (círculo com iniciais)
- [X] 5.4.6: Exibir nome completo
- [X] 5.4.7: Exibir email (não editável)
- [X] 5.4.8: Exibir telefone
- [X] 5.4.9: Exibir data de cadastro
- [X] 5.4.10: Adicionar botão "Editar Perfil"
- [X] 5.4.11: Criar design com cards estilizados

#### Tarefa 5.5: Edição de Perfil
**Descrição**: Criar formulário para editar perfil

**Subtarefas**:
- [X] 5.5.1: Criar `profiles/forms.py`
- [X] 5.5.2: Criar ProfileForm
- [X] 5.5.3: Incluir fields: full_name, phone
- [X] 5.5.4: Aplicar widgets com TailwindCSS
- [X] 5.5.5: Adicionar labels e placeholders em português
- [X] 5.5.6: No `profiles/views.py`, criar ProfileUpdateView
- [X] 5.5.7: Configurar para editar perfil do usuário logado
- [X] 5.5.8: Criar `templates/profiles/profile_form.html`
- [X] 5.5.9: Criar formulário estilizado
- [X] 5.5.10: Adicionar botões Salvar e Cancelar

#### Tarefa 5.6: URLs de Dashboard e Profile
**Descrição**: Configurar URLs para dashboard e perfil

**Subtarefas**:
- [X] 5.6.1: Criar `profiles/urls.py`
- [X] 5.6.2: Adicionar paths para profile detail e update
- [X] 5.6.3: Incluir no `core/urls.py`
- [X] 5.6.4: Adicionar URL do dashboard no `core/urls.py`
- [X] 5.6.5: Configurar LOGIN_REDIRECT_URL = '/dashboard/' no settings.py

#### Tarefa 5.7: Formatação de Valores Monetários
**Descrição**: Criar template tags para formatar valores em reais

**Subtarefas**:
- [X] 5.7.1: Criar diretório `users/templatetags/`
- [X] 5.7.2: Criar arquivo `__init__.py`
- [X] 5.7.3: Criar arquivo `currency_filters.py`
- [X] 5.7.4: Criar filtro currency para formatar em R$
- [X] 5.7.5: Usar locale pt_BR
- [X] 5.7.6: Testar formatação em templates
- [X] 5.7.7: Aplicar em todos os templates que exibem valores

#### Tarefa 5.8: Mensagens de Feedback
**Descrição**: Padronizar sistema de mensagens do Django

**Subtarefas**:
- [X] 5.8.1: No base.html, criar seção para mensagens
- [X] 5.8.2: Estilizar mensagens de sucesso (verde)
- [X] 5.8.3: Estilizar mensagens de erro (vermelho)
- [X] 5.8.4: Estilizar mensagens de aviso (amarelo)
- [X] 5.8.5: Estilizar mensagens de info (azul)
- [X] 5.8.6: Adicionar botão para fechar mensagens
- [X] 5.8.7: Adicionar auto-dismiss com JavaScript (opcional)
- [X] 5.8.8: Testar em todas as views

#### Tarefa 5.9: Melhorias de UX
**Descrição**: Implementar melhorias de experiência do usuário

**Subtarefas**:
- [X] 5.9.1: Adicionar breadcrumbs nas páginas internas
- [X] 5.9.2: Adicionar título da página no navegador (tag title)
- [X] 5.9.3: Adicionar confirmação JavaScript para exclusões
- [X] 5.9.4: Adicionar loading states em botões (opcional)
- [X] 5.9.5: Melhorar responsividade em mobile
- [X] 5.9.6: Adicionar tooltips onde necessário
- [X] 5.9.7: Padronizar espaçamentos
- [X] 5.9.8: Adicionar animações suaves (transitions)

#### Tarefa 5.10: Testes Manuais Completos
**Descrição**: Testar fluxo completo da aplicação

**Subtarefas**:
- [X] 5.10.1: Testar cadastro de novo usuário
- [X] 5.10.2: Verificar criação automática de perfil e categorias
- [X] 5.10.3: Navegar pelo dashboard
- [X] 5.10.4: Criar contas, categorias e transações
- [X] 5.10.5: Verificar cálculos no dashboard
- [X] 5.10.6: Testar filtros de transações
- [X] 5.10.7: Editar perfil
- [X] 5.10.8: Testar navegação entre páginas
- [X] 5.10.9: Testar responsividade mobile
- [X] 5.10.10: Verificar mensagens de feedback
- [X] 5.10.11: Testar logout e login novamente
- [X] 5.10.12: Verificar isolamento de dados entre usuários

---

### Sprint 8: Refinamentos e Otimizações

#### Tarefa 8.1: Validações Adicionais
**Descrição**: Implementar validações de negócio adicionais

**Subtarefas**:
- [X] 8.1.1: Validar que não é possível excluir conta com transações
- [X] 8.1.2: Validar que não é possível excluir categoria com transações
- [X] 8.1.3: Adicionar validação de data no futuro para transações
- [X] 8.1.4: Validar valores negativos
- [X] 8.1.5: Adicionar validação de saldo suficiente (opcional)
- [X] 8.1.6: Testar todas as validações

#### Tarefa 8.2: Ordenação e Paginação ✅
**Descrição**: Melhorar ordenação e adicionar paginação onde necessário

**Subtarefas**:
- [X] 8.2.1: Adicionar ordenação clicável em tabelas
- [X] 8.2.2: Implementar paginação em lista de contas
- [X] 8.2.3: Melhorar paginação de transações
- [X] 8.2.4: Adicionar "Mostrar X por página"
- [X] 8.2.5: Estilizar componentes de paginação

#### Tarefa 8.3: Busca e Filtros Avançados ✅
**Descrição**: Implementar funcionalidades de busca

**Subtarefas**:
- [X] 8.3.1: Adicionar campo de busca em transações (descrição)
- [X] 8.3.2: Adicionar filtro por status ativo em contas
- [X] 8.3.3: Implementar busca em categorias
- [X] 8.3.4: Adicionar filtros rápidos (Este Mês, Último Mês, etc)
- [X] 8.3.5: Salvar filtros em query string

#### Tarefa 8.4: Gráficos e Visualizações (Opcional) ✅
**Descrição**: Adicionar gráficos simples usando Chart.js

**Subtarefas**:
- [X] 8.4.1: Adicionar Chart.js ao projeto
- [X] 8.4.2: Criar gráfico de pizza para categorias no dashboard
- [X] 8.4.3: Criar gráfico de linha para evolução mensal
- [X] 8.4.4: Estilizar gráficos com tema escuro
- [X] 8.4.5: Adicionar responsividade aos gráficos

#### Tarefa 8.5: Otimizações de Consultas ✅
**Descrição**: Otimizar queries do banco de dados

**Subtarefas**:
- [X] 8.5.1: Adicionar select_related em queries com ForeignKey
- [X] 8.5.2: Adicionar prefetch_related onde necessário
- [X] 8.5.3: Revisar N+1 queries nos templates
- [X] 8.5.4: Adicionar índices no banco (já configurado nos models)
- [X] 8.5.5: Testar performance com dados de exemplo

#### Tarefa 8.6: Tratamento de Erros 404 e 500
**Descrição**: Criar páginas de erro personalizadas

**Subtarefas**:
- [X] 8.6.1: Criar template `templates/404.html`
- [X] 8.6.2: Estilizar página 404
- [X] 8.6.3: Adicionar link para voltar ao dashboard
- [X] 8.6.4: Criar template `templates/500.html`
- [X] 8.6.5: Estilizar página 500
- [X] 8.6.6: Configurar DEBUG = False para testar
- [X] 8.6.7: Testar páginas de erro

#### Tarefa 8.7: Documentação do Código ✅
**Descrição**: Adicionar docstrings e comentários

**Subtarefas**:
- [X] 8.7.1: Adicionar docstrings em todas as classes
- [X] 8.7.2: Adicionar docstrings em métodos complexos
- [X] 8.7.3: Comentar lógica não-óbvia
- [X] 8.7.4: Atualizar README.md com instruções de setup
- [X] 8.7.5: Documentar variáveis de ambiente necessárias

#### Tarefa 8.8: Revisão de Código ✅
**Descrição**: Revisar código seguindo boas práticas

**Subtarefas**:
- [X] 8.8.1: Verificar conformidade com PEP 8
- [X] 8.8.2: Executar linter (flake8 ou pylint)
- [X] 8.8.3: Corrigir warnings
- [X] 8.8.4: Verificar uso consistente de aspas simples
- [X] 8.8.5: Remover código comentado não utilizado
- [X] 8.8.6: Verificar imports não utilizados
- [X] 8.8.7: Organizar imports (isort)

#### Tarefa 8.9: Segurança ✅
**Descrição**: Implementar melhorias de segurança

**Subtarefas**:
- [X] 8.9.1: Configurar SECURE_SSL_REDIRECT para produção
- [X] 8.9.2: Configurar SESSION_COOKIE_SECURE
- [X] 8.9.3: Configurar CSRF_COOKIE_SECURE
- [X] 8.9.4: Adicionar SECURE_HSTS_SECONDS
- [X] 8.9.5: Revisar permissões de acesso em todas as views
- [X] 8.9.6: Testar injeção SQL (Django já protege)
- [X] 8.9.7: Testar XSS (Django já protege)

#### Tarefa 8.10: Testes Finais
**Descrição**: Realizar bateria final de testes

**Subtarefas**:
- [X] 8.10.1: Testar em Chrome
- [X] 8.10.2: Testar em Firefox
- [X] 8.10.3: Testar em Safari
- [X] 8.10.4: Testar em Edge
- [X] 8.10.5: Testar em mobile (Chrome mobile)
- [X] 8.10.6: Testar em mobile (Safari iOS)
- [X] 8.10.7: Testar com múltiplos usuários simultâneos
- [X] 8.10.8: Testar com grande volume de dados
- [X] 8.10.9: Verificar todos os fluxos críticos
- [X] 8.10.10: Listar bugs encontrados

---

### Sprint 7: Preparação para Produção (Opcional) ✅ CONCLUÍDA

#### Tarefa 7.1: Configuração de Ambientes ✅
**Descrição**: Separar configurações de desenvolvimento e produção

**Subtarefas**:
- [X] 7.1.1: Criar settings/base.py
- [X] 7.1.2: Criar settings/development.py
- [X] 7.1.3: Criar settings/production.py
- [X] 7.1.4: Configurar variáveis de ambiente
- [X] 7.1.5: Atualizar manage.py
### Sprint 9: Agente de IA Financeiro

#### Tarefa 9.1: Criacao do Modelo AIAnalysis
**Descricao**: Criar model para armazenar analises financeiras geradas pela IA

**Subtarefas**:
- [ ] 9.1.1: Abrir arquivo `ai/models.py`
- [ ] 9.1.2: Importar models e get_user_model
- [ ] 9.1.3: Criar classe AIAnalysis com ForeignKey para User (on_delete=CASCADE)
- [ ] 9.1.4: Adicionar campo analysis_text (TextField) - texto completo da analise
- [ ] 9.1.5: Adicionar campo summary (CharField, max_length=255) - resumo para dashboard
- [ ] 9.1.6: Adicionar campo is_latest (BooleanField, default=True) - indicador de analise mais recente
- [ ] 9.1.7: Adicionar campos created_at e updated_at
- [ ] 9.1.8: Adicionar metodo __str__ retornando resumo ou data
- [ ] 9.1.9: Adicionar Meta com ordering=['-created_at'], verbose_name e indexes
- [ ] 9.1.10: Configurar Admin para AIAnalysis no `ai/admin.py`
- [ ] 9.1.11: Executar makemigrations e migrate para criar a tabela

#### Tarefa 9.2: Criacao da Camada de Servico (analysis_service)
**Descricao**: Criar service que orquestra a coleta de dados, invocacao do agente e persistencia

**Subtarefas**:
- [ ] 9.2.1: Criar diretorio `ai/services/`
- [ ] 9.2.2: Criar arquivo `ai/services/__init__.py`
- [ ] 9.2.3: Criar arquivo `ai/services/analysis_service.py`
- [ ] 9.2.4: Implementar funcao `get_user_financial_context(user)` que coleta:
  - Contas do usuario com saldos
  - Categorias e totais por tipo
  - Transacoes recentes (ultimos 30 dias)
  - Agregados: total receitas, total despesas, balanco do periodo
- [ ] 9.2.5: Implementar funcao `run_analysis_for_user(user)` que:
  - Coleta contexto financeiro do usuario
  - Invoca o agente de IA com o contexto
  - Persiste resultado no modelo AIAnalysis
  - Marca is_latest=True na nova analise e False nas anteriores
  - Retorna a analise gerada ou None em caso de erro
- [ ] 9.2.6: Implementar funcao `run_analysis_for_all_users()` que:
  - Itera sobre todos os usuarios ativos
  - Chama run_analysis_for_user para cada um
  - Retorna resumo: total processados, sucessos, erros
- [ ] 9.2.7: Adicionar log de progresso e tratamento de erros por usuario

#### Tarefa 9.3: Configuracao do LangChain e Integracao com Groq API
**Descricao**: Criar o agente LangChain com tools de consulta ao banco de dados

**Subtarefas**:
- [ ] 9.3.1: Criar diretorio `ai/agents/`
- [ ] 9.3.2: Criar arquivo `ai/agents/__init__.py`
- [ ] 9.3.3: Criar arquivo `ai/agents/finance_insight_agent.py`
- [ ] 9.3.4: Configurar ChatOpenAI com base_url da Groq e modelo gpt-oss-120b:
  ```python
  from langchain_openai import ChatOpenAI

  llm = ChatOpenAI(
      model='gpt-oss-120b',
      base_url='https://api.groq.com/openai/v1',
      api_key=config('GROQ_API_KEY'),
      temperature=0.7,
      max_tokens=2000,
  )
  ```
- [ ] 9.3.5: Criar tool `get_user_transactions(user_id)` - consulta transacoes do usuario
- [ ] 9.3.6: Criar tool `get_user_accounts(user_id)` - consulta contas e saldos
- [ ] 9.3.7: Criar tool `get_user_categories(user_id)` - consulta categorias e totais
- [ ] 9.3.8: Criar tool `get_user_incomes(user_id, period)` - consulta receitas por periodo
- [ ] 9.3.9: Criar tool `get_user_expenses(user_id, period)` - consulta despesas por periodo
- [ ] 9.3.10: Definir system prompt do agente financeiro:
  - Papel: conselheiro financeiro pessoal especializado
  - Tom: profissional, acolhedor, pratico e direto
  - Idioma: portugues brasileiro
  - Escopo: analise de padroes de gasto, Insights de economia, alertas de risco, sugestoes de melhoria
  - Limitacao: nao dar aconselhamento de investimento ou juridico
- [ ] 9.3.11: Criar o agente usando `create_react_agent` ou equivalente LangChain 1.0
- [ ] 9.3.12: Implementar funcao `invoke_agent(user, context)` que orquestra a chamada ao agente
- [ ] 9.3.13: Adicionar variavel GROQ_API_KEY ao arquivo .env
- [ ] 9.3.14: Adicionar GROQ_API_KEY e GROQ_BASE_URL ao settings.py via python-decouple

#### Tarefa 9.4: Criacao do Django Command run_finance_analysis
**Descricao**: Criar management command para executar a analise financeira

**Subtarefas**:
- [ ] 9.4.1: Criar diretorio `ai/management/`
- [ ] 9.4.2: Criar arquivo `ai/management/__init__.py`
- [ ] 9.4.3: Criar diretorio `ai/management/commands/`
- [ ] 9.4.4: Criar arquivo `ai/management/commands/__init__.py`
- [ ] 9.4.5: Criar arquivo `ai/management/commands/run_finance_analysis.py`
- [ ] 9.4.6: Criar classe Command herdando de BaseCommand
- [ ] 9.4.7: Configurar help text descritivo
- [ ] 9.4.8: Implementar handle() que:
  - Exibe mensagem de inicio
  - Chama run_analysis_for_all_users() do analysis_service
  - Exibe progresso no console (usuario por usuario)
  - Ao final, exibe resumo: X processados, Y analises geradas, Z erros
- [ ] 9.4.9: Adicionar opcao --user_id para executar para um usuario especifico (opcional)
- [ ] 9.4.10: Testar execucao: `python manage.py run_finance_analysis`

#### Tarefa 9.5: Exibicao da Analise no Dashboard
**Descricao**: Atualizar dashboard para exibir a ultima analise do usuario

**Subtarefas**:
- [ ] 9.5.1: Importar AIAnalysis na view do dashboard
- [ ] 9.5.2: Buscar ultima analise do usuario: AIAnalysis.objects.filter(user=request.user, is_latest=True).first()
- [ ] 9.5.3: Adicionar analise ao context do dashboard
- [ ] 9.5.4: Criar secao "Insights da IA" no template dashboard.html
- [ ] 9.5.5: Exibir summary em card destacado com icone de IA
- [ ] 9.5.6: Adicionar botao/link para ver analise completa
- [ ] 9.5.7: Adicionar mensagem amigavel quando nao ha analise disponivel

#### Tarefa 9.6: Atualizacao da Documentacao
**Descricao**: Documentar a funcionalidade de IA financeira

**Subtarefas**:
- [ ] 9.6.1: Criar documento `docs/ai-finance-agent.md` com:
  - Funcionamento do agente de IA
  - Fluxo completo de geracao e exibicao
  - Como executar o Django Command
  - Integracao com o sistema
  - Manutencao e expansao futura
- [ ] 9.6.2: Atualizar `docs/README.md` com link para novo documento
- [ ] 9.6.3: Atualizar `docs/data-models.md` com modelo AIAnalysis
- [ ] 9.6.4: Atualizar `docs/architecture.md` com app `ai` na estrutura

#### Tarefa 9.7: Criacao do Agente Especialista de Integracao IA
**Descricao**: Criar documento de referencia tecnica para futuros agentes de IA

**Subtarefas**:
- [ ] 9.7.1: Criar arquivo `ai/agents/ai_integration_expert.md`
- [ ] 9.7.2: Documentar diretrizes para criacao de agentes com LangChain 1.0
- [ ] 9.7.3: Documentar padroes de integracao com Django
- [ ] 9.7.4: Documentar modelos de configuracao e boas praticas
- [ ] 9.7.5: Documentar uso do MCP Server do Context7 para documentacao do LangChain
- [ ] 9.7.6: Incluir exemplo de fluxo basico de criacao de agente integrado
- [ ] 9.7.7: Mover/copiar o arquivo para `agents/ai_integration_expert.md` na raiz do diretorio de agentes
- [ ] 9.7.8: Atualizar `agents/README.md` com entrada para o agente especialista

---

### Sprint 10: Testes Automatizados

#### Tarefa 10.1: Configuracao de Testes
**Descrição**: Configurar ambiente de testes

**Subtarefas**:
- [X] 10.1.1: Criar diretório tests em cada app
- [X] 10.1.2: Configurar pytest-django (opcional)
- [X] 10.1.3: Criar factories com factory_boy (opcional)
- [X] 10.1.4: Configurar coverage

#### Tarefa 10.2: Testes de Models ✅
**Descrição**: Criar testes para models

**Subtarefas**:
- [X] 10.2.1: Testes de CustomUser
- [X] 10.2.2: Testes de Profile
- [X] 10.2.3: Testes de Account
- [X] 10.2.4: Testes de Category
- [X] 10.2.5: Testes de Transaction
- [X] 10.2.6: Testar métodos __str__
- [X] 10.2.7: Testar validações

#### Tarefa 10.3: Testes de Views
**Descrição**: Criar testes para views

**Subtarefas**:
- [ ] 10.3.1: Testes de autenticação (signup, login, logout)
- [ ] 10.3.2: Testes de CRUD de contas
- [ ] 10.3.3: Testes de CRUD de categorias
- [ ] 10.3.4: Testes de CRUD de transações
- [ ] 10.3.5: Testes de dashboard
- [ ] 10.3.6: Testes de perfil
- [ ] 10.3.7: Testar permissões de acesso

#### Tarefa 10.4: Testes de Signals
**Descrição**: Testar signals e lógica de negócio

**Subtarefas**:
- [ ] 10.4.1: Testar criação automática de perfil
- [ ] 10.4.2: Testar criação de categorias padrão
- [ ] 10.4.3: Testar atualização de saldo ao criar transação
- [ ] 10.4.4: Testar atualização de saldo ao editar transação
- [ ] 10.4.5: Testar atualização de saldo ao excluir transação

#### Tarefa 10.5: Testes de Integração
**Descrição**: Testar fluxos completos

**Subtarefas**:
- [ ] 10.5.1: Testar fluxo completo de cadastro e primeira transação
- [ ] 10.5.2: Testar fluxo de múltiplas transações e saldo
- [ ] 10.5.3: Testar fluxo de filtros e busca
- [ ] 10.5.4: Testar isolamento entre usuários

#### Tarefa 10.6: Executar e Analisar Coverage
**Descrição**: Verificar cobertura de testes

**Subtarefas**:
- [ ] 10.6.1: Executar todos os testes
- [ ] 10.6.2: Gerar relatório de coverage
- [ ] 10.6.3: Identificar áreas sem cobertura
- [ ] 10.6.4: Adicionar testes faltantes
- [ ] 10.6.5: Atingir pelo menos 80% de cobertura

---

### Sprint 11: Agente de IA Chatbot & Migração para Neon ✅ CONCLUÍDA

#### Tarefa 11.1: Migração do Banco de Dados para Neon PostgreSQL ✅
**Descrição**: Configurar e migrar todos os dados da aplicação para a instância do Neon PostgreSQL

**Subtarefas**:
- [X] 11.1.1: Gerar backup/dump de dados do banco de dados SQLite local (`python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 4 > data_backup.json`)
- [X] 11.1.2: Configurar dependências de PostgreSQL (`psycopg2-binary` e `dj-database-url`) no arquivo `requirements/production.txt` e `requirements/base.txt`
- [X] 11.1.3: Modificar `core/settings/base.py`, `core/settings/development.py` e `core/settings/production.py` para apontar exclusivamente para a URL do Neon (`NEON_POSTGRESQL`) usando o parser `dj_database_url`
- [X] 11.1.4: Rodar migrações do sistema na nova base de dados do Neon (`python manage.py migrate`)
- [X] 11.1.5: Carregar os dados consolidados do backup no banco do Neon (`python manage.py loaddata data_backup.json`)
- [X] 11.1.6: Remover o arquivo `db.sqlite3` antigo do workspace e testar a integridade local da aplicação acessando os dados no Neon

#### Tarefa 11.2: Inicialização da App Chatbot ✅
**Descrição**: Estruturar a nova app Django responsável pela lógica do chatbot e do assistente de IA

**Subtarefas**:
- [X] 11.2.1: Criar a app Django chatbot via terminal (`python manage.py startapp chatbot`)
- [X] 11.2.2: Registrar a nova app `chatbot` em `INSTALLED_APPS` no `core/settings/base.py`
- [X] 11.2.3: Criar arquivo `urls.py` na pasta `chatbot/` e registrá-lo nas rotas globais em `core/urls.py`

#### Tarefa 11.3: Modelo de Armazenamento ChatbotAnalysis ✅
**Descrição**: Modelar a tabela de armazenamento das análises e dicas da IA financeira no banco de dados

**Subtarefas**:
- [X] 11.3.1: Criar o modelo `ChatbotAnalysis` em `chatbot/models.py` com chaves estrangeiras, textos da análise, resumo de insights, JSON de snapshot do mercado financeiro e flags de controle
- [X] 11.3.2: Gerar migrações para a nova tabela no banco (`python manage.py makemigrations` e `python manage.py migrate`)
- [X] 11.3.3: Registrar a tabela no Django admin (`chatbot/admin.py`) para fiscalização e auditoria das análises geradas

#### Tarefa 11.4: Integração com Langchain 1.0 e Groq ✅
**Descrição**: Criar a inteligência do chatbot conectada com Groq e modelada com Langchain 1.0

**Subtarefas**:
- [X] 11.4.1: Adicionar dependências mais recentes de IA (`langchain`, `langchain-openai`, `langchain-core`, `langchain-groq`) nas dependências do projeto
- [X] 11.4.2: Criar e estruturar o arquivo de orquestração do agente em `chatbot/services/agent.py`
- [X] 11.4.3: Instanciar a LLM compatível da Groq usando `ChatOpenAI` parametrizada com o modelo `gpt-oss-120b` e `GROQ_API_KEY` do `.env`
- [X] 11.4.4: Elaborar o System Prompt especializado para o assistente (tom profissional, amigável, focado em finanças, em português do Brasil)

#### Tarefa 11.5: Desenvolvimento das Tools do Agente de IA ✅
**Descrição**: Implementar ferramentas especializadas para o agente coletar dados e pesquisar o mercado financeiro

**Subtarefas**:
- [X] 11.5.1: Implementar tool `get_user_financial_data` para expor transações, receitas, despesas, saldo e categorias do usuário autenticado no Django ORM
- [X] 11.5.2: Implementar tool `get_realtime_market_data` em `chatbot/services/market.py` para consultar cotações de moedas, bolsas de valores e mercado imobiliário em tempo real (utilizando APIs públicas resilientes ou scraping/mock robusto)
- [X] 11.5.3: Vincular e registrar as ferramentas no fluxo de decisão (`create_react_agent`) do Langchain

#### Tarefa 11.6: Views e Lógica do Chatbot no Django ✅
**Descrição**: Implementar as views e controladores que integram a interface do chat com o orquestrador do agente

**Subtarefas**:
- [X] 11.6.1: Implementar view em `chatbot/views.py` para carregar o histórico de conversas do usuário autenticado
- [X] 11.6.2: Criar rota POST/AJAX para enviar mensagens e processar a resposta do agente em segundo plano sem recarregar a página
- [X] 11.6.3: Implementar controle lógico para persistir a nova análise no banco e atualizar a flag `is_latest=True` para a análise mais recente daquele usuário

#### Tarefa 11.7: Interface Gráfica do Chatbot (Template chat.html) ✅
**Descrição**: Construir uma UI incrível, responsiva e alinhada ao design e paleta de cores da Landing Page do sistema

**Subtarefas**:
- [X] 11.7.1: Criar o template `templates/chatbot/chat.html` herdando de `base.html`
- [X] 11.7.2: Estilizar a janela de chat com tema escuro, caixas de diálogo adequadas (User: `bg-bg-tertiary`, Bot: `bg-[#0D1A0D]`), bordas finas com gradiente e efeitos de glassmorphism
- [X] 11.7.3: Criar um painel de destaque que mostre permanentemente o último insight de IA do usuário
- [X] 11.7.4: Implementar JavaScript para envio assíncrono (Fetch API) de mensagens, rolagem automática e animação visual de digitação ("typing indicator")

#### Tarefa 11.8: Validação e Testes Manuais de Segurança ✅
**Descrição**: Validar o chatbot contra falhas, vazamento de dados de terceiros e resiliência a quedas de APIs de mercado

**Subtarefas**:
- [X] 11.8.1: Testar fluxo completo com diferentes perfis e garantir que um usuário nunca veja as dicas ou transações de outro
- [X] 11.8.2: Testar comportamento em caso de queda na API da Groq ou da API de mercado em tempo real, verificando se o chatbot emite uma resposta amigável e baseada nos dados locais de forma elegante

---

### Sprint 12: Docker e CI/CD (Sprint Final)

#### Tarefa 12.1: Dockerfile
**Descrição**: Criar Dockerfile para containerização

**Subtarefas**:
- [ ] 12.1.1: Criar Dockerfile na raiz do projeto
- [ ] 12.1.2: Usar imagem Python oficial
- [ ] 12.1.3: Configurar workdir
- [ ] 12.1.4: Copiar requirements e instalar
- [ ] 12.1.5: Copiar código da aplicação
- [ ] 12.1.6: Configurar comando de inicialização
- [ ] 12.1.7: Testar build da imagem

#### Tarefa 12.2: Docker Compose
**Descrição**: Criar docker-compose para ambiente completo

**Subtarefas**:
- [ ] 12.2.1: Criar docker-compose.yml
- [ ] 12.2.2: Configurar serviço web
- [ ] 12.2.3: Configurar serviço de banco (PostgreSQL se migrar)
- [ ] 12.2.4: Configurar volumes
- [ ] 12.2.5: Configurar networks
- [ ] 12.2.6: Testar com docker-compose up

#### Tarefa 12.3: CI/CD com GitHub Actions
**Descrição**: Configurar pipeline de CI/CD

**Subtarefas**:
- [ ] 12.3.1: Criar .github/workflows/ci.yml
- [ ] 12.3.2: Configurar job de testes
- [ ] 12.3.3: Configurar job de linting
- [ ] 12.3.4: Configurar job de build
- [ ] 12.3.5: Configurar deploy automático (opcional)
- [ ] 12.3.6: Testar pipeline

#### Tarefa 12.4: Documentação Final
**Descrição**: Finalizar documentação do projeto

**Subtarefas**:
- [ ] 12.4.1: Atualizar docs/README.md completo
- [ ] 12.4.2: Documentar variáveis de ambiente
- [ ] 12.4.3: Documentar comandos úteis
- [ ] 12.4.4: Criar guia de contribuição (se open source)
- [ ] 12.4.5: Documentar processo de deploy
- [ ] 12.4.6: Criar CHANGELOG.md

