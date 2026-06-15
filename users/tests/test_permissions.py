import pytest
from django.urls import reverse

@pytest.mark.django_db
@pytest.mark.parametrize('url_name, kwargs', [
    ('users:dashboard', {}),
    ('accounts:account_list', {}),
    ('accounts:account_create', {}),
    ('categories:category_list', {}),
    ('categories:category_create', {}),
    ('transactions:transaction_list', {}),
    ('transactions:transaction_create', {}),
    ('profiles:profile_detail', {}),
    ('profiles:profile_update', {}),
])
def test_login_required_redirect(client, url_name, kwargs):
    url = reverse(url_name, kwargs=kwargs)
    response = client.get(url)
    assert response.status_code == 302
    assert reverse('users:login') in response.url
