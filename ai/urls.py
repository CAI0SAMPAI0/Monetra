from django.urls import path
from .views import generate_summary_api

app_name = 'ai'

urlpatterns = [
    path('generate-summary/', generate_summary_api, name='generate_summary'),
]
