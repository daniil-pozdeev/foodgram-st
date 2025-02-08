from django.db.models import Sum
from django.http import FileResponse, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.pagination import MainPagePagination
from api.permissions import IsAuthorOrReadOnly
from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart)
from recipes.serializers import (CreateRecipeSerializer, FavoriteSerializer,
                                 RecipeSerializer, ShoppingCartSerializer,
                                 ShortIngredientsSerializer)
import tempfile


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = ShortIngredientsSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = MainPagePagination
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return CreateRecipeSerializer

        return RecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(
        detail=True,
        methods=("post", "delete"),
        permission_classes=(IsAuthenticated,),
        url_path="favorite",
        url_name="favorite",
    )
    def favorite(self, request, pk):
        if request.method == "POST":
            return self.create_user_recipe_relation(
                request, pk, FavoriteSerializer
            )
        return self.delete_user_recipe_relation(
            request,
            pk,
            "favorites",
            Favorite.DoesNotExist,
            "Рецепт не в избранном.",
        )

    @action(
        detail=True,
        methods=("post", "delete"),
        permission_classes=(IsAuthenticated,),
        url_path="shopping_cart",
        url_name="shopping_cart",
    )
    def shopping_cart(self, request, pk):
        if request.method == "POST":
            return self.create_user_recipe_relation(
                request, pk, ShoppingCartSerializer
            )
        return self.delete_user_recipe_relation(
            request,
            pk,
            "shopping_carts",
            ShoppingCart.DoesNotExist,
            "Рецепт не в списке покупок (корзине).",
        )

    def create_user_recipe_relation(self, request, pk, serializer_class):
        serializer = serializer_class(
            data={
                "user": request.user.id,
                "recipe": pk,
            }
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_user_recipe_relation(
        self,
        request,
        pk,
        related_name_for_user,
        does_not_exist_exception,
        does_not_exist_message,
    ):
        try:
            getattr(request.user, related_name_for_user).get(
                user=request.user, recipe_id=pk
            ).delete()
        except does_not_exist_exception:
            return Response(
                does_not_exist_message,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
        url_path="download_shopping_cart",
        url_name="download_shopping_cart",
    )
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientInRecipe.objects.filter(
                recipe__shopping_recipe__user=request.user
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(sum=Sum("amount"))
        )

        return self.ingredients_to_txt(ingredients)


    @staticmethod
    def ingredients_to_txt(ingredients):
        shopping_list = "\n".join(
            f"{ingredient['ingredient_name']} - {ingredient['sum']} "
            f"({ingredient['ingredient__measurement_unit']})"
            for ingredient in ingredients
        )
        temp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt")
        temp_file.write(shopping_list)
        temp_file.seek(0)
        return FileResponse(temp_file, as_attachment=True, filename="shoping_list.txt", content_type="text/plain")

    @action(
        detail=True,
        methods=("get",),
        permission_classes=(IsAuthenticatedOrReadOnly,),
        url_path="get-link",
        url_name="get-link",
    )
    def get_link(self, request, pk):
        instance = self.get_object()

        url = f"{request.get_host()}/s/{instance.id}"

        return Response(data={"short-link": url})
