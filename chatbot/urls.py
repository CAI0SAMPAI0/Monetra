from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('send/', views.send_message, name='send'),
    path('clear/', views.clear_chat, name='clear'),
    path('session/new/', views.create_new_session, name='new_session'),
    path('session/<uuid:session_id>/delete/', views.delete_session, name='delete_session'),
]
