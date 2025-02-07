from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from foodgram.constants import (USER_AVATAR_UPLOAD_TO, USER_EMAIL_MAX_LENGTH,
                                USER_FIRST_NAME_MAX_LENGTH,
                                USER_LAST_NAME_MAX_LENGTH,
                                USER_USERNAME_MAX_LENGTH, USER_USERNAME_REGEX)


class User(AbstractUser):

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=USER_EMAIL_MAX_LENGTH,
        unique=True,
    )
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=USER_USERNAME_MAX_LENGTH,
        unique=True,
        db_index=True,
        validators=[RegexValidator(regex=USER_USERNAME_REGEX)],
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=USER_FIRST_NAME_MAX_LENGTH,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=USER_LAST_NAME_MAX_LENGTH,
    )
    avatar = models.ImageField(
        verbose_name="Аватар пользователя",
        upload_to=USER_AVATAR_UPLOAD_TO,
        blank=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self):
        return self.username


class Subscription(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
        verbose_name="Автор",
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriber",
        verbose_name="Подписчик",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["subscriber", "author"], name="unique_subscription"
            )
        ]
        ordering = ("author__username",)

    def __str__(self):
        return f"{self.subscriber} подписан на {self.author}"
