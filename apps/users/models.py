from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email: str, password: str, phone=None, group=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.is_confirm = False
        user.set_password(password)
        user.save(using=self._db)

        if group is not None:
            group.user_set.add(user)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('first_name', "admin")
        extra_fields.setdefault('last_name', "admin")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(
        max_length=100, unique=True,
        error_messages={"unique": _("This email already exists.")}
    )
    password = models.CharField(max_length=255)
    username = None
    phone = models.CharField(
        max_length=100, unique=True, blank=True, null=True,
        error_messages={"unique": _("This phone number already exists.")}
    )
    is_confirm = models.BooleanField(default=False, verbose_name=_("account confirmed"))

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
