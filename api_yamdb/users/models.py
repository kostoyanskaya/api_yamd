from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import UserRole
from .validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        'Username',
        unique=True,
        blank=False,
        max_length=150,
        validators=[validate_username]
    )
    email = models.EmailField(
        'E-mail address',
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        'first name',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'last name',
        max_length=150,
        blank=True
    )
    bio = models.CharField(
        'bio',
        max_length=150,
        blank=True,
        null=False,
        default=''
    )
    role = models.CharField(
        max_length=10,
        choices=UserRole.CHOICES,
        default=UserRole.USER
    )

    class Meta:
        ordering = ('username',)

    @property
    def is_admin(self):
        return (
            self.role == UserRole.ADMIN or self.is_staff or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR or self.is_admin
