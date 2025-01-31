from rest_framework import serializers

from api.serializers import UserProfileSerializer
from recipes.serializers import ShortRecipeSerializer
from users.models import Subscription


class SubscriptionSerializer(UserProfileSerializer):
    recipes = serializers.SerializerMethodField(method_name="get_recipes")
    recipes_count = serializers.ReadOnlyField(source="recipes.count")

    class Meta(UserProfileSerializer.Meta):
        fields = UserProfileSerializer.Meta.fields + (
            "recipes",
            "recipes_count",
        )

    def get_recipes(self, obj):
        request = self.context.get("request")
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get("recipes_limit")

        if recipes_limit:
            try:
                recipes = recipes[:int(recipes_limit)]
            except ValueError:
                pass

        return ShortRecipeSerializer(
            recipes, context={"request": request}, many=True
        ).data


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    recipes = serializers.ReadOnlyField(source="author.recipes.all")
    recipes_count = serializers.ReadOnlyField(source="author.recipes.count")

    class Meta:
        model = Subscription
        fields = (
            "author",
            "subscriber",
            "recipes",
            "recipes_count",
        )
        extra_kwargs = {
            "author": {"write_only": True},
            "subscriber": {"write_only": True},
        }

    def to_representation(self, instance):
        data = UserProfileSerializer(
            instance.author, context={"request": self.context["request"]}
        ).data

        data.update(super().to_representation(instance))

        return data

    def validate(self, data):
        if data["subscriber"] == data["author"]:
            raise serializers.ValidationError(
                "Вы пытаетесь подписаться на себя!"
            )

        return data
