from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    full_name = models.CharField('nome completo', max_length=200, blank=True)
    phone = models.CharField('telefone', max_length=20, blank=True)
    pluggy_client_id = models.CharField('Pluggy Client ID', max_length=255, blank=True, null=True, help_text='Client ID da API Pluggy para sincronização bancária.')
    pluggy_client_secret = models.CharField('Pluggy Client Secret', max_length=255, blank=True, null=True, help_text='Client Secret da API Pluggy.')
    pluggy_item_id = models.TextField('Conexões Pluggy (Item IDs)', blank=True, null=True, help_text='Item IDs / UUIDs das conexões bancárias da Pluggy (um por linha ou separados por vírgula).')
    pluggy_last_sync = models.DateTimeField('Última sincronização Pluggy', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfis'

    def __str__(self):
        return self.full_name or self.user.email

    @property
    def pluggy_item_ids_list(self):
        """Returns a clean list of all valid UUIDs found in pluggy_item_id"""
        import re
        if not self.pluggy_item_id:
            return []
        uuids = re.findall(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', str(self.pluggy_item_id).lower())
        return list(dict.fromkeys(uuids))

