from django.contrib import admin
from django.urls import path, include
from core import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('profile/', include('profiles.urls')),
    path('accounts/', include('accounts.urls')),
    path('categories/', include('categories.urls')),
    path('transactions/', include('transactions.urls')),
    path('ai/', include('ai.urls')),
    path('chatbot/', include('chatbot.urls')),

    # REST API endpoints
    path('api/auth/login/', api.api_login, name='api_login'),
    path('api/auth/signup/', api.api_signup, name='api_signup'),
    path('api/auth/logout/', api.api_logout, name='api_logout'),
    path('api/auth/status/', api.api_auth_status, name='api_auth_status'),
    path('api/auth/csrf/', api.api_csrf, name='api_csrf'),
    path('api/dashboard/', api.api_dashboard, name='api_dashboard'),
    path('api/accounts/', api.api_accounts, name='api_accounts'),
    path('api/accounts/<int:pk>/', api.api_account_detail, name='api_account_detail'),
    path('api/categories/', api.api_categories, name='api_categories'),
    path('api/categories/<int:pk>/', api.api_category_detail, name='api_category_detail'),
    path('api/transactions/', api.api_transactions, name='api_transactions'),
    path('api/transactions/<int:pk>/', api.api_transaction_detail, name='api_transaction_detail'),
    path('api/profile/', api.api_profile, name='api_profile'),
    path('api/chatbot/history/', api.api_chat_history, name='api_chat_history'),
]

