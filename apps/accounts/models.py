import logging
import secrets

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models
from django.utils import timezone

from core.helpers import get_file_path

logger = logging.getLogger(__name__)


__all__ = (
    'User',
)


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)

    email = models.EmailField(unique=True)
    email_confirmation_token = models.CharField(max_length=64, editable=False, null=True)

    reset_password_token = models.CharField(max_length=64, editable=False, null=True)
    reset_password_request_date = models.DateTimeField(null=True)

    avatar = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    username = None
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def generate_password_request_date(self):
        self.reset_password_request_date = timezone.now()

    def is_password_token_fresh(self) -> bool:
        if self.reset_password_request_date is None:
            return True

        return self.reset_password_request_date + timezone.timedelta(hours=24) > timezone.now()

    @staticmethod
    def generate_token() -> str:
        return secrets.token_hex(32).replace('=', '0')

    def absolute_avatar_url(self):
        return self.avatar.url
