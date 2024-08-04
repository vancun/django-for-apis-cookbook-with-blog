
from django.contrib.auth import get_user_model
import pytest

from accounts.models import CustomUser

pytestmark = pytest.mark.model

class TestCustomUser:
    def test_should_be_recognized_as_user_model_by_django_auth(self):
        user_model = get_user_model()
        assert user_model is CustomUser

    @pytest.mark.django_db
    def test_should_create_user_instance(self):
        # WHEN New user model instance is created
        u = CustomUser.objects.create()
        # THEN the object is a CustomUser instance
        assert isinstance(u, CustomUser)
        # AND is persisted in the database
        u.refresh_from_db()

    @pytest.mark.django_db
    def test_should_delete_user_instance(self, user: CustomUser):
        # WHEN User is deleted
        user.delete()
        # THEN the user instance is no longer found in the database
        with pytest.raises(CustomUser.DoesNotExist):
            user.refresh_from_db()
