import pytest
from profiles.tests.factories import ProfileFactory


@pytest.mark.django_db
class TestProfileModel:
    def test_create_profile(self):
        profile = ProfileFactory()
        assert profile.user is not None
        assert profile.created_at is not None
        assert profile.updated_at is not None

    def test_str_method_with_full_name(self):
        profile = ProfileFactory()
        profile.full_name = 'John Doe'
        profile.save()
        assert str(profile) == 'John Doe'

    def test_str_method_without_full_name(self):
        profile = ProfileFactory(full_name='', user__email='jane@example.com')
        assert str(profile) == 'jane@example.com'
