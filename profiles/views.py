from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)



import logging
from django.views import View
from django.shortcuts import redirect
from .services.pluggy_service import PluggyService

logger = logging.getLogger(__name__)


class PluggySyncView(LoginRequiredMixin, View):
    """
    Triggers manual synchronization of Pluggy Open Finance data for the logged-in user.
    Supports both POST (forms/buttons) and GET (redirects/links).
    """
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if not profile.pluggy_client_id or not profile.pluggy_client_secret:
            messages.error(
                request,
                'Você precisa configurar seu Client ID e Client Secret da Pluggy antes de sincronizar.'
            )
            return redirect('profiles:profile_update')

        try:
            service = PluggyService(profile.pluggy_client_id, profile.pluggy_client_secret)
            result = service.sync_user_data(request.user)
            messages.success(request, result.get('message', 'Sincronização realizada com sucesso!'))
        except Exception as e:
            logger.error(f'Erro na sincronização Pluggy para {request.user.email}: {e}', exc_info=True)
            messages.error(request, f'Erro ao sincronizar com Pluggy: {str(e)}')

        next_url = request.POST.get('next') or request.GET.get('next') or 'profiles:profile_detail'
        try:
            return redirect(next_url)
        except Exception:
            return redirect('profiles:profile_detail')


class PluggyAddConnectionView(LoginRequiredMixin, View):
    """
    Adds a new bank connection (Pluggy Item ID) to the user profile and triggers automatic sync.
    """
    def get(self, request, *args, **kwargs):
        return redirect('profiles:profile_detail')

    def post(self, request, *args, **kwargs):
        new_item_id = request.POST.get('item_id', '').strip()
        if not new_item_id:
            messages.error(request, 'Informe um Item ID (UUID) válido para conectar.')
            return redirect('profiles:profile_detail')

        profile, _ = Profile.objects.get_or_create(user=request.user)
        existing_items = profile.pluggy_item_ids_list
        if new_item_id.lower() in [i.lower() for i in existing_items]:
            messages.info(request, 'Esta conexão bancária já está cadastrada no seu perfil.')
        else:
            current = profile.pluggy_item_id or ''
            profile.pluggy_item_id = f'{current}\n{new_item_id}'.strip()
            profile.save(update_fields=['pluggy_item_id'])
            messages.success(request, f'Conexão {new_item_id[:8]}... adicionada!')

        # Trigger auto-sync for newly connected bank
        if profile.pluggy_client_id and profile.pluggy_client_secret:
            try:
                service = PluggyService(profile.pluggy_client_id, profile.pluggy_client_secret)
                res = service.sync_user_data(request.user)
                messages.success(request, res['message'])
            except Exception as e:
                logger.warning(f'Aviso na sincronização ao adicionar conexão: {e}')
                messages.warning(request, f'Conexão salva, aviso na sincronização: {str(e)}')

        return redirect('profiles:profile_detail')


class PluggyRemoveConnectionView(LoginRequiredMixin, View):
    """
    Removes a bank connection (Pluggy Item ID) from the user profile.
    """
    def get(self, request, *args, **kwargs):
        return redirect('profiles:profile_detail')

    def post(self, request, *args, **kwargs):
        item_to_remove = request.POST.get('item_id', '').strip()
        profile, _ = Profile.objects.get_or_create(user=request.user)
        current_items = profile.pluggy_item_ids_list
        updated_items = [i for i in current_items if i.lower() != item_to_remove.lower()]
        profile.pluggy_item_id = '\n'.join(updated_items)
        profile.save(update_fields=['pluggy_item_id'])
        messages.success(request, 'Conexão bancária removida.')
        return redirect('profiles:profile_detail')

