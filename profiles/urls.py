from django.urls import path
from .views import (
    ProfileDetailView,
    ProfileUpdateView,
    PluggySyncView,
    PluggyAddConnectionView,
    PluggyRemoveConnectionView
)

app_name = 'profiles'

urlpatterns = [
    path('', ProfileDetailView.as_view(), name='profile_detail'),
    path('edit/', ProfileUpdateView.as_view(), name='profile_update'),
    path('sync/', PluggySyncView.as_view(), name='sync_pluggy'),
    path('connection/add/', PluggyAddConnectionView.as_view(), name='add_connection'),
    path('connection/remove/', PluggyRemoveConnectionView.as_view(), name='remove_connection'),
]


