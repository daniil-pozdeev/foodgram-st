import django_filters
from django_filters import rest_framework
from django_filters.rest_framework import FilterSet

from recipes.models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    name = rest_framework.CharFilter(lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipeFilter(django_filters.FilterSet):
    is_favorited = django_filters.filters.BooleanFilter(
        method="is_recipe_in_favorites_filter"
    )
    is_in_shopping_cart = django_filters.filters.BooleanFilter(
        method="is_recipe_in_shoppingcart_filter"
    )

    def is_recipe_in_favorites_filter(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(favorites__user_id=user.id)
        return queryset

    def is_recipe_in_shoppingcart_filter(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(shopping_recipe__user_id=user.id)
        return queryset

    class Meta:
        model = Recipe
        fields = ("author", "is_favorited", "is_in_shopping_cart")
