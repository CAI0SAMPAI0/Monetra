import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from .factories import CategoryFactory
from users.tests.factories import UserFactory
from categories.models import Category

@pytest.mark.django_db
class TestCategoryViews:
    def test_category_list_view(self, client):
        user = UserFactory()
        CategoryFactory.create_batch(2, user=user, category_type='INCOME')
        CategoryFactory.create_batch(2, user=user, category_type='EXPENSE')
        
        client.force_login(user)
        url = reverse('categories:category_list')
        response = client.get(url)
        
        assert response.status_code == 200
        assert len(response.context['categories']) == 14
        assert len(response.context['income_categories']) == 5
        assert len(response.context['expense_categories']) == 9

    def test_category_create_view_post(self, client):
        user = UserFactory()
        client.force_login(user)
        url = reverse('categories:category_create')
        data = {
            'name': 'Nova Categoria',
            'category_type': 'EXPENSE',
            'color': '#FF0000',
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('categories:category_list')
        assert Category.objects.filter(name='Nova Categoria', user=user).exists()
        
        messages = list(get_messages(response.wsgi_request))
        assert any('Categoria criada com sucesso!' in str(m) for m in messages)

    def test_category_update_view_post(self, client):
        user = UserFactory()
        category = CategoryFactory(user=user, name='Antigo Nome')
        client.force_login(user)
        url = reverse('categories:category_update', kwargs={'pk': category.pk})
        data = {
            'name': 'Novo Nome',
            'category_type': category.category_type,
            'color': '#00FF00',
        }
        response = client.post(url, data)
        assert response.status_code == 302
        category.refresh_from_db()
        assert category.name == 'Novo Nome'
        
        messages = list(get_messages(response.wsgi_request))
        assert any('Categoria atualizada com sucesso!' in str(m) for m in messages)

    def test_category_delete_view_post(self, client):
        user = UserFactory()
        category = CategoryFactory(user=user)
        client.force_login(user)
        url = reverse('categories:category_delete', kwargs={'pk': category.pk})
        response = client.post(url)
        assert response.status_code == 302
        assert not Category.objects.filter(pk=category.pk).exists()
        
        messages = list(get_messages(response.wsgi_request))
        assert any('Categoria excluída com sucesso!' in str(m) for m in messages)
