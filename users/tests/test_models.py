import pytest
from django.contrib.auth import get_user_model
from users.tests.factories import UserFactory

User = get_user_model()


@pytest.mark.django_db
class TestCustomUserModel:
    def test_create_user(self):
        user = UserFactory()
        assert User.objects.count() == 1
        assert user.email is not None

    def test_str_method(self):
        user = UserFactory(email='test@example.com')
        assert str(user) == 'test@example.com'

    def test_created_at_updated_at(self):
        user = UserFactory()
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_email_uniqueness(self):
        UserFactory(email='duplicate@example.com')
        with pytest.raises(Exception):
            UserFactory(email='duplicate@example.com')
