from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.serializers import UserProfileAvatarSerializer, UserProfileSerializer
from users.models import Subscription, User
from users.serializers import (CreateSubscriptionSerializer,
                               SubscriptionSerializer)


class UserProfileViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
        url_path="me",
        url_name="me",
    )
    def me(self, request):
        serializer = UserProfileSerializer(
            request.user, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        detail=True,
        methods=("put", "delete"),
        permission_classes=(IsAuthenticated,),
        url_path="avatar",
        url_name="avatar",
    )
    def avatar(self, request, id):
        if request.method == "PUT":
            return self.create_avatar(request)
        return self.delete_avatar(request)

    def create_avatar(self, request):
        serializer = UserProfileAvatarSerializer(
            request.user, data=request.data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete_avatar(self, request):
        user = request.user
        if user.avatar:
            user.avatar.delete()
            user.avatar = None
            user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
        url_path="subscriptions",
        url_name="subscriptions",
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(
            subscriptions_where_subscriber__author=request.user
        )

        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={"request": request}
        )

        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=("post", "delete"),
        permission_classes=(IsAuthenticated,),
        url_path="subscribe",
        url_name="subscribe",
    )
    def subscribe(self, request, id):
        if request.method == "POST":
            return self.create_subscription(request, id)
        return self.delete_subscription(request, id)

    def create_subscription(self, request, id):
        serializer = CreateSubscriptionSerializer(
            data={
                "subscriber": request.user.id,
                "author": id,
            },
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_subscription(self, request, id):
        subscription = Subscription.objects.filter(
            subscriber=request.user.id, author=id
        )

        author = User.objects.get(pk=id)
        if not subscription.exists():
            return Response(
                f"Вы не подписаны на {author}",
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription.delete()

        return Response(
            f"Вы отписались от {author}", status=status.HTTP_204_NO_CONTENT
        )
