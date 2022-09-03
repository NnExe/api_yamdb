from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    В ролевую модель добавлены только собственно роль и
    биография.
    """
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    role = models.CharField(
        choices=ROLE_CHOICES, blank=False,
        null=False, default=USER,
        max_length=max(map(lambda x: len(x[0]), ROLE_CHOICES))
    )
    username = models.CharField(
        unique=True, null=False,
        blank=False, max_length=150
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
