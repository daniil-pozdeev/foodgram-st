from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from foodgram.constants import (INGREDIENT_MEASUREMENT_UNIT_MAX_LENGTH,
                                INGREDIENT_MIN_AMOUNT_IN_RECIPE,
                                INGREDIENT_NAME_MAX_LENGTH,
                                RECIPE_IMAGE_UPLOAD_TO,
                                RECIPE_MIN_COOKING_TIME,
                                RECIPE_NAME_MAX_LENGTH)

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=INGREDIENT_NAME_MAX_LENGTH,
        verbose_name="Название ингредиента",
    )
    measurement_unit = models.CharField(
        max_length=INGREDIENT_MEASUREMENT_UNIT_MAX_LENGTH,
        verbose_name="Единицы измерения",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"], name="unique_ingredient"
            )
        ]
        ordering = ("-name",)

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
        related_name="ingredients_in_recipe",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredients_in_recipe",
        verbose_name="Ингредиент",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        validators=[
            MinValueValidator(INGREDIENT_MIN_AMOUNT_IN_RECIPE),
        ],
    )

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецептах"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_ingredient_recipe_relation",
            )
        ]
        ordering = ("recipe__name",)

    def __str__(self):
        return f"{self.ingredient} {self.recipe}"


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор рецепта",
    )
    name = models.CharField(
        max_length=RECIPE_NAME_MAX_LENGTH, verbose_name="Название рецепта"
    )
    image = models.ImageField(
        verbose_name="Фотография рецепта",
        upload_to=RECIPE_IMAGE_UPLOAD_TO,
        blank=True,
    )
    text = models.TextField(verbose_name="Описание рецепта")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientInRecipe",
        verbose_name="Ингредиенты",
    )
    cooking_time = models.PositiveSmallIntegerField(
        "Время приготовления",
        validators=[
            MinValueValidator(RECIPE_MIN_COOKING_TIME),
        ],
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Дата публикации рецепта",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        default_related_name = "recipes"
        ordering = ("-created",)

    def __str__(self):
        return self.name


class UserRecipeRelation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_user_recipe_%(class)s"
            )
        ]
        ordering = ("-user",)

    def __str__(self):
        return f"{self.user} {self.recipe}"


class Favorite(UserRecipeRelation):

    class Meta(UserRecipeRelation.Meta):
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        default_related_name = "favorites"


class ShoppingCart(UserRecipeRelation):

    class Meta(UserRecipeRelation.Meta):
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        default_related_name = "shopping_carts"
