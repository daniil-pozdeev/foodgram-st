from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import User


@register(User)
class UserAdminConfig(UserAdmin):
    list_display = (
        "pk",
        "username",
        "email",
        "first_name",
        "last_name",
        "password",
        "avatar",
        "recipes_count",
        "subscribers_count",
    )
    list_filter = ("username", "email")
    search_fields = ("username", "email")

    @admin.display(description="Количество рецептов")
    def recipes_count(self, obj):
        return obj.recipes.count()

    @admin.display(description="Количество подписчиков")
    def subscribers_count(self, obj):
        return obj.subscriptions_where_author.count()
