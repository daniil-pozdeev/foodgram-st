from django.contrib import admin
from django.contrib.admin import ModelAdmin, register

from foodgram.constants import INGREDIENT_INLINE_MIN_AMOUNT
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart)
from users.models import Subscription


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ("pk", "name", "measurement_unit")
    search_fields = ("name",)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    min_num = INGREDIENT_INLINE_MIN_AMOUNT


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ("pk", "name", "author", "get_favorites", "created")
    list_filter = ("author", "name")
    search_fields = ("name", "author__username")
    inlines = [IngredientInRecipeInline]

    @admin.display(description="Количество добавлений рецепта в избранное")
    def get_favorites(self, obj):
        return obj.favorites.count()


@register(IngredientInRecipe)
class IngredientInRecipe(ModelAdmin):
    list_display = ("pk", "recipe", "ingredient", "amount")


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ("pk", "user", "recipe")


@register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    list_display = ("pk", "subscriber", "author")
    search_fields = ("subscriber__username", "author__username")
    list_filter = ("subscriber", "author")


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ("pk", "user", "recipe")
