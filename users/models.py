from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager as UserBaseManager
from django.db import models
from django.apps import apps


class UserCManager(UserBaseManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', null=True, blank=True)
    country = models.CharField(max_length=100, verbose_name='Страна', null=True, blank=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', null=True, blank=True)
    token = models.CharField(max_length=15, verbose_name='токен', null=True, blank=True)
    token_time = models.DateTimeField(auto_now_add=True, verbose_name='время создания токена', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
