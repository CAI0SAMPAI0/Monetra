from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('profile/', include('profiles.urls')),
    path('accounts/', include('accounts.urls')),
    path('categories/', include('categories.urls')),
    path('transactions/', include('transactions.urls')),
    path('ai/', include('ai.urls')),
    path('chatbot/', include('chatbot.urls')),
]
